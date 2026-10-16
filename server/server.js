const http = require('http');
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@localhost:5432/src_db',
  max: 10,
  idleTimeoutMillis: 30000
});

pool.query(`
  CREATE TABLE IF NOT EXISTS deleted_patients (
    id VARCHAR(30) PRIMARY KEY,
    deleted_at TIMESTAMPTZ DEFAULT NOW()
  );
`).catch(err => console.error('Table init error:', err));

const PORT = process.env.PORT || 4106;

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (e) {
        reject(e);
      }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    return res.end();
  }

  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname.replace(/\/+$/, '') || '/';

  try {
    // Health check
    if (pathname === '/api/health' || pathname === '/health') {
      return sendJson(res, 200, { status: 'healthy', time: new Date().toISOString() });
    }

    // 1. GET FULL DATA
    if (req.method === 'GET' && (pathname === '/api/data' || pathname === '/api/sync')) {
      const pRes = await pool.query('SELECT id, name, mobile, country, dob, notes FROM patients ORDER BY id ASC');
      const aRes = await pool.query('SELECT id, patient_id as "patientId", date, start_time as start, end_time as "end", status, fee, paid, pay_method as "payMethod", notes, created FROM appointments ORDER BY created DESC, date DESC');
      const cRes = await pool.query("SELECT value FROM settings WHERE key = 'counter'");
      const dRes = await pool.query('SELECT id FROM deleted_patients');
      const deletedPatientIds = dRes.rows.map(r => r.id);
      
      let counter = 0;
      if (cRes.rows.length > 0) {
        counter = parseInt(cRes.rows[0].value, 10) || 0;
      } else {
        pRes.rows.forEach(p => {
          const num = parseInt(p.id, 10);
          if (!isNaN(num) && num > counter) counter = num;
        });
      }

      return sendJson(res, 200, {
        success: true,
        patients: pRes.rows,
        appts: aRes.rows.map(a => ({
          ...a,
          fee: parseFloat(a.fee) || 0,
          paid: parseFloat(a.paid) || 0,
          created: a.created ? Number(a.created) : Date.now()
        })),
        counter,
        deletedPatientIds
      });
    }

    // 2. UPSERT PATIENT
    if (req.method === 'POST' && pathname === '/api/patient') {
      const data = await parseBody(req);
      const p = data.patient || data;
      if (!p.id || !p.name) {
        return sendJson(res, 400, { error: 'Patient id and name are required' });
      }

      const q = `
        INSERT INTO patients (id, name, mobile, country, dob, notes, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, NOW())
        ON CONFLICT (id) DO UPDATE SET
          name = EXCLUDED.name,
          mobile = EXCLUDED.mobile,
          country = EXCLUDED.country,
          dob = EXCLUDED.dob,
          notes = EXCLUDED.notes,
          updated_at = NOW()
        RETURNING id, name, mobile, country, dob, notes;
      `;
      const result = await pool.query(q, [
        String(p.id).padStart(4, '0'),
        p.name,
        p.mobile || '',
        p.country || '92',
        p.dob || '',
        p.notes || ''
      ]);

      // Update counter if needed
      const pidNum = parseInt(p.id, 10);
      if (!isNaN(pidNum)) {
        await pool.query(`
          INSERT INTO settings (key, value)
          VALUES ('counter', $1)
          ON CONFLICT (key) DO UPDATE SET
            value = GREATEST(CAST(settings.value AS INTEGER), EXCLUDED.value::INTEGER)::TEXT;
        `, [String(pidNum)]);
      }

      // If re-registering an ID, remove from blacklist
      await pool.query('DELETE FROM deleted_patients WHERE id = $1 OR id = $2', [String(p.id), String(p.id).padStart(4, '0')]);

      return sendJson(res, 200, { success: true, patient: result.rows[0] });
    }

    // 3. DELETE PATIENT
    if (req.method === 'DELETE' && pathname === '/api/patient') {
      let id = url.searchParams.get('id');
      if (!id) {
        try {
          const b = await parseBody(req);
          id = b.id;
        } catch(e){}
      }
      if (!id) return sendJson(res, 400, { error: 'Patient id is required' });

      const sId = String(id).trim();
      const cleanId = sId.replace(/^0+/, '') || '0';
      const paddedId = sId.padStart(4, '0');

      await pool.query('INSERT INTO deleted_patients (id) VALUES ($1), ($2), ($3) ON CONFLICT (id) DO NOTHING', [sId, cleanId, paddedId]);
      await pool.query('DELETE FROM appointments WHERE patient_id = $1 OR patient_id = $2 OR patient_id = $3', [sId, cleanId, paddedId]);
      await pool.query('DELETE FROM patients WHERE id = $1 OR id = $2 OR id = $3', [sId, cleanId, paddedId]);
      return sendJson(res, 200, { success: true, deleted: id });
    }

    // 4. UPSERT APPOINTMENT
    if (req.method === 'POST' && pathname === '/api/appointment') {
      const data = await parseBody(req);
      const a = data.appointment || data;
      if (!a.id || !a.patientId || !a.date) {
        return sendJson(res, 400, { error: 'Appointment id, patientId, and date are required' });
      }

      const q = `
        INSERT INTO appointments (id, patient_id, date, start_time, end_time, status, fee, paid, pay_method, notes, created, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW())
        ON CONFLICT (id) DO UPDATE SET
          patient_id = EXCLUDED.patient_id,
          date = EXCLUDED.date,
          start_time = EXCLUDED.start_time,
          end_time = EXCLUDED.end_time,
          status = EXCLUDED.status,
          fee = EXCLUDED.fee,
          paid = EXCLUDED.paid,
          pay_method = EXCLUDED.pay_method,
          notes = EXCLUDED.notes,
          created = EXCLUDED.created,
          updated_at = NOW()
        RETURNING id, patient_id as "patientId", date, start_time as start, end_time as "end", status, fee, paid, pay_method as "payMethod", notes, created;
      `;
      const result = await pool.query(q, [
        a.id,
        String(a.patientId).padStart(4, '0'),
        a.date,
        a.start || '10:00',
        a.end || '11:00',
        a.status || 'Confirmed',
        parseFloat(a.fee) || 0,
        parseFloat(a.paid) || 0,
        a.payMethod || 'Cash / Direct',
        a.notes || '',
        a.created ? String(a.created) : String(Date.now())
      ]);

      return sendJson(res, 200, { success: true, appointment: result.rows[0] });
    }

    // 5. DELETE APPOINTMENT
    if (req.method === 'DELETE' && pathname === '/api/appointment') {
      let id = url.searchParams.get('id');
      if (!id) {
        try {
          const b = await parseBody(req);
          id = b.id;
        } catch(e){}
      }
      if (!id) return sendJson(res, 400, { error: 'Appointment id is required' });

      await pool.query('DELETE FROM appointments WHERE id = $1', [id]);
      return sendJson(res, 200, { success: true, deleted: id });
    }

    // 6. BULK SYNC (Import / sync initial data)
    if (req.method === 'POST' && pathname === '/api/sync') {
      const body = await parseBody(req);
      const patients = body.patients || [];
      const appts = body.appts || [];
      const counter = parseInt(body.counter || '0', 10);

      const client = await pool.connect();
      try {
        await client.query('BEGIN');

        if (Array.isArray(body.deletedPatientIds) && body.deletedPatientIds.length > 0) {
          for (const dId of body.deletedPatientIds) {
            const sId = String(dId).trim();
            const cleanId = sId.replace(/^0+/, '') || '0';
            const paddedId = sId.padStart(4, '0');
            await client.query('INSERT INTO deleted_patients (id) VALUES ($1), ($2), ($3) ON CONFLICT (id) DO NOTHING', [sId, cleanId, paddedId]);
            await client.query('DELETE FROM appointments WHERE patient_id = $1 OR patient_id = $2 OR patient_id = $3', [sId, cleanId, paddedId]);
            await client.query('DELETE FROM patients WHERE id = $1 OR id = $2 OR id = $3', [sId, cleanId, paddedId]);
          }
        }

        if (Array.isArray(body.deletedApptIds) && body.deletedApptIds.length > 0) {
          for (const aId of body.deletedApptIds) {
            await client.query('DELETE FROM appointments WHERE id = $1', [String(aId)]);
          }
        }

        // Fetch all deleted IDs from DB to completely prevent resurrection
        const curDeletedRes = await client.query('SELECT id FROM deleted_patients');
        const deletedSet = new Set(curDeletedRes.rows.map(r => r.id));
        
        for (const p of patients) {
          const pId = String(p.id).trim();
          const cleanId = pId.replace(/^0+/, '') || '0';
          const paddedId = pId.padStart(4, '0');
          if (deletedSet.has(pId) || deletedSet.has(cleanId) || deletedSet.has(paddedId)) {
            continue; // Skip resurrecting deleted patient!
          }

          await client.query(`
            INSERT INTO patients (id, name, mobile, country, dob, notes, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
            ON CONFLICT (id) DO UPDATE SET
              name = EXCLUDED.name,
              mobile = EXCLUDED.mobile,
              country = EXCLUDED.country,
              dob = EXCLUDED.dob,
              notes = EXCLUDED.notes,
              updated_at = NOW();
          `, [paddedId, p.name, p.mobile || '', p.country || '92', p.dob || '', p.notes || '']);
        }

        for (const a of appts) {
          const aPid = String(a.patientId).trim();
          const aClean = aPid.replace(/^0+/, '') || '0';
          const aPadded = aPid.padStart(4, '0');
          if (deletedSet.has(aPid) || deletedSet.has(aClean) || deletedSet.has(aPadded)) {
            continue; // Skip resurrecting appointments of deleted patient!
          }

          await client.query(`
            INSERT INTO appointments (id, patient_id, date, start_time, end_time, status, fee, paid, pay_method, notes, created, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW())
            ON CONFLICT (id) DO UPDATE SET
              date = EXCLUDED.date,
              start_time = EXCLUDED.start_time,
              end_time = EXCLUDED.end_time,
              status = EXCLUDED.status,
              fee = EXCLUDED.fee,
              paid = EXCLUDED.paid,
              pay_method = EXCLUDED.pay_method,
              notes = EXCLUDED.notes,
              created = EXCLUDED.created,
              updated_at = NOW();
          `, [
            a.id,
            aPadded,
            a.date,
            a.start || '10:00',
            a.end || '11:00',
            a.status || 'Confirmed',
            parseFloat(a.fee) || 0,
            parseFloat(a.paid) || 0,
            a.payMethod || 'Cash / Direct',
            a.notes || '',
            a.created ? String(a.created) : String(Date.now())
          ]);
        }

        if (counter > 0) {
          await client.query(`
            INSERT INTO settings (key, value)
            VALUES ('counter', $1)
            ON CONFLICT (key) DO UPDATE SET
              value = GREATEST(CAST(settings.value AS INTEGER), EXCLUDED.value::INTEGER)::TEXT;
          `, [String(counter)]);
        }

        await client.query('COMMIT');
      } catch (err) {
        await client.query('ROLLBACK');
        throw err;
      } finally {
        client.release();
      }

      // Return fresh state
      const pRes = await pool.query('SELECT id, name, mobile, country, dob, notes FROM patients ORDER BY id ASC');
      const aRes = await pool.query('SELECT id, patient_id as "patientId", date, start_time as start, end_time as "end", status, fee, paid, pay_method as "payMethod", notes, created FROM appointments ORDER BY created DESC, date DESC');
      const finalDRes = await pool.query('SELECT id FROM deleted_patients');
      return sendJson(res, 200, {
        success: true,
        patients: pRes.rows,
        appts: aRes.rows,
        counter,
        deletedPatientIds: finalDRes.rows.map(r => r.id)
      });
    }

    return sendJson(res, 404, { error: 'Not Found' });
  } catch (err) {
    console.error('API Error:', err);
    return sendJson(res, 500, { error: err.message || 'Internal Server Error' });
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`SRC Database API server listening on http://0.0.0.0:${PORT}`);
});
