"""Russell's gramophone: the song player page (gramophone.html).

build.py calls page(SONGS) for the page body. Lyrics live in tools/lyrics/<song-id>.txt:
  [Verse 1], [Chorus], [Bridge]... become small headings; other [notes] are hidden.
  A time in front of a line, [0:21.5], makes that line light up as it is sung.
"""
import json, math, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
HEAD_RE = re.compile(r'^(Verse|Chorus|Final Chorus|Pre-Chorus|Bridge|Intro|Outro|Refrain)\b', re.I)

def lyrics(song_id):
    out = []
    for raw in open(os.path.join(HERE, 'lyrics', song_id + '.txt'), encoding='utf-8').read().strip().split('\n'):
        line = raw.strip()
        if not line:
            continue
        m = re.match(r'^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$', line)
        if m:
            out.append({'t': round(int(m.group(1)) * 60 + float(m.group(2)), 2), 'x': m.group(3)})
        elif line.startswith('['):
            name = line.strip('[]')
            if HEAD_RE.match(name):
                out.append({'h': name})
        else:
            out.append({'x': line})
    # drop headings with no words under them (e.g. an instrumental intro)
    return [l for i, l in enumerate(out) if 'x' in l or (i + 1 < len(out) and 'x' in out[i + 1])]

def cog(r, teeth, depth=7, hole=6):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r if i % 4 in (0, 1) else r - depth
        pts.append(f"{rr * math.cos(a):.1f},{rr * math.sin(a):.1f}")
    spokes = ''.join(f'<rect x="-2.2" y="{-(r - depth - 3):.1f}" width="4.4" height="{2 * (r - depth - 3):.1f}" transform="rotate({k * 60})" fill="#0003"/>' for k in range(3))
    return (f'<polygon points="{" ".join(pts)}"/><circle r="{r - depth - 4:.1f}" fill="#0002"/>{spokes}'
            f'<circle r="{hole + 4}" fill="#3a2a1a"/><circle r="{hole}" fill="#d9c9a8"/>')

def rivets(points, r=3.2):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6b4a12"/><circle cx="{x - .8}" cy="{y - .9}" r="{r * .45:.1f}" fill="#ffe9a8"/>' for x, y in points)

RAYS = ''.join(f'<path d="M0 0L{620 * math.cos(math.radians(a - 7)):.0f} {620 * math.sin(math.radians(a - 7)):.0f}L{620 * math.cos(math.radians(a + 7)):.0f} {620 * math.sin(math.radians(a + 7)):.0f}Z"/>' for a in range(0, 360, 30))
GROOVES = ''.join(f'<circle r="{r}" fill="none" stroke="{"#3a3a40" if i % 3 else "#55555c"}" stroke-width="{1.4 if i % 3 else 2.2}"/>' for i, r in enumerate(range(78, 166, 8)))

SVG = '''<svg class="gram" id="gram" viewBox="0 20 800 680" role="img" aria-label="A home-made gramophone, built by Russell the Sheep, with a spinning record and a big patched brass horn">
<defs>
  <linearGradient id="g-brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE48A"/><stop offset=".45" stop-color="#E0A93A"/><stop offset="1" stop-color="#8E5E17"/></linearGradient>
  <linearGradient id="g-brass2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E5E17"/><stop offset=".4" stop-color="#F3C55A"/><stop offset=".62" stop-color="#FFE9A0"/><stop offset="1" stop-color="#9A6619"/></linearGradient>
  <linearGradient id="g-copper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0A27A"/><stop offset="1" stop-color="#9C4A26"/></linearGradient>
  <radialGradient id="g-bell" cx=".46" cy=".56" r=".62"><stop offset="0" stop-color="#1b0f06"/><stop offset=".42" stop-color="#5a3510"/><stop offset=".8" stop-color="#C98E2C"/><stop offset="1" stop-color="#FFE08A"/></radialGradient>
  <linearGradient id="g-wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98B50"/><stop offset="1" stop-color="#8A5429"/></linearGradient>
  <linearGradient id="g-wood2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9703A"/><stop offset="1" stop-color="#6F411D"/></linearGradient>
  <linearGradient id="g-steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E6EAEE"/><stop offset="1" stop-color="#7C8894"/></linearGradient>
  <radialGradient id="g-vinyl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#2a2a30"/><stop offset=".7" stop-color="#141418"/><stop offset="1" stop-color="#26262c"/></radialGradient>
  <radialGradient id="g-bulb" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFFBE0"/><stop offset=".5" stop-color="#FFD34D"/><stop offset="1" stop-color="#E08A1A"/></radialGradient>
  <clipPath id="c-label"><circle r="62"/></clipPath>
  <clipPath id="c-horn"><path d="M546 436C530 380 440 340 430 258L750 142C740 300 610 370 578 436Z"/></clipPath>
  <clipPath id="c-bell"><ellipse rx="150" ry="121"/></clipPath>
  <clipPath id="c-crate"><rect x="150" y="446" width="452" height="170" rx="8"/></clipPath>
</defs>

<g class="rays" id="g-rays" transform="translate(400 360)"><g id="rays-spin">__RAYS__</g></g>
<ellipse class="floor" cx="392" cy="676" rx="318" ry="20"/>

<g id="g-machine">
  <!-- chimney pipe and steam -->
  <g class="pipe">
    <path d="M176 520H118q-20 0-20-20V372" fill="none" stroke="#6b7682" stroke-width="20" stroke-linecap="round"/>
    <path d="M176 520H118q-20 0-20-20V372" fill="none" stroke="#b9c3cc" stroke-width="7" stroke-linecap="round" transform="translate(-3 -2)" opacity=".55"/>
    <rect x="82" y="356" width="32" height="18" rx="4" fill="#4c5661"/>
    <rect x="88" y="430" width="20" height="9" fill="#4c5661"/><rect x="134" y="510" width="9" height="20" fill="#4c5661"/>
  </g>
  <g class="steam" aria-hidden="true"><circle cx="98" cy="346" r="11"/><circle cx="98" cy="346" r="9"/><circle cx="98" cy="346" r="12"/></g>

  <!-- legs: one proper, one spring, one stack of books -->
  <rect x="176" y="610" width="24" height="56" rx="4" fill="url(#g-wood2)"/>
  <g id="g-spring"><path d="M548 612l28 7-28 7 28 7-28 7 28 7-28 7 28 7" fill="none" stroke="#8a95a1" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>
  <g><rect x="352" y="646" width="78" height="16" rx="3" fill="#1FA7A3"/><rect x="358" y="630" width="70" height="16" rx="3" fill="#E3262E"/><rect x="350" y="614" width="80" height="16" rx="3" fill="#6A3A94"/><rect x="356" y="650" width="26" height="4" fill="#fff8" /><rect x="364" y="634" width="20" height="4" fill="#fff8"/></g>

  <!-- the horn -->
  <g id="g-horn">
    <path d="M546 436C530 380 440 340 430 258L750 142C740 300 610 370 578 436Z" fill="url(#g-brass2)"/>
    <g clip-path="url(#c-horn)">
      __SEAMS__
      <path d="M452 372L640 300L652 350L486 410Z" fill="url(#g-copper)"/>
      <path d="M560 338l66-26 10 30-64 26z" fill="#3E7E7A"/>
      <path d="M560 338l66-26 10 30-64 26z" fill="none" stroke="#fff8" stroke-width="2" stroke-dasharray="5 5"/>
      <path d="M520 404L600 380L608 408L530 440Z" fill="#B9C3CC"/>
      <path d="M430 258C440 340 530 380 546 436" fill="none" stroke="#5c3b0c" stroke-width="6" opacity=".45"/>
    </g>
    __RIVETS__
    <g transform="translate(590 200) rotate(-20)">
      <path d="__SCALLOP__" fill="url(#g-brass)" stroke="#7a4f10" stroke-width="3" stroke-linejoin="round"/>
      <ellipse rx="150" ry="121" fill="url(#g-bell)"/>
      <g clip-path="url(#c-bell)">__PETALS__</g>
      <ellipse rx="150" ry="121" fill="none" stroke="#7a4f10" stroke-opacity=".5" stroke-width="2"/>
      <ellipse cx="-8" cy="14" rx="30" ry="24" fill="#0b0603"/>
      <path d="M-128 -52Q-70 -116 30 -112" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".5"/>
      <g transform="translate(142 62) rotate(58)"><rect x="-23" y="-8" width="46" height="16" rx="8" fill="#F2C9A0"/><rect x="-8" y="-8" width="16" height="16" fill="#E2A979"/></g>
    </g>
    <!-- Russell's nightcap, left on the horn -->
    <g transform="translate(-62 50)"><g class="cap" id="g-cap">
      <path d="M498 214c-34 6-62 44-66 96 12 6 22 6 30 0 0-36 16-62 46-74z" fill="#F4F7FB"/>
      <path d="M487 219c-10 6-19 14-26 25l22 13c6-10 14-17 24-22zM447 268c-5 9-8 19-10 30l25 5c1-9 4-17 8-25z" fill="#5B79C9"/>
      <circle cx="447" cy="318" r="13" fill="#F4F7FB"/>
    </g></g>
    <rect x="538" y="424" width="48" height="22" rx="6" fill="#6b4a12"/><rect x="538" y="424" width="48" height="7" rx="3.5" fill="#F3C55A"/>
  </g>

  <!-- tea-chest body -->
  <rect x="150" y="446" width="452" height="170" rx="8" fill="url(#g-wood)"/>
  <g clip-path="url(#c-crate)">
    <path d="M150 502H602M150 560H602" stroke="#6F411D" stroke-width="3" opacity=".55"/>
    <path d="M300 446V502M452 502V560M244 560V616M520 560V616" stroke="#6F411D" stroke-width="3" opacity=".4"/>
    <rect x="150" y="446" width="452" height="12" fill="#fff" opacity=".14"/>
    <g transform="rotate(-4 452 590)"><rect x="392" y="570" width="124" height="38" rx="3" fill="#D9A566"/><circle cx="399" cy="577" r="2.5" fill="#4a2f14"/><circle cx="509" cy="601" r="2.5" fill="#4a2f14"/><circle cx="509" cy="577" r="2.5" fill="#4a2f14"/><circle cx="399" cy="601" r="2.5" fill="#4a2f14"/></g>
    <text x="392" y="538" class="stencil">FROGSBOTTOM</text>
    <g transform="rotate(180 346 592)"><text x="346" y="590" class="stencil s2">THIS WAY UP</text><path d="M346 612v-14m-5 5l5-6 5 6" fill="none" stroke="#4a2f14" stroke-width="3" opacity=".5"/></g>
  </g>
  <rect x="150" y="446" width="452" height="170" rx="8" fill="none" stroke="#5a3415" stroke-width="3"/>
  <g fill="#b9c3cc" stroke="#55606b" stroke-width="1.5"><rect x="146" y="442" width="26" height="26" rx="4"/><rect x="580" y="442" width="26" height="26" rx="4"/><rect x="146" y="594" width="26" height="26" rx="4"/><rect x="580" y="594" width="26" height="26" rx="4"/></g>

  <!-- cogs -->
  <g class="cogs">
    <g transform="translate(222 548)"><g id="cog-a" fill="url(#g-brass)" stroke="#7a4f10" stroke-width="1.5">__COG_A__</g></g>
    <g transform="translate(277 583)"><g id="cog-b" fill="url(#g-copper)" stroke="#6e3216" stroke-width="1.5">__COG_B__</g></g>
    <g transform="translate(190 594)"><g id="cog-c" fill="url(#g-steel)" stroke="#55606b" stroke-width="1.5">__COG_C__</g></g>
  </g>

  <!-- pressure gauge and valves -->
  <g transform="translate(556 540)">
    <circle r="33" fill="#55606b"/><circle r="28" fill="#FFFDF2"/>
    <path d="M-20 12A23 23 0 1 1 20 12" fill="none" stroke="#1B1A1F" stroke-width="2.5" stroke-dasharray="2 6.2"/>
    <path d="M9 -19A23 23 0 0 1 20 12" fill="none" stroke="#E3262E" stroke-width="5"/>
    <g id="needle"><path d="M0 4L-2.5 0 0-22 2.5 0z" fill="#E3262E"/></g><circle r="4" fill="#1B1A1F"/>
  </g>
  <g class="bulbs">
    <g transform="translate(424 588)"><rect x="-7" y="6" width="14" height="10" rx="2" fill="#55606b"/><circle class="bulb" id="bulb-1" r="11" fill="url(#g-bulb)"/></g>
    <g transform="translate(454 588)"><rect x="-7" y="6" width="14" height="10" rx="2" fill="#55606b"/><circle class="bulb" id="bulb-2" r="11" fill="url(#g-bulb)"/></g>
    <g transform="translate(484 588)"><rect x="-7" y="6" width="14" height="10" rx="2" fill="#55606b"/><circle class="bulb" id="bulb-3" r="11" fill="url(#g-bulb)"/></g>
  </g>

  <!-- winding handle -->
  <g transform="translate(606 560)">
    <rect x="-8" y="-10" width="18" height="20" rx="3" fill="#55606b"/>
    <g id="g-crank"><path d="M0 0L34 -22" stroke="#8a95a1" stroke-width="8" stroke-linecap="round"/><path d="M34 -22h24" stroke="#8a95a1" stroke-width="8" stroke-linecap="round"/><rect x="50" y="-33" width="30" height="22" rx="10" fill="#E3262E"/><circle r="7" fill="#3a424b"/></g>
  </g>

  <!-- turntable -->
  <ellipse cx="360" cy="446" rx="186" ry="54" fill="#3a2a1a" opacity=".45"/>
  <ellipse cx="360" cy="436" rx="182" ry="55" fill="#6b7682"/><ellipse cx="360" cy="431" rx="182" ry="55" fill="url(#g-steel)"/>
  <g id="g-wobble">
    <g transform="translate(360 424) scale(1 .3)">
      <g id="g-record">
        <circle r="170" fill="url(#g-vinyl)"/>
        __GROOVES__
        <path d="M-150 -40A156 156 0 0 1 -96 -122" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".5"/>
        <path d="M120 96A152 152 0 0 1 66 138" fill="none" stroke="#8ED0E8" stroke-width="4" stroke-linecap="round" opacity=".5"/>
        <circle r="66" fill="#F6EFE0"/>
        <image id="label-img" href="" x="-62" y="-62" width="124" height="124" preserveAspectRatio="xMidYMid slice" clip-path="url(#c-label)"/>
        <circle r="62" fill="none" stroke="#1B1A1F" stroke-opacity=".35" stroke-width="2"/>
        <circle r="7" fill="#d9dde2"/><circle r="3" fill="#33383e"/>
      </g>
      <path d="M0 0L-170 -34A174 174 0 0 1 -150 -84Z" fill="#fff" opacity=".1"/><path d="M0 0L170 34A174 174 0 0 1 150 84Z" fill="#fff" opacity=".1"/>
    </g>
  </g>

  <!-- tone arm: a golf club, naturally -->
  <g transform="translate(196 392)">
    <rect x="-9" y="0" width="18" height="44" rx="4" fill="#55606b"/><circle r="15" fill="url(#g-brass)" stroke="#7a4f10" stroke-width="2"/>
    <g id="g-arm">
      <path d="M0 0L118 22" stroke="url(#g-steel)" stroke-width="7" stroke-linecap="round"/>
      <path d="M-26 -5L0 0" stroke="#55606b" stroke-width="12" stroke-linecap="round"/>
      <path d="M112 16l26 2q9 2 7 12l-4 11q-10 3-18-4z" fill="#b9c3cc" stroke="#55606b" stroke-width="2"/>
      <path d="M124 26l12 1M123 32l11 1" stroke="#55606b" stroke-width="1.6"/>
      <path d="M132 40l1 8" stroke="#1B1A1F" stroke-width="2.4" stroke-linecap="round"/>
    </g>
    <circle r="5" fill="#3a2a1a"/>
  </g>
</g>
</svg>'''

def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])

def stage_svg():
    L = [(546, 436), (530, 380), (440, 340), (430, 258)]; R = [(578, 436), (610, 370), (740, 300), (750, 142)]
    pts = []
    for t in (.2, .4, .6, .8):
        x, y = _bez(*L, t); pts.append((round(x + 9), round(y - 3)))
        x, y = _bez(*R, t); pts.append((round(x - 10), round(y - 2)))
    riv = rivets(pts + [(462, 378), (490, 398), (640, 312), (646, 340)])
    seams = ''.join(f'<path d="M562 440L{x} {y}" stroke="#5c3b0c" stroke-width="2.5" opacity=".35"/>' for x, y in ((470, 250), (540, 224), (610, 198), (680, 172)))
    n = 240; sc = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + .055 * abs(math.sin(5 * a))
        sc.append(f"{165 * k * math.cos(a):.1f},{134 * k * math.sin(a):.1f}")
    scallop = 'M' + 'L'.join(sc) + 'Z'
    petals = ''
    for i in range(10):
        a0, a1 = math.radians(i * 36), math.radians(i * 36 + 36)
        fill = ('#fff', '#3a1f08')[i % 2]
        if i == 3: fill = '#3E7E7A'
        if i == 8: fill = '#C4553A'
        op = .5 if i in (3, 8) else .1
        petals += f'<path d="M-8 14L{-8 + 260 * math.cos(a0):.0f} {14 + 260 * math.sin(a0):.0f}L{-8 + 260 * math.cos(a1):.0f} {14 + 260 * math.sin(a1):.0f}Z" fill="{fill}" opacity="{op}"/>'
    return (SVG.replace('__SEAMS__', seams).replace('__SCALLOP__', scallop).replace('__PETALS__', petals).replace('__RAYS__', RAYS).replace('__GROOVES__', GROOVES).replace('__RIVETS__', riv)
            .replace('__COG_A__', cog(38, 12)).replace('__COG_B__', cog(26, 8, 6, 5)).replace('__COG_C__', cog(20, 6, 6, 4)))

ICON = {
  'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>',
  'pause': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zm8 0h4v14h-4z" fill="currentColor"/></svg>',
  'back': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z" fill="currentColor"/></svg>',
  'fwd': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z" fill="currentColor"/></svg>',
  'start': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2.5v14H6zM19 5v14l-9.5-7z" fill="currentColor"/></svg>',
}

def page(songs, pic_src, credits):
    data = [dict(id=s['id'], title=s['title'], by=s['by'], kicker=s['kicker'], src=s['src'],
                 cover=pic_src(s['cover']), theme=('night' if 'sheep' in s['id'] else 'day'),
                 credits=credits, lines=lyrics(s['id']),
                 env=open(os.path.join(HERE, 'lyrics', s['id'] + '.env')).read().strip()) for s in songs]
    sleeves = ''.join(
        f'<button type="button" class="sleeve" data-song="{s["id"]}" aria-pressed="false"><img src="{pic_src(s["cover"])}" alt="" width="64" height="64"><span><small>{html.escape(s["kicker"])}</small><b>{html.escape(s["title"])}</b></span></button>'
        for s in songs)
    return f'''
<section class="gp" id="gp" data-theme="day">
  <div class="gp-sky" aria-hidden="true"><i class="moon"></i><div class="stars" id="gp-stars"></div></div>
  <div class="wrap gp-wrap">
    <div class="gp-head">
      <a class="gp-back" href="songs.html">&#8592; All songs</a>
      <p class="kicker" id="gp-kicker"></p>
      <h1 id="gp-title">Russell’s gramophone</h1>
      <p class="gp-by">Now playing on Russell’s home-made gramophone</p>
    </div>

    <div class="gp-stage" id="gp-stage">
      {stage_svg()}
      <img class="gp-frankie" id="gp-frankie" src="img/frankie-grin-193.webp" alt="" width="193" height="505">
      <div class="gp-notes" id="gp-notes" aria-hidden="true"></div>
      <button type="button" class="gp-bigplay" id="gp-bigplay" aria-label="Play">{ICON['play']}<span>Wind it up</span></button>
    </div>

    <div class="gp-deck">
      <div class="gp-seek">
        <span class="gp-time" id="gp-cur">0:00</span>
        <input type="range" id="gp-range" min="0" max="1000" value="0" step="1" aria-label="Song position">
        <span class="gp-time" id="gp-dur">0:00</span>
      </div>
      <div class="gp-btns">
        <button type="button" id="gp-start" aria-label="Back to the start">{ICON['start']}</button>
        <button type="button" id="gp-back" aria-label="Back 10 seconds">{ICON['back']}<small>10</small></button>
        <button type="button" id="gp-play" class="main" aria-label="Play"><span class="i-play">{ICON['play']}</span><span class="i-pause">{ICON['pause']}</span></button>
        <button type="button" id="gp-fwd" aria-label="Forward 10 seconds">{ICON['fwd']}<small>10</small></button>
        <button type="button" id="gp-next" aria-label="Play the other record"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.5 5H18v14h-2.5zM5 5v14l9.5-7z" fill="currentColor"/></svg></button>
      </div>
      <div class="gp-sleeves" role="group" aria-label="Choose a record">{sleeves}</div>
    </div>

    <div class="gp-words">
      <img class="gp-cover" id="gp-cover" src="" alt="" width="480" height="480">
      <div class="gp-three" id="gp-three" aria-live="off">
        <p class="gp-sec" id="gp-sec">Sing along</p>
        <div class="gp-three-in" id="gp-three-in"><div class="gp-strip" id="gp-strip"></div></div>
      </div>
      <div class="gp-pills">
        <button type="button" class="gp-pill" id="gp-open-lyrics">Full lyrics</button>
        <button type="button" class="gp-pill" id="gp-open-credits">Credits</button>
      </div>
      <figure class="gp-maker">
        <img src="img/russell-lt-welding-480.webp" alt="Russell the Sheep in welding goggles and his striped nightcap, building a machine at his workbench" width="480" height="480" loading="lazy">
        <figcaption>Built by Russell. No instructions were read.</figcaption>
      </figure>
    </div>
  </div>
  <dialog class="gp-dlg" id="gp-dlg-lyrics" aria-labelledby="gp-dlg-lt">
    <div class="gp-dlg-head"><h2 id="gp-dlg-lt">Lyrics</h2><button type="button" class="gp-x" data-close aria-label="Close">&#215;</button></div>
    <div class="gp-lines" id="gp-lines" tabindex="0"></div>
  </dialog>
  <dialog class="gp-dlg small" id="gp-dlg-credits" aria-labelledby="gp-dlg-ct">
    <div class="gp-dlg-head"><h2 id="gp-dlg-ct">Credits</h2><button type="button" class="gp-x" data-close aria-label="Close">&#215;</button></div>
    <p class="gp-credits" id="gp-credits"></p>
  </dialog>
  <audio id="gp-audio" preload="metadata"></audio>
  <script type="application/json" id="gp-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
</section>
'''
