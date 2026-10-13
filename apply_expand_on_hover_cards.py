import re

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. New CSS Block
old_nav_css = """  /* ---------- Nav Tabs Expand-On-Hover ---------- */
  nav.tabs{
    background:rgba(255,255,255,.95);
    backdrop-filter:blur(10px);
    -webkit-backdrop-filter:blur(10px);
    display:flex;gap:8px;padding:8px 18px;
    border-bottom:1.5px solid var(--border);
    position:sticky;top:72px;z-index:40;
    overflow-x:auto;
    align-items:center;
  }
  nav.tabs button.tab-btn{
    border:1.5px solid var(--border);
    background:rgba(255,255,255,.8);
    height:42px;
    padding:0 14px;
    border-radius:999px;
    font-size:13.5px;
    font-weight:700;
    color:var(--muted);
    cursor:pointer;
    white-space:nowrap;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 1px 4px rgba(61,40,29,.03);
    /* Expand on hover effect */
    transition:all .28s cubic-bezier(.2,.8,.2,1);
    position:relative;
    overflow:hidden;
  }
  nav.tabs button.tab-btn .tab-icon{
    font-size:15px;
    line-height:1;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    flex-shrink:0;
    transition:transform .2s ease;
  }
  nav.tabs button.tab-btn .tab-text{
    max-width:0;
    opacity:0;
    overflow:hidden;
    white-space:nowrap;
    transition:max-width .3s cubic-bezier(.2,.8,.2,1), opacity .22s ease, margin .22s ease;
  }
  /* Active tab is expanded */
  nav.tabs button.tab-btn.active{
    background:var(--brown);
    color:#ffffff;
    border-color:var(--brown-dark);
    box-shadow:0 3px 12px rgba(124,83,57,.3);
    padding:0 18px;
  }
  nav.tabs button.tab-btn.active .tab-icon{
    transform:scale(1.1);
  }
  nav.tabs button.tab-btn.active .tab-text{
    max-width:170px;
    opacity:1;
    margin-left:8px;
  }
  /* Inactive tab expands on hover */
  nav.tabs button.tab-btn:not(.active):hover{
    background:#ffffff;
    color:var(--brown-dark);
    border-color:var(--brown);
    box-shadow:0 6px 18px rgba(124,83,57,.18);
    transform:translateY(-2px);
    padding:0 18px;
  }
  nav.tabs button.tab-btn:not(.active):hover .tab-icon{
    transform:scale(1.15);
  }
  nav.tabs button.tab-btn:not(.active):hover .tab-text{
    max-width:170px;
    opacity:1;
    margin-left:8px;
  }
  .nav-tab-wrapper button.tab-btn .nav-arrow{
    max-width:0;
    opacity:0;
    overflow:hidden;
    transition:max-width .3s ease, opacity .2s ease, margin .2s ease;
  }
  .nav-tab-wrapper button.tab-btn.active .nav-arrow,
  .nav-tab-wrapper:hover button.tab-btn .nav-arrow{
    max-width:16px;
    opacity:0.8;
    margin-left:4px;
  }"""

new_nav_css = """  /* ================= MINIMALIST EXPAND-ON-HOVER CARD NAVIGATION ================= */
  .expand-nav-container {
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1.5px solid var(--border);
    padding: 10px 18px;
    position: sticky;
    top: 72px;
    z-index: 45;
    box-shadow: 0 2px 10px rgba(61, 40, 29, 0.03);
  }
  .expand-nav-track {
    max-width: 1240px;
    margin: 0 auto;
    display: flex;
    gap: 10px;
    align-items: stretch;
    height: 168px;
    position: relative;
  }
  
  /* The Base Card */
  .expand-card {
    position: relative;
    flex: 1 1 85px;
    min-width: 78px;
    max-width: 140px;
    height: 100%;
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 1px 4px rgba(61, 40, 29, 0.03);
    user-select: none;
    display: flex;
    transition: flex 0.35s cubic-bezier(0.25, 1, 0.5, 1),
                max-width 0.35s cubic-bezier(0.25, 1, 0.5, 1),
                border-color 0.25s ease,
                box-shadow 0.25s ease,
                background-color 0.25s ease;
  }
  .expand-card:hover {
    border-color: #c9bbae;
  }

  /* Active card (when track is not hovered) */
  .expand-card.active {
    flex: 4.2 1 380px;
    max-width: 650px;
    border-color: var(--brown);
    box-shadow: 0 4px 18px rgba(124, 83, 57, 0.10);
    background: #fffdfa;
  }

  /* When track is hovered by mouse: the hovered card expands, other cards stay collapsed */
  .expand-nav-track:hover .expand-card.is-hovered {
    flex: 4.2 1 380px;
    max-width: 650px;
    border-color: var(--brown);
    box-shadow: 0 6px 20px rgba(124, 83, 57, 0.12);
    background: #fffdfa;
  }
  .expand-nav-track:hover .expand-card.active:not(.is-hovered) {
    flex: 1 1 85px;
    max-width: 140px;
    border-color: var(--border);
    box-shadow: 0 1px 4px rgba(61, 40, 29, 0.03);
    background: #ffffff;
  }

  /* --- Collapsed View --- */
  .card-collapsed-view {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px 6px;
    gap: 8px;
    text-align: center;
    transition: opacity 0.2s ease, transform 0.2s ease;
    opacity: 1;
    pointer-events: auto;
  }
  .card-c-icon {
    font-size: 24px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #fbf7f1;
    border: 1px solid var(--border);
    transition: transform 0.2s ease;
  }
  .card-collapsed-view:hover .card-c-icon {
    transform: scale(1.08);
  }
  .card-c-title {
    font-size: 12.5px;
    font-weight: 800;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 90px;
  }
  .card-c-badge {
    font-size: 10px;
    font-weight: 700;
    color: var(--brown);
    background: #f4ece2;
    padding: 2px 8px;
    border-radius: 999px;
    white-space: nowrap;
    border: 1px solid rgba(124, 83, 57, 0.12);
  }

  /* Hide Collapsed View when Card is Expanded */
  .expand-card.active .card-collapsed-view,
  .expand-nav-track:hover .expand-card.is-hovered .card-collapsed-view {
    opacity: 0;
    pointer-events: none;
    position: absolute;
    transform: scale(0.9);
  }
  /* Restore Collapsed View when Active Card is compressed by hover on another */
  .expand-nav-track:hover .expand-card.active:not(.is-hovered) .card-collapsed-view {
    opacity: 1;
    pointer-events: auto;
    position: relative;
    transform: none;
  }

  /* --- Expanded View --- */
  .card-expanded-view {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 12px 16px;
    opacity: 0;
    pointer-events: none;
    transform: translateX(8px);
    transition: opacity 0.25s ease, transform 0.25s ease;
    overflow: hidden;
  }

  .expand-card.active .card-expanded-view,
  .expand-nav-track:hover .expand-card.is-hovered .card-expanded-view {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0);
    transition-delay: 0.05s;
  }
  .expand-nav-track:hover .expand-card.active:not(.is-hovered) .card-expanded-view {
    opacity: 0;
    pointer-events: none;
    transform: translateX(8px);
    transition-delay: 0s;
  }

  /* Expanded Card Header */
  .card-exp-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    border-bottom: 1px solid #ebdccb;
    padding-bottom: 8px;
    flex-shrink: 0;
  }
  .card-exp-lead {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
  }
  .card-exp-icon {
    font-size: 20px;
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: #fbf6ee;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .card-exp-title {
    font-size: 14.5px;
    font-weight: 800;
    color: var(--brown-dark);
    line-height: 1.2;
    white-space: nowrap;
  }
  .card-exp-sub {
    font-size: 11px;
    color: var(--muted);
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-exp-action-btn {
    border: 1px solid var(--border);
    background: #ffffff;
    color: var(--brown);
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 7px;
    cursor: pointer;
    white-space: nowrap;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.18s ease;
    flex-shrink: 0;
  }
  .card-exp-action-btn:hover {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
    box-shadow: 0 2px 8px rgba(124, 83, 57, 0.2);
  }

  /* Directories Layout on the Card */
  .card-directories-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px 10px;
    margin-top: 8px;
    flex: 1;
    align-content: center;
  }
  .card-dir-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.16s ease;
    text-align: left;
    min-width: 0;
  }
  .card-dir-item:hover {
    background: #fbf6ef;
    border-color: var(--brown);
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(124, 83, 57, 0.08);
  }
  .card-dir-item .dir-icon {
    font-size: 15px;
    line-height: 1;
    flex-shrink: 0;
  }
  .card-dir-item .dir-text {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }
  .card-dir-item .dir-title {
    font-size: 11.5px;
    font-weight: 750;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-dir-item .dir-sub {
    font-size: 10px;
    color: var(--muted);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Categories Directory Grid for Patients Card */
  .card-directories-categories {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px 7px;
    margin-top: 7px;
    flex: 1;
    align-content: center;
    overflow-y: auto;
  }
  .card-cat-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    padding: 4px 8px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.16s ease;
    font-size: 11px;
    font-weight: 700;
    color: var(--brown-dark);
    min-width: 0;
  }
  .card-cat-chip:hover {
    background: #fbf6ee;
    border-color: var(--brown);
    color: var(--brown-dark);
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(124, 83, 57, 0.07);
  }
  .card-cat-chip.active {
    background: var(--brown);
    color: #ffffff;
    border-color: var(--brown-dark);
  }
  .card-cat-chip.active .chip-cnt {
    background: rgba(255, 255, 255, 0.25);
    color: #ffffff;
  }
  .card-cat-chip .chip-left {
    display: flex;
    align-items: center;
    gap: 5px;
    min-width: 0;
    overflow: hidden;
  }
  .card-cat-chip .chip-icon {
    font-size: 12px;
    line-height: 1;
    flex-shrink: 0;
  }
  .card-cat-chip .chip-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-cat-chip .chip-cnt {
    font-size: 10px;
    font-weight: 700;
    background: #f4ece2;
    color: var(--brown);
    padding: 1px 5px;
    border-radius: 999px;
    flex-shrink: 0;
  }

  /* Responsive / Mobile Styling */
  @media(max-width: 960px) {
    .expand-nav-container {
      position: relative;
      top: auto;
      padding: 8px 12px;
    }
    .expand-nav-track {
      height: 172px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
      padding-bottom: 2px;
      gap: 8px;
    }
    .expand-nav-track::-webkit-scrollbar {
      display: none;
    }
    .expand-card {
      flex: 0 0 54px;
      min-width: 54px;
      max-width: 54px;
    }
    .expand-card.active,
    .expand-nav-track:hover .expand-card.is-hovered {
      flex: 0 0 calc(100vw - 36px);
      min-width: 290px;
      max-width: 420px;
    }
    .card-directories-categories {
      grid-template-columns: repeat(2, 1fr);
    }
    .card-c-title {
      font-size: 11px;
    }
    .card-c-icon {
      width: 36px;
      height: 36px;
      font-size: 18px;
    }
  }"""

assert old_nav_css in content, "old_nav_css not found"
content = content.replace(old_nav_css, new_nav_css, 1)

# 2. HTML Markup
old_nav_html = """<nav class="tabs" id="mainNavTabs">
  <button type="button" data-tab="dashboard" class="tab-btn active" title="Dashboard">
    <span class="tab-icon">📊</span>
    <span class="tab-text">Dashboard</span>
  </button>
  <button type="button" data-tab="register" class="tab-btn" title="Add Patient">
    <span class="tab-icon">➕</span>
    <span class="tab-text">Add Patient</span>
  </button>
  <div class="nav-tab-wrapper">
    <button type="button" data-tab="patients" class="tab-btn" id="navPatientsBtn" title="Patient Directory">
      <span class="tab-icon">👥</span>
      <span class="tab-text">Patient Directory</span>
      <span class="nav-arrow">▾</span>
    </button>
    <div class="nav-category-dropdown">
      <div class="nav-cat-head">
        <span>Categories Directory</span>
        <span class="nav-cat-total" id="navCatTotal">0 Total</span>
      </div>
      <div class="nav-cat-list" id="navCatList"></div>
    </div>
  </div>
  <button type="button" data-tab="appointments" class="tab-btn" title="Appointments">
    <span class="tab-icon">📅</span>
    <span class="tab-text">Appointments</span>
  </button>
  <button type="button" data-tab="reports" class="tab-btn" title="Reports & Data">
    <span class="tab-icon">🖨️</span>
    <span class="tab-text">Reports & Data</span>
  </button>
</nav>"""

new_nav_html = """<nav class="expand-nav-container" id="expandNavContainer" aria-label="Portal Navigation">
  <div class="expand-nav-track" id="expandNavTrack" role="tablist">

    <!-- Card 1: Dashboard -->
    <div class="expand-card active" data-tab="dashboard" role="tab" aria-selected="true" onclick="handleCardNavClick(event, 'dashboard')" title="Dashboard Overview">
      <div class="card-collapsed-view">
        <div class="card-c-icon">📊</div>
        <div class="card-c-title">Dashboard</div>
        <div class="card-c-badge" id="cBadgeDash">Overview</div>
      </div>
      <div class="card-expanded-view">
        <div class="card-exp-header">
          <div class="card-exp-lead">
            <div class="card-exp-icon">📊</div>
            <div>
              <div class="card-exp-title">Admin Dashboard</div>
              <div class="card-exp-sub">Portal Overview &amp; Live Activity</div>
            </div>
          </div>
          <button type="button" class="card-exp-action-btn" onclick="event.stopPropagation(); goTab('dashboard')">
            Open Page &rarr;
          </button>
        </div>
        <div class="card-directories-grid">
          <div class="card-dir-item" onclick="event.stopPropagation(); jumpToSection('dashboard', 'dashboardQuickBar')">
            <span class="dir-icon">⚡</span>
            <div class="dir-text">
              <span class="dir-title">Quick Actions</span>
              <span class="dir-sub">1-click task shortcuts</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); jumpToSection('dashboard', 'dashboardStats')">
            <span class="dir-icon">📈</span>
            <div class="dir-text">
              <span class="dir-title">Key Metrics</span>
              <span class="dir-sub">Patients &amp; sessions stats</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); jumpToSection('dashboard', 'todayTable')">
            <span class="dir-icon">🕒</span>
            <div class="dir-text">
              <span class="dir-title">Today's Queue</span>
              <span class="dir-sub">Active appointments</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); jumpToSection('dashboard', 'dashboardCatGrid')">
            <span class="dir-icon">🏷️</span>
            <div class="dir-text">
              <span class="dir-title">Category Directory</span>
              <span class="dir-sub">Spiritual case groups</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Card 2: Add Patient -->
    <div class="expand-card" data-tab="register" role="tab" aria-selected="false" onclick="handleCardNavClick(event, 'register')" title="Register Patient">
      <div class="card-collapsed-view">
        <div class="card-c-icon">➕</div>
        <div class="card-c-title">Add Patient</div>
        <div class="card-c-badge" id="cBadgeRegister">Intake</div>
      </div>
      <div class="card-expanded-view">
        <div class="card-exp-header">
          <div class="card-exp-lead">
            <div class="card-exp-icon">➕</div>
            <div>
              <div class="card-exp-title">Add Patient</div>
              <div class="card-exp-sub">Patient Registration &amp; Spiritual Profile</div>
            </div>
          </div>
          <button type="button" class="card-exp-action-btn" onclick="event.stopPropagation(); goTab('register')">
            Open Form &rarr;
          </button>
        </div>
        <div class="card-directories-grid">
          <div class="card-dir-item" onclick="event.stopPropagation(); startFreshRegistration()">
            <span class="dir-icon">📝</span>
            <div class="dir-text">
              <span class="dir-title">New Registration</span>
              <span class="dir-sub">Reset and intake new record</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); focusPatientField('pName')">
            <span class="dir-icon">🔮</span>
            <div class="dir-text">
              <span class="dir-title">Numerology Engine</span>
              <span class="dir-sub">Pythagorean &amp; Chaldean</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); focusPatientField('pCountry')">
            <span class="dir-icon">🌍</span>
            <div class="dir-text">
              <span class="dir-title">Country &amp; Dial Code</span>
              <span class="dir-sub">Auto currency &amp; WhatsApp prefix</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); focusPatientField('pProblem')">
            <span class="dir-icon">🏷️</span>
            <div class="dir-text">
              <span class="dir-title">Diagnosis Category</span>
              <span class="dir-sub">Ruqyah &amp; spiritual classification</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Card 3: Patients Directory -->
    <div class="expand-card" data-tab="patients" role="tab" aria-selected="false" onclick="handleCardNavClick(event, 'patients')" title="Patients Directory">
      <div class="card-collapsed-view">
        <div class="card-c-icon">👥</div>
        <div class="card-c-title">Directory</div>
        <div class="card-c-badge" id="cBadgePatients">9 Groups</div>
      </div>
      <div class="card-expanded-view">
        <div class="card-exp-header">
          <div class="card-exp-lead">
            <div class="card-exp-icon">👥</div>
            <div>
              <div class="card-exp-title">Patients Directory</div>
              <div class="card-exp-sub">Filter Patient Cases by Spiritual Category</div>
            </div>
          </div>
          <button type="button" class="card-exp-action-btn" onclick="event.stopPropagation(); selectCategory('')">
            View All &rarr;
          </button>
        </div>
        <div class="card-directories-categories" id="cardNavCatList">
          <!-- Dynamic category chips with live counters -->
        </div>
      </div>
    </div>

    <!-- Card 4: Appointments -->
    <div class="expand-card" data-tab="appointments" role="tab" aria-selected="false" onclick="handleCardNavClick(event, 'appointments')" title="Appointment Bookings">
      <div class="card-collapsed-view">
        <div class="card-c-icon">📅</div>
        <div class="card-c-title">Appointments</div>
        <div class="card-c-badge" id="cBadgeAppts">Schedule</div>
      </div>
      <div class="card-expanded-view">
        <div class="card-exp-header">
          <div class="card-exp-lead">
            <div class="card-exp-icon">📅</div>
            <div>
              <div class="card-exp-title">Appointments</div>
              <div class="card-exp-sub">Session Scheduling, Bookings &amp; Slips</div>
            </div>
          </div>
          <button type="button" class="card-exp-action-btn" onclick="event.stopPropagation(); goTab('appointments')">
            Open Schedule &rarr;
          </button>
        </div>
        <div class="card-directories-grid">
          <div class="card-dir-item" onclick="event.stopPropagation(); openBookSessionDirect()">
            <span class="dir-icon">➕</span>
            <div class="dir-text">
              <span class="dir-title">Schedule New Session</span>
              <span class="dir-sub">Select patient &amp; time slot</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); filterAppointmentsStatus('Pending')">
            <span class="dir-icon">⏳</span>
            <div class="dir-text">
              <span class="dir-title">Pending Approvals</span>
              <span class="dir-sub">Filter awaiting confirmation</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); filterAppointmentsStatus('Confirmed')">
            <span class="dir-icon">✅</span>
            <div class="dir-text">
              <span class="dir-title">Confirmed Queue</span>
              <span class="dir-sub">Upcoming confirmed sessions</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); filterAppointmentsStatus('Completed')">
            <span class="dir-icon">🏁</span>
            <div class="dir-text">
              <span class="dir-title">Completed Sessions</span>
              <span class="dir-sub">Archived treatment history</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Card 5: Reports & Data -->
    <div class="expand-card" data-tab="reports" role="tab" aria-selected="false" onclick="handleCardNavClick(event, 'reports')" title="Reports & Data Management">
      <div class="card-collapsed-view">
        <div class="card-c-icon">🖨️</div>
        <div class="card-c-title">Reports &amp; Data</div>
        <div class="card-c-badge" id="cBadgeReports">Records</div>
      </div>
      <div class="card-expanded-view">
        <div class="card-exp-header">
          <div class="card-exp-lead">
            <div class="card-exp-icon">🖨️</div>
            <div>
              <div class="card-exp-title">Reports &amp; Data</div>
              <div class="card-exp-sub">Printable Records, Financials &amp; Backups</div>
            </div>
          </div>
          <button type="button" class="card-exp-action-btn" onclick="event.stopPropagation(); goTab('reports')">
            Open Reports &rarr;
          </button>
        </div>
        <div class="card-directories-grid">
          <div class="card-dir-item" onclick="event.stopPropagation(); triggerPrintListDirect()">
            <span class="dir-icon">📄</span>
            <div class="dir-text">
              <span class="dir-title">Print Patient List</span>
              <span class="dir-sub">Full patient directory layout</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); jumpToSection('reports', 'repStats')">
            <span class="dir-icon">💰</span>
            <div class="dir-text">
              <span class="dir-title">Financial Summary</span>
              <span class="dir-sub">Fees received &amp; balances</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); exportData()">
            <span class="dir-icon">💾</span>
            <div class="dir-text">
              <span class="dir-title">Export JSON Backup</span>
              <span class="dir-sub">1-click full database download</span>
            </div>
          </div>
          <div class="card-dir-item" onclick="event.stopPropagation(); triggerImportPrompt()">
            <span class="dir-icon">📥</span>
            <div class="dir-text">
              <span class="dir-title">Restore Database</span>
              <span class="dir-sub">Import from backup JSON file</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</nav>"""

assert old_nav_html in content, "old_nav_html not found"
content = content.replace(old_nav_html, new_nav_html, 1)

# Add IDs to dashboard quick bar and stats for smooth anchor jump
content = content.replace('<div class="admin-quick-bar">', '<div class="admin-quick-bar" id="dashboardQuickBar">', 1)
content = content.replace('<div class="stats">', '<div class="stats" id="dashboardStats">', 1)

# 3. Navigation JavaScript Block
old_js_nav = """/* ---------- Navigation ---------- */
document.querySelectorAll('nav.tabs button').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('nav.tabs button').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
    btn.classList.add('active');
    $(btn.dataset.tab).classList.add('active');
    if(btn.dataset.tab==='register' && !$('editId').value) resetPatientForm();
    if(btn.dataset.tab==='dashboard') renderDashboard();
    if(btn.dataset.tab==='patients') renderPatients();
    if(btn.dataset.tab==='appointments'){ fillPatientSelect(); renderAppts(); }
    if(btn.dataset.tab==='reports') renderReports();
    window.scrollTo(0,0);
  });
});
function goTab(name){ document.querySelector('nav.tabs button[data-tab="'+name+'"]').click(); }"""

new_js_nav = """/* ================= CARD EXPAND-ON-HOVER NAVIGATION ENGINE ================= */
let CURRENT_ACTIVE_TAB = 'dashboard';

function initExpandNavEngine(){
  const track = document.getElementById('expandNavTrack');
  if(!track) return;
  const cards = Array.from(track.querySelectorAll('.expand-card'));

  cards.forEach((card, idx) => {
    // Mouse hover expand (smooth accordion effect)
    card.addEventListener('mouseenter', () => {
      cards.forEach(c => c.classList.remove('is-hovered'));
      card.classList.add('is-hovered');
    });

    // Keyboard navigation (Left / Right arrow keys)
    card.addEventListener('keydown', (e) => {
      if(e.key === 'ArrowRight' || e.key === 'ArrowDown'){
        e.preventDefault();
        const next = cards[(idx + 1) % cards.length];
        next.focus();
        goTab(next.dataset.tab);
      } else if(e.key === 'ArrowLeft' || e.key === 'ArrowUp'){
        e.preventDefault();
        const prev = cards[(idx - 1 + cards.length) % cards.length];
        prev.focus();
        goTab(prev.dataset.tab);
      }
    });
  });

  // When mouse leaves the track, smoothly revert to active tab
  track.addEventListener('mouseleave', () => {
    cards.forEach(c => c.classList.remove('is-hovered'));
  });

  // Render initial category chips on Patients Directory card
  renderCardNavCategories();
}

function handleCardNavClick(e, tabName){
  // If clicked inside a specific directory link or action, let child handler execute
  if(e.target.closest('.card-dir-item') || e.target.closest('.card-cat-chip') || e.target.closest('.card-exp-action-btn')) {
    return;
  }
  goTab(tabName);
}

function goTab(name){
  if(!name) return;
  CURRENT_ACTIVE_TAB = name;

  // 1. Update Expand-On-Hover Cards state
  const track = document.getElementById('expandNavTrack');
  if(track){
    const cards = track.querySelectorAll('.expand-card');
    cards.forEach(card => {
      const isAct = card.dataset.tab === name;
      card.classList.toggle('active', isAct);
      card.classList.remove('is-hovered');
      card.setAttribute('aria-selected', isAct ? 'true' : 'false');
    });
    // On mobile, scroll active card gently into center
    const activeCard = track.querySelector(`.expand-card[data-tab="${name}"]`);
    if(activeCard && window.innerWidth < 960){
      activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  // 2. Hide all pages, show target page
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = $(name);
  if(target) target.classList.add('active');

  // 3. Trigger page specific renders
  if(name === 'register' && !$('editId').value) resetPatientForm();
  if(name === 'dashboard') renderDashboard();
  if(name === 'patients') renderPatients();
  if(name === 'appointments'){ fillPatientSelect(); renderAppts(); }
  if(name === 'reports') renderReports();

  // 4. Smooth scroll to top of content
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderCardNavCategories(){
  const container = $('cardNavCatList');
  if(!container) return;
  container.innerHTML = CATEGORIES.map(c => {
    const cnt = getCategoryCount(c.id);
    const isAct = c.id === SELECTED_CATEGORY;
    return `<div class="card-cat-chip ${isAct ? 'active' : ''}" onclick="event.stopPropagation(); selectCategory('${esc(c.id)}')">
      <span class="chip-left">
        <span class="chip-icon">${c.icon}</span>
        <span class="chip-name">${esc(c.short || c.name)}</span>
      </span>
      <span class="chip-cnt" id="cardnav-cnt-${esc(c.id)}">${cnt}</span>
    </div>`;
  }).join('');
}

function jumpToSection(tab, targetId){
  goTab(tab);
  setTimeout(() => {
    const el = $(targetId);
    if(el){
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 100);
}

function startFreshRegistration(){
  goTab('register');
  resetPatientForm();
  const pName = $('pName');
  if(pName) pName.focus();
}

function focusPatientField(fieldId){
  goTab('register');
  setTimeout(() => {
    const el = $(fieldId);
    if(el){
      el.focus();
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 100);
}

function openBookSessionDirect(){
  goTab('appointments');
  setTimeout(() => {
    const pSel = $('aPatient');
    if(pSel){
      pSel.focus();
      pSel.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 100);
}

function filterAppointmentsStatus(status){
  goTab('appointments');
  const sel = $('apptStatusFilter');
  if(sel){
    sel.value = status;
    renderAppts();
  }
}

function triggerPrintListDirect(){
  goTab('reports');
  setTimeout(() => {
    printList();
  }, 150);
}

function triggerImportPrompt(){
  goTab('reports');
  const imp = $('importFile');
  if(imp) imp.click();
}"""

assert old_js_nav in content, "old_js_nav not found"
content = content.replace(old_js_nav, new_js_nav, 1)

# 4. Update updateCategoryBadges to also update cardNavCatList badges and card badges
old_cat_badges = """function updateCategoryBadges(){
  CATEGORIES.forEach(c => {
    const cnt = getCategoryCount(c.id);
    const pill = $(`pill-cnt-${c.id}`);
    if(pill) pill.textContent = cnt;
    const dash = $(`dash-cnt-${c.id}`);
    if(dash) dash.textContent = cnt + ' case' + (cnt===1?'':'s');
    const nav = $(`nav-cnt-${c.id}`);
    if(nav) nav.textContent = cnt;
  });
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
}"""

new_cat_badges = """function updateCategoryBadges(){
  CATEGORIES.forEach(c => {
    const cnt = getCategoryCount(c.id);
    const pill = $(`pill-cnt-${c.id}`);
    if(pill) pill.textContent = cnt;
    const dash = $(`dash-cnt-${c.id}`);
    if(dash) dash.textContent = cnt + ' case' + (cnt===1?'':'s');
    const nav = $(`nav-cnt-${c.id}`);
    if(nav) nav.textContent = cnt;
    const cardNav = $(`cardnav-cnt-${c.id}`);
    if(cardNav) cardNav.textContent = cnt;
  });
  const navTotal = $('navCatTotal');
  if(navTotal) navTotal.textContent = DB.patients.length + ' Total';
  const cBadgePat = $('cBadgePatients');
  if(cBadgePat) cBadgePat.textContent = DB.patients.length + ' Cases';
  const cBadgeApp = $('cBadgeAppts');
  if(cBadgeApp) cBadgeApp.textContent = DB.appts.length + ' Booked';
}"""

assert old_cat_badges in content, "old_cat_badges not found"
content = content.replace(old_cat_badges, new_cat_badges, 1)

# 5. Call initExpandNavEngine in bootstrap
old_boot = """/* ================= INIT ================= */
resetPatientForm();
renderDashboard();
initCategoriesUI();"""

new_boot = """/* ================= INIT ================= */
resetPatientForm();
renderDashboard();
initCategoriesUI();
initExpandNavEngine();"""

assert old_boot in content, "old_boot not found"
content = content.replace(old_boot, new_boot, 1)

# Write to AIR-Patient-Management-System.html and index.html
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Expand-On-Hover Card Navigation applied successfully!")
