import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Smooth scrolling & tap highlights on html
    if 'scroll-behavior: smooth' not in content:
        content = content.replace(
            "*{box-sizing:border-box;margin:0;padding:0}",
            "html{scroll-behavior:smooth;-webkit-tap-highlight-color:transparent}\n  *{box-sizing:border-box;margin:0;padding:0}"
        )

    # 2. Modern luxury calendar CSS with beautiful, crisp, perfectly aligned day boxes
    old_cal_css_regex = r'/\* Calendar Box \(Left Column\) \*/.*?/\* Details Box \(Right Column\) \*/'
    
    new_cal_css = """/* Calendar Box (Left Column) */
  .ras-calendar-box {
    background: #ffffff;
    border: 1.5px solid #ebdccb;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 4px 18px rgba(61, 40, 29, 0.04);
    box-sizing: border-box;
    width: 100%;
    transition: all 0.25s ease;
  }
  .ras-cal-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f2e7db;
  }
  .ras-cal-month-title {
    font-family: 'Cinzel', Georgia, serif;
    font-size: 14.5px;
    font-weight: 800;
    color: var(--brown-dark);
    letter-spacing: 0.6px;
  }
  .ras-cal-nav-btn {
    width: 32px;
    height: 32px;
    border-radius: 9px;
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
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
    text-align: center;
    margin-bottom: 8px;
  }
  .ras-cal-weekdays span {
    font-size: 11px;
    font-weight: 800;
    color: var(--brown);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.85;
  }
  .ras-cal-days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
  }
  .ras-day-cell {
    height: 38px;
    min-height: 38px;
    width: 100%;
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
  }
  .ras-day-num {
    font-size: 13px;
    font-weight: 750;
    color: var(--brown-dark);
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }
  .ras-day-cell:hover:not(.empty) {
    background: #ffffff;
    border-color: var(--brown);
    transform: translateY(-1.5px);
    box-shadow: 0 4px 10px rgba(124, 83, 57, 0.12);
  }
  .ras-day-cell:hover:not(.empty) .ras-day-num {
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
  .ras-day-cell.empty {
    background: transparent;
    border: 1px dashed rgba(235, 220, 203, 0.6);
    box-shadow: none;
    cursor: default;
    pointer-events: none;
    opacity: 0.4;
  }
  .ras-day-dot {
    width: 4.5px;
    height: 4.5px;
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
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #f2e7db;
  }
  .ras-preset-btn {
    height: 32px;
    padding: 0 6px;
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

    content = re.sub(old_cal_css_regex, new_cal_css, content, flags=re.DOTALL)

    # 3. Responsive rules for Scheduler & Mobile viewports
    old_responsive_regex = r'@media\(max-width:\s*860px\)\s*\{\s*\.ras-layout-grid\s*\{.*?\}\s*\}'
    new_responsive = """@media(max-width: 860px) {
    .ras-layout-grid {
      grid-template-columns: 1fr;
    }
    .ras-calendar-box {
      max-width: 380px;
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
    .ras-cal-days-grid {
      gap: 3.5px;
    }
    .ras-day-cell {
      height: 34px;
      min-height: 34px;
    }
    .ras-day-num {
      font-size: 12px;
    }
    .ras-cal-presets {
      grid-template-columns: repeat(2, 1fr);
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
  }"""
    # Replace existing media queries for ras
    if '@media(max-width: 860px)' in content and '.ras-layout-grid' in content:
        content = re.sub(r'@media\(max-width:\s*860px\)\s*\{\s*\.ras-layout-grid\s*\{[\s\S]*?\}\s*\}\s*(@media\(max-width:\s*520px\)\s*\{\s*[\s\S]*?\}\s*\})?', new_responsive, content)

    # 4. In renderRegCalendar(): use <span class="ras-day-num"> and data-date for cell selection
    old_render_day = """    html += `<div class="ras-day-cell ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" 
                  onclick="selectRegCalendarDate('${isoDate}', this)"
                  title="${fmtDate(isoDate)}${hasAppts ? ' (' + apptsOnDate.length + ' booked)' : ''}">
      <span>${d}</span>
      ${hasAppts ? '<span class="ras-day-dot"></span>' : ''}
    </div>`;"""

    new_render_day = """    html += `<div class="ras-day-cell ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" 
                  data-date="${isoDate}"
                  role="button"
                  tabindex="0"
                  onclick="selectRegCalendarDate('${isoDate}', this)"
                  onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();selectRegCalendarDate('${isoDate}', this);}"
                  title="${fmtDate(isoDate)}${hasAppts ? ' (' + apptsOnDate.length + ' booked)' : ''}">
      <span class="ras-day-num">${d}</span>
      ${hasAppts ? '<span class="ras-day-dot"></span>' : ''}
    </div>`;"""
    if old_render_day in content:
        content = content.replace(old_render_day, new_render_day)

    # 5. In selectRegCalendarDate(): instant data-date sync
    old_select_date = """function selectRegCalendarDate(isoDate, cellEl){
  REG_SELECTED_DATE = isoDate;
  if($('regApptDate')) $('regApptDate').value = isoDate;
  
  // Highlight cell immediately without full re-render jump
  document.querySelectorAll('.ras-day-cell').forEach(c => c.classList.remove('selected'));
  if(cellEl){
    cellEl.classList.add('selected');
  } else {
    renderRegCalendar();
  }

  updateSelectedDateDisplay();
  updateRosterForSelectedDate();
}"""

    new_select_date = """function selectRegCalendarDate(isoDate, cellEl){
  REG_SELECTED_DATE = isoDate;
  if($('regApptDate')) $('regApptDate').value = isoDate;
  
  // Highlight cell immediately without full re-render jump
  document.querySelectorAll('.ras-day-cell').forEach(c => {
    const isSel = c.dataset.date === isoDate;
    c.classList.toggle('selected', isSel);
    c.setAttribute('aria-selected', isSel ? 'true' : 'false');
  });

  updateSelectedDateDisplay();
  updateRosterForSelectedDate();
}"""
    if old_select_date in content:
        content = content.replace(old_select_date, new_select_date)

    # 6. In updateSelectedDateDisplay(): human-friendly status badge
    old_update_disp = """function updateSelectedDateDisplay(){
  const disp = $('regSelectedDateDisplay');
  const d = new Date(REG_SELECTED_DATE + 'T12:00:00');
  if(disp && !isNaN(d.getTime())){
    disp.textContent = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
}"""
    new_update_disp = """function updateSelectedDateDisplay(){
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
}"""
    if old_update_disp in content:
        content = content.replace(old_update_disp, new_update_disp)

    # 7. Refined DOB input box alignment in .dob-row
    old_dob_css = """.dob-row{display:flex;gap:8px;width:100%;align-items:center}
  #pDobD{flex:1;min-width:0;text-align:center;padding:0 8px}
  #pDobM{flex:1.5;min-width:0;padding-left:10px;padding-right:28px;background-position:right 8px center}
  #pDobY{flex:1.2;min-width:0;text-align:center;padding:0 8px}"""

    new_dob_css = """.dob-row{display:flex;gap:8px;width:100%;align-items:center}
  #pDobD{flex:1;min-width:0;text-align:center;padding:0 8px;font-weight:700}
  #pDobM{flex:1.6;min-width:0;padding-left:12px;padding-right:28px;background-position:right 8px center;font-weight:700}
  #pDobY{flex:1.3;min-width:0;text-align:center;padding:0 8px;font-weight:700}"""
    if old_dob_css in content:
        content = content.replace(old_dob_css, new_dob_css)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully upgraded {filepath}")

if __name__ == '__main__':
    update_file('/home/projects/src-online.com/AIR-Patient-Management-System.html')
    update_file('/home/projects/src-online.com/index.html')
    print("All done!")
