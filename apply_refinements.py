import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. dateToISO helper
    if 'function dateToISO(d)' not in content:
        content = content.replace(
            "function todayISO(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }",
            "function dateToISO(d){ if(!d) return ''; return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }\nfunction todayISO(){ return dateToISO(new Date()); }"
        )

    # 2. setRegCalendarPreset target.toISOString().slice(0, 10)
    content = content.replace(
        "const iso = target.toISOString().slice(0, 10);",
        "const iso = dateToISO(target);"
    )

    # 3. setRegTimeSlot fallback when btnEl is omitted
    old_time_slot = """function setRegTimeSlot(start, end, btnEl){
  $('regApptStart').value = start;
  $('regApptEnd').value = end;

  // Highlight slot chip
  document.querySelectorAll('.ras-slot-chip').forEach(btn => {
    btn.classList.remove('active');
  });
  if(btnEl){
    btnEl.classList.add('active');
  }
}"""
    new_time_slot = """function setRegTimeSlot(start, end, btnEl){
  $('regApptStart').value = start;
  $('regApptEnd').value = end;

  // Highlight slot chip
  document.querySelectorAll('.ras-slot-chip').forEach(btn => {
    btn.classList.remove('active');
  });
  if(btnEl){
    btnEl.classList.add('active');
  } else {
    document.querySelectorAll('.ras-slot-chip').forEach(btn => {
      const oc = btn.getAttribute('onclick') || '';
      if(oc.includes("'" + start + "'") || oc.includes('"' + start + '"')){
        btn.classList.add('active');
      }
    });
  }
}"""
    if old_time_slot in content:
        content = content.replace(old_time_slot, new_time_slot)

    # 4. toggleRegApptBooking - handle editing state gracefully
    old_toggle = """function toggleRegApptBooking(enabled){
  const body = $('rasContentBody');
  const btn = $('savePatientBtn') || document.querySelector('#patientForm button[type=submit]');
  if(body) body.classList.toggle('disabled', !enabled);
  if(btn){
    btn.textContent = enabled ? '💾 Save Patient & Book Appointment' : '💾 Save Patient Record Only';
  }
}"""
    new_toggle = """function toggleRegApptBooking(enabled){
  const body = $('rasContentBody');
  const btn = $('savePatientBtn') || document.querySelector('#patientForm button[type=submit]');
  const isEditing = $('editId') && $('editId').value;
  if(body) body.classList.toggle('disabled', !enabled);
  if(btn){
    if(isEditing){
      btn.textContent = enabled ? '💾 Update Patient & Book Session' : '💾 Update Patient Record';
    } else {
      btn.textContent = enabled ? '💾 Save Patient & Book Appointment' : '💾 Save Patient Record Only';
    }
  }
}"""
    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)

    # 5. editPatient - disable regApptEnabled by default to avoid unintended appt creation
    old_edit_patient = """function editPatient(id){
  const p=patientById(id); if(!p) return;
  goTab('register');
  $('editId').value=p.id; $('pId').value=p.id; $('pDate').value=fmtDate(p.registered);
  $('pName').value=p.name; $('pFather').value=p.father||''; $('pMobile').value=p.mobile;
  $('pCountry').value=p.country||''; updateCountryHint();
  setDobBoxes(p.dob||''); $('pGender').value=p.gender||'';
  $('pProblem').value=p.problem||''; $('pAddress').value=p.address||''; $('pNotes').value=p.notes||'';
  document.querySelector('#patientForm button[type=submit]').textContent = '💾 Update Patient Record';
}"""
    new_edit_patient = """function editPatient(id){
  const p=patientById(id); if(!p) return;
  goTab('register');
  $('editId').value=p.id; $('pId').value=p.id; $('pDate').value=fmtDate(p.registered);
  $('pName').value=p.name; $('pFather').value=p.father||''; $('pMobile').value=p.mobile;
  $('pCountry').value=p.country||''; updateCountryHint();
  setDobBoxes(p.dob||''); $('pGender').value=p.gender||'';
  $('pProblem').value=p.problem||''; $('pAddress').value=p.address||''; $('pNotes').value=p.notes||'';
  if($('regApptEnabled')){
    $('regApptEnabled').checked = false;
    toggleRegApptBooking(false);
  }
  const btn = $('savePatientBtn') || document.querySelector('#patientForm button[type=submit]');
  if(btn) btn.textContent = '💾 Update Patient Record';
}"""
    if old_edit_patient in content:
        content = content.replace(old_edit_patient, new_edit_patient)

    # 6. openBookSessionForCategory - call updateApptCurrency
    old_open_book = """function openBookSessionForCategory(catId){
  goTab('appointments');
  setTimeout(() => {
    const pts = DB.patients.filter(p => !catId || p.problem === catId);
    const pSel = $('aPatient');
    if(pSel && pts.length > 0){
      pSel.value = pts[0].id;
      if(typeof updateApptAutoFields === 'function') updateApptAutoFields();
    }
    const f = $('apptForm');
    if(f) f.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 100);
}"""
    new_open_book = """function openBookSessionForCategory(catId){
  goTab('appointments');
  setTimeout(() => {
    const pts = DB.patients.filter(p => !catId || p.problem === catId);
    const pSel = $('aPatient');
    if(pSel && pts.length > 0){
      pSel.value = pts[0].id;
      if(typeof updateApptCurrency === 'function') updateApptCurrency();
    }
    const f = $('apptForm');
    if(f) f.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 100);
}"""
    if old_open_book in content:
        content = content.replace(old_open_book, new_open_book)

    # 7. handleRackPanelClick - smooth scroll into view on mobile
    old_handle_rack = """function handleRackPanelClick(catId, containerId, isDashboard){
  ACTIVE_RACK_CATEGORY = catId;
  SELECTED_CATEGORY = catId;

  // Sync panels in both tracks
  document.querySelectorAll('.rack-panel').forEach(p => {
    const isAct = p.dataset.cat === catId;
    p.classList.toggle('active', isAct);
    p.classList.remove('is-hovered');
  });

  // Update hint text on Patients page"""

    new_handle_rack = """function handleRackPanelClick(catId, containerId, isDashboard){
  ACTIVE_RACK_CATEGORY = catId;
  SELECTED_CATEGORY = catId;

  // Sync panels in both tracks
  document.querySelectorAll('.rack-panel').forEach(p => {
    const isAct = p.dataset.cat === catId;
    p.classList.toggle('active', isAct);
    p.classList.remove('is-hovered');
  });

  // Smooth scroll active panel into center on mobile
  const activePanel = document.querySelector(`#${containerId} .rack-panel[data-cat="${catId}"]`);
  if(activePanel && window.innerWidth < 960){
    activePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }

  // Update hint text on Patients page"""
    if old_handle_rack in content:
        content = content.replace(old_handle_rack, new_handle_rack)

    # 8. selectCategory - preserve hero panel if catId is empty
    old_select_cat = """  // Sync retail rack accordion panels
  document.querySelectorAll('.rack-panel').forEach(card => {
    const isAct = card.dataset.cat === catId;
    card.classList.toggle('active', isAct);
    card.classList.remove('is-hovered');
  });"""
    new_select_cat = """  // Sync retail rack accordion panels (retain hero panel if showing all)
  const targetRackCat = catId || ACTIVE_RACK_CATEGORY || 'Nazar (Evil Eye)';
  document.querySelectorAll('.rack-panel').forEach(card => {
    const isAct = card.dataset.cat === targetRackCat;
    card.classList.toggle('active', isAct);
    card.classList.remove('is-hovered');
  });"""
    if old_select_cat in content:
        content = content.replace(old_select_cat, new_select_cat)

    # 9. Accessibility on rack panels
    old_rack_markup = """          <div class="rack-panel ${isAct ? 'active' : ''}" 
               data-cat="${esc(panel.id)}"
               style="background-color: ${panel.bg}; color: ${panel.textColor};"
               onclick="handleRackPanelClick('${esc(panel.id)}', '${containerId}', ${isDashboard})"
               title="${esc(panel.short)} &middot; ${esc(panel.subhead)}">"""

    new_rack_markup = """          <div class="rack-panel ${isAct ? 'active' : ''}" 
               data-cat="${esc(panel.id)}"
               role="tab"
               tabindex="0"
               aria-selected="${isAct ? 'true' : 'false'}"
               style="background-color: ${panel.bg}; color: ${panel.textColor};"
               onclick="handleRackPanelClick('${esc(panel.id)}', '${containerId}', ${isDashboard})"
               onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();handleRackPanelClick('${esc(panel.id)}', '${containerId}', ${isDashboard});}"
               title="${esc(panel.short)} &middot; ${esc(panel.subhead)}">"""
    if old_rack_markup in content:
        content = content.replace(old_rack_markup, new_rack_markup)

    # 10. CSS for small mobile screens (<= 520px)
    old_css_media = """  @media(max-width: 860px) {
    .ras-layout-grid {
      grid-template-columns: 1fr;
    }
    .ras-form-fields-grid {
      grid-template-columns: 1fr 1fr;
    }
  }"""
    new_css_media = """  @media(max-width: 860px) {
    .ras-layout-grid {
      grid-template-columns: 1fr;
    }
    .ras-form-fields-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media(max-width: 520px) {
    .ras-form-fields-grid {
      grid-template-columns: 1fr;
    }
    .ras-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }
  }"""
    if old_css_media in content:
        content = content.replace(old_css_media, new_css_media)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Refined {filepath}")

if __name__ == '__main__':
    update_file('/home/projects/src-online.com/AIR-Patient-Management-System.html')
    update_file('/home/projects/src-online.com/index.html')
    print("Done!")
