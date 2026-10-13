import re

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Expandable Category Card Deck
old_css_anchor = """  /* Dashboard Categories Directory */
  .cat-directory-card{
    margin-bottom:26px;
  }"""

new_css = """  /* ================= EXPANDABLE CATEGORY CARD DECK ================= */
  .cat-expand-deck {
    display: flex;
    gap: 12px;
    align-items: stretch;
    height: 220px;
    position: relative;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding: 6px 2px 14px;
    margin-bottom: 8px;
  }
  .cat-expand-deck::-webkit-scrollbar {
    display: none;
  }

  /* Base Category Card */
  .cat-expand-card {
    position: relative;
    flex: 1 1 95px;
    min-width: 88px;
    max-width: 140px;
    height: 100%;
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(61, 40, 29, 0.03);
    user-select: none;
    display: flex;
    transition: flex 0.38s cubic-bezier(0.25, 1, 0.5, 1),
                max-width 0.38s cubic-bezier(0.25, 1, 0.5, 1),
                border-color 0.25s ease,
                box-shadow 0.25s ease,
                background-color 0.25s ease,
                transform 0.2s ease;
  }
  .cat-expand-card:hover {
    border-color: #c4b5a6;
    transform: translateY(-2px);
  }

  /* Active / Expanded Category Card */
  .cat-expand-card.active {
    flex: 4.8 1 440px;
    min-width: 380px;
    max-width: 680px;
    border-color: var(--brown);
    box-shadow: 0 8px 26px rgba(124, 83, 57, 0.12);
    background: #fffdfa;
    transform: none;
  }

  /* Collapsed View of Category Card */
  .cec-collapsed {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 14px 8px;
    gap: 8px;
    text-align: center;
    transition: opacity 0.2s ease, transform 0.2s ease;
    opacity: 1;
    pointer-events: auto;
  }
  .cec-icon {
    font-size: 26px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: #fbf6ee;
    border: 1px solid var(--border);
    transition: transform 0.2s ease;
  }
  .cat-expand-card:hover .cec-icon {
    transform: scale(1.1);
  }
  .cec-title {
    font-size: 12.5px;
    font-weight: 800;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 95px;
  }
  .cec-count {
    font-size: 10.5px;
    font-weight: 700;
    color: var(--brown);
    background: #f4ece2;
    padding: 2px 8px;
    border-radius: 999px;
    white-space: nowrap;
    border: 1px solid rgba(124, 83, 57, 0.12);
  }
  .cec-hint {
    font-size: 9.5px;
    color: var(--muted);
    font-weight: 600;
    opacity: 0.8;
  }

  /* Hide Collapsed View when Expanded */
  .cat-expand-card.active .cec-collapsed {
    opacity: 0;
    pointer-events: none;
    position: absolute;
    transform: scale(0.92);
  }

  /* Expanded View of Category Card */
  .cec-expanded {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 14px 18px;
    opacity: 0;
    pointer-events: none;
    transform: translateX(8px);
    transition: opacity 0.28s ease, transform 0.28s ease;
    overflow: hidden;
  }
  .cat-expand-card.active .cec-expanded {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0);
    transition-delay: 0.05s;
  }

  /* Expanded Category Card Header */
  .cec-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border-bottom: 1px solid #ebdccb;
    padding-bottom: 10px;
    flex-shrink: 0;
  }
  .cec-head-left {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
  }
  .cec-head-icon {
    font-size: 24px;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: #fbf6ee;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .cec-head-title {
    font-size: 15px;
    font-weight: 800;
    color: var(--brown-dark);
    line-height: 1.2;
    white-space: nowrap;
  }
  .cec-head-desc {
    font-size: 11.5px;
    color: var(--muted);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .cec-head-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }
  .cec-badge {
    font-size: 11px;
    font-weight: 800;
    color: var(--brown);
    background: #f4ece2;
    padding: 3px 10px;
    border-radius: 999px;
    white-space: nowrap;
  }
  .cec-close-btn {
    border: 1px solid var(--border);
    background: #ffffff;
    color: var(--muted);
    width: 24px;
    height: 24px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
  }
  .cec-close-btn:hover {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
  }

  /* Directories Body */
  .cec-body {
    display: flex;
    gap: 12px;
    margin-top: 10px;
    flex: 1;
    min-height: 0;
  }

  /* Directory Action Buttons (Left column) */
  .cec-dir-actions {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 185px;
    flex-shrink: 0;
  }
  .cec-dir-btn {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 8px;
    cursor: pointer;
    font-size: 11.5px;
    font-weight: 700;
    color: var(--brown-dark);
    transition: all 0.16s ease;
    text-align: left;
    white-space: nowrap;
  }
  .cec-dir-btn:hover {
    background: #fbf6ef;
    border-color: var(--brown);
    color: var(--brown-dark);
    transform: translateX(2px);
  }
  .cec-dir-btn.primary {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
  }
  .cec-dir-btn.primary:hover {
    background: var(--brown-dark);
    color: #ffffff;
  }

  /* Directory Patient Cases Roster (Right column) */
  .cec-dir-patients {
    flex: 1;
    min-width: 0;
    background: #fdfaf6;
    border: 1px solid #ede1d2;
    border-radius: 10px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  .cec-patients-head {
    font-size: 10.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--muted);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .cec-patients-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    overflow-y: auto;
    flex: 1;
  }
  .cec-patient-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 5px 8px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 11px;
  }
  .cec-patient-item:hover {
    background: #fbf6ee;
    border-color: var(--brown);
    transform: translateX(2px);
  }
  .cec-pi-name {
    font-weight: 750;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .cec-pi-id {
    font-size: 9.5px;
    color: var(--muted);
    font-family: monospace;
    margin-left: 4px;
  }
  .cec-pi-meta {
    font-size: 10px;
    color: var(--muted);
    white-space: nowrap;
  }
  .cec-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 6px;
    height: 100%;
    color: var(--muted);
    font-size: 11px;
    padding: 8px;
  }

  /* Responsive Mobile */
  @media(max-width: 960px) {
    .cat-expand-deck {
      height: 250px;
      padding-bottom: 6px;
    }
    .cat-expand-card {
      flex: 0 0 58px;
      min-width: 58px;
      max-width: 58px;
    }
    .cat-expand-card.active {
      flex: 0 0 calc(100vw - 36px);
      min-width: 300px;
      max-width: 440px;
    }
    .cec-body {
      flex-direction: column;
      gap: 8px;
    }
    .cec-dir-actions {
      flex-direction: row;
      flex-wrap: wrap;
      width: 100%;
      gap: 6px;
    }
    .cec-dir-btn {
      flex: 1 1 45%;
      padding: 5px 8px;
      font-size: 11px;
    }
    .cec-dir-patients {
      max-height: 95px;
    }
  }

  /* Dashboard Categories Directory */
  .cat-directory-card{
    margin-bottom:26px;
  }"""

assert old_css_anchor in content, "old_css_anchor not found"
content = content.replace(old_css_anchor, new_css, 1)

# 2. Update HTML elements: add .cat-expand-deck class
content = content.replace('<div class="cat-grid" id="dashboardCatGrid"></div>', '<div class="cat-expand-deck" id="dashboardCatGrid"></div>', 1)
content = content.replace('<div class="category-pills-row" id="categoryPillsRow"></div>', '<div class="cat-expand-deck" id="categoryPillsRow"></div>', 1)

# 3. Update JavaScript logic for Category Cards Deck
old_cat_js = """function initCategoriesUI(){
  // 1. Render Category Explorer Pills
  const pillsRow = $('categoryPillsRow');
  if(pillsRow){
    pillsRow.innerHTML = CATEGORIES.map(c => {
      const cnt = getCategoryCount(c.id);
      const isAct = c.id === SELECTED_CATEGORY;
      return `<button type="button" class="cat-pill ${isAct?'active':''}" data-cat="${esc(c.id)}" onclick="selectCategory('${esc(c.id)}')">
        <span class="cat-icon">${c.icon}</span>
        <span class="cat-name">${esc(c.name)}</span>
        <span class="cat-count" id="pill-cnt-${esc(c.id)}">${cnt}</span>
        <span class="cat-expand-text">Open Directory &rarr;</span>
      </button>`;
    }).join('');
  }

  // 2. Render Dashboard Category Cards
  const dashGrid = $('dashboardCatGrid');
  if(dashGrid){
    dashGrid.innerHTML = CATEGORIES.filter(c => c.id !== '').map(c => {
      const cnt = getCategoryCount(c.id);
      return `<div class="cat-card" onclick="selectCategory('${esc(c.id)}')">
        <div class="cat-card-top">
          <div class="cat-card-icon">${c.icon}</div>
          <span class="cat-card-count" id="dash-cnt-${esc(c.id)}">${cnt} case${cnt===1?'':'s'}</span>
        </div>
        <div class="cat-card-title">${esc(c.name)}</div>
        <div class="cat-card-desc">${esc(c.desc)}</div>
        <div class="cat-card-action">Open Directory &rarr;</div>
      </div>`;
    }).join('');
  }

  // 3. Render Navigation Dropdown Items
  const navList = $('navCatList');
  if(navList){
    navList.innerHTML = CATEGORIES.map(c => {
      const cnt = getCategoryCount(c.id);
      return `<div class="nav-cat-item" onclick="selectCategory('${esc(c.id)}')">
        <div class="nav-ci-left">
          <span class="nav-ci-icon">${c.icon}</span>
          <span class="nav-ci-name">${esc(c.name)}</span>
        </div>
        <span class="nav-ci-badge" id="nav-cnt-${esc(c.id)}">${cnt}</span>
      </div>`;
    }).join('');
  }

  // Total badge in nav
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
}"""

new_cat_js = """function getPatientsForCategory(catId){
  if(!catId) return DB.patients.slice(0, 10);
  return DB.patients.filter(p => p.problem === catId);
}

function renderPatientRosterHtml(pts, catId){
  if(!pts || pts.length === 0){
    return `<div class="cec-empty-state">
      <span>No patient records in this category yet.</span>
      <button type="button" class="btn btn-outline btn-sm" onclick="event.stopPropagation(); openNewPatientForCategory('${esc(catId)}')">
        ＋ Register First Patient
      </button>
    </div>`;
  }
  return pts.map(p => `
    <div class="cec-patient-item" onclick="event.stopPropagation(); editPatient('${esc(p.id)}')" title="Click to view & edit patient record">
      <div>
        <span class="cec-pi-name">${esc(p.name)}</span>
        <span class="cec-pi-id">#${esc(p.id)}</span>
      </div>
      <span class="cec-pi-meta">${esc(p.mobile || 'No Phone')} ${p.age ? '&middot; ' + p.age + 'y' : ''}</span>
    </div>
  `).join('');
}

function renderCategoryCardsDeck(containerId, isDashboard){
  const deck = $(containerId);
  if(!deck) return;

  const catsToRender = isDashboard ? CATEGORIES.filter(c => c.id !== '') : CATEGORIES;

  deck.innerHTML = catsToRender.map(c => {
    const cnt = getCategoryCount(c.id);
    const isAct = c.id === SELECTED_CATEGORY;
    const pts = getPatientsForCategory(c.id);

    return `<div class="cat-expand-card ${isAct ? 'active' : ''}" data-cat="${esc(c.id)}" onclick="toggleCategoryCard('${esc(c.id)}', '${containerId}', ${isDashboard})" title="${esc(c.name)}">
      <!-- Collapsed Preview -->
      <div class="cec-collapsed">
        <div class="cec-icon">${c.icon}</div>
        <div class="cec-title">${esc(c.short || c.name)}</div>
        <div class="cec-count">${cnt} case${cnt===1?'':'s'}</div>
        <div class="cec-hint">Click to open &dtrif;</div>
      </div>

      <!-- Expanded Directory View -->
      <div class="cec-expanded">
        <div class="cec-header">
          <div class="cec-head-left">
            <div class="cec-head-icon">${c.icon}</div>
            <div>
              <div class="cec-head-title">${esc(c.name)}</div>
              <div class="cec-head-desc">${esc(c.desc)}</div>
            </div>
          </div>
          <div class="cec-head-actions">
            <span class="cec-badge">${cnt} Total Case${cnt===1?'':'s'}</span>
            <button type="button" class="cec-close-btn" onclick="event.stopPropagation(); closeCategoryDeck('${containerId}')" title="Collapse card">&times;</button>
          </div>
        </div>

        <div class="cec-body">
          <div class="cec-dir-actions">
            <button type="button" class="cec-dir-btn primary" onclick="event.stopPropagation(); filterCategoryDirectory('${esc(c.id)}')">
              <span>🔍</span> View Directory Table &rarr;
            </button>
            <button type="button" class="cec-dir-btn" onclick="event.stopPropagation(); openNewPatientForCategory('${esc(c.id)}')">
              <span>➕</span> Add [${esc(c.short || c.name)}] Patient
            </button>
            <button type="button" class="cec-dir-btn" onclick="event.stopPropagation(); openBookSessionForCategory('${esc(c.id)}')">
              <span>📅</span> Schedule Ruqyah Session
            </button>
            <button type="button" class="cec-dir-btn" onclick="event.stopPropagation(); printCategoryRoster('${esc(c.id)}')">
              <span>🖨️</span> Print Case Slips
            </button>
          </div>

          <div class="cec-dir-patients">
            <div class="cec-patients-head">
              <span>Live Patient Directory</span>
              <span>${pts.length} ${pts.length === 1 ? 'Record' : 'Records'}</span>
            </div>
            <div class="cec-patients-list">
              ${renderPatientRosterHtml(pts, c.id)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
  }).join('');
}

function toggleCategoryCard(catId, containerId, isDashboard){
  SELECTED_CATEGORY = catId;
  const deck = $(containerId);
  if(deck){
    deck.querySelectorAll('.cat-expand-card').forEach(c => {
      const isAct = c.dataset.cat === catId;
      c.classList.toggle('active', isAct);
    });
    const activeCard = deck.querySelector(`.cat-expand-card[data-cat="${catId}"]`);
    if(activeCard){
      activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  // Update hint text on Patients page
  const hint = $('catActiveHint');
  if(hint){
    if(catId){
      const catObj = CATEGORIES.find(c => c.id === catId);
      const icon = catObj ? catObj.icon + ' ' : '';
      const cnt = getCategoryCount(catId);
      hint.innerHTML = `Showing directory for: <strong>${icon}${esc(catId)}</strong> (${cnt} patient${cnt===1?'':'s'}) &middot; <a href="javascript:void(0)" onclick="selectCategory('')" style="color:var(--brown);font-weight:700">Show All &times;</a>`;
    } else {
      hint.textContent = `Showing all categories (${DB.patients.length} patients)`;
    }
  }

  if($('patFilter')) $('patFilter').value = catId;
  if(!isDashboard && CURRENT_ACTIVE_TAB === 'patients'){
    renderPatients();
  }
  updateCategoryBadges();
}

function closeCategoryDeck(containerId){
  SELECTED_CATEGORY = '';
  const deck = $(containerId);
  if(deck){
    deck.querySelectorAll('.cat-expand-card').forEach(c => c.classList.remove('active'));
  }
  if($('patFilter')) $('patFilter').value = '';
  const hint = $('catActiveHint');
  if(hint) hint.textContent = `Showing all categories (${DB.patients.length} patients)`;
  if(CURRENT_ACTIVE_TAB === 'patients') renderPatients();
  updateCategoryBadges();
}

function filterCategoryDirectory(catId){
  selectCategory(catId);
  setTimeout(() => {
    const table = $('patTable');
    if(table){
      table.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 100);
}

function openBookSessionForCategory(catId){
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
}

function printCategoryRoster(catId){
  selectCategory(catId);
  setTimeout(() => {
    goTab('reports');
    printList();
  }, 120);
}

function initCategoriesUI(){
  // 1. Render Category Cards Deck on Patient Directory page
  renderCategoryCardsDeck('categoryPillsRow', false);

  // 2. Render Category Cards Deck on Dashboard
  renderCategoryCardsDeck('dashboardCatGrid', true);

  // Total badge in nav
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
}"""

assert old_cat_js in content, "old_cat_js not found"
content = content.replace(old_cat_js, new_cat_js, 1)

# 4. In selectCategory, also expand the category card in both decks
old_sel_cat = """function selectCategory(catId){
  SELECTED_CATEGORY = catId;
  if($('patFilter')) $('patFilter').value = catId;

  // Update pills active state
  document.querySelectorAll('.cat-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.cat === catId);
  });"""

new_sel_cat = """function selectCategory(catId){
  SELECTED_CATEGORY = catId;
  if($('patFilter')) $('patFilter').value = catId;

  // Sync category expand cards in both decks
  document.querySelectorAll('.cat-expand-card').forEach(card => {
    const isAct = card.dataset.cat === catId;
    card.classList.toggle('active', isAct);
  });"""

assert old_sel_cat in content, "old_sel_cat not found"
content = content.replace(old_sel_cat, new_sel_cat, 1)

# Write to AIR-Patient-Management-System.html and index.html
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Expandable Category Cards Deck applied successfully!")
