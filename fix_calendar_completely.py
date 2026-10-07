import re

def apply_calendar_fix(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the entire CSS from /* Calendar Box (Left Column) */ up to /* Details Box (Right Column) */
    old_css_pattern = r'/\* Calendar Box \(Left Column\) \*/.*?/\* Details Box \(Right Column\) \*/'
    
    new_css = """/* Calendar Box (Left Column) */
  .ras-calendar-box {
    background: #ffffff;
    border: 1.5px solid #ebdccb;
    border-radius: 16px;
    padding: 16px 16px;
    box-shadow: 0 4px 18px rgba(61, 40, 29, 0.04);
    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
    transition: all 0.25s ease;
  }
  .ras-cal-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f2e7db;
  }
  .ras-cal-month-title {
    font-family: 'Cinzel', Georgia, serif;
    font-size: 14px;
    font-weight: 800;
    color: var(--brown-dark);
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .ras-cal-nav-btn {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    border: 1.5px solid #ebdccb;
    background: #faf6f0;
    color: var(--brown-dark);
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.18s ease;
  }
  .ras-cal-nav-btn:hover {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
    transform: scale(1.05);
    box-shadow: 0 2px 6px rgba(124, 83, 57, 0.2);
  }
  .ras-cal-weekdays {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 5px;
    text-align: center;
    margin-bottom: 6px;
    width: 100%;
    box-sizing: border-box;
  }
  .ras-cal-weekdays span {
    font-size: 11px;
    font-weight: 800;
    color: var(--brown);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.85;
    padding: 0;
    margin: 0;
  }
  .ras-cal-days-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 5px;
    width: 100%;
    box-sizing: border-box;
  }
  .ras-day-cell {
    height: 36px;
    min-height: 36px;
    width: 100%;
    min-width: 0;
    max-width: 100%;
    border-radius: 9px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    cursor: pointer;
    background: #fdfaf6;
    border: 1.5px solid #ebdccb;
    box-shadow: 0 1px 3px rgba(61, 40, 29, 0.03);
    transition: all 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
    user-select: none;
    box-sizing: border-box;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden;
  }
  .ras-day-num {
    font-size: 12.5px;
    font-weight: 750;
    color: var(--brown-dark);
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    padding: 0;
    margin: 0;
  }
  .ras-day-cell:hover:not(.ras-empty-day):not(.empty) {
    background: #ffffff;
    border-color: var(--brown);
    transform: translateY(-1.5px);
    box-shadow: 0 4px 10px rgba(124, 83, 57, 0.12);
  }
  .ras-day-cell:hover:not(.ras-empty-day):not(.empty) .ras-day-num {
    color: var(--brown);
  }
  .ras-day-cell.today {
    background: #fbf3e8;
    border-color: #b57a55;
    border-width: 1.5px;
  }
  .ras-day-cell.today .ras-day-num {
    color: var(--brown-dark);
    font-weight: 850;
  }
  .ras-day-cell.today::after {
    content: '';
    position: absolute;
    top: 3px;
    right: 3px;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--brown);
  }
  .ras-day-cell.selected {
    background: var(--brown) !important;
    border-color: var(--brown-dark) !important;
    box-shadow: 0 4px 12px rgba(124, 83, 57, 0.35) !important;
    transform: scale(1.04);
    z-index: 2;
  }
  .ras-day-cell.selected .ras-day-num {
    color: #ffffff !important;
    font-weight: 850;
  }
  .ras-day-cell.selected::after {
    background: #ffffff;
  }
  .ras-day-cell.ras-empty-day,
  .ras-day-cell.empty {
    background: transparent !important;
    border: 1px dashed rgba(235, 220, 203, 0.45) !important;
    box-shadow: none !important;
    cursor: default !important;
    pointer-events: none !important;
    opacity: 0.3 !important;
    padding: 0 !important;
    margin: 0 !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: 36px !important;
    width: 100% !important;
  }
  .ras-day-dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #d47a45;
    position: absolute;
    bottom: 3px;
    left: 50%;
    transform: translateX(-50%);
  }
  .ras-day-cell.selected .ras-day-dot {
    background: #ffffff;
  }

  .ras-cal-presets {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 6px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #f2e7db;
    width: 100%;
    box-sizing: border-box;
  }
  .ras-preset-btn {
    height: 32px;
    padding: 0 4px;
    border-radius: 8px;
    border: 1.5px solid #ebdccb;
    background: #faf6f0;
    font-size: 11px;
    font-weight: 750;
    color: var(--brown-dark);
    cursor: pointer;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.16s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
    box-sizing: border-box;
  }
  .ras-preset-btn:hover {
    background: #ffffff;
    border-color: var(--brown);
    color: var(--brown);
  }
  .ras-preset-btn.active {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
    box-shadow: 0 2px 8px rgba(124, 83, 57, 0.22);
  }

  /* Details Box (Right Column) */"""

    content = re.sub(old_css_pattern, new_css, content, flags=re.DOTALL)

    # 2. Update .ras-layout-grid definition to prevent grid blowout
    content = content.replace(
        "grid-template-columns: 310px 1fr;",
        "grid-template-columns: minmax(0, 316px) minmax(0, 1fr);"
    )

    # 3. Update media queries
    old_mq_pattern = r'@media\(max-width:\s*860px\)\s*\{.*?@media\(max-width:\s*520px\)\s*\{.*?</style>'
    new_mq = """@media(max-width: 920px) {
    .ras-layout-grid {
      grid-template-columns: 1fr;
    }
    .ras-calendar-box {
      max-width: 360px;
      margin: 0 auto;
    }
    .ras-form-fields-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media(max-width: 520px) {
    .ras-calendar-box {
      padding: 12px 10px;
    }
    .ras-cal-weekdays,
    .ras-cal-days-grid {
      gap: 3.5px;
    }
    .ras-day-cell {
      height: 33px;
      min-height: 33px;
      border-radius: 7px;
    }
    .ras-day-cell.ras-empty-day,
    .ras-day-cell.empty {
      height: 33px !important;
    }
    .ras-day-num {
      font-size: 11.5px;
    }
    .ras-cal-presets {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 6px;
    }
    .ras-form-fields-grid {
      grid-template-columns: 1fr;
    }
    .ras-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }
    .reg-appt-scheduler-card {
      padding: 16px 14px;
    }
  }
</style>"""
    content = re.sub(old_mq_pattern, new_mq, content, flags=re.DOTALL)

    # 4. Replace JS calendar engine functions from /* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= */ to the end of setRegCalendarPreset
    old_js_pattern = r'/\* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= \*/.*?function setRegCalendarPreset\(preset, btnEl\)\{.*?\n\}'
    
    new_js = """/* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= */
let REG_CAL_YEAR = new Date().getFullYear();
let REG_CAL_MONTH = new Date().getMonth(); // 0-11
let REG_SELECTED_DATE = todayISO(); // YYYY-MM-DD

function initRegCalendar(){
  renderRegCalendar();
  setRegCalendarPreset(0, document.querySelector('.ras-preset-btn'));
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
  const dayOffset = (firstDay === 0 ? 6 : firstDay - 1);
  const totalDays = new Date(REG_CAL_YEAR, REG_CAL_MONTH + 1, 0).getDate();

  const todayStr = todayISO();
  let html = '';

  // Blank padding cells at start
  for(let i = 0; i < dayOffset; i++){
    html += '<div class="ras-day-cell ras-empty-day" aria-hidden="true"></div>';
  }

  // Days in month
  for(let d = 1; d <= totalDays; d++){
    const dStr = String(d).padStart(2, '0');
    const mStr = String(REG_CAL_MONTH + 1).padStart(2, '0');
    const isoDate = `${REG_CAL_YEAR}-${mStr}-${dStr}`;

    const isToday = isoDate === todayStr;
    const isSelected = isoDate === REG_SELECTED_DATE;

    // Check if any appointments exist on this date
    const apptsOnDate = (typeof DB !== 'undefined' && DB.appts) ? DB.appts.filter(a => a.date === isoDate) : [];
    const hasAppts = apptsOnDate.length > 0;

    html += `<div class="ras-day-cell ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" 
                  data-date="${isoDate}"
                  role="button"
                  tabindex="0"
                  onclick="selectRegCalendarDate('${isoDate}', this)"
                  onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();selectRegCalendarDate('${isoDate}', this);}"
                  title="${fmtDate(isoDate)}${hasAppts ? ' (' + apptsOnDate.length + ' booked)' : ''}">
      <span class="ras-day-num">${d}</span>
      ${hasAppts ? '<span class="ras-day-dot"></span>' : ''}
    </div>`;
  }

  // Trailing empty cells to keep complete 7-day row
  const totalRendered = dayOffset + totalDays;
  const trailingCount = (7 - (totalRendered % 7)) % 7;
  for(let i = 0; i < trailingCount; i++){
    html += '<div class="ras-day-cell ras-empty-day" aria-hidden="true"></div>';
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

function selectRegCalendarDate(isoDate, cellEl){
  REG_SELECTED_DATE = isoDate;
  if($('regApptDate')) $('regApptDate').value = isoDate;

  // If calendar grid is not rendered or belongs to different month/year, render it
  const parts = isoDate.split('-');
  const y = parseInt(parts[0], 10);
  const m = parseInt(parts[1], 10) - 1;
  const cells = document.querySelectorAll('.ras-day-cell[data-date]');
  if(cells.length === 0 || REG_CAL_YEAR !== y || REG_CAL_MONTH !== m){
    REG_CAL_YEAR = y;
    REG_CAL_MONTH = m;
    renderRegCalendar();
  }

  // Highlight cell
  document.querySelectorAll('.ras-day-cell[data-date]').forEach(c => {
    const isSel = c.dataset.date === isoDate;
    c.classList.toggle('selected', isSel);
    c.setAttribute('aria-selected', isSel ? 'true' : 'false');
  });

  updateSelectedDateDisplay();
  updateRosterForSelectedDate();
}

function updateSelectedDateDisplay(){
  const disp = $('regSelectedDateDisplay');
  const badge = $('regDateBadge');
  const d = new Date(REG_SELECTED_DATE + 'T12:00:00');
  if(disp && !isNaN(d.getTime())){
    disp.textContent = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
  if(badge){
    const todayStr = todayISO();
    if(REG_SELECTED_DATE === todayStr){
      badge.textContent = 'Today';
    } else {
      const diff = Math.round((new Date(REG_SELECTED_DATE + 'T12:00:00') - new Date(todayStr + 'T12:00:00')) / (1000 * 60 * 60 * 24));
      if(diff === 1) badge.textContent = 'Tomorrow';
      else if(diff > 1) badge.textContent = 'In ' + diff + ' Days';
      else badge.textContent = 'Session Date';
    }
  }
}

function updateRosterForSelectedDate(){
  const countEl = $('regDayBookingCount');
  const listEl = $('regDayBookingsList');
  const hintEl = $('regSlotsAvailableHint');
  if(!countEl || !listEl) return;

  const appts = (typeof DB !== 'undefined' && DB.appts) ? DB.appts.filter(a => a.date === REG_SELECTED_DATE) : [];
  countEl.textContent = appts.length + (appts.length === 1 ? ' Booking' : ' Bookings');

  if(hintEl){
    if(appts.length === 0){
      hintEl.textContent = 'All session slots are open on this date';
    } else {
      hintEl.textContent = `${appts.length} session${appts.length===1?'':'s'} scheduled &middot; check slots below`;
    }
  }

  if(appts.length === 0){
    listEl.innerHTML = '<span style="color:var(--muted);font-size:11px;">No appointments yet on this date. Schedule is completely open!</span>';
    return;
  }

  listEl.innerHTML = appts.map(a => {
    const pt = (typeof patientById === 'function') ? patientById(a.patientId) : null;
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

function setRegCalendarPreset(preset, btnEl){
  const now = new Date();
  let target = new Date();

  if(preset === 0){
    target = now;
  } else if(preset === 1){
    target.setDate(now.getDate() + 1);
  } else if(preset === 2){
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
  renderRegCalendar();
  selectRegCalendarDate(iso);

  // Sync preset buttons active state
  document.querySelectorAll('.ras-preset-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  if(btnEl){
    btnEl.classList.add('active');
  } else {
    // Find matching preset button by index
    const btns = document.querySelectorAll('.ras-preset-btn');
    if(preset === 0 && btns[0]) btns[0].classList.add('active');
    else if(preset === 1 && btns[1]) btns[1].classList.add('active');
    else if(preset === 2 && btns[2]) btns[2].classList.add('active');
    else if(preset === 'nextMonday' && btns[3]) btns[3].classList.add('active');
  }
}"""

    content = re.sub(old_js_pattern, new_js, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} successfully.")

if __name__ == '__main__':
    apply_calendar_fix('/home/projects/src-online.com/AIR-Patient-Management-System.html')
    apply_calendar_fix('/home/projects/src-online.com/index.html')
