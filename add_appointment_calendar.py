import re

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS for Register Appointment Calendar
calendar_css = """  /* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ================= */
  .reg-appt-scheduler-card {
    margin-top: 24px;
    background: #fdfaf6;
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 10px rgba(61, 40, 29, 0.03);
    transition: all 0.25s ease;
  }
  .ras-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding-bottom: 16px;
    border-bottom: 1px solid #ebdccb;
    flex-wrap: wrap;
  }
  .ras-head-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .ras-head-icon {
    font-size: 26px;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #ffffff;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(61, 40, 29, 0.04);
  }
  .ras-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--brown-dark);
    margin: 0;
  }
  .ras-sub {
    font-size: 12px;
    color: var(--muted);
    font-weight: 500;
    margin: 2px 0 0;
  }
  .ras-toggle-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    background: #ffffff;
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 700;
    color: var(--brown-dark);
    box-shadow: 0 1px 4px rgba(61, 40, 29, 0.03);
  }
  .ras-toggle-label input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: var(--brown);
  }

  /* Two Column Layout */
  .ras-content {
    margin-top: 18px;
    transition: opacity 0.25s ease;
  }
  .ras-content.disabled {
    opacity: 0.45;
    pointer-events: none;
  }
  .ras-layout-grid {
    display: grid;
    grid-template-columns: 310px 1fr;
    gap: 20px;
    align-items: start;
  }

  /* Calendar Box (Left Column) */
  .ras-calendar-box {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(61, 40, 29, 0.03);
  }
  .ras-cal-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }
  .ras-cal-month-title {
    font-family: 'Cinzel', system-ui, sans-serif;
    font-size: 14px;
    font-weight: 800;
    color: var(--brown-dark);
    letter-spacing: 0.5px;
  }
  .ras-cal-nav-btn {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: #fbf7f1;
    color: var(--brown-dark);
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
  }
  .ras-cal-nav-btn:hover {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
  }
  .ras-cal-weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    font-size: 10.5px;
    font-weight: 800;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .ras-cal-days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
  }
  .ras-day-cell {
    aspect-ratio: 1;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: var(--brown-dark);
    cursor: pointer;
    position: relative;
    border: 1px solid transparent;
    transition: all 0.15s ease;
    user-select: none;
  }
  .ras-day-cell:hover:not(.empty):not(.disabled) {
    background: #fbf6ee;
    border-color: var(--brown);
  }
  .ras-day-cell.today {
    border-color: var(--brown-light);
    background: #faf3ea;
  }
  .ras-day-cell.selected {
    background: var(--brown) !important;
    color: #ffffff !important;
    border-color: var(--brown-dark) !important;
    box-shadow: 0 2px 8px rgba(124, 83, 57, 0.35);
  }
  .ras-day-cell.empty {
    cursor: default;
    opacity: 0;
  }
  .ras-day-cell.disabled {
    cursor: not-allowed;
    opacity: 0.35;
    color: var(--muted);
  }
  .ras-day-dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #d47a45;
    position: absolute;
    bottom: 2px;
  }
  .ras-day-cell.selected .ras-day-dot {
    background: #ffffff;
  }

  .ras-cal-presets {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid #ebdccb;
  }
  .ras-preset-btn {
    padding: 5px 2px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: #fdfaf6;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--brown-dark);
    cursor: pointer;
    text-align: center;
    transition: all 0.15s ease;
  }
  .ras-preset-btn:hover {
    background: #fbf6ee;
    border-color: var(--brown);
  }
  .ras-preset-btn.active {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
  }

  /* Details Box (Right Column) */
  .ras-details-box {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .ras-selected-date-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 14px;
    gap: 10px;
  }
  .ras-sdb-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .ras-sdb-icon {
    font-size: 22px;
  }
  .ras-sdb-title {
    font-size: 13.5px;
    font-weight: 800;
    color: var(--brown-dark);
  }
  .ras-sdb-sub {
    font-size: 11px;
    color: var(--muted);
    font-weight: 500;
  }
  .ras-status-pill {
    font-size: 10.5px;
    font-weight: 800;
    background: #f4ece2;
    color: var(--brown);
    padding: 2px 8px;
    border-radius: 999px;
  }

  /* Quick Time Slots */
  .ras-slots-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .ras-slots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
  }
  .ras-slot-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 7px 10px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 700;
    color: var(--brown-dark);
    cursor: pointer;
    transition: all 0.16s ease;
  }
  .ras-slot-chip:hover {
    background: #fbf6ee;
    border-color: var(--brown);
    transform: translateY(-1px);
  }
  .ras-slot-chip.active {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
    box-shadow: 0 2px 6px rgba(124, 83, 57, 0.25);
  }

  /* Form Grid inside Details */
  .ras-form-fields-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }

  /* Schedule on that Day */
  .ras-day-roster {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 120px;
    overflow-y: auto;
  }
  .ras-roster-title {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
  }
  .ras-roster-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    padding: 4px 6px;
    border-radius: 6px;
    background: #fcf9f5;
    border: 1px solid #ebdccb;
  }

  @media(max-width: 860px) {
    .ras-layout-grid {
      grid-template-columns: 1fr;
    }
    .ras-form-fields-grid {
      grid-template-columns: 1fr 1fr;
    }
  }"""

content = content.replace('</style>', f'{calendar_css}\n</style>', 1)

# 2. HTML: Insert Scheduler inside patientForm
ras_html = """        <!-- Interactive Calendar & Session Scheduler under Add Patient -->
        <div class="reg-appt-scheduler-card" id="regApptScheduler">
          <div class="ras-header">
            <div class="ras-head-left">
              <span class="ras-head-icon">📅</span>
              <div>
                <h3 class="ras-title">Schedule Patient Appointment</h3>
                <p class="ras-sub">Choose consultation date, session time slot, and treatment parameters</p>
              </div>
            </div>
            <label class="ras-toggle-label">
              <input type="checkbox" id="regApptEnabled" checked onchange="toggleRegApptBooking(this.checked)">
              <span>Book Appointment Now</span>
            </label>
          </div>

          <div class="ras-content" id="rasContentBody">
            <div class="ras-layout-grid">

              <!-- Left Column: Interactive Visual Calendar -->
              <div class="ras-calendar-box">
                <div class="ras-cal-nav">
                  <button type="button" class="ras-cal-nav-btn" onclick="navRegCalendar(-1)" title="Previous Month">&lsaquo;</button>
                  <span class="ras-cal-month-title" id="regCalMonthTitle">October 2026</span>
                  <button type="button" class="ras-cal-nav-btn" onclick="navRegCalendar(1)" title="Next Month">&rsaquo;</button>
                </div>

                <div class="ras-cal-weekdays">
                  <span>Mo</span><span>Tu</span><span>We</span><span>Th</span><span>Fr</span><span>Sa</span><span>Su</span>
                </div>

                <div class="ras-cal-days-grid" id="regCalDaysGrid">
                  <!-- Dynamically rendered days -->
                </div>

                <div class="ras-cal-presets">
                  <button type="button" class="ras-preset-btn active" onclick="setRegCalendarPreset(0)">Today</button>
                  <button type="button" class="ras-preset-btn" onclick="setRegCalendarPreset(1)">Tomorrow</button>
                  <button type="button" class="ras-preset-btn" onclick="setRegCalendarPreset(2)">+2 Days</button>
                  <button type="button" class="ras-preset-btn" onclick="setRegCalendarPreset('nextMonday')">Next Mon</button>
                </div>
                <input type="hidden" id="regApptDate" value="">
              </div>

              <!-- Right Column: Time Slot & Session Parameters -->
              <div class="ras-details-box">
                <div class="ras-selected-date-banner">
                  <div class="ras-sdb-left">
                    <span class="ras-sdb-icon">🕒</span>
                    <div>
                      <div class="ras-sdb-title" id="regSelectedDateDisplay">Selected Date</div>
                      <div class="ras-sdb-sub" id="regSlotsAvailableHint">Pick an available time slot below</div>
                    </div>
                  </div>
                  <span class="ras-status-pill" id="regDateBadge">Session Date</span>
                </div>

                <div class="ras-slots-group">
                  <label class="lbl-title">Select Time Slot Preset</label>
                  <div class="ras-slots-grid">
                    <button type="button" class="ras-slot-chip active" onclick="setRegTimeSlot('10:00','11:00')">
                      <span>🌅</span> 10:00 AM – 11:00 AM
                    </button>
                    <button type="button" class="ras-slot-chip" onclick="setRegTimeSlot('11:30','12:30')">
                      <span>☀️</span> 11:30 AM – 12:30 PM
                    </button>
                    <button type="button" class="ras-slot-chip" onclick="setRegTimeSlot('15:00','16:00')">
                      <span>☕</span> 03:00 PM – 04:00 PM
                    </button>
                    <button type="button" class="ras-slot-chip" onclick="setRegTimeSlot('17:00','18:00')">
                      <span>🌙</span> 05:00 PM – 06:00 PM
                    </button>
                    <button type="button" class="ras-slot-chip" onclick="setRegTimeSlot('20:00','21:00')">
                      <span>✨</span> 08:00 PM – 09:00 PM
                    </button>
                  </div>
                </div>

                <div class="ras-form-fields-grid">
                  <div class="field">
                    <label><span class="lbl-title">Start Time</span></label>
                    <input type="time" id="regApptStart" value="10:00">
                  </div>
                  <div class="field">
                    <label><span class="lbl-title">End Time</span></label>
                    <input type="time" id="regApptEnd" value="11:00">
                  </div>
                  <div class="field">
                    <label><span class="lbl-title">Session Status</span></label>
                    <select id="regApptStatus">
                      <option value="Confirmed" selected>Confirmed</option>
                      <option value="Pending">Pending</option>
                    </select>
                  </div>
                  <div class="field">
                    <label><span class="lbl-title">Total Fee (<span class="reg-cur-lbl">Rs.</span>)</span></label>
                    <input type="number" id="regApptFee" placeholder="0" min="0" step="1" oninput="updateRegBalance()">
                  </div>
                  <div class="field">
                    <label><span class="lbl-title">Paid Amount (<span class="reg-cur-lbl">Rs.</span>)</span></label>
                    <input type="number" id="regApptPaid" placeholder="0" min="0" step="1" oninput="updateRegBalance()">
                  </div>
                  <div class="field">
                    <label><span class="lbl-title">Balance Due (<span class="reg-cur-lbl">Rs.</span>)</span></label>
                    <input type="text" id="regApptBalance" readonly placeholder="0">
                  </div>
                </div>

                <!-- Existing Schedule on Selected Date -->
                <div class="ras-day-roster">
                  <div class="ras-roster-title">
                    <span>Schedule on Selected Date</span>
                    <span id="regDayBookingCount">0 Bookings</span>
                  </div>
                  <div class="ras-roster-items" id="regDayBookingsList">
                    <span style="color:var(--muted);font-size:11px;">No appointments yet on this date. Slot is wide open!</span>
                  </div>
                </div>

              </div>

            </div>
          </div>
        </div>"""

# Insert ras_html right above the btn-row in patientForm
old_btn_row = """        </div>
        <div class="btn-row">
          <button type="submit" class="btn btn-primary">💾 Save Patient Record</button>"""

new_btn_row = f"""        </div>

{ras_html}

        <div class="btn-row">
          <button type="submit" class="btn btn-primary" id="savePatientBtn">💾 Save Patient &amp; Book Appointment</button>"""

assert old_btn_row in content, "old_btn_row not found"
content = content.replace(old_btn_row, new_btn_row, 1)

# 3. JavaScript Engine for the Calendar Scheduler
calendar_js = """/* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= */
let REG_CAL_YEAR = new Date().getFullYear();
let REG_CAL_MONTH = new Date().getMonth(); // 0-11
let REG_SELECTED_DATE = todayISO(); // YYYY-MM-DD

function initRegCalendar(){
  setRegCalendarPreset(0);
  updateRegApptCurrency();
}

function renderRegCalendar(){
  const title = $('regCalMonthTitle');
  const grid = $('regCalDaysGrid');
  if(!title || !grid) return;

  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  title.textContent = monthNames[REG_CAL_MONTH] + ' ' + REG_CAL_YEAR;

  // First day of month (Monday=0..Sunday=6)
  const firstDay = new Date(REG_CAL_YEAR, REG_CAL_MONTH, 1).getDay();
  const dayOffset = (firstDay === 0 ? 6 : firstDay - 1); // convert Sunday=0 to index 6
  const totalDays = new Date(REG_CAL_YEAR, REG_CAL_MONTH + 1, 0).getDate();

  const todayStr = todayISO();
  let html = '';

  // Blank padding cells
  for(let i = 0; i < dayOffset; i++){
    html += '<div class="ras-day-cell empty"></div>';
  }

  // Days in month
  for(let d = 1; d <= totalDays; d++){
    const dStr = String(d).padStart(2, '0');
    const mStr = String(REG_CAL_MONTH + 1).padStart(2, '0');
    const isoDate = `${REG_CAL_YEAR}-${mStr}-${dStr}`;

    const isToday = isoDate === todayStr;
    const isSelected = isoDate === REG_SELECTED_DATE;

    // Check if any appointments exist on this date
    const apptsOnDate = DB.appts.filter(a => a.date === isoDate);
    const hasAppts = apptsOnDate.length > 0;

    html += `<div class="ras-day-cell ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" 
                  onclick="selectRegCalendarDate('${isoDate}')"
                  title="${fmtDate(isoDate)}${hasAppts ? ' (' + apptsOnDate.length + ' booked)' : ''}">
      <span>${d}</span>
      ${hasAppts ? '<span class="ras-day-dot"></span>' : ''}
    </div>`;
  }

  grid.innerHTML = html;
  updateSelectedDateDisplay();
}

function navRegCalendar(delta){
  REG_CAL_MONTH += delta;
  if(REG_CAL_MONTH < 0){
    REG_CAL_MONTH = 11;
    REG_CAL_YEAR--;
  } else if(REG_CAL_MONTH > 11){
    REG_CAL_MONTH = 0;
    REG_CAL_YEAR++;
  }
  renderRegCalendar();
}

function selectRegCalendarDate(isoDate){
  REG_SELECTED_DATE = isoDate;
  $('regApptDate').value = isoDate;
  renderRegCalendar();
  updateRosterForSelectedDate();
}

function updateSelectedDateDisplay(){
  const disp = $('regSelectedDateDisplay');
  const d = new Date(REG_SELECTED_DATE + 'T12:00:00');
  if(disp && !isNaN(d.getTime())){
    disp.textContent = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
}

function updateRosterForSelectedDate(){
  const countEl = $('regDayBookingCount');
  const listEl = $('regDayBookingsList');
  const hintEl = $('regSlotsAvailableHint');
  if(!countEl || !listEl) return;

  const appts = DB.appts.filter(a => a.date === REG_SELECTED_DATE);
  countEl.textContent = appts.length + (appts.length === 1 ? ' Booking' : ' Bookings');

  if(hintEl){
    if(appts.length === 0){
      hintEl.textContent = 'All time slots are open on this date';
    } else {
      hintEl.textContent = `${appts.length} session${appts.length===1?'':'s'} scheduled &middot; check slots below`;
    }
  }

  if(appts.length === 0){
    listEl.innerHTML = '<span style="color:var(--muted);font-size:11px;">No appointments yet on this date. Schedule is completely open!</span>';
    return;
  }

  listEl.innerHTML = appts.map(a => {
    const pt = patientById(a.patientId);
    const pName = pt ? pt.name : 'Patient';
    return `<div class="ras-roster-item">
      <span><strong>${fmtTime(a.start)} - ${fmtTime(a.end)}</strong>: ${esc(pName)}</span>
      <span class="badge ${badgeClass(a.status)}">${esc(a.status)}</span>
    </div>`;
  }).join('');
}

function badgeClass(status){
  return {Pending:'b-pending',Confirmed:'b-confirmed',Completed:'b-completed',Cancelled:'b-cancelled'}[status]||'b-pending';
}

function setRegCalendarPreset(preset){
  const now = new Date();
  let target = new Date();

  if(preset === 0){
    // Today
    target = now;
  } else if(preset === 1){
    // Tomorrow
    target.setDate(now.getDate() + 1);
  } else if(preset === 2){
    // In 2 Days
    target.setDate(now.getDate() + 2);
  } else if(preset === 'nextMonday'){
    const day = now.getDay();
    const diff = (day === 0 ? 1 : 8 - day);
    target.setDate(now.getDate() + diff);
  }

  const y = target.getFullYear();
  const m = String(target.getMonth() + 1).padStart(2, '0');
  const d = String(target.getDate()).padStart(2, '0');
  const iso = `${y}-${m}-${d}`;

  REG_CAL_YEAR = target.getFullYear();
  REG_CAL_MONTH = target.getMonth();
  selectRegCalendarDate(iso);

  // Sync preset buttons active state
  document.querySelectorAll('.ras-preset-btn').forEach((btn, idx) => {
    btn.classList.remove('active');
  });
}

function setRegTimeSlot(start, end){
  $('regApptStart').value = start;
  $('regApptEnd').value = end;

  // Highlight slot chip
  document.querySelectorAll('.ras-slot-chip').forEach(btn => {
    const isAct = btn.textContent.includes(start) || btn.getAttribute('onclick').includes(start);
    btn.classList.toggle('active', isAct);
  });
}

function toggleRegApptBooking(enabled){
  const body = $('rasContentBody');
  const btn = $('savePatientBtn');
  if(body) body.classList.toggle('disabled', !enabled);
  if(btn){
    btn.textContent = enabled ? '💾 Save Patient & Book Appointment' : '💾 Save Patient Record Only';
  }
}

function updateRegBalance(){
  const fee = parseFloat($('regApptFee').value) || 0;
  const paid = parseFloat($('regApptPaid').value) || 0;
  const bal = Math.max(0, fee - paid);
  const sym = currencyFor($('pCountry').value.trim()).sym;
  $('regApptBalance').value = bal;
}

function updateRegApptCurrency(){
  const sym = currencyFor($('pCountry').value.trim()).sym;
  document.querySelectorAll('.reg-cur-lbl').forEach(el => el.textContent = sym);
  updateRegBalance();
}"""

# Insert calendar_js into script
content = content.replace('/* ================= PATIENT REGISTRATION ================= */', f'{calendar_js}\n\n/* ================= PATIENT REGISTRATION ================= */', 1)

# 4. Hook into pCountry change to also update appointment currency
content = content.replace("$('pCountry').addEventListener('input',updateCountryHint);", "$('pCountry').addEventListener('input',()=>{ updateCountryHint(); updateRegApptCurrency(); });", 1)
content = content.replace("$('pCountry').addEventListener('change',updateCountryHint);", "$('pCountry').addEventListener('change',()=>{ updateCountryHint(); updateRegApptCurrency(); });", 1)

# 5. Update patientForm submit handler to schedule appointment if regApptEnabled
old_submit_handler = """  const editId=$('editId').value;
  if(editId){
    const p=patientById(editId);
    Object.assign(p,{name,father:$('pFather').value.trim(),mobile,country:$('pCountry').value.trim(),dob:$('pDob').value,gender:$('pGender').value,problem:$('pProblem').value,address:$('pAddress').value.trim(),notes:$('pNotes').value.trim()});
    save(); toast('Patient updated ✓'); resetPatientForm(); goTab('patients');
  }else{
    const id=nextId();
    DB.patients.unshift({id,name,father:$('pFather').value.trim(),mobile,country:$('pCountry').value.trim(),dob:$('pDob').value,gender:$('pGender').value,problem:$('pProblem').value,address:$('pAddress').value.trim(),notes:$('pNotes').value.trim(),registered:todayISO()});
    save(); toast('Patient saved: '+id+' ✓'); resetPatientForm();
    renderDashboard();
  }"""

new_submit_handler = """  const editId=$('editId').value;
  const shouldBookAppt = $('regApptEnabled').checked;
  const apptDate = $('regApptDate').value || todayISO();
  const apptStart = $('regApptStart').value || '10:00';
  const apptEnd = $('regApptEnd').value || '11:00';
  const apptFee = parseFloat($('regApptFee').value) || 0;
  const apptPaid = parseFloat($('regApptPaid').value) || 0;
  const apptStatus = $('regApptStatus').value || 'Confirmed';

  let targetPatientId = '';

  if(editId){
    targetPatientId = editId;
    const p=patientById(editId);
    Object.assign(p,{name,father:$('pFather').value.trim(),mobile,country:$('pCountry').value.trim(),dob:$('pDob').value,gender:$('pGender').value,problem:$('pProblem').value,address:$('pAddress').value.trim(),notes:$('pNotes').value.trim()});
  }else{
    targetPatientId = nextId();
    DB.patients.unshift({id:targetPatientId,name,father:$('pFather').value.trim(),mobile,country:$('pCountry').value.trim(),dob:$('pDob').value,gender:$('pGender').value,problem:$('pProblem').value,address:$('pAddress').value.trim(),notes:$('pNotes').value.trim(),registered:todayISO()});
  }

  // If appointment booking is enabled, create appointment on chosen date and time slot
  if(shouldBookAppt){
    const apptId = 'APT-' + Date.now().toString(36).toUpperCase();
    const newAppt = {
      id: apptId,
      patientId: targetPatientId,
      date: apptDate,
      start: apptStart,
      end: apptEnd,
      status: apptStatus,
      fee: apptFee,
      paid: apptPaid,
      payMethod: 'Cash',
      created: Date.now()
    };
    DB.appts.unshift(newAppt);
  }

  save();

  if(shouldBookAppt){
    toast('✓ Patient saved & appointment booked for ' + fmtDate(apptDate) + ' (' + fmtTime(apptStart) + ')');
  } else {
    toast(editId ? 'Patient updated ✓' : 'Patient saved: ' + targetPatientId + ' ✓');
  }

  resetPatientForm();
  renderDashboard();
  renderAppts();
  updateCategoryBadges();
  if(editId) goTab('patients');"""

assert old_submit_handler in content, "old_submit_handler not found"
content = content.replace(old_submit_handler, new_submit_handler, 1)

# 6. Call initRegCalendar in bootstrap
content = content.replace('initExpandNavEngine();', 'initExpandNavEngine();\ninitRegCalendar();', 1)

# 7. Update resetPatientForm to reset appointment calendar
old_reset_form = """function resetPatientForm(){
  $('patientForm').reset();
  $('editId').value='';
  $('pId').value = String(DB.counter+1).padStart(4,'0');
  $('pDate').value = fmtDate(todayISO());
  setDobBoxes('');
  $('pCountry').value='Pakistan'; updateCountryHint();
  document.querySelector('#patientForm button[type=submit]').textContent = '💾 Save Patient Record';
}"""

new_reset_form = """function resetPatientForm(){
  $('patientForm').reset();
  $('editId').value='';
  $('pId').value = String(DB.counter+1).padStart(4,'0');
  $('pDate').value = fmtDate(todayISO());
  setDobBoxes('');
  $('pCountry').value='Pakistan'; updateCountryHint();
  if($('regApptEnabled')) $('regApptEnabled').checked = true;
  toggleRegApptBooking(true);
  setRegCalendarPreset(0);
  setRegTimeSlot('10:00','11:00');
  if($('regApptFee')) $('regApptFee').value = '';
  if($('regApptPaid')) $('regApptPaid').value = '';
  if($('regApptBalance')) $('regApptBalance').value = '0';
  updateRegApptCurrency();
  const btn = $('savePatientBtn') || document.querySelector('#patientForm button[type=submit]');
  if(btn) btn.textContent = '💾 Save Patient & Book Appointment';
}"""

assert old_reset_form in content, "old_reset_form not found"
content = content.replace(old_reset_form, new_reset_form, 1)

# Write to AIR-Patient-Management-System.html and index.html
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Registration Calendar & Session Scheduler applied successfully!")
