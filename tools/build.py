import json, os, html
M = json.load(open('img/manifest.json'))
SPLAT = "https://www.splatthecat.com"
MAIL = "robbie00@mac.com"

def pic(name, alt, sizes="(max-width:860px) 100vw, 50vw", cls="", lazy=True, style="", attrs=""):
    m = M[name]
    srcset = ", ".join(f"img/{name}-{w}.webp {w}w" for (w, h, b) in m['sizes'])
    w0, h0, _ = m['sizes'][-1]
    src = f"img/{name}-{w0}.webp"
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    s = f' style="{style}"' if style else ''
    return f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{html.escape(alt)}" {load}{c}{s} {attrs}>'

def full(name):
    w0, h0, _ = M[name]['sizes'][-1]
    return f"img/{name}-{w0}.webp"

def zoom(name, alt, caption="", sizes="(max-width:540px) 100vw, (max-width:900px) 50vw, 33vw", cls="art"):
    return f'<figure style="margin:0"><button class="zoom {cls}" data-full="{full(name)}" data-caption="{html.escape(caption or alt)}" aria-label="View larger: {html.escape(alt)}">{pic(name, alt, sizes)}</button>{f"<figcaption>{caption}</figcaption>" if caption else ""}</figure>'

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'

import hashlib
def _fp(p): return hashlib.md5(open(p,'rb').read()).hexdigest()[:8]
ASSET_V = {'css': _fp('assets/site.css'), 'js': _fp('assets/site.js')}
NAV = [("index.html","Books"),("splat.html","Splat the Cat"),("russell.html","Russell the Sheep"),("max.html","Max and Moonbean"),("about.html","Meet Rob"),("activities.html","Activities"),("gallery.html","Gallery"),("contact.html","Contact")]
SITE_URL = "https://www.robscotton.com"   # change here if the site lives at another address
SHOW_LICENSING = False   # licensing is hidden for now; set True to bring it back

def shell(file, title, desc, body, theme="#F6B51F", extra_head=""):
    short = {"Splat the Cat":"Splat","Russell the Sheep":"Russell","Max and Moonbean":"Max &amp; Moonbean"}
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h==file or (h=="russell.html" and file=="russells-story.html") else ""}>' + (f'<span class="full">{t}</span><span class="short" aria-hidden="true">{short[t]}</span>' if t in short else t) + '</a>' for h,t in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="{theme}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/{'' if file=='index.html' else file}">
<meta property="og:image" content="{SITE_URL}/img/home-eyes-1200.webp">
<link rel="canonical" href="{SITE_URL}/{'' if file=='index.html' else file}">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Grandstander:wght@600..900&family=Figtree:ital,wght@0,400..800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v={ASSET_V['css']}">
{extra_head}
</head>
<body>
<a class="sr" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/splat-cutout-480.webp" alt="" width="40" height="40">Rob Scotton<small>Books</small></a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Site">{nav}<a class="splatlink" href="{SPLAT}" target="_blank" rel="noopener">splatthecat.com ↗</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <h4>Rob Scotton</h4>
        <p style="max-width:34ch">Author and illustrator of Splat the Cat, Russell the Sheep and Max and Moonbean. Rutland, England.</p>
        <a class="btn yellow" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a>
      </div>
      <div><h4>Books</h4><ul><li><a href="splat.html">Splat the Cat</a></li><li><a href="russell.html">Russell the Sheep</a></li><li><a href="max.html">Max and Moonbean</a></li></ul></div>
      <div><h4>More</h4><ul><li><a href="about.html">Meet Rob</a></li><li><a href="activities.html">Activities</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="contact.html">{"Contact &amp; licensing" if SHOW_LICENSING else "Contact"}</a></li></ul></div>
      <div><h4>Free downloads</h4><ul><li><a href="downloads/splat-colouring-sheet.jpg" download>Splat colouring sheet</a></li><li><a href="downloads/russell-colouring-sheet.jpg" download>Russell colouring sheet</a></li><li><a href="activities.html#max-act">Max and Moonbean printables</a></li></ul></div>
    </div>
    <div class="fine"><span>© Rob Scotton. Splat the Cat, Russell the Sheep and Max and Moonbean are © Rob Scotton. Published by HarperCollins.</span><span>robscotton.com</span></div>
  </div>
  <img class="car" src="img/splat-car-cutout-480.webp" alt="" width="480" height="450" loading="lazy">
</footer>
<script src="assets/site.js?v={ASSET_V['js']}" defer></script>
</body>
</html>'''

pages = {}

# ================= HOME =================
covers = [("cover-splat","Splat the Cat"),("cover-love-big","Love, Splat"),("cover-scaredy","Scaredy-Cat, Splat!"),("cover-merry","Merry Christmas, Splat"),("cover-secret-agent","Secret Agent Splat!"),("cover-splish","Splish, Splash, Splat!"),("cover-thankyou","Splat Says Thank You!"),("cover-show","Splat the Cat: On with the Show"),("cover-funny-valentine","Splat the Cat: Funny Valentine"),("cover-storybook","Splat the Cat Storybook Collection"),("cover-icr-1","I Can Read: Splat the Cat"),("cover-icr-2","I Can Read: Splat the Cat"),("cover-icr-3","I Can Read: Splat the Cat"),("cover-icr-4","I Can Read: Splat the Cat")]
def shelf_html(dark=True):
    items = "".join(f'<a href="{SPLAT}" target="_blank" rel="noopener" title="{t}: see it on splatthecat.com"><img src="img/{n}-{M[n]["sizes"][0][0]}.webp" alt="{html.escape(t)}" width="{M[n]["w"]}" height="{M[n]["h"]}" loading="lazy"></a>' for n,t in covers)
    return f'<div class="shelf" aria-label="Splat the Cat books">{items}</div><div class="shelf-wood"></div>'

# Musical notes that Splat sings out of the banner: (svg, colour, x drift, y drift, spin, size, delay)
_N1 = '<svg viewBox="0 0 24 32"><path d="M9 24.5V3.5L21 1v6l-9 2v15.5a5.2 4.2 0 1 1-3-.9z" fill="currentColor"/></svg>'
_N2 = '<svg viewBox="0 0 32 32"><path d="M8 25V6l20-4v19a5 4 0 1 1-3-.9V9.5L11 12.4V25a5 4 0 1 1-3-.9z" fill="currentColor"/></svg>'
_N3 = '<svg viewBox="0 0 24 32"><path d="M10 24.5V2c3 3.5 10 5 9 12-1-3.5-4.5-5-6-5.4v15.9a5.2 4.2 0 1 1-3-.9z" fill="currentColor"/></svg>'
_NOTE_SET = [(_N1,"#6A3A94","-150px","-210px","-28deg","1",".0s"),(_N2,"#1B1A1F","120px","-240px","22deg","1.2",".55s"),
             (_N3,"#E2232A","-60px","-260px","-14deg",".85","1.1s"),(_N1,"#1B1A1F","170px","-170px","30deg",".9","1.65s"),
             (_N2,"#6A3A94","-190px","-140px","-34deg",".8","2.2s"),(_N3,"#1FA7A3","60px","-280px","16deg","1.05","2.75s"),
             (_N1,"#E2232A","-110px","-300px","-8deg","1.15","3.3s"),(_N2,"#1B1A1F","200px","-260px","26deg",".75","3.85s")]
NOTES = "".join(f'<i class="note" style="color:{c};--dx:{dx};--dy:{dy};--rot:{r};--sz:{z};--dl:{d}">{svg}</i>' for svg,c,dx,dy,r,z,d in _NOTE_SET)

home = f'''
<section class="hero" aria-label="Introduction">
  <div class="wrap">
    <div class="hero-copy">
      <h1>Books<span class="dot" aria-hidden="true"></span></h1>
      <p class="lede">The picture-book worlds of Rob Scotton, home of a scruffy black cat called Splat, a sheep called Russell who cannot sleep, and a shy pup named Max who found a friend from the moon.</p>
      <div class="hero-actions">
        <a class="btn red" href="{SPLAT}" target="_blank" rel="noopener">Go to Splat's own website {EXT}</a>
        <a class="btn ghost" href="#worlds">Explore the books {ARROW}</a>
      </div>
    </div>
    <div class="hero-stage" aria-hidden="true">
      {pic("splat-sings","Splat the Cat, arms up, singing his heart out","(max-width:860px) 99vw, 46vw","splat",lazy=False)}
      <span class="notes">{NOTES}</span>
    </div>
  </div>
</section>

<section class="band tight" id="worlds" aria-label="The books">
  <div class="wrap">
    <div class="worlds">
      <a class="world splat" href="splat.html">{pic("tail-wiggled-bed","Splat lying in bed with his tail wiggling wildly in the air","(max-width:760px) 100vw, 33vw",style="object-position:50% 22%")}<h3>Splat the Cat</h3><span>Over five million books sold</span></a>
      <a class="world russell" href="russell.html">{pic("russell-cover-section","Russell the Sheep leaping over a green hill, with Frankie the frog riding on his stripy nightcap","(max-width:760px) 100vw, 33vw",style="object-position:50% 30%")}<h3>Russell the Sheep</h3><span>The woolly hero of Frogsbottom Field</span></a>
      <a class="world max" href="max.html">{pic("max-where","Max at his bedroom window meeting Moonbean, with Mr Ted on the sill","(max-width:760px) 100vw, 33vw",style="object-position:42% 55%")}<h3>Max and Moonbean</h3><span>A new story about a shy pup and a friend from the moon</span></a>
    </div>
  </div>
</section>

<section class="band portal launch" aria-labelledby="portal-h">
  <div class="sky" aria-hidden="true"></div>
  <div class="rocket" aria-hidden="true"><span class="flame"></span>{pic("splat-rocket-cutout","","(max-width:860px) 60vw, 26vw")}</div>
  <div class="wrap">
    <div class="split">
      <div>
        <p class="kicker" style="color:#FFD34D">Splat has a whole website of his own</p>
        <h2 id="portal-h">Blast off to splatthecat.com</h2>
        <p class="lede">Every Splat book, the characters, games, colouring sheets and all the latest news live over at Splat's place. This is where Splat fans should be.</p>
        <div class="portal-cta">
          <a class="btn yellow big" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a>
          <span class="url">www.splatthecat.com</span>
        </div>
      </div>
      <div class="launchpad" aria-hidden="true"></div>
    </div>
  </div>
  {shelf_html()}
  <p class="shelf-note">Tap any book to find it on splatthecat.com</p>
</section>

<section class="band night-band on-dark" aria-labelledby="max-h">
  <div class="moon-disc" aria-hidden="true"></div>
  <div class="bubbles" aria-hidden="true"></div>
  <div class="wrap">
    <div class="split rev">
      <div>
        <p class="kicker">New from Rob Scotton</p>
        <h2 id="max-h">Max and Moonbean</h2>
        <p class="lede">Max's show‑and‑tells always go wrong. Then one night a shooting star crashes into his closet, and out steps a small blue astronaut who talks in bubbles.</p>
        <p>A story about being shy, being brave, and finding out that the two can live in the same pup. Painted in moonlight, bubbles and bedroom shadows.</p>
        <a class="btn moon" href="max.html">Meet Max and Moonbean {ARROW}</a>
      </div>
      <figure class="art tilt-r" style="margin:0;background:var(--night-2)">{pic("max-shooting-star","Max and his teddy tumbling through a burst of starlight","(max-width:860px) 100vw, 50vw")}</figure>
    </div>
  </div>
</section>

<section class="band snow-band" aria-labelledby="russell-h">
  <div class="snow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="split">
      <div>
        <p class="kicker" style="color:var(--teal-2)">The one who started it all</p>
        <h2 id="russell-h">Russell the Sheep</h2>
        <p class="lede">A sheep who cannot fall asleep, no matter how hard he tries. Russell was Rob's first picture book, and he came, of all places, from a bike ride through a field in Rutland.</p>
        <a class="btn teal" href="russell.html">Russell's story, and his Christmas Magic {ARROW}</a>
      </div>
      <figure class="art tilt-l" style="margin:0">{pic("russell-branch","Russell the Sheep asleep on a branch with the birds, under a crescent moon","(max-width:860px) 100vw, 50vw")}</figure>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="rob-h">
  <div class="wrap">
    <div class="split rev">
      <div>
        <h2 id="rob-h">Meet Rob</h2>
        <p class="lede">Rob Scotton is the bestselling author and illustrator behind Splat the Cat, Russell the Sheep and Max and Moonbean. His characters have a knack for finding adventure in everyday life, particularly when everyday life isn't going quite according to plan.</p>
        <p>The idea for Splat arrived while Rob was mowing the lawn, watching a neighbour's cat lose its balance on a fence. The word “Splat” sprang to mind. The lawn was temporarily forgotten.</p>
        <a class="btn" href="about.html">Read Rob's story {ARROW}</a>
      </div>
      <figure class="art" style="margin:0;width:min(100%,440px);justify-self:center;border-radius:50% 50% 46% 46% / 42% 42% 58% 58%">{pic("author","Rob Scotton","(max-width:860px) 80vw, 36vw")}</figure>
    </div>
  </div>
</section>

<section class="band yellow-band tight" aria-label="One more nudge to Splat">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:18px"><img src="img/splat-ducks-cutout-480.webp" alt="" width="120" height="113" style="width:110px" loading="lazy"><div><h3 style="margin:0">Looking for Splat?</h3><p style="margin:0">Games, books and ducks. Lots of ducks.</p></div></div>
    <a class="btn red big" href="{SPLAT}" target="_blank" rel="noopener">Go to splatthecat.com {EXT}</a>
  </div>
</section>
'''
pages['index.html'] = shell('index.html', "Rob Scotton | Books", "The picture-book worlds of Rob Scotton: Splat the Cat, Russell the Sheep and Max and Moonbean. Home of the author and illustrator.", home)


# ================= WHERE TO BUY =================
def isbn10(i13):
    core=i13[3:12]; s=sum((10-k)*int(d) for k,d in enumerate(core)); c=(11-s%11)%11
    return core+('X' if c==10 else str(c))

US_SHOPS=[("HarperCollins","https://www.harpercollins.com/search?q={i13}"),("Amazon","https://www.amazon.com/dp/{i10}"),("Barnes &amp; Noble","https://www.barnesandnoble.com/s/{i13}"),("Bookshop.org","https://bookshop.org/search?keywords={i13}")]
UK_SHOPS=[("Amazon UK","https://www.amazon.co.uk/s?k={i13}&amp;i=stripbooks"),("Blackwell&#8217;s","https://blackwells.co.uk/bookshop/search/?keyword={i13}"),("Bookshop.org UK","https://uk.bookshop.org/search?keywords={i13}")]

def shop_links(i13, shops):
    return "".join(f'<a class="shop" href="{u.format(i13=i13,i10=isbn10(i13))}" target="_blank" rel="noopener">{n}</a>' for n,u in shops)

def buy_card(title, note, cover, us, uk=None):
    img = f'<div class="buy-cover">{pic(cover, title + " book cover", "160px")}</div>' if cover else '<div class="buy-cover none" aria-hidden="true"><span>' + title + '</span></div>'
    us_rows = "".join(f'<div class="fmt-row"><p class="fmt">{fmt} <span>ISBN {i}</span></p><div class="shops">{shop_links(i, US_SHOPS)}</div></div>' for fmt,i in us)
    uk_rows = "".join(f'<div class="fmt-row"><p class="fmt">{fmt} <span>ISBN {i}</span></p><div class="shops">{shop_links(i, UK_SHOPS)}</div></div>' for fmt,i in (uk or []))
    uk_block = f'<div class="region" data-region="uk" hidden>{uk_rows}</div>' if uk else ''
    return f'<article class="buy-card">{img}<div class="buy-body"><h3>{title}</h3><p class="buy-note">{note}</p><div class="region" data-region="us">{us_rows}</div>{uk_block}</div></article>'

def buy_section(heading, intro, cards, regions=False):
    toggle = '<div class="region-toggle" role="group" aria-label="Choose your country"><button type="button" data-set="us" aria-pressed="true">United States</button><button type="button" data-set="uk" aria-pressed="false">United Kingdom</button></div>' if regions else ''
    return f'''
<section class="band buy-band" id="buy" aria-labelledby="buy-h">
  <div class="wrap">
    <div class="buy-head"><div><h2 id="buy-h">{heading}</h2><p class="lede">{intro}</p></div>{toggle}</div>
    <div class="buy-grid" data-buy>{"".join(cards)}</div>
    <p class="buy-fine">Links open the retailer&#8217;s own site. Availability, editions and prices are set by each retailer.</p>
  </div>
</section>
'''

# ================= SPLAT =================
splat = f'''
<header class="hdr hdr-splat">
  <div class="bg">{pic("hdr-splat","","100vw",lazy=False)}</div>
  <div class="fade"></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">Rob Scotton's</p>
    <h1>Splat the Cat</h1>
    <p class="lede">A scruffy black cat with a big heart, wayward fur, a pet mouse called Seymour, and a talent for turning small worries into enormous adventures. Over five million books sold, and his very own website.</p>
    <div class="hero-actions"><a class="btn red big" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a></div>
  </div></div>
  {pic("splat-cutout","Splat the Cat, arms flung wide","(max-width:760px) 190px, 30vw","peek",lazy=False)}
</header>

<section class="band" aria-labelledby="song-h">
  <div class="wrap split">
    <figure class="art tilt-l" style="margin:0">{pic("his-tail-cover","His Tail Wiggled On: Splat on a penny-farthing with Seymour","(max-width:860px) 100vw, 50vw")}</figure>
    <div>
      <p class="kicker">Listen</p>
      <h2 id="song-h">His Tail Wiggled On</h2>
      <p class="lede">Splat rides, wobbles and wiggles his way through a song of his own. Press play and let his tail do the rest.</p>
      <div class="player">
        <button type="button" aria-label="Play"></button>
        <div class="meta"><b>His Tail Wiggled On</b><span>Rob Scotton's Splat the Cat</span><div class="bar"><i></i></div></div>
        <span class="time">0:00</span>
        <audio preload="metadata" src="audio/his-tail-wiggled-on.mp3"></audio>
      </div>
    </div>
  </div>
</section>

<section class="band red-band on-dark" aria-labelledby="books-h" style="padding-bottom:0">
  <div class="wrap">
    <div class="split">
      <div><h2 id="books-h">The books</h2><p class="lede">From Splat's first terrifying day at Cat School to secret missions, school plays, Halloween, Christmas and Valentine's Day. Every title, inside pages and where to buy are on splatthecat.com.</p></div>
      <div style="display:flex;gap:28px;flex-wrap:wrap;align-items:center"><div><span class="stat">5,000,000+</span><span>Splat the Cat books sold</span></div><a class="btn yellow" href="{SPLAT}" target="_blank" rel="noopener">See all the books {EXT}</a></div>
    </div>
  </div>
  {shelf_html()}
  <p class="shelf-note" style="padding-bottom:40px">Tap any book to find it on splatthecat.com</p>
</section>

<section class="band" aria-labelledby="peek-h">
  <div class="wrap">
    <h2 id="peek-h">A peek inside</h2>
    <p class="lede">Page art from Splat Says Thank You!, Splish, Splash, Splat! and friends.</p>
    <div class="masonry">
      {zoom("print-splat-in-bath","Splat in the bath wearing a rubber duck on his head","Gulp! From Splish, Splash, Splat!")}
      {zoom("thankyou-tree","Splat hanging from a tree branch","Splat Says Thank You!")}
      {zoom("print-waiting-for-splat","Splat racing past the grown-ups' legs","Waiting for Splat")}
      {zoom("splish-page","Spike and Splat in their swimming rings","Splish, Splash, Splat!")}
      {zoom("print-splat-doing-splat-stuff","Splat brushing his teeth in a mirror full of cats","Splat doing Splat stuff")}
      {zoom("print-thankyou-p20-08-copy","Splat with a foghorn, surrounded by fishbone wallpaper","Honk!")}
      {zoom("splat-making-plans","Splat scheming at his desk","Splat making plans")}
      {zoom("tail-wiggled-bed","Splat lying in bed with his tail in the air","His tail wiggled wildly")}
      {zoom("print-splat-gotcha","Splat bursting through the doorway","Gotcha!")}
    </div>
    <p style="margin-top:28px"><a class="btn" href="gallery.html">See more artwork in the gallery {ARROW}</a></p>
  </div>
</section>

<section class="band plum-band on-dark" aria-labelledby="chars-h">
  <div class="wrap">
    <h2 id="chars-h">Splat's world</h2>
    <p class="lede">Meet the cast: the friends, the frenemy and the ducks.</p>
    <div class="chars">
      <div class="char"><div class="pic">{pic("splat-thoughtful","Splat looking thoughtful","(max-width:560px) 90vw, 25vw")}</div><h3>Splat</h3><p>Fur that goes everywhere, a heart to match. Worries big, bounces back bigger.</p></div>
      <div class="char"><div class="pic">{pic("seymour-pose","Seymour the mouse, looking up in surprise","(max-width:560px) 90vw, 25vw",style="object-fit:contain;padding:6% 3%")}</div><h3>Seymour</h3><p>Small, quirky and full of personality. Splat's best friend and the brains of most operations.</p></div>
      <div class="char"><div class="pic">{pic("spike-sheet","Spike, Splat's frenemy, in his stripy jumper","(max-width:560px) 90vw, 25vw")}</div><h3>Spike</h3><p>A greyish‑white cat who really wants to be Splat's friend, but keeps breaking his favourite toy and eating all the candy fish.</p></div>
      <div class="char"><div class="pic">{pic("ducks-layered","A flock of brightly patterned toy ducks","(max-width:560px) 90vw, 25vw")}</div><h3>The ducks</h3><p>Splat's father makes toy ducks for a living. Splat has given every one of them a name, and counts them. Often.</p></div>
    </div>
    <div style="margin-top:28px;max-width:640px">
      {zoom("character-copy","Little Sis and Mrs Wimpydimple character notes","Little Sis and Mrs Wimpydimple","(max-width:560px) 100vw, 50vw")}
    </div>
  </div>
</section>


<section class="band paper-band" aria-labelledby="free-h">
  <div class="wrap">
    <h2 id="free-h">Free things to do</h2>
    <div class="dl">
      <a href="downloads/splat-colouring-sheet.jpg" download><img src="img/splat-colour-sheet-480.webp" alt="" width="480" height="338" loading="lazy"><div><b>Splat colouring sheet</b><span>Print it on A4 or US Letter and colour Splat in. Download</span></div></a>
      <a href="{SPLAT}" target="_blank" rel="noopener">{pic("splat-making-plans","","(max-width:560px) 90vw, 30vw")}<div><b>Games and more</b><span>Everything else lives on splatthecat.com ↗</span></div></a>
    </div>
  </div>
</section>

<section class="band yellow-band" aria-label="Go to splatthecat.com">
  <div class="wrap" style="text-align:center">
    <img src="img/splat-with-book-480.webp" alt="" width="480" height="511" style="width:min(60%,260px);margin:0 auto 10px" loading="lazy">
    <h2>That's the short version.</h2>
    <p class="lede" style="margin-inline:auto;color:var(--ink)">The whole story is waiting at Splat's own website: every book, every character, the games and the news.</p>
    <a class="btn red big" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a>
  </div>
</section>
<a class="floater" href="{SPLAT}" target="_blank" rel="noopener"><img src="img/splat-cutout-480.webp" alt="" width="44" height="42">splatthecat.com ↗</a>
'''
pages['splat.html'] = shell('splat.html', "Splat the Cat | Rob Scotton", "Splat the Cat by Rob Scotton: the books, the characters, and the way to splatthecat.com.", splat, "#E3262E")

# ================= RUSSELL =================
story = """<p>I was riding my bike through a field in Rutland, near where I live, playing my usual game of ‘Dodge the Woolly Thing’, when it occurred to me, yet again, that there must surely be a story to be found in this flock of woolly critters staring so disdainfully at my progress. Then I dismissed the idea… again. After all, who wants to read a story about a flock of sheep? They eat, they stare, they eat. Great material for a story? Not!</p>
<p>Just then, I saw a peculiar thing: a group of sheep sheltering from the sun in the shadow of a tree. ‘Curious,’ I thought, and sat for a while to see if the sheep would follow the shadow as the sun moved overhead. Know what? They did, and I got to thinking. Maybe there was an idea amongst all that wool after all. Nah! I thought on. A flock of sheep would be pretty dull. Anyway, they would need a playful name, and what would I call them? Worryingly, that was the moment the words ‘Frogsbottom Sheep’ leapt out of nowhere and slapped me around the head.</p>
<p>Frogsbottom Sheep? Why not? It sounded silly, but in a good way! There was bound to be a frog or two in the field, perhaps even a whole pondful of the little guys. A frog would make a good visual contrast to a big woolly sheep, and children would certainly giggle at the ‘bottom’ part. Well, you have to play to your audience.</p>
<p>Hmm. I began to ponder. I would need one special sheep to stand out from the flock: a star, a hero, a character of depth, intensity and spirit who could single-hoofedly bear the weight of a story. But who could it be? Wait! Maybe, just maybe, I had another thought. (It was a good day!)</p>
<p>Perspiration and inspiration, all on one bike ride: this was almost too much. I cycled home and rifled through a pile of my old greetings-card designs until I found the one I was looking for, a simple sheep character on an Easter card that I had painted in a previous life. Using that as a starting point, I began to doodle. Before long, a boggle-eyed character was staring back at me from the screen. He was such a simple, uncomplicated and ridiculous soul that a name came to mind instantly: ‘Russell the Sheep’. I cringed at the awful pun, but at least I had a working title. As the weeks passed, other names came along, but none seemed to fit. Russell the Sheep it was, and Russell the Sheep it stayed.</p>
<p>So I had my hero, Russell the Sheep. I had found him a home in Frogsbottom Field and a supporting cast of other sheep and even a little frog. Now just one thing was missing: a story.</p>
<p>For that, I needed a tale rich in substance and awash with humour, with an engaging plot woven with twists and unforeseen diversions. A story that would send our woolly hero on a rollercoaster of emotional extremes, with us, the readers, sitting right there beside him. And when Russell finally won through, as he must, we would applaud his efforts and still be cheering for him long after the final page was turned.</p>
<p>Hmm. Not an easy brief. But then… what if Russell couldn’t fall asleep, no matter how hard he tried? Maybe he could count things…</p>
<blockquote>By Granny Oldwool’s beard, there may be something there…</blockquote>
<p>Oh, and of course, there’s also a little frog… and an ant. Job done!</p>"""

DRAWERS = [("russell-the-sheep","Russell the Sheep"),("lost-treasure","Lost Treasure"),("christmas-magic","Christmas Magic"),("story","Russell&#8217;s story")]
drw_chips = '<nav class="drw-chips" aria-label="On this page">' + "".join(f'<a href="#{k}">{t}</a>' for k,t in DRAWERS) + '</nav>'

russell = f'''
<header class="hdr hdr-russell" id="russell-the-sheep">
  <div class="bg">{pic("hdr-russell","","100vw",lazy=False)}</div>
  <div class="fade"></div>
  <div class="twinkle" aria-hidden="true"></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">Book one, 2005</p>
    <h1>Russell the Sheep</h1>
    <p class="lede">Night falls on Frogsbottom Field and every sheep is fast asleep, except Russell. He tries everything: a new hat, a bed up a tree, counting his feet, counting the stars. There&#8217;s only one thing left to try. Counting sheep!</p>
    <a class="btn teal" href="#buy">Where to buy {ARROW}</a>
    {drw_chips}
  </div></div>
</header>
<section class="band tight inside" aria-label="Pictures from Russell the Sheep">
  <div class="wrap"><div class="inside-row">
    <figure style="margin:0" class="art tilt-l">{pic("cover-russell-sheep","Russell the Sheep book cover","(max-width:860px) 45vw, 22vw")}</figure>
    {zoom("russell-what-to-do","Russell standing wide awake in his striped nightcap","What&#8217;s a sheep to do?")}
    {zoom("russell-swing","Russell swinging from a tree while Frankie clings to the trunk","One more try")}
    {zoom("russell-sleeps","Russell asleep under a patchwork quilt","Russell sleeps, at last!")}
  </div></div>
</section>

<section class="hdr drawer drw-treasure" id="lost-treasure" aria-labelledby="treasure-h">
  <div class="bg">{pic("hdr-russell-treasure","","100vw")}</div>
  <div class="fade"></div>
  <div class="fx" data-fx="sparks" data-x="19.2" data-y="75.6" aria-hidden="true"><span class="torch-glow"></span></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">Book two, 2006</p>
    <h2 id="treasure-h">Russell and the Lost Treasure</h2>
    <p class="lede">Legend has it there&#8217;s a treasure lost somewhere in Frogsbottom Field. Russell builds a homemade treasure detector and goes looking, and the chest he finds holds a surprising prize.</p>
    <a class="btn teal" href="#buy">Where to buy {ARROW}</a>
  </div></div>
  <img class="frankie-peek" src="img/frankie-grin-193.webp" alt="" width="193" height="505" loading="lazy">
</section>
<section class="band tight inside" aria-label="Pictures from Russell and the Lost Treasure">
  <div class="wrap"><div class="inside-row">
    <figure style="margin:0" class="art tilt-l">{pic("cover-russell-treasure","Russell and the Lost Treasure book cover","(max-width:860px) 45vw, 22vw")}</figure>
    {zoom("russell-lt-plan","Russell peeping over a long scroll of drawings for a treasure-hunting machine","The big plan")}
    {zoom("russell-lt-auntie-uncle","Two sheep in sunglasses riding in a battered old car","Auntie and Uncle, out for a spin")}
    {zoom("russell-lt-shares","Russell reading from a glowing book to the flock under the night sky","Russell shares his treasure")}
  </div></div>
</section>

<section class="hdr drawer drw-xmas" id="christmas-magic" aria-labelledby="xmas-h">
  <div class="bg">{pic("hdr-russell-xmas","","100vw")}</div>
  <div class="fade"></div>
  <div class="fx" data-fx="lantern" data-x="84" data-y="50" aria-hidden="true"><span class="lantern-glow"></span></div>
  <div class="snow" aria-hidden="true"></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">Book three, 2007</p>
    <h2 id="xmas-h">Russell&#8217;s Christmas Magic</h2>
    <p class="lede">Santa Claus&#8217;s sleigh crashes in Firefly Wood and the Christmas Spell is broken. Santa declares that Christmas must be cancelled. But our fleecy hero doesn&#8217;t give up easily, and he soon has a woolly idea that just might save the day.</p>
    <a class="btn teal" href="#buy">Where to buy {ARROW}</a>
  </div></div>
</section>
<section class="band tight inside" aria-label="Pictures from Russell's Christmas Magic">
  <div class="wrap">
    <div class="inside-row">
      <figure style="margin:0" class="art tilt-l">{pic("cover-russell-xmas","Russell&#8217;s Christmas Magic book cover","(max-width:860px) 60vw, 22vw")}</figure>
      {zoom("russell-p8","Russell trudging through the snow","Russell&#8217;s Christmas Magic")}
      {zoom("russell-p9","Russell listening at the edge of the wood","Russell&#8217;s Christmas Magic")}
      {zoom("russell-art-14","Santa&#8217;s crashed sleigh in the snow","Russell&#8217;s Christmas Magic")}
    </div>
  </div>
</section>

<section class="band night-band on-dark" aria-labelledby="myer-h">
  <div class="bubbles" aria-hidden="true" style="display:none"></div>
  <div class="wrap">
    <div class="split">
      <div>
        <p class="kicker">Melbourne and Brisbane, Australia</p>
        <h2 id="myer-h">Myer's Christmas Windows</h2>
        <p class="lede">Russell's Christmas Magic was the theme for Myer's spectacular Christmas windows in Melbourne and Brisbane. Firefly Wood, the crashed sleigh and a flock of woolly helpers, built as moving window displays by Stage One Productions.</p>
        <p>Russell even made the national news. The reindeer rock.</p>
      </div>
      {zoom("myer-reindeer","Animated reindeer in Myer's Russell's Christmas Magic window","The reindeer, mid‑rock","(max-width:860px) 100vw, 50vw")}
    </div>
    <div class="grid c3" style="margin-top:32px">
      {"".join(zoom(f"myer-window-{i}", f"Myer Christmas window {i}", "Photo: Rob Anderson", cls="art wide") for i in range(1,7))}
    </div>
  </div>
</section>

<section class="hdr drawer drw-story" id="story" aria-labelledby="story-h">
  <div class="bg">{pic("hdr-russell-story","","100vw")}</div>
  <div class="fade"></div>
  <div class="fx" data-fx="count" data-x="54" data-y="52" aria-hidden="true"></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">So how did it all begin?</p>
    <h2 id="story-h">Russell&#8217;s story, according to Rob</h2>
    <p class="lede">A bike ride through a field in Rutland, a flock of sheep staring back, and an idea Rob kept dismissing. Here&#8217;s how Russell came to be.</p>
    <a class="btn" href="russells-story.html">Read Russell&#8217;s story {ARROW}</a>
  </div></div>
</section>

{buy_section("Where to buy Russell",
  "Russell the Sheep was first published by HarperCollins in the US and HarperCollins Children's Books in the UK. Choose your country to see the right editions.",
  [buy_card("Russell the Sheep","The original story of a sheep who cannot sleep.","cover-russell-sheep",
      [("Paperback","9780062392435"),("Board book","9780061709968"),("Hardcover","9780060598488")],
      [("UK edition","9780007206223")]),
   buy_card("Russell and the Lost Treasure","Russell goes looking for treasure in Frogsbottom Field.","cover-russell-treasure",
      [("Hardcover","9780060598518")],
      [("UK edition","9780007206254")]),
   buy_card("Russell&#8217;s Christmas Magic","Santa crashes in Firefly Wood, and Russell has a woolly idea.","cover-russell-xmas",
      [("Hardcover","9780060598549")],
      [("UK edition","9780007262946")])],
  regions=True)}

<section class="band" aria-labelledby="dl-h">
  <div class="wrap">
    <h2 id="dl-h">Colour Russell in</h2>
    <div class="dl">
      <a href="downloads/russell-colouring-sheet.jpg" download><img src="img/russell-colouring-300.webp" alt="" width="300" height="189" loading="lazy"><div><b>Russell's Christmas Magic colouring sheet</b><span>Free to print and colour. Download</span></div></a>
    </div>
  </div>
</section>
'''
pages['russell.html'] = shell('russell.html', "Russell the Sheep | Rob Scotton", "Rob Scotton's Russell the Sheep books in order: Russell the Sheep, Russell and the Lost Treasure and Russell's Christmas Magic, with page art, the Myer Christmas windows and where to buy.", russell, "#2B3850")

storypage = f'''
<section class="band paper-band" aria-labelledby="story-h" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap">
    <p><a href="russell.html#story" style="font-weight:700">&#8592; Back to Russell the Sheep</a></p>
    <div class="split" style="align-items:start">
      <div>
        <p class="kicker" style="color:var(--teal-2)">So how did it all begin?</p>
        <h1 id="story-h" style="font-size:clamp(2.4rem,5vw,4rem)">Russell&#8217;s story, according to Rob</h1>
        <div class="prose">{story}</div>
      </div>
      <div style="display:grid;gap:22px;position:sticky;top:90px">
        <div style="width:min(100%,300px)">{zoom("cover-russell-sheep","Russell the Sheep book cover","Russell the Sheep, the first book","(max-width:860px) 80vw, 25vw")}</div>
        <div class="grid c3" style="gap:12px">
          <img src="img/sheep-photo-1-90.webp" alt="One of the original Frogsbottom sheep" width="90" height="87" style="width:100%;border-radius:12px" loading="lazy">
          <img src="img/sheep-photo-2-106.webp" alt="A sheep lying in a field in Rutland" width="106" height="85" style="width:100%;border-radius:12px" loading="lazy">
          <img src="img/sheep-photo-3-90.webp" alt="Sheep sheltering in the shadow of a tree" width="90" height="87" style="width:100%;border-radius:12px" loading="lazy">
        </div>
        <p style="font-size:.9rem;color:var(--ink-2)">The original Frogsbottom sheep that Rob came across as he cycled through a field in Rutland, England. It all started with these guys.</p>
        <div style="display:flex;gap:14px;align-items:flex-end"><img src="img/russell-counting-215.webp" alt="Russell counting his feet" width="215" height="219" style="width:120px" loading="lazy"><img src="img/frankie-75.webp" alt="Frankie the frog" width="75" height="194" style="width:50px" loading="lazy"></div>
      </div>
    </div>
  </div>
</section>

'''
pages['russells-story.html'] = shell('russells-story.html', "Russell's story | Rob Scotton", "How Russell the Sheep came to be, in Rob Scotton's own words: a bike ride through a field in Rutland and a flock of staring sheep.", storypage, "#F2EBDD")

# ================= MAX =================
maxp = f'''
<header class="hdr hdr-max on-dark">
  <div class="bg">{pic("hdr-max","","100vw",lazy=False)}</div>
  <div class="fade"></div>
  <div class="bubbles" aria-hidden="true"></div>
  <div class="wrap"><div class="copy">
    <p class="kicker">New from Rob Scotton</p>
    <h1>Max and Moonbean</h1>
    <p class="lede">Max's show‑and‑tells always go wrong. Then one night a shooting star crashes into his closet, and out steps a small blue astronaut who talks in bubbles. His name is Moonbean, and he has a question: will Max come to the moon to be <em>his</em> show‑and‑tell?</p>
    <p>A story about a shy pup, a brave one, and the moment you realise they're the same dog.</p>
    <div class="hero-actions"><a class="btn moon" href="#spreads">Look inside {ARROW}</a><a class="btn ghost" href="#buy" style="color:#fff">Where to buy</a></div>
  </div></div>
</header>


<section class="band" aria-labelledby="meet-h">
  <div class="wrap">
    <h2 id="meet-h">Meet the two of them</h2>
    <div class="grid c2">
      <div class="card"><div style="aspect-ratio:1.1;overflow:hidden;background:var(--night-2)">{pic("max-friend","Max resting his chin on the windowsill beside his teddy","(max-width:560px) 100vw, 50vw",style="width:100%;height:100%;object-fit:cover")}</div><div class="body"><h3>Max</h3><p>A pup with a woolly hat, a teddy called Mr Ted and a goldfish. Clever, kind, of impeccable style, and quite sure he is not very brave.</p></div></div>
      <div class="card"><div style="aspect-ratio:1.1;overflow:hidden;background:var(--night-2)">{pic("max-blue-thingy","Moonbean, a small blue astronaut, dancing in the dark with bubbles above him","(max-width:560px) 100vw, 50vw",style="width:100%;height:100%;object-fit:cover")}</div><div class="body"><h3>Moonbean</h3><p>A strange blue thingy with a slightly odd stare who arrived by shooting star. Speaks in bubble‑speak, tells excellent jokes, and says “Piffaffle!” to the word <em>can't</em>.</p></div></div>
    </div>
  </div>
</section>

<section class="band night-band on-dark" id="spreads" aria-labelledby="spreads-h">
  <div class="bubbles" aria-hidden="true"></div>
  <div class="wrap">
    <h2 id="spreads-h">Inside the book</h2>
    <p class="lede">Painted spreads from the story. Tap any one to see it large.</p>
    <div class="spreads">
      {zoom("max-shooting-star","The shooting star flew in like a furious rocket","The shooting star flew in")}
      {zoom("max-hide","Max peers from behind the curtain at the blue visitor","I wanted to hide")}
      {zoom("max-blue-thingy","Moonbean smiles with a slightly odd stare","The blue thingy smiled")}
      {zoom("max-moon","Moonbean points up through the window at the moon","Moonbean raised a finger that led to the moon")}
      {zoom("max-courage","Max dances among the bubbles as Moonbean cheers","You're a pup of courage")}
      {zoom("max-sleep","Max lies awake in bed with his teddy and his goldfish","Max couldn't sleep")}
      {zoom("max-where","Max at the window as a flying saucer arrives","Where did you come from?")}
      {zoom("max-friend","Max chin on the windowsill with Mr Ted","It takes a friend")}
      {zoom("max-cover","Max and Moonbean under the moon","The cover")}
    </div>
  </div>
</section>

{buy_section("Where to buy Max and Moonbean",
  "Published in hardcover by HarperCollins in the United States.",
  [buy_card("Max and Moonbean","Hardcover, 48 pages, ages 4 to 8.","max-cover",
      [("Hardcover","9780062990389")])])}

<section class="band paper-band" aria-labelledby="making-h">
  <div class="wrap split">
    <div>
      <p class="kicker">From sketch to spread</p>
      <h2 id="making-h">How the story was made</h2>
      <p class="lede">Every Max spread began as a pencil thumbnail: a whole book roughed out on a few sheets, words and pictures finding each other page by page.</p>
      <p>The storyboard on the right is the real working draft, with crossed‑out lines, alternative verses and a “squeak!” that survived to the finished book. Tap to zoom in.</p>
      <a class="btn plum" href="contact.html">Ask about Max and Moonbean {ARROW}</a>
    </div>
    {zoom("max-draft","The full pencil storyboard draft of Max and Moonbean","Working storyboard for Max and Moonbean","(max-width:860px) 100vw, 50vw",cls="art tall")}
  </div>
</section>

<section class="band yellow-band tight" aria-label="Also by Rob">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:18px"><img src="img/splat-cutout-480.webp" alt="" width="120" height="115" style="width:100px" loading="lazy"><div><h3 style="margin:0">Also by Rob: Splat the Cat</h3><p style="margin:0">Max's scruffier cousin has a whole website to himself.</p></div></div>
    <a class="btn red" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a>
  </div>
</section>
'''
pages['max.html'] = shell('max.html', "Max and Moonbean | Rob Scotton", "Max and Moonbean, the new picture book from Rob Scotton: a shy pup, a shooting star and a small blue astronaut who talks in bubbles.", maxp, "#0B1733")

# ================= ABOUT =================
about = f'''
<section class="phero yellow-band">
  <div class="wrap">
    <div>
      <p class="kicker">Author and artist</p>
      <h1>Meet Rob</h1>
      <p class="lede" style="color:var(--ink)">Rob Scotton is the bestselling author and illustrator behind Splat the Cat, Russell the Sheep and Max and Moonbean. He studied Illustration at De Montfort University, and lives and paints in Rutland, England, with his wife Liz, who is also an artist.</p>
      <p>Splat began with a neighbour&#8217;s cat, a garden fence and a rather undignified landing. Seymour has been along for the ride since the very first book.</p>
    </div>
    <div class="stage"><figure class="art" style="margin:0;width:min(100%,420px);border-radius:50% 50% 46% 46% / 42% 42% 58% 58%">{pic("author","Rob Scotton","(max-width:860px) 80vw, 36vw",lazy=False)}</figure></div>
  </div>
</section>

<section class="band" aria-labelledby="bio-h">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="prose big">
        <p class="kicker">The long version</p>
        <h2 id="bio-h">From sketchbook to bookshelf</h2>
        <p>Rob&#8217;s characters have a knack for finding adventure in everyday life, particularly when everyday life isn&#8217;t going quite according to plan.</p>
        <p>His own adventure in picture books began at a New York licensing show in 2004, when HarperCollins editor Maria Modugno spotted some of his character artwork. A conversation about a collection of images featuring a sheep named Russell, a cat named Splat, a pup called Max and the worlds they might inhabit led to a publishing home for his creations.</p>
        <p>The first of those creations to reach the shelves was Russell the Sheep. The idea came on a bike ride through a field near Rob&#8217;s home in Rutland, where a flock of sheep sheltering from the sun shuffled along with the shadow of a tree as it moved. An old Easter card design gave Rob his woolly hero, the name stuck despite the pun, and the story arrived with one simple question: what if a sheep could not fall asleep, no matter how hard he tried? Published by HarperCollins in 2005, Russell the Sheep became Rob&#8217;s first New York Times bestseller, and Russell went on to star in Russell and the Lost Treasure and Russell&#8217;s Christmas Magic. <a href="russell.html">Read Russell&#8217;s story</a>.</p>
        <p>The inspiration for Splat was most unexpected. While mowing the lawn, Rob watched a neighbour&#8217;s cat lose its balance on a fence and land with considerably less elegance than cats generally advertise. The word &#8220;Splat&#8221; sprang to mind, the lawn was temporarily forgotten, and a character began to take shape. Inspiration, it turns out, is all around.</p>
        <p>With expressive faces, wayward fur and a fondness for visual mischief, Rob&#8217;s illustrations bring humour to the things that can feel enormous when you&#8217;re small: starting school, making friends, finding courage and getting something wrong. His characters may have paws or wool, but their feelings are reassuringly familiar.</p>
        <p>Beyond books, Rob&#8217;s artwork has appeared on everything from greeting cards to ceramics and textiles. Quite a journey for a cat whose first significant move was falling off a fence.</p>
      </div>
      <div style="display:grid;gap:22px">
        {zoom("early-sketches","Early pencil sketches of Splat","Early Splat sketches","(max-width:860px) 100vw, 45vw")}
        {zoom("rob-caption-splat","Splat pulling a face next to the name Rob Scotton","Rob Scotton, as introduced by Splat","(max-width:860px) 100vw, 45vw")}
        {zoom("splat-gets-ready-sketch","Purple pencil sketches of Splat in a sketchbook","Splat gets ready, from the sketchbook","(max-width:860px) 100vw, 45vw")}
      </div>
    </div>
  </div>
</section>

<section class="band paper-band" aria-labelledby="sofar-h">
  <div class="wrap">
    <h2 id="sofar-h">The story so far</h2>
    <ol class="timeline">
      <li><b>Art school</b><span>Studied Illustration at De Montfort University.</span></li>
      <li><b>2005: Russell the Sheep</b><span>His debut picture book, inspired by the sheep in the fields around his studio, and his first New York Times bestseller.</span></li>
      <li><b>2008: Splat the Cat</b><span>Splat&#8217;s first day at Cat School, with Seymour hiding in his lunchbox.</span></li>
      <li><b>A whole library</b><span>Dozens of Splat books since, up to Splat the Cat and the Obstacle Course in 2021. <a href="https://splatthecat.com/books.html" target="_blank" rel="noopener">See them all on splatthecat.com</a></span></li>
      <li><b>Max and Moonbean</b><span>A shy pup, a shooting star and a small blue astronaut who talks in bubbles. <a href="max.html">Meet Max</a></span></li>
    </ol>
  </div>
</section>

<section class="band" aria-labelledby="beyond-h">
  <div class="wrap">
    <h2 id="beyond-h">Beyond the page</h2>
    <div class="grid c3">
      <a class="card" href="gallery.html"><div style="aspect-ratio:1.5;overflow:hidden">{pic("print-splat-doing-splat-stuff","Splat brushing his teeth among his sketches","(max-width:560px) 100vw, 33vw",style="width:100%;height:100%;object-fit:cover")}</div><div class="body"><h3>The gallery</h3><p>Prints, page art and character studies.</p></div></a>
      <a class="card" href="russell.html#myer-h"><div style="aspect-ratio:1.5;overflow:hidden">{pic("myer-window-5","Myer's Christmas window in Melbourne","(max-width:560px) 100vw, 33vw",style="width:100%;height:100%;object-fit:cover")}</div><div class="body"><h3>Myer's Christmas windows</h3><p>Russell's Christmas Magic, built big in Melbourne and Brisbane.</p></div></a>
      <a class="card" href="activities.html"><div style="aspect-ratio:1.5;overflow:hidden">{pic("act-maze","Max and Moonbean moon maze activity sheet","(max-width:560px) 100vw, 33vw",style="width:100%;height:100%;object-fit:cover;object-position:top")}</div><div class="body"><h3>Things to make and do</h3><p>Colouring, puzzles and classroom ideas for Russell and Max.</p></div></a>
    </div>
  </div>
</section>

<section class="band red-band on-dark tight" aria-label="Splat website">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div><h3 style="margin:0">Here for Splat?</h3><p style="margin:0">He has his own website, and he'd like you to visit.</p></div>
    <a class="btn yellow big" href="{SPLAT}" target="_blank" rel="noopener">splatthecat.com {EXT}</a>
  </div>
</section>
'''
pages['about.html'] = shell('about.html', "Meet Rob Scotton", "About Rob Scotton, author and illustrator of Splat the Cat, Russell the Sheep and Max and Moonbean. How a cat falling off a fence started it all.", about)

# ================= ACTIVITIES =================
def kb(path): return f"{round(os.path.getsize(path)/1024)} KB"

RUSSELL_RES = [
  ("Teaching Ideas", "Ideas across the curriculum",
   "Find more homophones like Russell and rustle, hunt for sound words, retell the story from the frog&#8217;s point of view, count as high as you can, design a new hat for Russell on a printable sheet, and talk about what helps us relax.",
   ["English","Maths","Art","Geography","Wellbeing"], "By Mark Warner, Teaching Ideas", "teachingideas.co.uk",
   "https://www.teachingideas.co.uk/books/russell-the-sheep/", ""),
  ("Surviving a Teacher&#8217;s Salary", "Crazy counting, Froggy&#8217;s eyes and a sleep cap",
   "Count together in pairs, hunt the book for its biggest numbers, retell the night through the frog&#8217;s eyes, then make a stripy night cap for a favourite toy from an old sock. For ages 3 to 9.",
   ["Maths","Writing","Craft"], "By Crystal at Surviving a Teacher&#8217;s Salary", "survivingateacherssalary.com",
   "https://www.survivingateacherssalary.com/russell-the-sheep-lesson-plans-and-activity/", ""),
  ("Teaching notes", "Russell the Sheep teaching notes",
   "Questions for before and after reading, rhyming words and opposites, a word search and crossword, a look at how wool is made, and crafts from thumbprint sheep to cotton-wool lambs.",
   ["Reading","Science","Craft","Drama"], "By Christine Sarandis, shared by Pegi Williams Book Shop", "pegiwilliams.com.au (PDF)",
   "https://www.pegiwilliams.com.au/pdfs/teachernotes/9780007206223.pdf", ""),
  ("MathsThroughStories.org", "Counting forwards and backwards",
   "Use Russell&#8217;s sleepless counting to practise counting up to, and back from, 10 or 20. For ages 4 and up.",
   ["Maths"], "By MathsThroughStories.org, University of Reading Institute of Education", "mathsthroughstories.org",
   "https://www.mathsthroughstories.org/russell-the-sheep.html", ""),
  ("Growing Book by Book", "Russell and the Lost Treasure: a family treasure book",
   "Inspired by Russell&#8217;s treasure hunt, make a little book of the people who are your family treasure, with a photo and a label on every page.",
   ["Reading","Writing","Family"], "By Jodie Rodriguez, Growing Book by Book", "growingbookbybook.com",
   "https://growingbookbybook.com/russell-and-the-lost-treasure-digging-into-treasure-hunting/", "An older page from 2013, so a few of its links may no longer work."),
]

def res_card(provider, title, desc, tags, by, site, url, note):
    t = "".join(f"<li>{x}</li>" for x in tags)
    n = f'<p class="res-note">{note}</p>' if note else ''
    return f'<article class="res"><p class="res-from">{provider}</p><h3>{title}</h3><p>{desc}</p><ul class="tags">{t}</ul>{n}<p class="res-by">{by} <span>{site}</span></p><a class="btn small" href="{url}" target="_blank" rel="noopener" aria-label="Visit resource: {title} (opens {provider} in a new tab)">Visit resource {EXT}</a></article>'

MAX_SHEETS = [
  ("colouring-sheets","max-colouring-sheets.pdf","Colour in Max","Two colouring sheets drawn by Rob: Max and Mr Ted flying through a shower of jigsaw pieces, and Max at his school desk. Each sheet has a question to talk about while you colour.","landscape, 2 pages"),
  ("maze","max-moon-maze.pdf","Fly Max to the moon","Moonbean is waiting on the moon. Find the way through the maze from Max&#8217;s bubble.","1 page"),
  ("code","max-bubble-speak-code.pdf","Bubble-speak secret code","Moonbean talks in bubbles. Use the key to read his message, then write one of your own for a friend.","1 page"),
  ("show","max-show-and-tell.pdf","My show-and-tell","Max found Moonbean. Draw what you would bring, then write about it.","1 page"),
]
def sheet_card(key, pdf, title, desc, pages):
    path = os.path.join('downloads', pdf)
    return f'<article class="sheet"><a class="sheet-pic" href="downloads/{pdf}" download aria-hidden="true" tabindex="-1">{pic("act-"+key, title + " activity sheet preview", "(max-width:560px) 60vw, 240px")}</a><div><h3>{title}</h3><p>{desc}</p><p class="sheet-meta">PDF, US Letter, {pages}, {kb(path)}</p><a class="btn moon small" href="downloads/{pdf}" download>Download {title}</a></div></article>'

activities = f"""
<section class="phero act-hero">
  <div class="wrap">
    <div>
      <p class="kicker">Free to print</p>
      <h1>Things to make and do</h1>
      <p class="lede">Colouring, puzzles and classroom ideas for Russell the Sheep and Max and Moonbean. Print them at home or share them with your class.</p>
      <div class="hero-actions"><a class="btn teal" href="#russell-act">Russell the Sheep</a><a class="btn" href="#max-act" style="background:var(--night)">Max and Moonbean</a><a class="btn ghost" href="https://splatthecat.com/activities.html" target="_blank" rel="noopener">Splat activities {EXT}</a></div>
    </div>
    <div class="stage act-fan" aria-hidden="true">
      {pic("act-maze","","240px")}{pic("act-colouring","","240px")}{pic("act-code","","240px")}
    </div>
  </div>
</section>

<section class="band snow-band" id="russell-act" aria-labelledby="ra-h">
  <div class="snow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker" style="color:var(--teal-2)">Russell the Sheep</p>
    <h2 id="ra-h">Count, colour and craft with Russell</h2>
    <p class="lede">Start with Rob&#8217;s own colouring sheet, then try ideas from teachers and educators who have used Russell in their classrooms.</p>

    <h3 class="act-sub">From Rob&#8217;s studio</h3>
    <div class="dl">
      <a href="downloads/russell-colouring-sheet.jpg" download><img src="img/russell-colouring-300.webp" alt="" width="300" height="189" loading="lazy"><div><b>Russell&#8217;s Christmas Magic colouring sheet</b><span>Free to print and colour. Download</span></div></a>
    </div>

    <h3 class="act-sub">From teachers and educators</h3>
    <div class="res-grid">{"".join(res_card(*r) for r in RUSSELL_RES)}</div>
  </div>
</section>

<section class="band night-band on-dark" id="max-act" aria-labelledby="ma-h">
  <div class="bubbles" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker">Max and Moonbean</p>
    <h2 id="ma-h">Printables for little astronauts</h2>
    <p class="lede">Brand-new activities made for this site from Rob&#8217;s own sketches and paintings. Each one is a single PDF, ready to print.</p>
    <div class="sheet-grid">{"".join(sheet_card(*s) for s in MAX_SHEETS)}</div>

    <div class="talk">
      <h3>Talking about the story</h3>
      <p>Questions for reading together at home or in class.</p>
      <ul>
        <li>Max&#8217;s show-and-tells always seem to go wrong. Have you ever felt nervous about doing something in front of other people? What helped?</li>
        <li>When the blue thingy appears, Max wants to hide, but he steps forward and asks its name. What does being brave mean to you?</li>
        <li>Moonbean calls Max a &#8220;pup of courage&#8221;. Who helps you feel brave?</li>
        <li>If a shooting star landed in your room tonight, what would you hope to find?</li>
        <li>Moonbean speaks in bubble-speak. Could you and a friend invent a secret language of your own?</li>
      </ul>
    </div>
  </div>
</section>

<section class="band paper-band tight" aria-labelledby="links-h">
  <div class="wrap">
    <h2 id="links-h" style="font-size:clamp(1.4rem,2.4vw,1.8rem)">About these links</h2>
    <p>The teacher resources on this page are made, owned and hosted by the people credited on each one. We link to their sites rather than copying their work, so you always get their latest version and they get the credit. Each site has its own terms, and most are free for classroom and home use. Links checked October 2026.</p>
    <p>The Max and Moonbean printables and the Russell colouring sheet are free for home and classroom use. Artwork &#169; Rob Scotton.</p>
  </div>
</section>

<section class="band yellow-band tight" aria-label="Splat activities">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:18px"><img src="img/splat-with-book-480.webp" alt="" width="480" height="511" style="width:96px" loading="lazy"><div><h3 style="margin:0">Looking for Splat?</h3><p style="margin:0">Splat&#8217;s colouring pages and lesson plans live on his own website.</p></div></div>
    <a class="btn red big" href="https://splatthecat.com/activities.html" target="_blank" rel="noopener">Splat activities {EXT}</a>
  </div>
</section>
"""
pages['activities.html'] = shell('activities.html', "Activities | Rob Scotton", "Free activities for Russell the Sheep and Max and Moonbean by Rob Scotton: colouring pages, puzzles, printables and classroom ideas.", activities, "#1FA7A3")

# ================= GALLERY =================
# Three walls of hanging framed pictures, after the gallery on splatthecat.com.
# (image, alt text, plaque title, handwritten note)
WALLS = [
 ("russell", "Russell the Sheep", "Sleepless nights, starry skies, a lost treasure and a little Christmas magic.", [
  ("russell-cover","Russell the Sheep leaping over a green hill with Frankie the frog riding on his hat","Russell the Sheep","the one who couldn't sleep"),
  ("russell-what-to-do","Russell standing wide awake in his striped nightcap","What's a sheep to do?","wide awake, again"),
  ("russell-swing","Russell swinging from a tree while Frankie clings to the trunk","Swinging","one more try"),
  ("russell-branch","Russell asleep on a branch with a row of birds","Up a tree","sharing with the birds"),
  ("russell-stars","Russell sitting on a hill under a night sky with Frankie","Counting stars","Frankie keeps watch"),
  ("russell-stars-2","Russell seen from behind, gazing at the night sky","Still counting","how many now?"),
  ("russell-sleeps","Russell asleep under a patchwork quilt, his long striped hat framing the picture","Russell sleeps","at last!"),
  ("russell-lt-shares","Russell reading from a glowing book to the flock under the night sky","Russell shares his treasure","a story for everyone"),
  ("russell-lt-plan","Russell peeping over a long scroll of drawings for a treasure-hunting machine","The big plan","every bolt drawn out"),
  ("russell-lt-welding","Russell in goggles welding a gadget while Frankie sits in a lantern","Hard at work","Frankie keeps the lamp lit"),
  ("russell-lt-auntie-uncle","Two sheep in sunglasses riding in a battered old car","Auntie and Uncle","out for a spin"),
  ("russell-lt-determined","Russell upside down in his striped nightcap, watched by a crow","Determined","upside down, never beaten"),
  ("russell-lt-reflecting","Russell on a hilltop at night with the flock gathered below","Reflecting","a quiet night on the hill"),
  ("russell-art-1","Russell making a snow angel with Frankie the frog","Snow angels","Frankie joins in"),
  ("russell-art-2","Russell carrying Frankie past glowing lanterns in the snow","Russell's Christmas Magic","lanterns in the wood"),
 ]),
 ("splat", "Splat the Cat", "Prints and page art from Splat's books. There's plenty more on Splat's own site.", [
  ("print-ahh-kitten","Kitten, a white fluffy cat with a bow, and Splat","Ahh, Kitten","toothbrush in paw"),
  ("print-waiting-for-splat","Splat racing past the family in dressing gowns","Waiting for Splat","the whole family, in dressing gowns"),
  ("print-thankyou-p20-08-copy","Splat with a foghorn","Honk!","a page from Splat Says Thank You!"),
  ("print-splat-another-fine-mess","Splat hanging from a tree with a kite","Another fine mess","kite, meet tree"),
  ("print-splat-and-the-beanstalk-copy","Splat dressed up for the beanstalk","Splat and the beanstalk","dressed for the part"),
  ("print-time-for-bed-copy","Splat's mum sends him to bed","Time for bed","no arguments"),
  ("tail-wiggled-bed","Splat in bed, his tail wiggling","His tail wiggled wildly","a tail with a mind of its own"),
  ("print-splat-in-bath","Splat in the bath","Splat in the bath","Gulp!"),
  ("print-confetti-scene-flat","A crowd of cats cheering under confetti","Confetti!","the whole class celebrates"),
  ("print-splat-doing-splat-stuff","Splat drawing, taping and brushing his teeth","Splat doing Splat stuff","drawing, taping and tooth-brushing"),
  ("print-splat-bath-time","Splat in a bath full of bubbles with Seymour on the tap","Bath time","Seymour brings the soap"),
  ("print-splat-on-bike-2","Splat on a penny-farthing in the street","Out on the bike","a spin through town"),
  ("something-at-door","Splat peeking out of a doorway","There's something at the door","who can it be?"),
  ("splat-gets-ready-sketch","A sketch of Splat with his arms up","Splat gets ready","arms up, all set"),
  ("print-splat-gotcha","Splat bursting through the doorway","Gotcha!","surprise!"),
  ("splat-making-plans","Splat drawing up a plan","Making plans","a cunning plan, by Splat"),
  ("splats-world","A map of Splat's world","Splat's World","where everything happens"),
 ]),
 ("max", "Max and Moonbean", "Moonlight, bubbles and a brand new friend from the moon.", [
  ("max-cover","Max lying in the grass under a full moon as Moonbean dances on his nose","Max and Moonbean","moonlight and bubbles"),
  ("max-where","Max, Mr Ted and Moonbean at the window","Where were you?","a late-night visitor"),
  ("max-moon","Max looking out of the window as Moonbean peeps in","Who's there?","a knock at the window"),
  ("max-blue-thingy","Two Moonbeans with bubbles showing the moon","Bubble talk","Moonbean has a lot to say"),
  ("max-courage","Max dancing with three Moonbeans and bubbles","Dance party","bubbles everywhere"),
  ("max-hide","Moonbean in Max's messy bedroom while Max hides under a sheet","Hide and seek","who's under the sheet?"),
  ("max-shooting-star","Max leaping up as Mr Ted flies through the air","Whoosh!","Mr Ted goes flying"),
  ("max-sleep","Max asleep on his star-covered bed hugging Mr Ted","Lights out","Mr Ted is on guard"),
  ("max-friend","Max and Mr Ted in the doorway","Max","with Mr Ted, of course"),
 ]),
]
TILT = ["-1.6deg","1.2deg","-0.5deg","1.7deg","-1.1deg","0.6deg","1.3deg","-1.9deg"]

def hang(i, n, a, t, note):
    return (f'<figure class="g-hang" style="--r:{TILT[i % len(TILT)]}"><span class="g-nail" aria-hidden="true"></span>'
            f'<div class="g-frame"><button class="zoom g-frame-in" data-full="{full(n)}" data-caption="{html.escape(t)}: {html.escape(note)}" aria-label="View larger: {html.escape(a)}">'
            f'{pic(n, a, "(max-width:520px) 86vw, (max-width:960px) 42vw, 28vw")}</button></div>'
            f'<figcaption class="g-plaque"><b>{t}</b><span>{note}</span></figcaption></figure>')

def wall(k, title, intro, items):
    more = (f'<p class="g-more"><a class="btn red" href="{SPLAT}" target="_blank" rel="noopener">More on splatthecat.com {EXT}</a></p>'
            if k == "splat" else "")
    grid = "".join(hang(i, *it) for i, it in enumerate(items))
    return (f'\n<section class="g-wall wall-{k}" id="{k}" aria-labelledby="h-{k}">\n  <div class="wrap">\n'
            f'    <header class="g-head"><h2 id="h-{k}">{title}</h2><p>{intro}</p></header>\n'
            f'    <div class="g-grid">{grid}</div>\n    {more}\n  </div>\n</section>')

walls = "".join(wall(*w) for w in WALLS)
gallery = f"""
<section class="phero plum-band on-dark" style="padding-bottom:clamp(32px,5vw,64px)">
  <div class="wrap" style="grid-template-columns:1fr">
    <div><h1>Gallery</h1><p class="lede">Three walls of pictures from Russell, Splat and Max. Tap a frame to see it larger; use the arrow keys to wander.</p>
    <nav class="g-jump" aria-label="Gallery walls"><a href="#russell">Russell the Sheep</a><a href="#splat">Splat the Cat</a><a href="#max">Max and Moonbean</a></nav></div>
  </div>
</section>
{walls}
<section class="band yellow-band tight" aria-label="Splat website">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div><h3 style="margin:0">More Splat?</h3><p style="margin:0">Games, books and much more are all on Splat's own site.</p></div>
    <a class="btn red" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a>
  </div>
</section>
"""
CAVEAT = '<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500..700&display=swap" rel="stylesheet">'
pages['gallery.html'] = shell('gallery.html', "Gallery | Rob Scotton", "Artwork by Rob Scotton hung on three walls: Russell the Sheep, Splat the Cat and Max and Moonbean.", gallery, "#6A3A94", CAVEAT)

# ================= CONTACT =================
LICENSING = f'''<section class="band" aria-labelledby="lic-h">
  <div class="wrap split">
    <div>
      <h2 id="lic-h">Licensing</h2>
      <p class="lede">Splat the Cat, Russell the Sheep and Max and Moonbean are available for licensing across publishing, television, toys, greetings, homeware, textiles and apparel.</p>
      <p>Splat the Cat is published by HarperCollins Children's Books and represented for licensing by Moxie &amp; Company. For enquiries about any of the characters, email Rob and he'll point you to the right person.</p>
      <p><a class="btn" href="mailto:{MAIL}?subject=Licensing%20enquiry">Licensing enquiry {ARROW}</a></p>
    </div>
    {zoom("brand-stuff","Splat the Cat brand style guide: logos, fonts and colour palette","Splat the Cat brand guide","(max-width:860px) 100vw, 50vw",cls="art tall")}
  </div>
</section>'''

contact = f'''
<section class="phero teal-band on-dark">
  <div class="wrap">
    <div><h1>Get in touch</h1><p class="lede">For school visits, events, press or simply to say hello.</p>
      <p><a class="btn yellow big" href="mailto:{MAIL}">Email Rob {ARROW}</a></p>
      <p style="font-family:var(--display);font-weight:700">{MAIL}</p>
    </div>
    <div class="stage">{pic("splat-ducks-cutout","Splat holding an armful of toy ducks","(max-width:860px) 70vw, 36vw",lazy=False)}</div>
  </div>
</section>

{LICENSING if SHOW_LICENSING else ""}

<section class="band paper-band" aria-labelledby="visits-h">
  <div class="wrap split rev">
    <div>
      <h2 id="visits-h">Schools, festivals and events</h2>
      <p class="lede">Rob has toured Splat the Cat across the United States and the UK, drawing live, reading aloud and answering the only question that really matters: what happened to the cat on the fence?</p>
      <p>Email with dates, location and the age of your audience.</p>
    </div>
    {zoom("splat-arms","Splat, arms outstretched","Splat, arms outstretched","(max-width:860px) 100vw, 50vw")}
  </div>
</section>

<section class="band red-band on-dark tight" aria-label="Splat website">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;justify-content:space-between">
    <div><h3 style="margin:0">Splat fan mail?</h3><p style="margin:0">Splat reads his at splatthecat.com.</p></div>
    <a class="btn yellow big" href="{SPLAT}" target="_blank" rel="noopener">splatthecat.com {EXT}</a>
  </div>
</section>
'''
pages['contact.html'] = shell('contact.html', "Contact | Rob Scotton", "Contact Rob Scotton for school visits, events and press enquiries about Splat the Cat, Russell the Sheep and Max and Moonbean.", contact, "#1FA7A3")

# ================= 404 =================
nf = f"""
<section class="phero yellow-band" style="padding-bottom:clamp(40px,6vw,80px)">
  <div class="wrap" style="grid-template-columns:1fr;text-align:center">
    <div>{pic("splat-thoughtful","Splat the Cat looking puzzled","(max-width:560px) 60vw, 280px",style="width:min(60%,280px);margin:0 auto 12px")}
    <h1>Oops. Splat can't find that page.</h1>
    <p class="lede" style="margin:0 auto">It may have moved when the site was rebuilt. Try the books, or hop over to Splat's own website.</p>
    <div class="hero-actions" style="justify-content:center"><a class="btn" href="index.html">Back to Books {ARROW}</a><a class="btn red" href="{SPLAT}" target="_blank" rel="noopener">Visit splatthecat.com {EXT}</a></div></div>
  </div>
</section>
"""
pages['404.html'] = shell('404.html', "Page not found | Rob Scotton", "This page could not be found on robscotton.com.", nf, "#F6B51F", '<base href="/"><meta name="robots" content="noindex">')

for f, h in pages.items():
    open(f, 'w').write(h)
print("built", list(pages))
