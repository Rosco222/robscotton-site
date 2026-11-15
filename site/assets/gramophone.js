/* Russell's gramophone: plays a song, spins the record, puffs notes out of the horn and rolls the words. */
(function () {
  var root = document.getElementById('gp');
  if (!root) return;
  var SONGS = JSON.parse(document.getElementById('gp-data').textContent);
  var $ = function (id) { return document.getElementById(id); };
  var audio = $('gp-audio'), stage = $('gp-stage'), svg = $('gram'), notesBox = $('gp-notes');
  var linesBox = $('gp-lines'), range = $('gp-range'), cur = $('gp-cur'), dur = $('gp-dur');
  var el = { record: $('g-record'), wobble: $('g-wobble'), arm: $('g-arm'), horn: $('g-horn'), machine: $('g-machine'),
    cogA: $('cog-a'), cogB: $('cog-b'), cogC: $('cog-c'), crank: $('g-crank'), needle: $('needle'), rays: $('rays-spin'),
    spring: $('g-spring'), frankie: $('gp-frankie'), bulbs: [$('bulb-1'), $('bulb-2'), $('bulb-3')] };
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var song = null, songIdx = 0, lineEls = [], timed = false, activeLine = -1;
  var dragging = false;

  function fmt(s) { s = Math.max(0, Math.floor(s || 0)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }

  /* ---------- songs ---------- */
  function load(i, autoplay) {
    songIdx = (i + SONGS.length) % SONGS.length; song = SONGS[songIdx];
    audio.src = song.src; audio.load();
    root.setAttribute('data-theme', song.theme);
    var tc = document.querySelector('meta[name="theme-color"]'); if (tc) tc.content = song.theme === 'night' ? '#0B1733' : '#F6B51F';
    $('gp-kicker').textContent = song.kicker; $('gp-title').textContent = song.title;
    document.title = song.title + ' | Russell’s gramophone | Rob Scotton';
    $('label-img').setAttribute('href', song.cover); $('gp-cover').src = song.cover; $('gp-cover').alt = 'Cover art for ' + song.title;
    $('gp-credits').textContent = song.credits;
    Array.prototype.forEach.call(document.querySelectorAll('.sleeve'), function (b) { b.setAttribute('aria-pressed', b.dataset.song === song.id ? 'true' : 'false'); });
    renderLines();
    range.value = 0; range.style.setProperty('--p', '0%'); cur.textContent = '0:00'; dur.textContent = '0:00';
    try { history.replaceState(null, '', location.pathname + '?song=' + song.id); } catch (e) {}
    if ('mediaSession' in navigator && window.MediaMetadata) {
      navigator.mediaSession.metadata = new MediaMetadata({ title: song.title, artist: song.by, artwork: [{ src: song.cover }] });
    }
    if (autoplay) play();
  }

  var seq = [], rollEls = [], secEl = $('gp-sec'), threeIn = $('gp-three-in'), strip = $('gp-strip');
  function renderLines() {
    linesBox.textContent = ''; lineEls = []; seq = []; activeLine = -2;
    timed = song.lines.some(function (l) { return l.t != null; });
    linesBox.classList.toggle('timed', timed);
    var sec = '';
    song.lines.forEach(function (l) {
      var p = document.createElement('p');
      if (l.h) { p.className = 'h'; p.textContent = l.h; sec = l.h; }
      else { p.textContent = l.x; lineEls.push(p); seq.push({ x: l.x, t: l.t, sec: sec, el: p }); p.dataset.i = seq.length - 1; }
      linesBox.appendChild(p);
    });
    // the rolling strip: a note to start with, then every line of the song
    strip.textContent = ''; rollEls = [];
    [{ x: '\u266A' }].concat(seq).forEach(function (l) { var r = document.createElement('p'); r.textContent = l.x; strip.appendChild(r); rollEls.push(r); });
    strip.style.transition = 'none'; roll(-1); strip.offsetHeight; strip.style.transition = '';
    estimate();
  }
  // roll the strip so the line being sung sits in the middle of the window
  function roll(idx) {
    var k = idx + 1;
    rollEls.forEach(function (r, i) { r.className = i === k ? 'now' : i === k - 1 ? 'past' : i === k + 1 ? 'next' : i < k ? 'gone' : ''; });
    var r = rollEls[k]; if (!r) return;
    strip.style.transform = 'translateY(' + (threeIn.clientHeight / 2 - r.offsetTop - r.offsetHeight / 2).toFixed(1) + 'px)';
  }
  window.addEventListener('resize', function () { roll(activeLine < -1 ? -1 : activeLine); });
  // a song with no line times yet: spread the lines over the song by their length, so the words still keep pace
  function estimate() {
    if (timed || !seq.length) return;
    var d = audio.duration; if (!d || !isFinite(d)) return;
    var lead = Math.min(12, d * 0.05), tail = Math.min(16, d * 0.06), total = 0, acc = 0;
    var w = seq.map(function (l, i) { var k = 8 + l.x.length + (i && seq[i - 1].sec !== l.sec ? 14 : 0); total += k; return k; });
    seq.forEach(function (l, i) { l.t = lead + (d - lead - tail) * acc / total; acc += w[i]; });
    activeLine = -2;
  }
  audio.addEventListener('loadedmetadata', estimate);

  linesBox.addEventListener('click', function (e) {
    var p = e.target.closest('p[data-i]'); if (!p) return;
    var l = seq[+p.dataset.i]; if (l.t == null) return;
    audio.currentTime = Math.max(0, l.t - 0.15); play();
  });

  function syncLines(t) {
    var idx = -1;
    for (var i = 0; i < seq.length; i++) { if (seq[i].t != null && seq[i].t <= t + 0.05) idx = i; else break; }
    if (idx === activeLine) return;
    activeLine = idx;
    roll(idx);
    secEl.textContent = idx >= 0 && seq[idx].sec ? seq[idx].sec : 'Sing along';
    lineEls.forEach(function (p, i) { p.classList.toggle('on', i === idx); });
    if (idx >= 0 && $('gp-dlg-lyrics').open) centre(seq[idx].el, !calm);
  }

  /* ---------- pop-ups: full lyrics and credits ---------- */
  function centre(p, smooth) {
    var top = Math.max(0, p.offsetTop - linesBox.offsetTop - linesBox.clientHeight / 2 + p.offsetHeight / 2);
    if (smooth && linesBox.scrollTo) linesBox.scrollTo({ top: top, behavior: 'smooth' }); else linesBox.scrollTop = top;
  }
  function openDlg(d) { if (d.showModal) d.showModal(); else d.setAttribute('open', ''); if (d.id === 'gp-dlg-lyrics' && activeLine >= 0) centre(seq[activeLine].el, false); }
  $('gp-open-lyrics').addEventListener('click', function () { openDlg($('gp-dlg-lyrics')); });
  $('gp-open-credits').addEventListener('click', function () { openDlg($('gp-dlg-credits')); });
  Array.prototype.forEach.call(document.querySelectorAll('.gp-dlg'), function (d) {
    d.addEventListener('click', function (e) { if (e.target === d || e.target.closest('[data-close]')) { if (d.close) d.close(); else d.removeAttribute('open'); } });
  });

  /* ---------- transport ---------- */
  function play() { root.classList.add('started'); var p = audio.play(); if (p && p.catch) p.catch(function () { root.classList.remove('started'); }); }
  function toggle() { if (audio.paused) play(); else audio.pause(); }
  $('gp-play').addEventListener('click', toggle);
  $('gp-bigplay').addEventListener('click', play);
  $('gp-start').addEventListener('click', function () { audio.currentTime = 0; });
  $('gp-back').addEventListener('click', function () { audio.currentTime = Math.max(0, audio.currentTime - 10); });
  $('gp-fwd').addEventListener('click', function () { if (audio.duration) audio.currentTime = Math.min(audio.duration - 0.2, audio.currentTime + 10); });
  $('gp-next').addEventListener('click', function () { load(songIdx + 1, true); });
  Array.prototype.forEach.call(document.querySelectorAll('.sleeve'), function (b) {
    b.addEventListener('click', function () {
      var i = SONGS.findIndex(function (s) { return s.id === b.dataset.song; });
      if (i === songIdx) toggle(); else load(i, true);
    });
  });
  audio.addEventListener('play', function () { root.classList.add('playing', 'started'); $('gp-play').setAttribute('aria-label', 'Pause'); });
  audio.addEventListener('pause', function () { root.classList.remove('playing'); $('gp-play').setAttribute('aria-label', 'Play'); });
  audio.addEventListener('ended', function () { root.classList.remove('playing'); });
  audio.addEventListener('loadedmetadata', function () { dur.textContent = fmt(audio.duration); });
  range.addEventListener('input', function () {
    dragging = true; range.style.setProperty('--p', (range.value / 10) + '%');
    if (audio.duration) cur.textContent = fmt(range.value / 1000 * audio.duration);
  });
  range.addEventListener('change', function () { if (audio.duration) audio.currentTime = range.value / 1000 * audio.duration; dragging = false; });
  document.addEventListener('keydown', function (e) {
    if (e.code !== 'Space' || /^(BUTTON|INPUT|A|TEXTAREA|SELECT)$/.test((e.target.tagName || ''))) return;
    e.preventDefault(); toggle();
  });

  /* ---------- how loud is the music right now? (worked out when the site was built) ---------- */
  function level(t) {
    var env = song && song.env; if (!env) return 0.5;
    var x = t * 20, i = Math.floor(x), f = x - i;
    var a = parseInt(env.charAt(Math.min(env.length - 1, i)) || '0', 36), b = parseInt(env.charAt(Math.min(env.length - 1, i + 1)) || '0', 36);
    return (a + (b - a) * f) / 35;
  }

  /* ---------- notes out of the horn ---------- */
  var SHAPES = [
    '<svg viewBox="0 0 24 32"><path d="M9 24.5V3.5L21 1v6l-9 2v15.5a5.2 4.2 0 1 1-3-.9z" fill="currentColor"/></svg>',
    '<svg viewBox="0 0 32 32"><path d="M8 25V6l20-4v19a5 4 0 1 1-3-.9V9.5L11 12.4V25a5 4 0 1 1-3-.9z" fill="currentColor"/></svg>',
    '<svg viewBox="0 0 24 32"><path d="M10 24.5V2c3 3.5 10 5 9 12-1-3.5-4.5-5-6-5.4v15.9a5.2 4.2 0 1 1-3-.9z" fill="currentColor"/></svg>'
  ];
  var STAR = '<svg viewBox="0 0 24 24"><path d="M12 1l3.2 7 7.6.8-5.7 5.1 1.7 7.5L12 17.500l-6.800 3.900 1.700-7.500L1.200 8.800l7.600-.8z" fill="currentColor"/></svg>';
  var PAL = { day: ['#6A3A94', '#1B1A1F', '#E3262E', '#0F7A77', '#fff'], night: ['#FFD34D', '#8ED0E8', '#fff', '#F7A8C8', '#9FE3DD'] };
  var live = 0, spawnDebt = 0, mouth = (el.horn.getAttribute('data-mouth') || '588 206').split(' ').map(Number);
  function spawn(kick) {
    if (calm || live > 46 || !notesBox.animate) return;
    var r = stage.getBoundingClientRect(), k = r.width / 800;
    var x0 = mouth[0] * k, y0 = (mouth[1] - 20) * k;
    var n = document.createElement('i'), roll = Math.random();
    var pal = PAL[song.theme] || PAL.day;
    n.style.color = pal[Math.floor(Math.random() * pal.length)];
    if (roll < 0.1) n.innerHTML = STAR;
    else if (roll < 0.17 && song.theme === 'night') n.textContent = 'z';
    else n.innerHTML = SHAPES[Math.floor(Math.random() * SHAPES.length)];
    var size = (20 + Math.random() * 26) * Math.max(0.62, k) * (kick ? 1.25 : 1);
    n.style.fontSize = size + 'px';
    notesBox.appendChild(n); live++;
    var ang = (-150 + Math.random() * 135) * Math.PI / 180;
    var dist = (190 + Math.random() * 330) * Math.max(0.6, k) * (kick ? 1.2 : 1);
    var dx = Math.cos(ang) * dist, dy = Math.sin(ang) * dist - 60 * k;
    var sway = (Math.random() - 0.5) * 110 * k, rot = (Math.random() - 0.5) * 80;
    var sx = x0 + (Math.random() - 0.5) * 60 * k - size / 2, sy = y0 + (Math.random() - 0.5) * 40 * k - size / 2;
    function tf(px, py, s, rr) { return 'translate(' + px + 'px,' + py + 'px) scale(' + s + ') rotate(' + rr + 'deg)'; }
    var a = n.animate([
      { transform: tf(sx, sy, 0.15, -rot), opacity: 0, offset: 0 },
      { transform: tf(sx + dx * 0.18, sy + dy * 0.2, 1.15, rot * 0.4), opacity: 1, offset: 0.14 },
      { transform: tf(sx + dx * 0.5 + sway, sy + dy * 0.55, 1, -rot * 0.5), opacity: 1, offset: 0.5 },
      { transform: tf(sx + dx * 0.8 - sway * 0.6, sy + dy * 0.85, 0.95, rot * 0.7), opacity: 0.8, offset: 0.8 },
      { transform: tf(sx + dx, sy + dy, 0.7, rot), opacity: 0, offset: 1 }
    ], { duration: 2300 + Math.random() * 1700, easing: 'cubic-bezier(.2,.6,.3,1)', fill: 'forwards' });
    a.onfinish = a.oncancel = function () { n.remove(); live--; };
  }

  /* ---------- the motion ---------- */
  function rot(node, deg, x, y) { node.setAttribute('transform', 'rotate(' + deg.toFixed(2) + (x != null ? ' ' + x + ' ' + y : '') + ')'); }
  var pivot = el.horn.getAttribute('data-pivot') || '562 436', pivotBack = pivot.split(' ').map(function (v) { return -v; }).join(' ');
  var last = performance.now(), ang = 0, spin = 0, arm = -32, lvl = 0, slow = 0, kickV = 0, rays = 0, crank = 0, cog = 0, clock = 0;
  function frame(now) {
    var dt = Math.min(0.05, (now - last) / 1000); last = now; clock += dt;
    var playing = !audio.paused && !audio.ended, t = audio.currentTime || 0, d = audio.duration || 0;

    var raw = playing ? level(t) : 0;
    lvl += (raw - lvl) * Math.min(1, dt * 14);
    slow += (raw - slow) * Math.min(1, dt * 1.6);
    var kick = playing && raw > slow * 1.22 + 0.06 && kickV < 0.25;
    if (kick) kickV = 1;
    kickV = Math.max(0, kickV - dt * 4.5);

    // record: eases up to speed and coasts to a stop
    spin += ((playing ? 200 : 0) - spin) * Math.min(1, dt * (playing ? 2.2 : 1.1));
    ang = (ang + spin * dt) % 360;
    rot(el.record, ang);
    if (!calm) el.wobble.setAttribute('transform', 'translate(0 ' + (Math.sin(ang * Math.PI / 180) * 1.3 * (spin / 200)).toFixed(2) + ')');

    // arm: swings on, creeps inwards through the song, lifts off when stopped
    var prog = d ? t / d : 0, target = playing ? 4 - 9 * prog + Math.sin(ang * Math.PI / 180) * 0.5 : (t > 0.2 && !audio.ended ? -10 : -32);
    arm += (target - arm) * Math.min(1, dt * 3.2);
    rot(el.arm, arm);

    if (!calm) {
      var pulse = 1 + lvl * 0.035 + kickV * 0.035;
      el.horn.setAttribute('transform', 'translate(' + pivot + ') rotate(' + (Math.sin(clock * 5.2) * lvl * 1.4 - kickV * 1.2).toFixed(2) + ') scale(' + pulse.toFixed(4) + ') translate(' + pivotBack + ')');
      var bounce = lvl * 3 + kickV * 4;
      el.machine.setAttribute('transform', 'translate(0 ' + (-bounce).toFixed(2) + ')');
      el.spring.setAttribute('transform', 'translate(0 612) scale(1 ' + (1 + bounce / 56).toFixed(3) + ') translate(0 -612)');
      el.frankie.style.transform = 'translateY(' + (-kickV * 16 - lvl * 5).toFixed(1) + 'px) rotate(' + (Math.sin(clock * 4) * lvl * 7).toFixed(1) + 'deg) scaleY(' + (1 - kickV * 0.05).toFixed(3) + ')';
      rays += dt * (4 + spin * 0.08 + lvl * 14); rot(el.rays, rays % 360);
    }
    cog += spin * dt * 0.6; rot(el.cogA, cog); rot(el.cogB, -cog * 1.5 + 12); rot(el.cogC, -cog * 2 + 8);
    crank += spin * dt * 1.4; rot(el.crank, crank % 360);
    rot(el.needle, -105 + lvl * 190 + (playing ? Math.sin(clock * 31) * 3 : 0));
    el.bulbs.forEach(function (b, i) { b.style.opacity = (0.3 + Math.max(0, Math.min(1, lvl * 1.7 - i * 0.3)) * 0.7).toFixed(2); });

    if (playing) {
      spawnDebt += dt * (1.6 + lvl * 9);
      while (spawnDebt >= 1) { spawnDebt -= 1; spawn(false); }
      if (kick) { spawn(true); spawn(true); }
    }

    // time, bar and words
    if (d && !dragging) { range.value = Math.round(t / d * 1000); range.style.setProperty('--p', (t / d * 100) + '%'); cur.textContent = fmt(t); }
    syncLines(t);
    requestAnimationFrame(frame);
  }

  /* ---------- stars for Russell's night ---------- */
  (function () {
    var box = $('gp-stars'), h = '';
    for (var i = 0; i < 46; i++) {
      var s = 1 + Math.random() * 2.4;
      h += '<i style="left:' + (Math.random() * 100).toFixed(1) + '%;top:' + (Math.random() * 62).toFixed(1) + '%;width:' + s.toFixed(1) + 'px;height:' + s.toFixed(1) + 'px;animation-delay:-' + (Math.random() * 3).toFixed(2) + 's;animation-duration:' + (2 + Math.random() * 3).toFixed(1) + 's"></i>';
    }
    box.innerHTML = h;
  })();

  var q = new URLSearchParams(location.search), want = q.get('song') || (location.hash || '').slice(1);
  var start = Math.max(0, SONGS.findIndex(function (s) { return s.id === want; }));
  load(start, false);
  if (q.get('play')) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
  requestAnimationFrame(frame);
})();
