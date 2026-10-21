const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
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

function parseBody(req, limitBytes = 25 * 1024 * 1024) {
  return new Promise((resolve, reject) => {
    let body = '';
    let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > limitBytes) {
        req.destroy();
        reject(new Error('Payload too large'));
        return;
      }
      body += chunk;
    });
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

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }, timeout: 8000 }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(new Error('Parse error: ' + data.slice(0, 100))); }
      });
    }).on('error', reject);
  });
}

function postForm(url, postData) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      timeout: 10000
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Parse error: ' + data.slice(0, 100)));
        }
      });
    });
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Translation request timed out'));
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function translateText(text, targetLang, sourceLang = 'auto') {
  if (!text || !text.trim()) {
    return { translated: '', detected: sourceLang, target: targetLang || 'en' };
  }
  const hasUrdu = /[\u0600-\u06FF]/.test(text);
  if (!targetLang) {
    targetLang = hasUrdu ? 'en' : 'ur';
  }
  if (targetLang === 'ur') {
    sourceLang = (sourceLang && sourceLang !== 'auto' && sourceLang !== 'ur') ? sourceLang : 'en';
  } else if (targetLang === 'en') {
    sourceLang = (sourceLang && sourceLang !== 'auto' && sourceLang !== 'en') ? sourceLang : 'ur';
  }

  // Primary: Google dict-chrome-ex using POST
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=dict-chrome-ex&sl=${encodeURIComponent(sourceLang)}&tl=${encodeURIComponent(targetLang)}&dt=t`;
    const postData = 'q=' + encodeURIComponent(text);
    const json = await postForm(url, postData);
    const translated = (json[0] || []).map(s => s[0]).join('');
    return { translated, detected: json[2] || sourceLang, target: targetLang };
  } catch (err) {
    console.warn('Google POST translation failed, trying MyMemory fallback:', err.message);
    try {
      const mmUrl = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text.slice(0, 500))}&langpair=${encodeURIComponent(sourceLang)}|${encodeURIComponent(targetLang)}`;
      const mmJson = await fetchJson(mmUrl);
      if (mmJson && mmJson.responseData && mmJson.responseData.translatedText) {
        return { translated: mmJson.responseData.translatedText, detected: sourceLang, target: targetLang };
      }
    } catch (e2) {
      console.warn('MyMemory fallback failed:', e2.message);
    }
    throw err;
  }
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

    // TRANSLATE TEXT ENDPOINT (POST & GET)
    if ((req.method === 'POST' || req.method === 'GET') && pathname === '/api/translate') {
      let text = '';
      let to = '';
      let from = 'auto';

      if (req.method === 'GET') {
        text = url.searchParams.get('text') || '';
        to = url.searchParams.get('to') || '';
        from = url.searchParams.get('from') || 'auto';
      } else {
        const body = await parseBody(req);
        text = body.text || '';
        to = body.to || '';
        from = body.from || 'auto';
      }

      if (!text || !text.trim()) {
        return sendJson(res, 400, { error: 'Text is required for translation' });
      }

      try {
        const result = await translateText(text, to, from);
        return sendJson(res, 200, {
          success: true,
          translatedText: result.translated,
          sourceLang: result.detected,
          targetLang: result.target
        });
      } catch (err) {
        console.error('Translation error:', err);
        return sendJson(res, 500, { error: 'Translation failed', details: err.message });
      }
    }

    // UPLOAD IMAGE ENDPOINT
    if (req.method === 'POST' && pathname === '/api/upload') {
      const data = await parseBody(req);
      if (!data || !data.data) {
        return sendJson(res, 400, { error: 'No image data provided' });
      }

      const match = data.data.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
      let buffer;
      let ext = 'png';
      if (match) {
        const mime = match[1];
        if (mime.includes('jpeg') || mime.includes('jpg')) ext = 'jpg';
        else if (mime.includes('webp')) ext = 'webp';
        else if (mime.includes('gif')) ext = 'gif';
        buffer = Buffer.from(match[2], 'base64');
      } else {
        buffer = Buffer.from(data.data, 'base64');
      }

      const uploadsDir = path.join(__dirname, '..', 'media', 'uploads');
      if (!fs.existsSync(uploadsDir)) {
        fs.mkdirSync(uploadsDir, { recursive: true });
      }

      const rawName = (data.filename || 'whatsapp-image').replace(/[^a-zA-Z0-9_\-\.]/g, '_');
      const baseName = path.parse(rawName).name || 'whatsapp-image';
      const filename = `${Date.now()}-${baseName.slice(0, 30)}.${ext}`;
      const filePath = path.join(uploadsDir, filename);

      fs.writeFileSync(filePath, buffer);
      return sendJson(res, 200, {
        success: true,
        url: `/media/uploads/${filename}`,
        filename
      });
    }

    // 0. RESET COUNTER ENDPOINT
    if (req.method === 'POST' && pathname === '/api/reset-counter') {
      await pool.query("INSERT INTO settings (key, value) VALUES ('counter', '0') ON CONFLICT (key) DO UPDATE SET value = '0'");
      return sendJson(res, 200, { success: true, counter: 0 });
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
      }
      pRes.rows.forEach(p => {
        const num = parseInt(p.id, 10);
        if (!isNaN(num) && num > counter) counter = num;
      });

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
      const pidStr = String(p.id).padStart(3, '0');
      const result = await pool.query(q, [
        pidStr,
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
      await pool.query('DELETE FROM deleted_patients WHERE id = $1 OR id = $2 OR id = $3', [String(p.id), String(p.id).padStart(4, '0'), pidStr]);

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
          const padded3 = pId.padStart(3, '0');
          if (deletedSet.has(pId) || deletedSet.has(cleanId) || deletedSet.has(paddedId) || deletedSet.has(padded3)) {
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
          `, [padded3, p.name, p.mobile || '', p.country || '92', p.dob || '', p.notes || '']);
        }

        for (const a of appts) {
          const aPid = String(a.patientId).trim();
          const aClean = aPid.replace(/^0+/, '') || '0';
          const aPadded = aPid.padStart(4, '0');
          const aPadded3 = aPid.padStart(3, '0');
          if (deletedSet.has(aPid) || deletedSet.has(aClean) || deletedSet.has(aPadded) || deletedSet.has(aPadded3)) {
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
            aPadded3,
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

        let maxPid = 0;
        for (const p of patients) {
          const pId = String(p.id).trim();
          const cleanId = pId.replace(/^0+/, '') || '0';
          const paddedId = pId.padStart(4, '0');
          const padded3 = pId.padStart(3, '0');
          if (deletedSet.has(pId) || deletedSet.has(cleanId) || deletedSet.has(paddedId) || deletedSet.has(padded3)) continue;
          const num = parseInt(p.id, 10);
          if (!isNaN(num) && num > maxPid) maxPid = num;
        }

        if (maxPid > 0) {
          await client.query(`
            INSERT INTO settings (key, value)
            VALUES ('counter', $1)
            ON CONFLICT (key) DO UPDATE SET
              value = GREATEST(CAST(settings.value AS INTEGER), EXCLUDED.value::INTEGER)::TEXT;
          `, [String(maxPid)]);
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
      const cRes = await pool.query("SELECT value FROM settings WHERE key = 'counter'");
      const finalCounter = cRes.rows.length > 0 ? (parseInt(cRes.rows[0].value, 10) || 0) : 0;
      return sendJson(res, 200, {
        success: true,
        patients: pRes.rows,
        appts: aRes.rows,
        counter: finalCounter,
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
