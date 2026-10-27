/* ================= ISLAMIC HIJRI ENGINE & UMM AL-QURA ALGORITHM ================= */
var HIJRI_OFFSET_DAYS = parseInt(localStorage.getItem('shifa_hijri_offset') || '0', 10);
var INPAGE_HIJRI_YEAR = null;
var INPAGE_HIJRI_MONTH = null;
var SELECTED_INPAGE_HIJRI_DATE_ISO = null;

var HIJRI_MONTHS_EN = [
  'Muharram', 'Safar', 'Rabi al-Awwal', 'Rabi al-Thani',
  'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', "Sha'ban",
  'Ramadan', 'Shawwal', "Dhul-Qi'dah", 'Dhul-Hijjah'
];

var HIJRI_MONTHS_AR = [
  'المُحَرَّم', 'صَفَر', 'رَبِيع الأَوَّل', 'رَبِيع الآخِر',
  'جُمَادَى الأُولَى', 'جُمَادَى الآخِرَة', 'رَجَب', 'شَعْبَان',
  'رَمَضَان', 'شَوَّال', 'ذُو القَعْدَة', 'ذُو الحِجَّة'
];

var HIJRI_MONTHS_UR = [
  'محرم الحرام', 'صفر المظفر', 'ربیع الاول', 'ربیع الثانی',
  'جمادی الاول', 'جمادی الثانی', 'رجب المرجب', 'شعبان المعظم',
  'رمضان المبارک', 'شوال المکرم', 'ذی القعدہ', 'ذی الحجہ'
];

var WEEKDAYS_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
var WEEKDAYS_AR = ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];
var WEEKDAYS_UR = ['اتوار', 'پیر', 'منگل', 'بدھ', 'جمعرات', 'جمعہ', 'ہفتہ'];

function getAdjustedDate(baseDate, offsetDays){
  const d = new Date(baseDate.getTime());
  d.setDate(d.getDate() + (offsetDays || 0));
  return d;
}

function getHijriDetails(dateObj, offsetDays){
  const off = (offsetDays !== undefined) ? offsetDays : HIJRI_OFFSET_DAYS;
  const targetDate = getAdjustedDate(dateObj, off);

  try {
    const formatter = new Intl.DateTimeFormat('en-u-ca-islamic-umalqura', {
      day: 'numeric',
      month: 'numeric',
      year: 'numeric'
    });
    const parts = formatter.formatToParts(targetDate);
    let hDay = 1, hMonth = 1, hYear = 1448;
    parts.forEach(p => {
      if(p.type === 'day') hDay = parseInt(p.value, 10);
      if(p.type === 'month') hMonth = parseInt(p.value, 10);
      if(p.type === 'year') hYear = parseInt(p.value, 10);
    });

    const mIdx = Math.max(0, Math.min(11, hMonth - 1));
    const isWhiteDay = (hDay === 13 || hDay === 14 || hDay === 15);
    const dow = targetDate.getDay();
    const isFriday = (dow === 5);
    const isSacredMonth = (mIdx === 0 || mIdx === 6 || mIdx === 10 || mIdx === 11);

    return {
      day: hDay,
      monthIndex: mIdx,
      monthEn: HIJRI_MONTHS_EN[mIdx],
      monthAr: HIJRI_MONTHS_AR[mIdx],
      monthUr: HIJRI_MONTHS_UR[mIdx],
      year: hYear,
      isWhiteDay: isWhiteDay,
      isFriday: isFriday,
      isSacredMonth: isSacredMonth,
      formattedEn: `${hDay} ${HIJRI_MONTHS_EN[mIdx]} ${hYear} AH`,
      formattedAr: `${hDay} ${HIJRI_MONTHS_AR[mIdx]} ${hYear} هـ`,
      formattedUr: `${hDay} ${HIJRI_MONTHS_UR[mIdx]} ${hYear}ھ`
    };
  } catch(e) {
    return {
      day: 16,
      monthIndex: 4,
      monthEn: 'Jumada al-Awwal',
      monthAr: 'جُمَادَى الأُولَى',
      monthUr: 'جمادی الاول',
      year: 1448,
      isWhiteDay: false,
      isFriday: false,
      isSacredMonth: false,
      formattedEn: '16 Jumada al-Awwal 1448 AH',
      formattedAr: '16 جُمَادَى الأُولَى 1448 هـ',
      formattedUr: '16 جمادی الاول 1448ھ'
    };
  }
}

function getMoonPhaseInfo(hijriDay){
  const d = hijriDay || 1;
  if(d === 1 || d === 30) return { nameEn: 'New Moon (Hilal)', nameUr: 'نیا چاند (ہلال)', icon: '🌑' };
  if(d >= 2 && d <= 6) return { nameEn: 'Waxing Crescent', nameUr: 'ہلال (بڑھتا ہوا)', icon: '🌒' };
  if(d >= 7 && d <= 9) return { nameEn: 'First Quarter', nameUr: 'تربیع اول', icon: '🌓' };
  if(d >= 10 && d <= 13) return { nameEn: 'Waxing Gibbous', nameUr: 'محدب (بڑھتا ہوا)', icon: '🌔' };
  if(d === 14 || d === 15) return { nameEn: 'Full Moon (Badr)', nameUr: 'بدر کامل (چودھویں کا چاند)', icon: '🌕' };
  if(d >= 16 && d <= 21) return { nameEn: 'Waning Gibbous', nameUr: 'محدب (گھٹتا ہوا)', icon: '🌖' };
  if(d >= 22 && d <= 24) return { nameEn: 'Last Quarter', nameUr: 'تربیع ثانی', icon: '🌗' };
  return { nameEn: 'Waning Crescent', nameUr: 'ہلال (آخری ایام)', icon: '🌘' };
}

function updateLiveIslamicHeaderClock(){
  const now = new Date();
  const hijri = getHijriDetails(now);
  const isUr = (typeof getAppLanguage === 'function' ? getAppLanguage() === 'ur' : (document.documentElement.lang === 'ur'));

  // Header badge (sleek & compact so it never overflows header)
  const hDateEl = document.getElementById('headerHijriDate');
  const badgeEl = document.getElementById('headerDateTimeBadge');
  if(hDateEl) {
    const compactEn = `${hijri.day} ${hijri.monthEn}`;
    const compactUr = `${hijri.day} ${hijri.monthUr}`;
    hDateEl.textContent = isUr ? compactUr : compactEn;
  }
  if(badgeEl) {
    badgeEl.title = isUr ? `${hijri.formattedUr} • اسلامی کیلنڈر دیکھیں` : `${hijri.formattedEn} • Click to view Hijri Calendar`;
  }

  // Overview live bar
  const ilbMain = document.getElementById('ilbHijriMain');
  const ilbSub = document.getElementById('ilbGregSub');
  const ilbBadge = document.getElementById('ilbSunnahText');

  if(ilbMain) ilbMain.textContent = isUr ? hijri.formattedUr : hijri.formattedEn;
  if(ilbSub){
    const gregStr = now.toLocaleDateString(isUr ? 'ur-PK' : 'en-GB', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
    });
    const moon = getMoonPhaseInfo(hijri.day);
    ilbSub.textContent = `${gregStr} • ${moon.icon} ${isUr ? moon.nameUr : moon.nameEn}`;
  }
  if(ilbBadge){
    if(hijri.isWhiteDay) ilbBadge.textContent = isUr ? 'ایامِ بیض کا مسنون روزہ' : 'Sunnah Fast (Ayyam al-Beed)';
    else if(hijri.isFriday) ilbBadge.textContent = isUr ? 'مبارک جمعۃ المبارک' : 'Blessed Jumu’ah';
    else if(hijri.isSacredMonth) ilbBadge.textContent = isUr ? 'حرمت والا مہینہ' : 'Sacred Islamic Month';
    else ilbBadge.textContent = isUr ? 'مسنون دعا و شفاء' : 'Ruqyah Shari’ah Guidance';
  }
}
setInterval(updateLiveIslamicHeaderClock, 1000);

/* ================= IN-PAGE HIJRI CALENDAR RENDERING ================= */
function renderInPageHijriCalendar(){
  const grid = document.getElementById('inpageCalGrid');
  if(!grid) return;

  const now = new Date();
  const currentHijri = getHijriDetails(now);

  if(INPAGE_HIJRI_YEAR === null) INPAGE_HIJRI_YEAR = currentHijri.year;
  if(INPAGE_HIJRI_MONTH === null) INPAGE_HIJRI_MONTH = currentHijri.monthIndex;

  const isUr = (typeof getAppLanguage === 'function' ? getAppLanguage() === 'ur' : (document.documentElement.lang === 'ur'));
  const mIdx = INPAGE_HIJRI_MONTH;
  const hYear = INPAGE_HIJRI_YEAR;

  // Header Titles
  const arTitle = document.getElementById('inpageHijriMonthAr');
  const enTitle = document.getElementById('inpageHijriMonthEn');
  const navTitle = document.getElementById('inpageNavMonthTitle');
  const moonPhaseText = document.getElementById('inpageMoonPhaseText');
  const moonIcon = document.getElementById('inpageMoonIcon');

  if(arTitle) arTitle.textContent = `${HIJRI_MONTHS_AR[mIdx]} ${hYear} هـ`;
  if(enTitle) enTitle.textContent = `${HIJRI_MONTHS_EN[mIdx]} ${hYear} AH • ${isUr ? HIJRI_MONTHS_UR[mIdx] : ''}`;
  if(navTitle) navTitle.textContent = `${isUr ? HIJRI_MONTHS_UR[mIdx] : HIJRI_MONTHS_EN[mIdx]} ${hYear}`;

  const currentMoon = getMoonPhaseInfo(currentHijri.day);
  if(moonIcon) moonIcon.textContent = currentMoon.icon;
  if(moonPhaseText) moonPhaseText.textContent = isUr ? currentMoon.nameUr : currentMoon.nameEn;

  // Offset Buttons State
  [-2, -1, 0, 1, 2].forEach(val => {
    const btn = document.getElementById(val === 0 ? 'inpageOffset_0' : (val < 0 ? `inpageOffset_m${Math.abs(val)}` : `inpageOffset_p${val}`));
    if(btn){
      if(val === HIJRI_OFFSET_DAYS) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  });

  // Calculate day tiles matching this Hijri month
  const testCenter = new Date();
  const approxDeltaDays = (hYear - currentHijri.year) * 354 + (mIdx - currentHijri.monthIndex) * 29.5;
  testCenter.setDate(testCenter.getDate() + Math.round(approxDeltaDays));

  // Find start of this Hijri month
  let dPointer = new Date(testCenter.getTime());
  dPointer.setDate(dPointer.getDate() - 35);

  let monthDays = [];
  for(let i = 0; i < 75; i++){
    const hMeta = getHijriDetails(dPointer);
    if(hMeta.year === hYear && hMeta.monthIndex === mIdx){
      monthDays.push({
        gregDate: new Date(dPointer.getTime()),
        iso: dPointer.toISOString().split('T')[0],
        dow: dPointer.getDay(),
        hMeta: hMeta
      });
    }
    dPointer.setDate(dPointer.getDate() + 1);
  }

  if(monthDays.length === 0){
    const fallbackBase = new Date();
    for(let d = 1; d <= 30; d++){
      const fbD = new Date(fallbackBase.getTime());
      fbD.setDate(fbD.getDate() + (d - currentHijri.day));
      monthDays.push({
        gregDate: fbD,
        iso: fbD.toISOString().split('T')[0],
        dow: fbD.getDay(),
        hMeta: {
          day: d,
          monthIndex: mIdx,
          monthEn: HIJRI_MONTHS_EN[mIdx],
          monthAr: HIJRI_MONTHS_AR[mIdx],
          monthUr: HIJRI_MONTHS_UR[mIdx],
          year: hYear,
          isWhiteDay: (d === 13 || d === 14 || d === 15),
          isFriday: (fbD.getDay() === 5),
          formattedEn: `${d} ${HIJRI_MONTHS_EN[mIdx]} ${hYear} AH`,
          formattedUr: `${d} ${HIJRI_MONTHS_UR[mIdx]} ${hYear}ھ`
        }
      });
    }
  }

  // Update Range in Hero
  const gregRangeEl = document.getElementById('inpageHijriGregRange');
  if(gregRangeEl && monthDays.length > 0){
    const firstG = monthDays[0].gregDate;
    const lastG = monthDays[monthDays.length - 1].gregDate;
    const fmtMonth = (d) => d.toLocaleDateString(isUr ? 'ur-PK' : 'en-GB', { day: 'numeric', month: 'short' });
    gregRangeEl.textContent = `${fmtMonth(firstG)} – ${fmtMonth(lastG)} ${lastG.getFullYear()} (${monthDays.length} Days)`;
  }

  // Build Grid HTML
  let gridHtml = '';

  // Weekday Headers
  for(let w = 0; w < 7; w++){
    const wName = isUr ? WEEKDAYS_UR[w] : (window.innerWidth < 640 ? WEEKDAYS_EN[w] : `${WEEKDAYS_EN[w]}<br><span style="font-family:'Amiri';font-size:0.75rem;">${WEEKDAYS_AR[w]}</span>`);
    gridHtml += `<div class="inpage-weekday-header ${w === 5 ? 'is-friday' : ''}">${wName}</div>`;
  }

  // Empty leading cells
  const firstDow = monthDays[0].dow;
  for(let e = 0; e < firstDow; e++){
    gridHtml += '<div style="visibility:hidden;"></div>';
  }

  const todayIso = new Date().toISOString().split('T')[0];

  monthDays.forEach(item => {
    const isToday = (item.iso === todayIso);
    const isSelected = (item.iso === SELECTED_INPAGE_HIJRI_DATE_ISO);

    let badgeHtml = '';
    if(item.hMeta.isWhiteDay){
      badgeHtml = `<span class="inpage-tile-badge badge-white">${isUr ? 'ایامِ بیض' : '🌕 Ayyam Beed'}</span>`;
    } else if(item.hMeta.isFriday){
      badgeHtml = `<span class="inpage-tile-badge badge-friday">${isUr ? 'جمعہ' : 'Jumu’ah'}</span>`;
    } else if(item.dow === 1 || item.dow === 4){
      badgeHtml = `<span class="inpage-tile-badge badge-sunnah">${isUr ? 'مسنون' : 'Sunnah'}</span>`;
    }

    const gregFormatted = item.gregDate.toLocaleDateString(isUr ? 'ur-PK' : 'en-GB', { day: 'numeric', month: 'short' });

    gridHtml += `
      <div class="inpage-day-tile ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}"
           onclick="selectInpageHijriDayByIso('${item.iso}')"
           data-iso="${item.iso}"
           title="${item.hMeta.formattedEn} (${item.iso})">
        <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
          <span class="inpage-tile-hday">${item.hMeta.day}</span>
          ${isToday ? '<span style="font-size:0.55rem; font-weight:800; color:var(--gold-dark); background:var(--gold-light); padding:1px 4px; border-radius:4px;">TODAY</span>' : ''}
        </div>
        <span class="inpage-tile-greg">${gregFormatted}</span>
        ${badgeHtml}
      </div>
    `;
  });

  grid.innerHTML = gridHtml;

  // Cache month days globally
  window._inpageCurrentMonthDays = monthDays;

  // Auto-select today or first day
  if(!SELECTED_INPAGE_HIJRI_DATE_ISO){
    const todayItem = monthDays.find(m => m.iso === todayIso) || monthDays[0];
    if(todayItem) selectInpageHijriDay(todayItem);
  }
}

function inpageNavHijriMonth(delta){
  if(INPAGE_HIJRI_MONTH === null) return;
  INPAGE_HIJRI_MONTH += delta;
  if(INPAGE_HIJRI_MONTH > 11){
    INPAGE_HIJRI_MONTH = 0;
    INPAGE_HIJRI_YEAR++;
  } else if(INPAGE_HIJRI_MONTH < 0){
    INPAGE_HIJRI_MONTH = 11;
    INPAGE_HIJRI_YEAR--;
  }
  renderInPageHijriCalendar();
}

function inpageResetHijriMonth(){
  const now = new Date();
  const c = getHijriDetails(now);
  INPAGE_HIJRI_YEAR = c.year;
  INPAGE_HIJRI_MONTH = c.monthIndex;
  renderInPageHijriCalendar();
}

function inpageSetOffset(val){
  HIJRI_OFFSET_DAYS = val;
  localStorage.setItem('shifa_hijri_offset', String(val));
  updateLiveIslamicHeaderClock();
  inpageResetHijriMonth();
}

function selectInpageHijriDayByIso(iso){
  if(!window._inpageCurrentMonthDays) return;
  const item = window._inpageCurrentMonthDays.find(d => d.iso === iso);
  if(item) selectInpageHijriDay(item);
}

function selectInpageHijriDay(item){
  if(!item) return;
  SELECTED_INPAGE_HIJRI_DATE_ISO = item.iso;
  document.querySelectorAll('.inpage-day-tile').forEach(t => {
    if(t.getAttribute('data-iso') === item.iso) t.classList.add('selected');
    else t.classList.remove('selected');
  });

  const isUr = (typeof getAppLanguage === 'function' ? getAppLanguage() === 'ur' : (document.documentElement.lang === 'ur'));
  const titleEl = document.getElementById('inpageSelHijriTitle');
  const subEl = document.getElementById('inpageSelGregSubtitle');
  const bookBtn = document.getElementById('inpageBookBtn');

  if(titleEl){
    titleEl.textContent = isUr ? item.hMeta.formattedUr : item.hMeta.formattedEn;
  }
  if(subEl){
    const gregFmt = new Date(item.iso).toLocaleDateString(isUr ? 'ur-PK' : 'en-GB', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
    });
    let extra = '';
    if(item.hMeta.isWhiteDay) extra = isUr ? ' • ایامِ بیض کا مسنون روزہ' : ' • Sunnah Fast (Ayyam al-Beed)';
    else if(item.hMeta.isFriday) extra = isUr ? ' • مبارک جمعۃ المبارک' : ' • Blessed Jumu’ah';
    else if(item.dow === 1 || item.dow === 4) extra = isUr ? ' • پیر / جمعرات کا مسنون روزہ' : ' • Recommended Sunnah Fast Day';
    subEl.textContent = `${gregFmt}${extra}`;
  }
  if(bookBtn){
    bookBtn.innerHTML = isUr ? `اس مسنون تاریخ پر بکنگ کریں (${item.iso}) ←` : `Book Ruqyah on this Date (${item.iso}) →`;
  }
}

function bookFromInpageCalendar(){
  if(!SELECTED_INPAGE_HIJRI_DATE_ISO) return;
  if(typeof switchTab === 'function') switchTab('book');
  if(typeof selectDate === 'function'){
    selectDate(SELECTED_INPAGE_HIJRI_DATE_ISO);
  }
}

/* ================= @SKIPER-UI/SKIPER48 CARD SWIPE CAROUSEL ENGINE ================= */
var SKIPER_NAMES_DATA = window.ASMAUL_HUSNA_DATA || [];
var SKIPER_SWIPER_INSTANCE = null;
var SKIPER_ACTIVE_INDEX = 0;
var SKIPER_AUTOPLAY_ACTIVE = false;
var SKIPER_AUTO_VOICE = false;
var SKIPER_SPEED = 1.0;
var SKIPER_AUDIO_PLAYER = new Audio();
var SKIPER_PLAYING_INDEX = null;
var SKIPER_TASBEEH_COUNTS = {};

function formatDetailMarkdown(txt){
  if(!txt) return '';
  return txt
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .split('\n\n').join('<br><br>')
    .split('\n').join('<br>');
}

function initSkiperCarousel(){
  const deck = document.getElementById('skiperCardDeck');
  const jumpSel = document.getElementById('skiperJumpSelect');
  if(!deck) return;

  const data = window.ASMAUL_HUSNA_DATA || SKIPER_NAMES_DATA;
  if(!data || data.length === 0) return;
  SKIPER_NAMES_DATA = data;

  // Build Jump Dropdown options
  if(jumpSel){
    let optHtml = '';
    data.forEach((item, idx) => {
      optHtml += `<option value="${idx}">${idx + 1}. ${item.transliteration} (${item.arabic})</option>`;
    });
    jumpSel.innerHTML = optHtml;
  }

  // Build 99 Swiper Slides
  let slidesHtml = '';
  data.forEach((item, idx) => {
    const numPadded = String(idx + 1).padStart(2, '0');
    slidesHtml += `
      <div class="swiper-slide skiper-card-slide" id="skiperSlide_${idx}" data-index="${idx}">
        <div class="skiper-card-header">
          <span class="skiper-num-pill">№ ${numPadded}</span>
          <button type="button" class="skiper-voiceover-pill" id="skiperVoiceBtn_${idx}" onclick="toggleSkiperVoiceOver(${idx})" title="Listen to Voice-Over">
            <span class="sound-wave-anim" id="soundWaveAnim_${idx}">
              <span class="sound-wave-bar"></span>
              <span class="sound-wave-bar"></span>
              <span class="sound-wave-bar"></span>
              <span class="sound-wave-bar"></span>
            </span>
            <span id="skiperVoiceTxt_${idx}">Voice-Over</span>
          </button>
        </div>

        <div class="skiper-hero-name">
          <h2 class="skiper-arabic-title" dir="rtl">${item.arabic}</h2>
          <div class="skiper-translit-title">${item.transliteration}</div>
        </div>

        <div class="skiper-meanings-box">
          <div class="skiper-mean-row">
            <span class="skiper-flag-badge" style="font-size:0.72rem;font-weight:800;color:var(--gold-dark);background:var(--gold-light);padding:1px 6px;border-radius:4px;border:1px solid var(--gold-border);letter-spacing:0.04em;">EN</span>
            <div class="skiper-mean-en">
              <strong>${item.en.translated}:</strong> ${item.en.meaning}
            </div>
          </div>
          <div class="skiper-mean-row">
            <span class="skiper-flag-badge" style="font-size:0.72rem;font-weight:800;color:#1e6b37;background:rgba(30,107,55,0.12);padding:1px 6px;border-radius:4px;border:1px solid rgba(30,107,55,0.28);font-family:'Noto Nastaliq Urdu',serif;">اردو</span>
            <div class="skiper-mean-ur">
              <strong>${item.ur.translated}:</strong> ${item.ur.meaning}
            </div>
          </div>
        </div>

        <div class="skiper-virtues-wrap">
          <div class="skiper-tab-toggle">
            <button type="button" class="skiper-subtab-btn active" id="subtabBtnEn_${idx}" onclick="switchSkiperSubtab(${idx}, 'en')">English Reflection</button>
            <button type="button" class="skiper-subtab-btn" id="subtabBtnUr_${idx}" onclick="switchSkiperSubtab(${idx}, 'ur')">فضائل و برکات</button>
          </div>
          <div id="subtabContent_${idx}">
            ${formatDetailMarkdown(item.en.details || item.en.meaning)}
          </div>
        </div>

        <div class="skiper-tasbeeh-card-bar">
          <button type="button" class="skiper-tasbeeh-tap" onclick="tapSkiperTasbeeh(${idx})">
            <span>📿 Recite (${item.transliteration})</span>
            <span class="skiper-tasbeeh-count" id="tasbeehCount_${idx}">0</span>
          </button>
          <button type="button" class="skiper-tasbeeh-reset-btn" onclick="resetSkiperTasbeeh(${idx})" title="Reset Counter">↺</button>
        </div>
      </div>
    `;
  });

  deck.innerHTML = slidesHtml;

  // Initialize Swiper with effect: 'cards' (@skiper-ui/skiper48)
  try {
    if(typeof Swiper !== 'undefined'){
      if(SKIPER_SWIPER_INSTANCE){
        SKIPER_SWIPER_INSTANCE.destroy(true, true);
      }

      SKIPER_SWIPER_INSTANCE = new Swiper('.skiper48-swiper', {
        effect: 'cards',
        grabCursor: true,
        rewind: true,
        cardsEffect: {
          perSlideOffset: 12,
          perSlideRotate: 3,
          rotate: true,
          slideShadows: true,
        },
        keyboard: {
          enabled: true,
        },
        on: {
          slideChange: function(){
            const realIdx = this.realIndex;
            handleSkiperSlideChanged(realIdx);
          }
        }
      });
    }
  } catch(e) {
    console.warn('Swiper initialization:', e);
  }

  handleSkiperSlideChanged(0);
}

function handleSkiperSlideChanged(realIdx){
  SKIPER_ACTIVE_INDEX = realIdx;
  const total = SKIPER_NAMES_DATA.length || 99;

  // Counter
  const idxEl = document.getElementById('skiperCurrentIndex');
  if(idxEl) idxEl.textContent = String(realIdx + 1).padStart(2, '0');

  // Jump select
  const jumpSel = document.getElementById('skiperJumpSelect');
  if(jumpSel && jumpSel.value != realIdx){
    jumpSel.value = realIdx;
  }

  // Progress Bar
  const progFill = document.getElementById('skiperProgressFill');
  if(progFill){
    const pct = ((realIdx + 1) / total) * 100;
    progFill.style.width = `${pct}%`;
  }

  // Auto Voice-Over trigger if enabled
  if(SKIPER_AUTO_VOICE){
    playSkiperVoiceOver(realIdx);
  }
}

function nextSkiperSlide(){
  if(SKIPER_SWIPER_INSTANCE){
    SKIPER_SWIPER_INSTANCE.slideNext();
  } else {
    SKIPER_ACTIVE_INDEX = (SKIPER_ACTIVE_INDEX + 1) % 99;
    handleSkiperSlideChanged(SKIPER_ACTIVE_INDEX);
  }
}

function prevSkiperSlide(){
  if(SKIPER_SWIPER_INSTANCE){
    SKIPER_SWIPER_INSTANCE.slidePrev();
  } else {
    SKIPER_ACTIVE_INDEX = (SKIPER_ACTIVE_INDEX - 1 + 99) % 99;
    handleSkiperSlideChanged(SKIPER_ACTIVE_INDEX);
  }
}

function jumpToSkiperSlide(idx){
  if(SKIPER_SWIPER_INSTANCE){
    SKIPER_SWIPER_INSTANCE.slideToLoop(idx);
  } else {
    handleSkiperSlideChanged(idx);
  }
}

function pickRandomSkiperSlide(){
  const rand = Math.floor(Math.random() * (SKIPER_NAMES_DATA.length || 99));
  jumpToSkiperSlide(rand);
}

function toggleSkiperAutoplay(){
  SKIPER_AUTOPLAY_ACTIVE = !SKIPER_AUTOPLAY_ACTIVE;
  const btn = document.getElementById('skiperAutoplayBtn');
  const icon = document.getElementById('skiperAutoplayIcon');
  const txt = document.getElementById('skiperAutoplayText');
  const isUr = (typeof getAppLanguage === 'function' ? getAppLanguage() === 'ur' : (document.documentElement.lang === 'ur'));

  if(SKIPER_AUTOPLAY_ACTIVE){
    if(btn) btn.classList.add('active');
    if(icon) icon.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16" rx="1"></rect><rect x="14" y="4" width="4" height="16" rx="1"></rect></svg>';
    if(txt) txt.textContent = isUr ? 'روکیں' : 'Pause';
    startAutoplayLoop();
  } else {
    if(btn) btn.classList.remove('active');
    if(icon) icon.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
    if(txt) txt.textContent = isUr ? 'آٹو پلے' : 'Auto-Play';
    stopAutoplayLoop();
  }
}

var _skiperAutoplayInterval = null;
function startAutoplayLoop(){
  stopAutoplayLoop();
  _skiperAutoplayInterval = setInterval(() => {
    if(!SKIPER_AUDIO_PLAYER.paused) return; // Wait for voice-over to finish
    nextSkiperSlide();
  }, 4500);
}
function stopAutoplayLoop(){
  if(_skiperAutoplayInterval){
    clearInterval(_skiperAutoplayInterval);
    _skiperAutoplayInterval = null;
  }
}

function toggleAutoVoiceOver(){
  SKIPER_AUTO_VOICE = !SKIPER_AUTO_VOICE;
  const btn = document.getElementById('skiperAutoVoiceBtn');
  const icon = document.getElementById('skiperAutoVoiceIcon');
  const txt = document.getElementById('skiperAutoVoiceText');
  const isUr = (typeof getAppLanguage === 'function' ? getAppLanguage() === 'ur' : (document.documentElement.lang === 'ur'));

  if(SKIPER_AUTO_VOICE){
    if(btn) btn.classList.add('active');
    if(icon) icon.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>';
    if(txt) txt.textContent = isUr ? 'آٹو وائس: آن' : 'Auto Voice: ON';
    playSkiperVoiceOver(SKIPER_ACTIVE_INDEX);
  } else {
    if(btn) btn.classList.remove('active');
    if(icon) icon.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>';
    if(txt) txt.textContent = isUr ? 'آٹو وائس: آف' : 'Auto Voice: OFF';
    stopSkiperVoiceOver();
  }
}

function toggleAudioSpeed(){
  SKIPER_SPEED = (SKIPER_SPEED === 1.0) ? 0.8 : 1.0;
  const label = document.getElementById('skiperSpeedLabel');
  if(label) label.textContent = `${SKIPER_SPEED}x`;
  SKIPER_AUDIO_PLAYER.playbackRate = SKIPER_SPEED;
}

function switchSkiperSubtab(idx, lang){
  const item = SKIPER_NAMES_DATA[idx];
  if(!item) return;
  const btnEn = document.getElementById(`subtabBtnEn_${idx}`);
  const btnUr = document.getElementById(`subtabBtnUr_${idx}`);
  const content = document.getElementById(`subtabContent_${idx}`);

  if(lang === 'en'){
    btnEn?.classList.add('active');
    btnUr?.classList.remove('active');
    if(content){
      content.style.direction = 'ltr';
      content.style.textAlign = 'left';
      content.innerHTML = formatDetailMarkdown(item.en.details || item.en.meaning);
    }
  } else {
    btnUr?.classList.add('active');
    btnEn?.classList.remove('active');
    if(content){
      content.style.direction = 'rtl';
      content.style.textAlign = 'right';
      content.innerHTML = formatDetailMarkdown(item.ur.details || item.ur.meaning);
    }
  }
}

function tapSkiperTasbeeh(idx){
  SKIPER_TASBEEH_COUNTS[idx] = (SKIPER_TASBEEH_COUNTS[idx] || 0) + 1;
  const el = document.getElementById(`tasbeehCount_${idx}`);
  if(el) el.textContent = SKIPER_TASBEEH_COUNTS[idx];
  try { if(navigator.vibrate) navigator.vibrate(12); } catch(e){}
}

function resetSkiperTasbeeh(idx){
  SKIPER_TASBEEH_COUNTS[idx] = 0;
  const el = document.getElementById(`tasbeehCount_${idx}`);
  if(el) el.textContent = '0';
}

function toggleSkiperVoiceOver(idx){
  if(SKIPER_PLAYING_INDEX === idx){
    stopSkiperVoiceOver();
  } else {
    playSkiperVoiceOver(idx);
  }
}

function playSkiperVoiceOver(idx){
  const item = SKIPER_NAMES_DATA[idx];
  if(!item) return;

  stopSkiperVoiceOver();
  SKIPER_PLAYING_INDEX = idx;

  const btn = document.getElementById(`skiperVoiceBtn_${idx}`);
  const anim = document.getElementById(`soundWaveAnim_${idx}`);
  const txt = document.getElementById(`skiperVoiceTxt_${idx}`);

  if(btn) btn.classList.add('playing');
  if(anim) anim.classList.add('active');
  if(txt) txt.textContent = 'Playing...';

  SKIPER_AUDIO_PLAYER.src = item.audio_url;
  SKIPER_AUDIO_PLAYER.playbackRate = SKIPER_SPEED;

  const playPromise = SKIPER_AUDIO_PLAYER.play();
  if(playPromise !== undefined){
    playPromise.catch(err => {
      if('speechSynthesis' in window){
        window.speechSynthesis.cancel();
        const ut = new SpeechSynthesisUtterance(item.arabic);
        ut.lang = 'ar-SA';
        ut.rate = SKIPER_SPEED;
        ut.onend = () => stopSkiperVoiceOver();
        ut.onerror = () => stopSkiperVoiceOver();
        window.speechSynthesis.speak(ut);
      } else {
        stopSkiperVoiceOver();
      }
    });
  }

  SKIPER_AUDIO_PLAYER.onended = () => {
    stopSkiperVoiceOver();
  };
}

function stopSkiperVoiceOver(){
  try {
    SKIPER_AUDIO_PLAYER.pause();
    SKIPER_AUDIO_PLAYER.currentTime = 0;
  } catch(e){}
  if('speechSynthesis' in window){
    window.speechSynthesis.cancel();
  }
  if(SKIPER_PLAYING_INDEX !== null){
    const btn = document.getElementById(`skiperVoiceBtn_${SKIPER_PLAYING_INDEX}`);
    const anim = document.getElementById(`soundWaveAnim_${SKIPER_PLAYING_INDEX}`);
    const txt = document.getElementById(`skiperVoiceTxt_${SKIPER_PLAYING_INDEX}`);
    if(btn) btn.classList.remove('playing');
    if(anim) anim.classList.remove('active');
    if(txt) txt.textContent = 'Voice-Over';
  }
  SKIPER_PLAYING_INDEX = null;
}

// Auto-initialize when DOM is ready
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      initSkiperCarousel();
      renderInPageHijriCalendar();
      updateLiveIslamicHeaderClock();
    }, 200);
  });
} else {
  setTimeout(() => {
    initSkiperCarousel();
    renderInPageHijriCalendar();
    updateLiveIslamicHeaderClock();
  }, 200);
}

// Hook into existing APP_I18N dictionary if present
if(window.APP_I18N && window.APP_I18N.dict){
  if(window.APP_I18N.dict.en){
    window.APP_I18N.dict.en.tab_book = 'Book';
    window.APP_I18N.dict.en.tab_tracker = 'Appointments';
    window.APP_I18N.dict.en.tab_profile = 'Adhkar';
  }
  if(window.APP_I18N.dict.ur){
    window.APP_I18N.dict.ur.tab_book = 'بکنگ';
    window.APP_I18N.dict.ur.tab_tracker = 'اپائنٹمنٹس';
    window.APP_I18N.dict.ur.tab_profile = 'اذکار';
  }

  const enAdd = {
    tab_names: '99 Names',
    tab_calendar: 'Hijri Cal',
    m_tab_names: '99 Names',
    m_tab_calendar: 'Hijri',
    names_view_title: 'الأَسْمَاءُ الْحُسْنَىٰ • 99 Beautiful Names of Allah',
    names_view_sub: 'Swipe through the divine attributes in @skiper-ui/skiper48 3D stack format. Listen to authentic voice-overs, study bilingual translations, and recite with integrated Tasbeeh.',
    cal_view_title: 'التقويم الهجري الإسلامي • Islamic Hijri Calendar',
    cal_view_sub: 'Explore Sunnah fasting days (Ayyam al-Beed), moon sighting adjustments, and sacred Islamic months with direct appointment scheduling.',
    btn_view_hijri_cal: 'Hijri Calendar',
    btn_view_99_names: '99 Names of Allah',
    qfc_names_title: '99 Names of Allah',
    qfc_names_sub: '@skiper-ui/skiper48 3D swipe cards with authentic voice-overs, bilingual reflections & Tasbeeh.',
    qfc_cal_title: 'Islamic Hijri Calendar',
    qfc_cal_sub: 'Umm al-Qura moon phases, Ayyam al-Beed Sunnah fast days & instant session booking.',
    qfc_book_title: "Book Ruqyah Shari'ah",
    qfc_book_sub: 'Schedule 1-on-1 direct appointment with Islamic Hijri & Gregorian alignment.',
    skiper_random: 'Random Name',
    skiper_auto_voice: 'Auto Voice-Over: OFF',
    skiper_autoplay: 'Auto-Play',
    lbl_current_view: 'Viewing Month:',
    lbl_moon_adjust: 'Moon Sighting Adjustment:',
    btn_book_on_this_date: 'Book Ruqyah on this Date →'
  };

  const urAdd = {
    tab_names: '۹۹ اسمائے حسنیٰ',
    tab_calendar: 'ہجری کیلنڈر',
    m_tab_names: 'اسمائے حسنیٰ',
    m_tab_calendar: 'ہجری',
    names_view_title: 'الأَسْمَاءُ الْحُسْنَىٰ • اللہ تعالیٰ کے ۹۹ مبارک نام',
    names_view_sub: 'اللہ تعالیٰ کے اسمائے حسنیٰ کو تھری ڈی سوائپ کارڈز کے ذریعے دریافت کریں۔ مستند صوتی تلاوت سنیں اور تسبیح کاؤنٹر سے ذکر کریں۔',
    cal_view_title: 'التقويم الهجري الإسلامي • اسلامی ہجری کیلنڈر',
    cal_view_sub: 'ایامِ بیض کے مسنون روزے، چاند کی رویت اور اہم اسلامی تاریخوں کے ساتھ براہِ راست سیشن بکنگ کریں۔',
    btn_view_hijri_cal: 'ہجری کیلنڈر',
    btn_view_99_names: '۹۹ اسمائے حسنیٰ',
    qfc_names_title: '۹۹ اسمائے حسنیٰ',
    qfc_names_sub: '@skiper-ui/skiper48 تھری ڈی کارڈز، مستند آواز، اردو ترجمہ اور تسبیح۔',
    qfc_cal_title: 'اسلامی ہجری کیلنڈر',
    qfc_cal_sub: 'ام القریٰ نظام، ایامِ بیض کے روزے اور مسنون تاریخوں پر فوری بکنگ۔',
    qfc_book_title: 'شرعی رقیہ سیشن بک کریں',
    qfc_book_sub: 'ہجری اور عیسوی تاریخوں کی مطابقت کے ساتھ اپنا سیشن بک کروائیں۔',
    skiper_random: 'کوئی ایک نام منتخب کریں',
    skiper_auto_voice: 'آٹو وائس: آف',
    skiper_autoplay: 'آٹو پلے',
    lbl_current_view: 'موجودہ مہینہ:',
    lbl_moon_adjust: 'چاند رویت ایڈجسٹمنٹ:',
    btn_book_on_this_date: 'اس مسنون تاریخ پر بکنگ کریں ←'
  };

  Object.assign(window.APP_I18N.dict.en, enAdd);
  Object.assign(window.APP_I18N.dict.ur, urAdd);
}

// Hook into switchTab to update swiper & calendar dimensions
const _origSwitchTab = window.switchTab;
if(typeof _origSwitchTab === 'function'){
  window.switchTab = function(tabId){
    _origSwitchTab(tabId);
    if(tabId === 'names'){
      setTimeout(() => {
        if(SKIPER_SWIPER_INSTANCE){
          SKIPER_SWIPER_INSTANCE.update();
        }
      }, 50);
    } else if(tabId === 'calendar'){
      renderInPageHijriCalendar();
    }
  };
}
