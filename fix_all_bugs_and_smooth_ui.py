import re

html_path = '/home/projects/src-online.com/AIR-Patient-Management-System.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================================
# 1. FIX CSS: Scope all hover rules to (hover: hover) and (pointer: fine)
#    and fix mobile responsive layout for Rack Accordion & Nav Cards
# ==============================================================================

# Replace Retail Rack Accordion CSS with robust, responsive, non-buggy version
old_rack_css_pattern = r'/\* ================= RETAIL RACK ACCORDION GALLERY & DIRECTORY ================= \*/.*?/\* Reduced Motion \*/\s*@media\(prefers-reduced-motion: reduce\) \{.*?\}'

new_rack_css = """/* ================= RETAIL RACK ACCORDION GALLERY & DIRECTORY ================= */
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
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .rack-accordion-track::-webkit-scrollbar {
    display: none;
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
    transition: flex 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                max-width 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                min-width 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                transform 0.35s ease,
                box-shadow 0.35s ease;
  }

  /* Expanded Hero Panel (Default / Active) */
  .rack-panel.active {
    flex: 5.6 1 420px;
    min-width: 380px;
    max-width: 720px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
    cursor: default;
  }

  /* Desktop Hover Mechanics (Scoped strictly to pointer devices with true hover support) */
  @media (hover: hover) and (pointer: fine) {
    .rack-panel:hover:not(.active) {
      transform: translateY(-2px);
    }
    .rack-accordion-track:hover .rack-panel.is-hovered {
      flex: 5.6 1 420px;
      min-width: 380px;
      max-width: 720px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
    }
    .rack-accordion-track:hover .rack-panel.active:not(.is-hovered) {
      flex: 1 1 78px;
      min-width: 68px;
      max-width: 110px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }
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
    .rack-accordion-track:hover .rack-panel.is-hovered .rack-expanded-view {
      opacity: 1;
      pointer-events: auto;
      transform: translateX(0);
      transition-delay: 0.08s;
    }
    .rack-accordion-track:hover .rack-panel.active:not(.is-hovered) .rack-expanded-view {
      opacity: 0;
      pointer-events: none;
      transform: translateX(12px);
      transition-delay: 0s;
    }
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

  /* Permanent Index Tag (#01, #02...) */
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
  .rack-panel.active .rack-collapsed-view {
    opacity: 0;
    pointer-events: none;
    transform: scale(0.9);
  }

  /* --- Expanded Hero Panel View --- */
  .rack-expanded-view {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 16px;
    padding: 22px 26px;
    z-index: 3;
    opacity: 0;
    pointer-events: none;
    transform: translateX(12px);
    transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
    overflow: hidden;
  }
  .rack-panel.active .rack-expanded-view {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0);
    transition-delay: 0.08s;
  }

  /* Left Side: Editorial Typography Poster Stack */
  .rack-poster-left {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
    border-right: 1px solid rgba(255, 255, 255, 0.12);
    padding-right: 14px;
    overflow: hidden;
  }
  .rack-meta-top {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rack-headline-stack {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin: auto 0;
    overflow: hidden;
  }
  .rack-headline-line {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(20px, 2.2vw, 28px);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.2px;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rack-blurb-bottom {
    font-size: 11px;
    line-height: 1.4;
    opacity: 0.85;
    margin-top: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* Right Side: Seamless Integrated Directory */
  .rack-directory-right {
    display: flex;
    flex-direction: column;
    min-width: 0;
    gap: 8px;
    height: 100%;
    overflow: hidden;
  }
  .rack-dir-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    flex-shrink: 0;
  }
  .rack-dir-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    opacity: 0.95;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rack-dir-badge {
    font-size: 10px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    flex-shrink: 0;
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
    justify-content: center;
    gap: 5px;
    padding: 6px 8px;
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
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    border-radius: 10px;
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }
  .rack-roster-head {
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    opacity: 0.8;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .rack-roster-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
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

  /* Responsive / Mobile (Horizontal Fluid Garment Swiping) */
  @media(max-width: 860px) {
    .rack-accordion-track {
      height: 350px;
      padding: 4px;
      gap: 6px;
    }
    .rack-panel {
      flex: 0 0 68px;
      min-width: 68px;
      max-width: 68px;
      height: 100%;
    }
    .rack-panel.active {
      flex: 0 0 calc(100vw - 36px);
      min-width: 290px;
      max-width: 390px;
    }
    .rack-expanded-view {
      grid-template-columns: 1fr;
      gap: 12px;
      padding: 16px;
      overflow-y: auto;
    }
    .rack-poster-left {
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding-right: 0;
      padding-bottom: 10px;
    }
    .rack-headline-line {
      font-size: 22px;
    }
    .rack-patients-roster {
      max-height: 110px;
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

content = re.sub(old_rack_css_pattern, new_rack_css, content, flags=re.DOTALL)

# ==============================================================================
# 2. FIX CSS for Top Navigation Bar (.expand-nav-container) on desktop & mobile
# ==============================================================================
old_nav_css_pattern = r'/\* ================= MINIMALIST EXPAND-ON-HOVER CARD NAVIGATION ================= \*/.*?@media\(max-width: 960px\) \{.*?\.expand-nav-container \{.*?\}\s*\}'

new_nav_css = """/* ================= MINIMALIST EXPAND-ON-HOVER CARD NAVIGATION ================= */
  .expand-nav-container {
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1.5px solid var(--border);
    padding: 8px 18px;
    position: sticky;
    top: 68px;
    z-index: 45;
    box-shadow: 0 2px 10px rgba(61, 40, 29, 0.03);
  }
  .expand-nav-track {
    max-width: 1240px;
    margin: 0 auto;
    display: flex;
    gap: 8px;
    align-items: stretch;
    height: 145px;
    position: relative;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .expand-nav-track::-webkit-scrollbar {
    display: none;
  }
  
  /* The Base Card */
  .expand-card {
    position: relative;
    flex: 1 1 85px;
    min-width: 78px;
    max-width: 130px;
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

  /* Active card (when track is not hovered) */
  .expand-card.active {
    flex: 4 1 360px;
    max-width: 620px;
    border-color: var(--brown);
    box-shadow: 0 4px 18px rgba(124, 83, 57, 0.10);
    background: #fffdfa;
  }

  /* Scoped desktop hover */
  @media (hover: hover) and (pointer: fine) {
    .expand-card:hover:not(.active) {
      border-color: #c9bbae;
    }
    .expand-nav-track:hover .expand-card.is-hovered {
      flex: 4 1 360px;
      max-width: 620px;
      border-color: var(--brown);
      box-shadow: 0 6px 20px rgba(124, 83, 57, 0.12);
      background: #fffdfa;
    }
    .expand-nav-track:hover .expand-card.active:not(.is-hovered) {
      flex: 1 1 85px;
      max-width: 130px;
      border-color: var(--border);
      box-shadow: 0 1px 4px rgba(61, 40, 29, 0.03);
      background: #ffffff;
    }
    .expand-nav-track:hover .expand-card.is-hovered .card-collapsed-view {
      opacity: 0;
      pointer-events: none;
      transform: scale(0.9);
    }
    .expand-nav-track:hover .expand-card.active:not(.is-hovered) .card-collapsed-view {
      opacity: 1;
      pointer-events: auto;
      transform: none;
    }
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
  }

  /* --- Collapsed View --- */
  .card-collapsed-view {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px 6px;
    gap: 6px;
    text-align: center;
    transition: opacity 0.2s ease, transform 0.2s ease;
    opacity: 1;
    pointer-events: auto;
  }
  .card-c-icon {
    font-size: 22px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: #fbf7f1;
    border: 1px solid var(--border);
    transition: transform 0.2s ease;
  }
  .card-c-title {
    font-size: 12px;
    font-weight: 800;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 85px;
  }
  .card-c-badge {
    font-size: 9.5px;
    font-weight: 700;
    color: var(--brown);
    background: #f4ece2;
    padding: 1px 7px;
    border-radius: 999px;
    white-space: nowrap;
    border: 1px solid rgba(124, 83, 57, 0.12);
  }

  .expand-card.active .card-collapsed-view {
    opacity: 0;
    pointer-events: none;
    position: absolute;
    transform: scale(0.9);
  }

  /* --- Expanded View --- */
  .card-expanded-view {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 10px 14px;
    opacity: 0;
    pointer-events: none;
    transform: translateX(8px);
    transition: opacity 0.25s ease, transform 0.25s ease;
    overflow: hidden;
  }
  .expand-card.active .card-expanded-view {
    opacity: 1;
    pointer-events: auto;
    transform: translateX(0);
    transition-delay: 0.05s;
  }

  /* Expanded Card Header */
  .card-exp-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    border-bottom: 1px solid #ebdccb;
    padding-bottom: 6px;
    flex-shrink: 0;
  }
  .card-exp-lead {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
  }
  .card-exp-icon {
    font-size: 18px;
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: #fbf6ee;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .card-exp-title {
    font-size: 13.5px;
    font-weight: 800;
    color: var(--brown-dark);
    line-height: 1.2;
    white-space: nowrap;
  }
  .card-exp-sub {
    font-size: 10.5px;
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
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
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
  }

  /* Directories Layout on Nav Card */
  .card-directories-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px 8px;
    margin-top: 6px;
    flex: 1;
    align-content: center;
  }
  .card-dir-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 5px 8px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.16s ease;
    text-align: left;
    min-width: 0;
  }
  .card-dir-item:hover {
    background: #fbf6ef;
    border-color: var(--brown);
    transform: translateY(-1px);
  }
  .card-dir-item .dir-icon {
    font-size: 14px;
    line-height: 1;
    flex-shrink: 0;
  }
  .card-dir-item .dir-text {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }
  .card-dir-item .dir-title {
    font-size: 11px;
    font-weight: 750;
    color: var(--brown-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-dir-item .dir-sub {
    font-size: 9.5px;
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
    gap: 4px 6px;
    margin-top: 6px;
    flex: 1;
    align-content: center;
    overflow-y: auto;
  }
  .card-cat-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5px;
    padding: 3px 6px;
    background: #ffffff;
    border: 1px solid #ebdccb;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.16s ease;
    font-size: 10.5px;
    font-weight: 700;
    color: var(--brown-dark);
    min-width: 0;
  }
  .card-cat-chip:hover {
    background: #fbf6ee;
    border-color: var(--brown);
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
    gap: 4px;
    min-width: 0;
    overflow: hidden;
  }
  .card-cat-chip .chip-icon {
    font-size: 11px;
    line-height: 1;
    flex-shrink: 0;
  }
  .card-cat-chip .chip-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-cat-chip .chip-cnt {
    font-size: 9.5px;
    font-weight: 700;
    background: #f4ece2;
    color: var(--brown);
    padding: 1px 4px;
    border-radius: 999px;
    flex-shrink: 0;
  }

  /* Responsive / Mobile Styling */
  @media(max-width: 960px) {
    .expand-nav-container {
      position: relative;
      top: auto;
      padding: 6px 10px;
    }
    .expand-nav-track {
      height: 145px;
      gap: 6px;
    }
    .expand-card {
      flex: 0 0 54px;
      min-width: 54px;
      max-width: 54px;
    }
    .expand-card.active {
      flex: 0 0 calc(100vw - 36px);
      min-width: 280px;
      max-width: 380px;
    }
    .card-directories-categories {
      grid-template-columns: repeat(2, 1fr);
    }
  }"""

content = re.sub(old_nav_css_pattern, new_nav_css, content, flags=re.DOTALL)

# ==============================================================================
# 3. FIX JavaScript: Calendar Presets, validation, slot selection, balance
# ==============================================================================
old_cal_engine_pattern = r'/\* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= \*/.*?function updateRegApptCurrency\(\)\{.*?\}'

new_cal_engine = """/* ================= REGISTRATION CALENDAR & APPOINTMENT SCHEDULER ENGINE ================= */
let REG_CAL_YEAR = new Date().getFullYear();
let REG_CAL_MONTH = new Date().getMonth(); // 0-11
let REG_SELECTED_DATE = todayISO(); // YYYY-MM-DD

function initRegCalendar(){
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
                  onclick="selectRegCalendarDate('${isoDate}', this)"
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

function selectRegCalendarDate(isoDate, cellEl){
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
}

function setRegTimeSlot(start, end, btnEl){
  $('regApptStart').value = start;
  $('regApptEnd').value = end;

  // Highlight slot chip
  document.querySelectorAll('.ras-slot-chip').forEach(btn => {
    btn.classList.remove('active');
  });
  if(btnEl){
    btnEl.classList.add('active');
  }
}

function toggleRegApptBooking(enabled){
  const body = $('rasContentBody');
  const btn = $('savePatientBtn') || document.querySelector('#patientForm button[type=submit]');
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
  $('regApptBalance').value = sym + ' ' + bal;
}

function updateRegApptCurrency(){
  const sym = currencyFor($('pCountry').value.trim()).sym;
  document.querySelectorAll('.reg-cur-lbl').forEach(el => el.textContent = sym);
  updateRegBalance();
}"""

content = re.sub(old_cal_engine_pattern, new_cal_engine, content, flags=re.DOTALL)

# ==============================================================================
# 4. FIX HTML: preset buttons and slot chips pass 'this' to their handlers
# ==============================================================================
content = content.replace("onclick=\"setRegCalendarPreset(0)\"", "onclick=\"setRegCalendarPreset(0, this)\"")
content = content.replace("onclick=\"setRegCalendarPreset(1)\"", "onclick=\"setRegCalendarPreset(1, this)\"")
content = content.replace("onclick=\"setRegCalendarPreset(2)\"", "onclick=\"setRegCalendarPreset(2, this)\"")
content = content.replace("onclick=\"setRegCalendarPreset('nextMonday')\"", "onclick=\"setRegCalendarPreset('nextMonday', this)\"")

content = content.replace("onclick=\"setRegTimeSlot('10:00','11:00')\"", "onclick=\"setRegTimeSlot('10:00','11:00', this)\"")
content = content.replace("onclick=\"setRegTimeSlot('11:30','12:30')\"", "onclick=\"setRegTimeSlot('11:30','12:30', this)\"")
content = content.replace("onclick=\"setRegTimeSlot('15:00','16:00')\"", "onclick=\"setRegTimeSlot('15:00','16:00', this)\"")
content = content.replace("onclick=\"setRegTimeSlot('17:00','18:00')\"", "onclick=\"setRegTimeSlot('17:00','18:00', this)\"")
content = content.replace("onclick=\"setRegTimeSlot('20:00','21:00')\"", "onclick=\"setRegTimeSlot('20:00','21:00', this)\"")

# Set default date in hidden input
content = content.replace('<input type="hidden" id="regApptDate" value="">', '<input type="hidden" id="regApptDate" value="' + "2026-10-07" + '">')

# ==============================================================================
# 5. FIX VALIDATION in patientForm submit handler
# ==============================================================================
old_submit_validation = """  // If appointment booking is enabled, create appointment on chosen date and time slot
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
  }"""

new_submit_validation = """  // Validate appointment times and fees if enabled
  if(shouldBookAppt){
    if(apptEnd <= apptStart){
      toast('Appointment end time must be after start time', true);
      return;
    }
    if(apptPaid > apptFee){
      toast('Paid amount cannot be more than total fee', true);
      return;
    }
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
  }"""

assert old_submit_validation in content, "old_submit_validation not found"
content = content.replace(old_submit_validation, new_submit_validation, 1)

# Write to file
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

with open('/home/projects/src-online.com/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: All bugs fixed and UI smoothed across Web/Mobile!")
