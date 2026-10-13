import io, base64
from PIL import Image

# 1. Generate base64 data URI for circular logo
im = Image.open('/home/projects/src-online.com/logo/src-logo.png')
im360 = im.resize((360, 360), Image.Resampling.LANCZOS)
buf = io.BytesIO()
im360.save(buf, format='WEBP', quality=90)
b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
data_uri = f"data:image/webp;base64,{b64}"
print(f"Generated base64 logo: {len(data_uri)} chars")

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 2. Update CSS for Card-Style Navigation and Big Loader
old_nav_css_block = """  /* ---------- Nav Tabs Expand-On-Hover ---------- */
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

new_nav_css_block = """  /* ---------- Card-Style Expand-On-Hover Navigation ---------- */
  .nav-cards-container{
    background:rgba(255,255,255,.95);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
    padding:10px 18px;
    border-bottom:1.5px solid var(--border);
    position:sticky;
    top:74px;
    z-index:40;
    box-shadow:0 2px 12px rgba(61,40,29,.04);
  }
  .nav-cards-wrapper{
    max-width:1150px;
    margin:0 auto;
    display:grid;
    grid-template-columns:repeat(5, 1fr);
    gap:12px;
  }
  @media(max-width:960px){
    .nav-cards-wrapper{
      display:flex;
      overflow-x:auto;
      padding-bottom:4px;
      gap:10px;
      -webkit-overflow-scrolling:touch;
    }
    .nav-card{
      min-width:170px;
      flex:0 0 auto;
    }
  }
  .nav-card{
    background:#ffffff;
    border:1.5px solid var(--border);
    border-radius:13px;
    padding:10px 14px;
    display:flex;
    align-items:center;
    gap:10px;
    cursor:pointer;
    position:relative;
    overflow:hidden;
    box-shadow:0 2px 6px rgba(61,40,29,.03);
    /* Expand on hover effect */
    transition:all .28s cubic-bezier(.2,.8,.2,1);
    user-select:none;
  }
  .nav-card .nc-icon{
    font-size:20px;
    line-height:1;
    display:flex;
    align-items:center;
    justify-content:center;
    width:36px;
    height:36px;
    border-radius:10px;
    background:#fbf6ee;
    flex-shrink:0;
    transition:all .25s ease;
  }
  .nav-card .nc-content{
    display:flex;
    flex-direction:column;
    min-width:0;
    flex:1;
  }
  .nav-card .nc-title{
    font-size:13.5px;
    font-weight:800;
    color:var(--brown-dark);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    letter-spacing:.2px;
    transition:color .2s ease;
  }
  .nav-card .nc-sub{
    font-size:11px;
    color:var(--muted);
    font-weight:600;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
    margin-top:1px;
    /* Expand on hover micro-interaction */
    max-height:0;
    opacity:0;
    transition:max-height .28s cubic-bezier(.2,.8,.2,1), opacity .22s ease, margin .22s ease;
  }
  .nav-card .nc-action{
    font-size:14px;
    color:var(--brown);
    font-weight:800;
    opacity:0;
    transform:translateX(-6px);
    transition:all .22s ease;
    flex-shrink:0;
  }

  /* Expand on Hover */
  .nav-card:hover{
    background:#fffdfa;
    border-color:var(--brown);
    transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(124,83,57,.18);
    padding:11px 16px;
  }
  .nav-card:hover .nc-icon{
    background:#f4e6d4;
    transform:scale(1.12);
  }
  .nav-card:hover .nc-sub{
    max-height:18px;
    opacity:1;
    margin-top:2px;
  }
  .nav-card:hover .nc-action{
    opacity:1;
    transform:translateX(0);
  }

  /* Active Card */
  .nav-card.active{
    background:linear-gradient(135deg, var(--brown-dark) 0%, var(--brown) 100%);
    border-color:var(--brown-dark);
    box-shadow:0 4px 16px rgba(61,40,29,.25);
    transform:translateY(-1px);
  }
  .nav-card.active .nc-icon{
    background:rgba(255,255,255,.2);
    color:#ffffff;
  }
  .nav-card.active .nc-title{
    color:#ffffff;
  }
  .nav-card.active .nc-sub{
    color:rgba(255,255,255,.85);
    max-height:18px;
    opacity:1;
    margin-top:2px;
  }
  .nav-card.active .nc-action{
    color:#ffffff;
    opacity:0.85;
    transform:translateX(0);
  }"""

assert old_nav_css_block in content, "old_nav_css_block not found"
content = content.replace(old_nav_css_block, new_nav_css_block, 1)

# 3. Update Page Loader CSS for Big Logo & Big White Smoke
old_loader_css_block = """  /* ================= FULLSCREEN UHD PAGE LOADER ================= */
  .page-loader{
    position:fixed;
    inset:0;
    z-index:99999;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#1e1610; /* Deep warm velvet espresso */
    color:#fdfaf6;
    overflow:hidden;
    transition:opacity .7s cubic-bezier(.2,.8,.2,1), visibility .7s;
  }
  .page-loader.loaded{
    opacity:0;
    visibility:hidden;
    pointer-events:none;
  }
  .loader-bg-overlay{
    position:absolute;
    inset:0;
    background:radial-gradient(circle at center, #2e2017 0%, #17100b 65%, #0b0705 100%);
    pointer-events:none;
  }
  .loader-content{
    position:relative;
    z-index:2;
    display:flex;
    flex-direction:column;
    align-items:center;
    text-align:center;
    padding:20px;
    max-width:440px;
  }
  .loader-smoke-wrapper{
    position:relative;
    width:130px;
    height:130px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:26px;
    cursor:pointer;
  }
  .loader-smoke-canvas{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%, -50%);
    width:340px;
    height:340px;
    pointer-events:none;
    z-index:1;
  }
  .loader-aura{
    position:absolute;
    inset:-10px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(255,255,255,.3) 0%, rgba(212,175,55,.2) 40%, transparent 70%);
    filter:blur(14px);
    pointer-events:none;
    z-index:0;
    animation:loaderAuraPulse 3s ease-in-out infinite alternate;
  }
  @keyframes loaderAuraPulse{
    0%{transform:scale(0.92);opacity:0.55}
    100%{transform:scale(1.12);opacity:0.95}
  }
  .loader-logo-orb{
    position:relative;
    width:124px;
    height:124px;
    border-radius:50%;
    overflow:hidden;
    border:2.5px solid rgba(224,195,130,.85);
    box-shadow:0 10px 30px rgba(0,0,0,.6), 0 0 25px rgba(255,255,255,.25), 0 0 15px rgba(212,175,55,.4);
    z-index:2;
    background:#252525;
    animation:loaderOrbFloat 4s ease-in-out infinite alternate;
    transition:transform .2s ease;
  }
  @keyframes loaderOrbFloat{
    0%{transform:translateY(0) scale(1)}
    100%{transform:translateY(-6px) scale(1.02)}
  }
  .loader-logo-img{
    width:100%;
    height:100%;
    object-fit:cover;
    display:block;
    border-radius:50%;
    user-select:none;
    -webkit-user-drag:none;
  }
  .loader-text-group{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:6px;
  }
  .loader-brand-title{
    font-size:20px;
    font-weight:800;
    letter-spacing:1.5px;
    color:#fdfbf8;
    margin:0;
    text-shadow:0 2px 10px rgba(0,0,0,.4);
  }
  .loader-brand-sub{
    font-size:12.5px;
    color:#d8c6b4;
    letter-spacing:.5px;
    margin:0 0 18px;
    font-weight:600;
  }
  .loader-progress-track{
    width:220px;
    height:3px;
    background:rgba(255,255,255,.12);
    border-radius:999px;
    overflow:hidden;
    position:relative;
  }
  .loader-progress-bar{
    height:100%;
    width:0%;
    background:linear-gradient(90deg, #d4af37, #ffffff, #d4af37);
    border-radius:999px;
    transition:width .25s ease;
  }
  .loader-status{
    font-size:11px;
    color:#a99889;
    font-weight:600;
    letter-spacing:.8px;
    text-transform:uppercase;
    margin-top:10px;
  }"""

new_loader_css_block = """  /* ================= FULLSCREEN UHD PAGE LOADER (BIG LOGO & WHITE SMOKE) ================= */
  .page-loader{
    position:fixed;
    inset:0;
    z-index:99999;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#17110d; /* Luxurious deep obsidian espresso */
    color:#fdfaf6;
    overflow:hidden;
    cursor:pointer;
    transition:opacity .75s cubic-bezier(.2,.8,.2,1), visibility .75s;
  }
  .page-loader.loaded{
    opacity:0;
    visibility:hidden;
    pointer-events:none;
  }
  .loader-bg-overlay{
    position:absolute;
    inset:0;
    background:radial-gradient(circle at center, #2c1d15 0%, #150d09 60%, #0a0604 100%);
    pointer-events:none;
  }
  .loader-content{
    position:relative;
    z-index:2;
    display:flex;
    flex-direction:column;
    align-items:center;
    text-align:center;
    padding:24px;
    max-width:520px;
  }
  /* Big Logo & Smoke Area */
  .loader-smoke-wrapper{
    position:relative;
    width:210px;
    height:210px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom:28px;
    user-select:none;
  }
  .loader-smoke-canvas{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%, -50%);
    width:480px;
    height:480px;
    pointer-events:none;
    z-index:1;
  }
  .loader-aura{
    position:absolute;
    inset:-16px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(255,255,255,.32) 0%, rgba(212,175,55,.24) 40%, transparent 70%);
    filter:blur(18px);
    pointer-events:none;
    z-index:0;
    animation:loaderAuraPulse 3.5s ease-in-out infinite alternate;
  }
  @keyframes loaderAuraPulse{
    0%{transform:scale(0.94);opacity:0.55}
    100%{transform:scale(1.12);opacity:0.95}
  }
  /* BIG 210px Logo Orb */
  .loader-logo-orb{
    position:relative;
    width:210px;
    height:210px;
    border-radius:50%;
    overflow:hidden;
    border:3px solid rgba(224,195,130,.92);
    box-shadow:0 14px 44px rgba(0,0,0,.7), 0 0 35px rgba(255,255,255,.3), 0 0 24px rgba(212,175,55,.5);
    z-index:2;
    background:#252525;
    animation:loaderOrbFloat 4s ease-in-out infinite alternate;
    transition:transform .2s ease;
  }
  @media(max-width:600px){
    .loader-smoke-wrapper{width:160px;height:160px;margin-bottom:20px}
    .loader-logo-orb{width:160px;height:160px}
    .loader-smoke-canvas{width:360px;height:360px}
  }
  @keyframes loaderOrbFloat{
    0%{transform:translateY(0) scale(1)}
    100%{transform:translateY(-8px) scale(1.02)}
  }
  .loader-logo-img{
    width:100%;
    height:100%;
    object-fit:cover;
    display:block;
    border-radius:50%;
    user-select:none;
    -webkit-user-drag:none;
  }
  .loader-text-group{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:6px;
  }
  .loader-brand-title{
    font-size:22px;
    font-weight:800;
    letter-spacing:1.8px;
    color:#fdfbf8;
    margin:0;
    text-shadow:0 2px 12px rgba(0,0,0,.5);
  }
  .loader-brand-sub{
    font-size:13px;
    color:#dfcbbb;
    letter-spacing:.6px;
    margin:0 0 20px;
    font-weight:600;
  }
  .loader-progress-track{
    width:240px;
    height:3.5px;
    background:rgba(255,255,255,.14);
    border-radius:999px;
    overflow:hidden;
    position:relative;
  }
  .loader-progress-bar{
    height:100%;
    width:0%;
    background:linear-gradient(90deg, #d4af37, #ffffff, #d4af37);
    border-radius:999px;
    transition:width .22s ease;
  }
  .loader-status{
    font-size:11.5px;
    color:#bca998;
    font-weight:600;
    letter-spacing:.8px;
    text-transform:uppercase;
    margin-top:12px;
  }
  .loader-skip-hint{
    font-size:10.5px;
    color:#7a6858;
    letter-spacing:.4px;
    margin-top:8px;
  }"""

assert old_loader_css_block in content, "old_loader_css_block not found"
content = content.replace(old_loader_css_block, new_loader_css_block, 1)

# 4. Replace Nav Tabs HTML with Card-Style Navigation
old_nav_html_block = """<nav class="tabs" id="mainNavTabs">
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

new_nav_html_block = """<!-- Expand-On-Hover Card-Style Navigation Bar -->
<nav class="nav-cards-container" id="navCardsContainer">
  <div class="nav-cards-wrapper">
    <div class="nav-card active" data-tab="dashboard" onclick="openPage('dashboard')" title="Open Dashboard">
      <div class="nc-icon">📊</div>
      <div class="nc-content">
        <div class="nc-title">Dashboard</div>
        <div class="nc-sub">Overview &amp; Stats</div>
      </div>
      <div class="nc-action">&rarr;</div>
    </div>

    <div class="nav-card" data-tab="register" onclick="openPage('register')" title="Open Add Patient Form">
      <div class="nc-icon">➕</div>
      <div class="nc-content">
        <div class="nc-title">Add Patient</div>
        <div class="nc-sub">New Registration</div>
      </div>
      <div class="nc-action">&rarr;</div>
    </div>

    <div class="nav-card" data-tab="patients" onclick="openPage('patients')" title="Open Patient Directory">
      <div class="nc-icon">👥</div>
      <div class="nc-content">
        <div class="nc-title">Patient Directory</div>
        <div class="nc-sub">Browse All Cases</div>
      </div>
      <div class="nc-action">&rarr;</div>
    </div>

    <div class="nav-card" data-tab="appointments" onclick="openPage('appointments')" title="Open Appointments Manager">
      <div class="nc-icon">📅</div>
      <div class="nc-content">
        <div class="nc-title">Appointments</div>
        <div class="nc-sub">Bookings &amp; Schedule</div>
      </div>
      <div class="nc-action">&rarr;</div>
    </div>

    <div class="nav-card" data-tab="reports" onclick="openPage('reports')" title="Open Reports & Backup">
      <div class="nc-icon">🖨️</div>
      <div class="nc-content">
        <div class="nc-title">Reports &amp; Data</div>
        <div class="nc-sub">Summary &amp; Backup</div>
      </div>
      <div class="nc-action">&rarr;</div>
    </div>
  </div>
</nav>"""

assert old_nav_html_block in content, "old_nav_html_block not found"
content = content.replace(old_nav_html_block, new_nav_html_block, 1)

# 5. Replace Page Loader HTML with embedded base64 big logo
old_loader_html = """<!-- Full-Screen UHD Page Loader with Center Logo & White UHD Smoke -->
<div id="pageLoader" class="page-loader" aria-label="Loading Shifa-Ruqiyah Centre">
  <div class="loader-bg-overlay"></div>
  <div class="loader-content">
    <div class="loader-smoke-wrapper" id="loaderSmokeWrapper" title="Shifa-Ruqiyah Centre">
      <canvas id="loaderSmokeCanvas" class="loader-smoke-canvas" width="340" height="340" aria-hidden="true"></canvas>
      <div class="loader-aura" aria-hidden="true"></div>
      <div class="loader-logo-orb" id="loaderLogoOrb">
        <img src="logo/src-logo-512.png" onerror="this.onerror=null;this.src='logo/src-logo.webp'" alt="Shifa-Ruqiyah Centre Emblem" class="loader-logo-img">
      </div>
    </div>
    <div class="loader-text-group">
      <h2 class="loader-brand-title">SHIFA-RUQIYAH CENTRE</h2>
      <p class="loader-brand-sub">Spiritual Guidance &middot; Patient Management Portal</p>
      <div class="loader-progress-track">
        <div class="loader-progress-bar" id="loaderProgressBar"></div>
      </div>
      <div class="loader-status" id="loaderStatus">Initializing Portal...</div>
    </div>
  </div>
</div>"""

new_loader_html = f"""<!-- Full-Screen UHD Page Loader with BIG Center Logo & White UHD Smoke -->
<div id="pageLoader" class="page-loader" onclick="dismissLoaderNow()" aria-label="Loading Shifa-Ruqiyah Centre">
  <div class="loader-bg-overlay"></div>
  <div class="loader-content">
    <div class="loader-smoke-wrapper" id="loaderSmokeWrapper" title="Shifa-Ruqiyah Centre - Click to Enter">
      <canvas id="loaderSmokeCanvas" class="loader-smoke-canvas" width="480" height="480" aria-hidden="true"></canvas>
      <div class="loader-aura" aria-hidden="true"></div>
      <div class="loader-logo-orb" id="loaderLogoOrb">
        <img src="{data_uri}" onerror="this.src='logo/src-logo.webp'" alt="Shifa-Ruqiyah Centre Emblem" class="loader-logo-img">
      </div>
    </div>
    <div class="loader-text-group">
      <h2 class="loader-brand-title">SHIFA-RUQIYAH CENTRE</h2>
      <p class="loader-brand-sub">Spiritual Guidance &middot; Patient Management Portal</p>
      <div class="loader-progress-track">
        <div class="loader-progress-bar" id="loaderProgressBar"></div>
      </div>
      <div class="loader-status" id="loaderStatus">Initializing Portal...</div>
      <div class="loader-skip-hint">Click anywhere to enter portal</div>
    </div>
  </div>
</div>"""

assert old_loader_html in content, "old_loader_html not found"
content = content.replace(old_loader_html, new_loader_html, 1)

# Also update header logo to use the embedded base64 data URI for instant 0ms load
old_header_logo = """<img src="logo/src-logo.webp" onerror="this.onerror=null;this.src='logo/src-logo-256.png'" alt="Shifa-Ruqiyah Centre Logo" class="brand-logo-img">"""
new_header_logo = f"""<img src="{data_uri}" onerror="this.src='logo/src-logo.webp'" alt="Shifa-Ruqiyah Centre Logo" class="brand-logo-img">"""
if old_header_logo in content:
    content = content.replace(old_header_logo, new_header_logo, 1)

# 6. Update JavaScript for openPage & goTab and Big White Smoke
old_nav_js = """/* ---------- Navigation ---------- */
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

new_nav_js = """/* ---------- Card-Style Navigation Engine ---------- */
function openPage(tabName){
  if(!tabName) return;
  // 1. Update active card styling
  document.querySelectorAll('.nav-card').forEach(card => {
    card.classList.toggle('active', card.dataset.tab === tabName);
  });
  // 2. Hide all pages, show target page
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = $(tabName);
  if(target){
    target.classList.add('active');
  }
  // 3. Trigger page specific renders
  if(tabName === 'register' && !$('editId').value) resetPatientForm();
  if(tabName === 'dashboard') renderDashboard();
  if(tabName === 'patients') renderPatients();
  if(tabName === 'appointments'){ fillPatientSelect(); renderAppts(); }
  if(tabName === 'reports') renderReports();
  // 4. Smooth scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
function goTab(name){ openPage(name); }"""

assert old_nav_js in content, "old_nav_js not found"
content = content.replace(old_nav_js, new_nav_js, 1)

# 7. Update Loader Engine JS for 480x480 canvas and 210px big logo
old_loader_js_block = """/* ================= WHITE UHD SMOKE PAGE LOADER ENGINE ================= */
(function initPageLoader(){
  const loader = document.getElementById('pageLoader');
  const canvas = document.getElementById('loaderSmokeCanvas');
  const wrapper = document.getElementById('loaderSmokeWrapper');
  const orb = document.getElementById('loaderLogoOrb');
  const pBar = document.getElementById('loaderProgressBar');
  const statusEl = document.getElementById('loaderStatus');
  if(!loader || !canvas || !orb) return;

  const ctx = canvas.getContext('2d');
  if(!ctx) return;

  // UHD Retina scale
  const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
  const CSS_SIZE = 340;
  canvas.width = Math.round(CSS_SIZE * dpr);
  canvas.height = Math.round(CSS_SIZE * dpr);
  ctx.scale(dpr, dpr);

  const cx = CSS_SIZE / 2;
  const cy = CSS_SIZE / 2;
  const orbRadius = 62; // Center 124px logo orb radius

  let mouse = { x: cx, y: cy, active: false };
  let particles = [];
  const MAX_PARTICLES = 44;

  // Offscreen pre-rendered WHITE smoke puff sprite for ultra-soft feathered rendering
  const spriteSize = 80;
  const spriteCanvas = document.createElement('canvas');
  spriteCanvas.width = spriteSize;
  spriteCanvas.height = spriteSize;
  const sctx = spriteCanvas.getContext('2d');
  const scx = spriteSize / 2;
  const scy = spriteSize / 2;
  const sGrad = sctx.createRadialGradient(scx, scy, 0, scx, scy, scx);

  // Pure ethereal WHITE smoke palette
  sGrad.addColorStop(0, 'rgba(255, 255, 255, 0.70)');
  sGrad.addColorStop(0.2, 'rgba(252, 250, 246, 0.52)');
  sGrad.addColorStop(0.45, 'rgba(242, 238, 230, 0.28)');
  sGrad.addColorStop(0.75, 'rgba(225, 220, 212, 0.08)');
  sGrad.addColorStop(1, 'rgba(210, 205, 195, 0)');
  sctx.fillStyle = sGrad;
  sctx.beginPath();
  sctx.arc(scx, scy, scx, 0, Math.PI * 2);
  sctx.fill();

  class WhiteSmokeParticle {
    constructor(forcedX, forcedY, isBurst = false){
      this.reset(forcedX, forcedY, isBurst);
    }
    reset(forcedX, forcedY, isBurst = false){
      const angle = isBurst
        ? Math.random() * Math.PI * 2
        : (Math.random() * Math.PI * 1.5 + 0.25 * Math.PI); // sides & bottom perimeter
      const spawnDist = orbRadius * (0.85 + Math.random() * 0.35);

      this.x = forcedX != null ? forcedX : cx + Math.cos(angle) * spawnDist;
      this.y = forcedY != null ? forcedY : cy + Math.sin(angle) * spawnDist;

      const speed = isBurst ? (0.8 + Math.random() * 1.4) : (0.25 + Math.random() * 0.45);
      this.vx = isBurst ? Math.cos(angle) * speed : (Math.random() - 0.5) * 0.4;
      this.vy = isBurst ? Math.sin(angle) * speed : (-0.45 - Math.random() * 0.45);

      this.size = 20 + Math.random() * 16;
      this.maxSize = this.size * (2.2 + Math.random() * 1.4);
      this.rotation = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - 0.5) * 0.012;

      this.age = 0;
      this.lifespan = isBurst ? (50 + Math.random() * 30) : (75 + Math.random() * 55);
      this.maxAlpha = isBurst ? (0.48 + Math.random() * 0.2) : (0.26 + Math.random() * 0.16);
      this.swayFreq = 0.025 + Math.random() * 0.025;
      this.swayPhase = Math.random() * Math.PI * 2;
      this.swayAmp = 0.35 + Math.random() * 0.45;
    }
    update(){
      this.age++;
      if(this.age >= this.lifespan){
        this.reset();
        return;
      }
      this.x += this.vx + Math.sin(this.age * this.swayFreq + this.swayPhase) * this.swayAmp;
      this.y += this.vy;
      this.vy *= 0.993;
      this.rotation += this.rotSpeed;

      if(mouse.active){
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const dist = Math.hypot(dx, dy);
        if(dist < 70 && dist > 1){
          const force = (1 - dist / 70) * 0.65;
          this.vx += (dx / dist) * force;
          this.vy += (dy / dist) * force;
        }
      }
    }
    draw(){
      const progress = this.age / this.lifespan;
      const alpha = Math.sin(progress * Math.PI) * this.maxAlpha;
      if(alpha <= 0.005) return;

      const currentSize = this.size + (this.maxSize - this.size) * progress;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.drawImage(spriteCanvas, -currentSize / 2, -currentSize / 2, currentSize, currentSize);
      ctx.restore();
    }
  }

  // Pre-seed particles staggered
  for(let i = 0; i < MAX_PARTICLES; i++){
    const p = new WhiteSmokeParticle();
    p.age = Math.floor(Math.random() * p.lifespan);
    particles.push(p);
  }

  // Interactive mouse/touch movement
  wrapper.addEventListener('mousemove', e => {
    const rect = wrapper.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    mouse.x = (mx / rect.width) * CSS_SIZE;
    mouse.y = (my / rect.height) * CSS_SIZE;
    mouse.active = true;

    const tiltX = -((mouse.y - cy) / cy) * 10;
    const tiltY = ((mouse.x - cx) / cx) * 10;
    orb.style.transform = `perspective(400px) rotateX(${tiltX.toFixed(1)}deg) rotateY(${tiltY.toFixed(1)}deg) scale(1.04)`;

    if(Math.random() < 0.4 && particles.length < MAX_PARTICLES + 12){
      particles.push(new WhiteSmokeParticle(mouse.x, mouse.y, false));
    }
  });

  wrapper.addEventListener('mouseleave', () => {
    mouse.active = false;
    orb.style.transform = 'perspective(400px) rotateX(0deg) rotateY(0deg) scale(1)';
  });

  wrapper.addEventListener('click', () => {
    for(let i = 0; i < 14; i++){
      particles.push(new WhiteSmokeParticle(cx, cy, true));
    }
  });

  let animRunning = true;
  function renderLoader(){
    if(!animRunning) return;
    ctx.clearRect(0, 0, CSS_SIZE, CSS_SIZE);
    for(let i = particles.length - 1; i >= 0; i--){
      const p = particles[i];
      p.update();
      p.draw();
      if(p.age >= p.lifespan && particles.length > MAX_PARTICLES){
        particles.splice(i, 1);
      }
    }
    requestAnimationFrame(renderLoader);
  }
  requestAnimationFrame(renderLoader);

  // Progressive loader bar & dismiss sequence
  let progress = 0;
  const statuses = ['Loading Core Modules...', 'Connecting Database...', 'Calibrating Spiritual Engine...', 'Ready'];
  const interval = setInterval(() => {
    progress += Math.floor(Math.random() * 18) + 12;
    if(progress > 100) progress = 100;
    if(pBar) pBar.style.width = progress + '%';
    const statusIdx = Math.min(Math.floor((progress / 100) * (statuses.length - 1)), statuses.length - 1);
    if(statusEl) statusEl.textContent = statuses[statusIdx];

    if(progress >= 100){
      clearInterval(interval);
      // Gentle white burst wave
      for(let i = 0; i < 16; i++){
        particles.push(new WhiteSmokeParticle(cx, cy, true));
      }
      setTimeout(() => {
        loader.classList.add('loaded');
        setTimeout(() => {
          animRunning = false;
          loader.remove(); // Remove from DOM after transition
        }, 750);
      }, 400);
    }
  }, 140);

  // Fallback auto-dismiss after 3.5s
  setTimeout(() => {
    if(!loader.classList.contains('loaded')){
      clearInterval(interval);
      loader.classList.add('loaded');
      setTimeout(() => { animRunning = false; loader.remove(); }, 750);
    }
  }, 3500);
})();"""

new_loader_js_block = """/* ================= WHITE UHD SMOKE PAGE LOADER ENGINE (BIG LOGO) ================= */
let dismissLoaderNow = null;
(function initPageLoader(){
  const loader = document.getElementById('pageLoader');
  const canvas = document.getElementById('loaderSmokeCanvas');
  const wrapper = document.getElementById('loaderSmokeWrapper');
  const orb = document.getElementById('loaderLogoOrb');
  const pBar = document.getElementById('loaderProgressBar');
  const statusEl = document.getElementById('loaderStatus');
  if(!loader || !canvas || !orb) return;

  const ctx = canvas.getContext('2d');
  if(!ctx) return;

  // UHD Retina scale for 480x480 canvas
  const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
  const CSS_SIZE = 480;
  canvas.width = Math.round(CSS_SIZE * dpr);
  canvas.height = Math.round(CSS_SIZE * dpr);
  ctx.scale(dpr, dpr);

  const cx = CSS_SIZE / 2;
  const cy = CSS_SIZE / 2;
  const orbRadius = 104; // Center 210px big logo orb radius

  let mouse = { x: cx, y: cy, active: false };
  let particles = [];
  const MAX_PARTICLES = 52;

  // Offscreen pre-rendered pure WHITE smoke puff sprite
  const spriteSize = 100;
  const spriteCanvas = document.createElement('canvas');
  spriteCanvas.width = spriteSize;
  spriteCanvas.height = spriteSize;
  const sctx = spriteCanvas.getContext('2d');
  const scx = spriteSize / 2;
  const scy = spriteSize / 2;
  const sGrad = sctx.createRadialGradient(scx, scy, 0, scx, scy, scx);

  // Luminous white and pearlescent smoke layers
  sGrad.addColorStop(0, 'rgba(255, 255, 255, 0.75)');
  sGrad.addColorStop(0.22, 'rgba(252, 250, 246, 0.54)');
  sGrad.addColorStop(0.48, 'rgba(240, 235, 226, 0.28)');
  sGrad.addColorStop(0.78, 'rgba(222, 215, 205, 0.08)');
  sGrad.addColorStop(1, 'rgba(205, 195, 185, 0)');
  sctx.fillStyle = sGrad;
  sctx.beginPath();
  sctx.arc(scx, scy, scx, 0, Math.PI * 2);
  sctx.fill();

  class WhiteSmokeParticle {
    constructor(forcedX, forcedY, isBurst = false){
      this.reset(forcedX, forcedY, isBurst);
    }
    reset(forcedX, forcedY, isBurst = false){
      const angle = isBurst
        ? Math.random() * Math.PI * 2
        : (Math.random() * Math.PI * 1.5 + 0.25 * Math.PI); // sides & bottom perimeter
      const spawnDist = orbRadius * (0.88 + Math.random() * 0.3);

      this.x = forcedX != null ? forcedX : cx + Math.cos(angle) * spawnDist;
      this.y = forcedY != null ? forcedY : cy + Math.sin(angle) * spawnDist;

      const speed = isBurst ? (1.0 + Math.random() * 1.6) : (0.3 + Math.random() * 0.5);
      this.vx = isBurst ? Math.cos(angle) * speed : (Math.random() - 0.5) * 0.45;
      this.vy = isBurst ? Math.sin(angle) * speed : (-0.45 - Math.random() * 0.5);

      this.size = 28 + Math.random() * 22;
      this.maxSize = this.size * (2.2 + Math.random() * 1.3);
      this.rotation = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - 0.5) * 0.012;

      this.age = 0;
      this.lifespan = isBurst ? (55 + Math.random() * 30) : (80 + Math.random() * 55);
      this.maxAlpha = isBurst ? (0.50 + Math.random() * 0.2) : (0.28 + Math.random() * 0.16);
      this.swayFreq = 0.022 + Math.random() * 0.025;
      this.swayPhase = Math.random() * Math.PI * 2;
      this.swayAmp = 0.4 + Math.random() * 0.55;
    }
    update(){
      this.age++;
      if(this.age >= this.lifespan){
        this.reset();
        return;
      }
      this.x += this.vx + Math.sin(this.age * this.swayFreq + this.swayPhase) * this.swayAmp;
      this.y += this.vy;
      this.vy *= 0.994;
      this.rotation += this.rotSpeed;

      if(mouse.active){
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const dist = Math.hypot(dx, dy);
        if(dist < 90 && dist > 1){
          const force = (1 - dist / 90) * 0.7;
          this.vx += (dx / dist) * force;
          this.vy += (dy / dist) * force;
        }
      }
    }
    draw(){
      const progress = this.age / this.lifespan;
      const alpha = Math.sin(progress * Math.PI) * this.maxAlpha;
      if(alpha <= 0.005) return;

      const currentSize = this.size + (this.maxSize - this.size) * progress;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      ctx.drawImage(spriteCanvas, -currentSize / 2, -currentSize / 2, currentSize, currentSize);
      ctx.restore();
    }
  }

  // Pre-seed particles
  for(let i = 0; i < MAX_PARTICLES; i++){
    const p = new WhiteSmokeParticle();
    p.age = Math.floor(Math.random() * p.lifespan);
    particles.push(p);
  }

  // Interactive mouse/touch movement
  wrapper.addEventListener('mousemove', e => {
    const rect = wrapper.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    mouse.x = (mx / rect.width) * CSS_SIZE;
    mouse.y = (my / rect.height) * CSS_SIZE;
    mouse.active = true;

    const tiltX = -((mouse.y - cy) / cy) * 11;
    const tiltY = ((mouse.x - cx) / cx) * 11;
    orb.style.transform = `perspective(500px) rotateX(${tiltX.toFixed(1)}deg) rotateY(${tiltY.toFixed(1)}deg) scale(1.04)`;

    if(Math.random() < 0.4 && particles.length < MAX_PARTICLES + 16){
      particles.push(new WhiteSmokeParticle(mouse.x, mouse.y, false));
    }
  });

  wrapper.addEventListener('mouseleave', () => {
    mouse.active = false;
    orb.style.transform = 'perspective(500px) rotateX(0deg) rotateY(0deg) scale(1)';
  });

  wrapper.addEventListener('click', e => {
    e.stopPropagation();
    for(let i = 0; i < 18; i++){
      particles.push(new WhiteSmokeParticle(cx, cy, true));
    }
  });

  let animRunning = true;
  function renderLoader(){
    if(!animRunning) return;
    ctx.clearRect(0, 0, CSS_SIZE, CSS_SIZE);
    for(let i = particles.length - 1; i >= 0; i--){
      const p = particles[i];
      p.update();
      p.draw();
      if(p.age >= p.lifespan && particles.length > MAX_PARTICLES){
        particles.splice(i, 1);
      }
    }
    requestAnimationFrame(renderLoader);
  }
  requestAnimationFrame(renderLoader);

  function dismiss(){
    if(loader.classList.contains('loaded')) return;
    for(let i = 0; i < 20; i++){
      particles.push(new WhiteSmokeParticle(cx, cy, true));
    }
    loader.classList.add('loaded');
    setTimeout(() => {
      animRunning = false;
      loader.remove();
    }, 750);
  }
  dismissLoaderNow = dismiss;

  // Progressive loader animation
  let progress = 0;
  const statuses = ['Loading Core System...', 'Calibrating Portal...', 'Opening Workspace...', 'Ready'];
  const interval = setInterval(() => {
    progress += Math.floor(Math.random() * 14) + 10;
    if(progress > 100) progress = 100;
    if(pBar) pBar.style.width = progress + '%';
    const statusIdx = Math.min(Math.floor((progress / 100) * (statuses.length - 1)), statuses.length - 1);
    if(statusEl) statusEl.textContent = statuses[statusIdx];

    if(progress >= 100){
      clearInterval(interval);
      setTimeout(dismiss, 350);
    }
  }, 130);

  // Auto dismiss fallback
  setTimeout(() => {
    clearInterval(interval);
    dismiss();
  }, 4000);
})();"""

assert old_loader_js_block in content, "old_loader_js_block not found"
content = content.replace(old_loader_js_block, new_loader_js_block, 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Also write to index.html
with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied Big Logo base64 and Card-Style Expand-on-Hover Navigation successfully!")
