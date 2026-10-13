import re

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Fonts for Display Serif (Playfair Display & Cinzel) if not already present
font_link = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,700&display=swap" rel="stylesheet">"""

if "family=Playfair+Display" not in content:
    content = content.replace('<head>', f'<head>\n{font_link}', 1)

# 2. Add Retail Rack Accordion CSS
rack_css = """  /* ================= RETAIL RACK ACCORDION GALLERY & DIRECTORY ================= */
  .rack-accordion-container {
    width: 100%;
    margin: 8px 0 24px;
    position: relative;
  }
  .rack-accordion-track {
    display: flex;
    gap: 8px;
    align-items: stretch;
    height: 380px;
    width: 100%;
    position: relative;
    padding: 6px 2px 14px;
    border-radius: 24px;
    user-select: none;
  }

  /* Each Rack Panel (Garment on the rack) */
  .rack-panel {
    position: relative;
    flex: 1 1 78px;
    min-width: 68px;
    max-width: 110px;
    height: 100%;
    border-radius: 20px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    display: flex;
    transition: flex 0.65s cubic-bezier(0.22, 1, 0.36, 1),
                max-width 0.65s cubic-bezier(0.22, 1, 0.36, 1),
                transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.4s ease;
  }
  .rack-panel:hover {
    transform: translateY(-2px);
  }

  /* Expanded Hero Panel (Occupies ~40% width) */
  .rack-panel.active,
  .rack-accordion-track:hover .rack-panel.is-hovered {
    flex: 5.6 1 420px;
    max-width: 720px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
    transform: none;
    cursor: default;
  }
  .rack-accordion-track:hover .rack-panel.active:not(.is-hovered) {
    flex: 1 1 78px;
    max-width: 110px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  }

  /* Film Grain / Textile Noise Overlay */
  .rack-grain-overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.12;
    background-image: radial-gradient(rgba(255, 255, 255, 0.2) 1px, transparent 0);
    background-size: 4px 4px;
    z-index: 1;
  }

  /* Permanent Index Tag (#01, #02...) visible in both states */
  .rack-index-anchor {
    position: absolute;
    bottom: 14px;
    right: 14px;
    font-family: 'Cinzel', serif, monospace;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.75;
    z-index: 4;
    transition: opacity 0.3s ease;
  }
  .rack-panel:hover .rack-index-anchor,
  .rack-panel.active .rack-index-anchor {
    opacity: 1;
  }

  /* --- Collapsed Rack Teaser View --- */
  .rack-collapsed-view {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 18px 8px;
    z-index: 2;
    transition: opacity 0.25s ease, transform 0.25s ease;
    opacity: 1;
  }
  .rack-collapsed-icon {
    font-size: 22px;
    line-height: 1;
  }
  .rack-collapsed-text {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    font-family: 'Cinzel', system-ui, sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    white-space: nowrap;
    opacity: 0.85;
    margin: auto 0;
  }
  .rack-collapsed-cnt {
    font-size: 10px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.15);
    white-space: nowrap;
    margin-bottom: 24px;
  }

  /* Hide Collapsed View when Expanded */
  .rack-panel.active .rack-collapsed-view,
  .rack-accordion-track:hover .rack-panel.is-hovered .rack-collapsed-view {
    opacity: 0;
    pointer-events: none;
    transform: scale(0.9);
  }
  .rack-accordion-track:hover .rack-panel.active:not(.is-hovered) .rack-collapsed-view {
    opacity: 1;
    pointer-events: auto;
    transform: none;
  }

  /* --- Expanded Hero Panel View --- */
  .rack-expanded-view {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 16px;
    padding: 24px 28px 24px 26px;
    z-index: 3;
    opacity: 0;
    pointer-events: none;
    transform: translateX(12px);
    transition: opacity 0.35s ease, transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    overflow: hidden;
  }
  .rack-panel.active .rack-expanded-view,
  .rack-accordion-track:hover .rack-panel.is-hovered .rack-expanded-view {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0);
    transition-delay: 0.1s;
  }
  .rack-accordion-track:hover .rack-panel.active:not(.is-hovered) .rack-expanded-view {
    opacity: 0;
    pointer-events: none;
    transform: translateX(12px);
    transition-delay: 0s;
  }

  /* Left Side: Editorial Typography Poster Stack */
  .rack-poster-left {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    padding-right: 16px;
  }
  .rack-meta-top {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.8;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .rack-headline-stack {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin: auto 0;
  }
  .rack-headline-line {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 34px;
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.5px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rack-blurb-bottom {
    font-size: 11.5px;
    line-height: 1.45;
    opacity: 0.85;
    margin-top: 10px;
    max-width: 260px;
  }

  /* Right Side: Seamless Integrated Directory */
  .rack-directory-right {
    display: flex;
    flex-direction: column;
    min-width: 0;
    gap: 10px;
    height: 100%;
  }
  .rack-dir-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }
  .rack-dir-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    opacity: 0.9;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .rack-dir-badge {
    font-size: 10px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
  }

  /* Directory Quick Actions */
  .rack-action-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    flex-shrink: 0;
  }
  .rack-act-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 7px 10px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    color: inherit;
    cursor: pointer;
    transition: all 0.18s ease;
    text-align: left;
    white-space: nowrap;
  }
  .rack-act-btn:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-1px);
  }
  .rack-act-btn.primary {
    background: rgba(255, 255, 255, 0.24);
    border-color: rgba(255, 255, 255, 0.45);
    font-weight: 800;
  }

  /* Live Patient Directory Roster */
  .rack-patients-roster {
    flex: 1;
    min-height: 0;
    background: rgba(0, 0, 0, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  .rack-roster-head {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
  }
  .rack-roster-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    overflow-y: auto;
    flex: 1;
  }
  .rack-roster-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 5px 8px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    cursor: pointer;
    font-size: 11px;
    transition: all 0.15s ease;
  }
  .rack-roster-item:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateX(2px);
  }
  .rack-ri-name {
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rack-ri-id {
    font-size: 9.5px;
    opacity: 0.7;
    font-family: monospace;
    margin-left: 4px;
  }
  .rack-ri-phone {
    font-size: 10px;
    opacity: 0.75;
    white-space: nowrap;
  }

  /* Responsive / Mobile (Rotated 90° Vertical Rack Accordion) */
  @media(max-width: 860px) {
    .rack-accordion-track {
      flex-direction: column;
      height: auto;
      gap: 8px;
      padding: 0;
    }
    .rack-panel {
      flex: none;
      width: 100%;
      min-width: 100%;
      max-width: 100%;
      height: 64px;
      border-radius: 16px;
    }
    .rack-panel.active {
      flex: none;
      height: 480px;
      max-width: 100%;
    }
    .rack-collapsed-view {
      flex-direction: row;
      padding: 12px 18px;
      justify-content: space-between;
    }
    .rack-collapsed-text {
      writing-mode: horizontal-tb;
      transform: none;
      font-size: 13px;
      letter-spacing: 2px;
      margin: 0;
    }
    .rack-collapsed-cnt {
      margin-bottom: 0;
    }
    .rack-expanded-view {
      grid-template-columns: 1fr;
      gap: 14px;
      padding: 18px;
      overflow-y: auto;
    }
    .rack-poster-left {
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-right: 0;
      padding-bottom: 12px;
    }
    .rack-headline-line {
      font-size: 26px;
    }
    .rack-action-row {
      grid-template-columns: 1fr;
    }
    .rack-patients-roster {
      max-height: 140px;
    }
  }

  /* Reduced Motion */
  @media(prefers-reduced-motion: reduce) {
    .rack-panel,
    .rack-expanded-view,
    .rack-collapsed-view {
      transition: none !important;
    }
  }"""

# Insert rack_css before </style>
content = content.replace('</style>', f'{rack_css}\n</style>', 1)

# 3. Add RACK_PANELS definition and render functions
rack_js = """/* ================= RETAIL RACK ACCORDION GALLERY ENGINE ================= */
const RACK_PANELS = [
  {
    id: 'Nazar (Evil Eye)',
    short: 'NAZAR',
    index: '#01',
    bg: '#1e1610',
    textColor: '#e8d7c3',
    accentColor: '#d4af37',
    icon: '🧿',
    headline: ['SHIELD', 'EVIL EYE', 'DEFENSE'],
    subhead: 'SPIRITUAL SHIELDING & PROTECTION',
    desc: 'Diagnostic assessment & protective Ruqyah shielding against envy and evil eye influences.'
  },
  {
    id: 'Jadu (Black Magic)',
    short: 'JADU',
    index: '#02',
    bg: '#16241a',
    textColor: '#c8d9ab',
    accentColor: '#8ca870',
    icon: '🌙',
    headline: ['ARCANE', 'UNBIND', 'RELEASE'],
    subhead: 'DELIVERANCE & CLEARING PROTOCOL',
    desc: 'Therapeutic clearing of arcane bondage, counter-spells & affliction deliverance.'
  },
  {
    id: 'Jinn Possession',
    short: 'JINN',
    index: '#03',
    bg: '#151318',
    textColor: '#dfd7eb',
    accentColor: '#9d8ab8',
    icon: '🕊️',
    headline: ['CLEARING', 'DELIVER', 'FREEDOM'],
    subhead: 'ENTITY DELIVERANCE & RECOVERY',
    desc: 'Spiritual deliverance, aura purification & entity detachment protocols.'
  },
  {
    id: 'Sihr (Sorcery)',
    short: 'SIHR',
    index: '#04',
    bg: '#2b1712',
    textColor: '#f5d4c8',
    accentColor: '#d97d64',
    icon: '📜',
    headline: ['CHRONIC', 'SORCERY', 'CLEAR'],
    subhead: 'DEEP THERAPEUTIC RUQYAH',
    desc: 'Intensive restorative Ruqyah addressing generational & embedded sorcery.'
  },
  {
    id: 'Waswas (Whispers)',
    short: 'WASWAS',
    index: '#05',
    bg: '#1b2226',
    textColor: '#cfe2e8',
    accentColor: '#7ba9b8',
    icon: '💭',
    headline: ['SERENITY', 'WHISPERS', 'PEACE'],
    subhead: 'MENTAL EQUANIMITY & PEACE',
    desc: 'Shielding intrusive doubts, spiritual anxieties & obsessive thoughts.'
  },
  {
    id: 'Marital Issue',
    short: 'MARITAL',
    index: '#06',
    bg: '#251b14',
    textColor: '#fae4cd',
    accentColor: '#e09f67',
    icon: '💍',
    headline: ['HARMONY', 'UNION', 'RESTORE'],
    subhead: 'SPOUSAL MEDIATION & PEACE',
    desc: 'Clearing discord between spouses, restoring affection & domestic barakah.'
  },
  {
    id: 'Health / Physical',
    short: 'HEALTH',
    index: '#07',
    bg: '#19231c',
    textColor: '#d4ebd9',
    accentColor: '#7bb88b',
    icon: '🌿',
    headline: ['SHIFA', 'HEALING', 'HOLISTIC'],
    subhead: 'BODY & SPIRITUAL ALIGNMENT',
    desc: 'Quranic healing prayers & spiritual shifa complementing clinical medical care.'
  },
  {
    id: 'Other',
    short: 'COUNSEL',
    index: '#08',
    bg: '#211c19',
    textColor: '#e8ded4',
    accentColor: '#bfa38a',
    icon: '📁',
    headline: ['INSIGHT', 'COUNSEL', 'WISDOM'],
    subhead: 'SPIRITUAL INTAKE & GUIDANCE',
    desc: 'Personal spiritual diagnosis, numerology profiling & life consultations.'
  }
];

let ACTIVE_RACK_CATEGORY = 'Nazar (Evil Eye)'; // Default hero panel

function renderRackAccordionGallery(containerId, isDashboard){
  const el = $(containerId);
  if(!el) return;

  const activeCat = SELECTED_CATEGORY || ACTIVE_RACK_CATEGORY || 'Nazar (Evil Eye)';

  el.className = 'rack-accordion-container';
  el.innerHTML = `
    <div class="rack-accordion-track" id="${containerId}_track" role="tablist">
      ${RACK_PANELS.map(panel => {
        const cnt = getCategoryCount(panel.id);
        const isAct = panel.id === activeCat;
        const pts = getPatientsForCategory(panel.id);

        return `
          <div class="rack-panel ${isAct ? 'active' : ''}" 
               data-cat="${esc(panel.id)}"
               style="background-color: ${panel.bg}; color: ${panel.textColor};"
               onclick="handleRackPanelClick('${esc(panel.id)}', '${containerId}', ${isDashboard})"
               title="${esc(panel.short)} &middot; ${esc(panel.subhead)}">
            
            <div class="rack-grain-overlay"></div>
            <div class="rack-index-anchor" style="color: ${panel.accentColor};">${panel.index}</div>

            <!-- Collapsed Teaser View -->
            <div class="rack-collapsed-view">
              <span class="rack-collapsed-icon">${panel.icon}</span>
              <span class="rack-collapsed-text" style="color: ${panel.textColor};">${panel.short}</span>
              <span class="rack-collapsed-cnt">${cnt}</span>
            </div>

            <!-- Expanded Hero View -->
            <div class="rack-expanded-view">
              <!-- Left: Editorial Typography Poster Stack -->
              <div class="rack-poster-left">
                <div class="rack-meta-top" style="color: ${panel.accentColor};">
                  <span>${panel.icon}</span>
                  <span>${panel.subhead}</span>
                </div>

                <div class="rack-headline-stack">
                  ${panel.headline.map(line => `
                    <div class="rack-headline-line" style="color: ${panel.textColor};">${line}</div>
                  `).join('')}
                </div>

                <div class="rack-blurb-bottom">
                  ${esc(panel.desc)}
                </div>
              </div>

              <!-- Right: Seamless Integrated Directory -->
              <div class="rack-directory-right">
                <div class="rack-dir-header">
                  <div class="rack-dir-title">
                    <span>${panel.icon}</span>
                    <span>${panel.short} Directory</span>
                  </div>
                  <span class="rack-dir-badge">${cnt} Cases</span>
                </div>

                <!-- Directory Actions -->
                <div class="rack-action-row">
                  <button type="button" class="rack-act-btn primary" onclick="event.stopPropagation(); filterCategoryDirectory('${esc(panel.id)}')">
                    <span>🔍</span> Filter Table &rarr;
                  </button>
                  <button type="button" class="rack-act-btn" onclick="event.stopPropagation(); openNewPatientForCategory('${esc(panel.id)}')">
                    <span>➕</span> Add [${panel.short}] Patient
                  </button>
                  <button type="button" class="rack-act-btn" onclick="event.stopPropagation(); openBookSessionForCategory('${esc(panel.id)}')">
                    <span>📅</span> Book Session
                  </button>
                  <button type="button" class="rack-act-btn" onclick="event.stopPropagation(); printCategoryRoster('${esc(panel.id)}')">
                    <span>🖨️</span> Print Slips
                  </button>
                </div>

                <!-- Live Patient Roster -->
                <div class="rack-patients-roster">
                  <div class="rack-roster-head">
                    <span>Registered Patients</span>
                    <span>${pts.length} Active</span>
                  </div>
                  <div class="rack-roster-list">
                    ${pts.length > 0 ? pts.map(p => `
                      <div class="rack-roster-item" onclick="event.stopPropagation(); editPatient('${esc(p.id)}')" title="View/Edit Patient Record">
                        <div>
                          <span class="rack-ri-name">${esc(p.name)}</span>
                          <span class="rack-ri-id">#${esc(p.id)}</span>
                        </div>
                        <span class="rack-ri-phone">${esc(p.mobile || 'No Phone')}</span>
                      </div>
                    `).join('') : `
                      <div class="cec-empty-state">
                        <span>No cases registered in this category.</span>
                        <button type="button" class="btn btn-outline btn-sm" style="font-size:10px;padding:3px 8px;margin-top:4px;" onclick="event.stopPropagation(); openNewPatientForCategory('${esc(panel.id)}')">
                          ＋ Register First Record
                        </button>
                      </div>
                    `}
                  </div>
                </div>

              </div>
            </div>

          </div>
        `;
      }).join('')}
    </div>
  `;

  // Attach hover mechanics
  const track = $(`${containerId}_track`);
  if(track){
    const panels = Array.from(track.querySelectorAll('.rack-panel'));
    panels.forEach(panel => {
      panel.addEventListener('mouseenter', () => {
        panels.forEach(p => p.classList.remove('is-hovered'));
        panel.classList.add('is-hovered');
      });
    });
    track.addEventListener('mouseleave', () => {
      panels.forEach(p => p.classList.remove('is-hovered'));
    });
  }
}

function handleRackPanelClick(catId, containerId, isDashboard){
  ACTIVE_RACK_CATEGORY = catId;
  SELECTED_CATEGORY = catId;

  // Sync panels in both tracks
  document.querySelectorAll('.rack-panel').forEach(p => {
    const isAct = p.dataset.cat === catId;
    p.classList.toggle('active', isAct);
    p.classList.remove('is-hovered');
  });

  // Update hint text on Patients page
  const hint = $('catActiveHint');
  if(hint){
    const catObj = CATEGORIES.find(c => c.id === catId);
    const icon = catObj ? catObj.icon + ' ' : '';
    const cnt = getCategoryCount(catId);
    hint.innerHTML = `Showing directory for: <strong>${icon}${esc(catId)}</strong> (${cnt} patient${cnt===1?'':'s'}) &middot; <a href="javascript:void(0)" onclick="selectCategory('')" style="color:var(--brown);font-weight:700">Show All &times;</a>`;
  }

  if($('patFilter')) $('patFilter').value = catId;
  if(!isDashboard && CURRENT_ACTIVE_TAB === 'patients'){
    renderPatients();
  }
  updateCategoryBadges();
}"""

# Replace initCategoriesUI implementation to render the Rack Accordion
old_init_cats = """function initCategoriesUI(){
  // 1. Render Category Cards Deck on Patient Directory page
  renderCategoryCardsDeck('categoryPillsRow', false);

  // 2. Render Category Cards Deck on Dashboard
  renderCategoryCardsDeck('dashboardCatGrid', true);

  // Total badge in nav
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
}"""

new_init_cats = rack_js + """

function initCategoriesUI(){
  // 1. Render Retail Rack Accordion Gallery on Patient Directory page
  renderRackAccordionGallery('categoryPillsRow', false);

  // 2. Render Retail Rack Accordion Gallery on Dashboard
  renderRackAccordionGallery('dashboardCatGrid', true);

  // Total badge in nav
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
}"""

assert old_init_cats in content, "old_init_cats not found"
content = content.replace(old_init_cats, new_init_cats, 1)

# Also update selectCategory to sync rack panels
old_sel_cat_sync = """  // Sync category expand cards in both decks
  document.querySelectorAll('.cat-expand-card').forEach(card => {
    const isAct = card.dataset.cat === catId;
    card.classList.toggle('active', isAct);
  });"""

new_sel_cat_sync = """  // Sync category expand cards in both decks
  document.querySelectorAll('.cat-expand-card').forEach(card => {
    const isAct = card.dataset.cat === catId;
    card.classList.toggle('active', isAct);
  });
  // Sync retail rack accordion panels
  document.querySelectorAll('.rack-panel').forEach(card => {
    const isAct = card.dataset.cat === catId;
    card.classList.toggle('active', isAct);
    card.classList.remove('is-hovered');
  });"""

assert old_sel_cat_sync in content, "old_sel_cat_sync not found"
content = content.replace(old_sel_cat_sync, new_sel_cat_sync, 1)

# Write out files
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Retail Rack Accordion Gallery applied successfully!")
