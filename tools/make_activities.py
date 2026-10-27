"""Build the Max and Moonbean printable activity sheets (US Letter, 200 dpi) and their web previews.

Outputs
  downloads/max-colouring-pages.pdf      two colouring pages from Rob's storyboard sketches
  downloads/max-moon-maze.pdf            help Max reach Moonbean on the moon
  downloads/max-bubble-speak-code.pdf    decode Moonbean's bubble-speak
  downloads/max-show-and-tell.pdf        plan your own show-and-tell
  img/act-*.webp                         small previews for the Activities page
"""
import os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
Image.MAX_IMAGE_PIXELS = None

SITE = os.path.dirname(os.path.abspath(__file__))
SRC = '/mnt/user-data/uploads/For Claude/_claude_work/src'
SCR = sys.argv[1]                      # folder holding the cleaned sketch PNGs
DPI = 200
W, H = int(8.5 * DPI), int(11 * DPI)   # US Letter
M = int(0.55 * DPI)                    # margin, safe for A4 printing too
GF = '/usr/share/fonts/truetype/google-fonts/'
def font(sz, w='Bold'): return ImageFont.truetype(GF + f'Poppins-{w}.ttf', sz)
INK = (27, 26, 31); NIGHT = (11, 23, 51); BLUE = (52, 92, 196); GREY = (110, 106, 118)

def page():
    return Image.new('RGB', (W, H), 'white')

def header(im, title, sub):
    d = ImageDraw.Draw(im)
    d.text((M, M), title, font=font(84), fill=INK)
    d.text((M, M + 112), sub, font=font(38, 'Regular'), fill=GREY)
    return M + 190

def footer(im, extra=''):
    d = ImageDraw.Draw(im)
    d.line((M, H - M - 70, W - M, H - M - 70), fill=(220, 218, 224), width=3)
    if extra: d.text((M, H - M - 56), extra, font=font(26, 'Medium'), fill=GREY)
    d.text((M, H - M - 22), 'Max and Moonbean. Artwork \u00a9 Rob Scotton. Published by HarperCollins.  robscotton.com', font=font(26, 'Regular'), fill=GREY)

def paste_fit(im, art, box):
    x0, y0, x1, y1 = box
    a = art.copy(); a.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
    x = x0 + (x1 - x0 - a.width) // 2; y = y0 + (y1 - y0 - a.height) // 2
    if a.mode == 'RGBA': im.paste(a, (x, y), a)
    else: im.paste(a.convert('RGB'), (x, y))
    return (x, y, x + a.width, y + a.height)

def cut(box):
    return Image.open(os.path.join(SRC, 'max-bubbles.webp')).convert('RGBA').crop(box)

MAX_BUBBLE = cut((2150, 600, 3500, 1900))
BEAN_BUBBLE = cut((1675, 2450, 2475, 3300))
BEAN_TOP = cut((1700, 175, 2400, 900))
MAX_HAND = cut((200, 450, 1150, 2500))

def save_pdf(pages, name):
    out = os.path.join(SITE, 'downloads', name)
    pages[0].save(out, 'PDF', resolution=DPI, save_all=True, append_images=pages[1:])
    return out

def preview(im, name):
    p = im.copy(); p.thumbnail((640, 640), Image.LANCZOS)
    p.save(os.path.join(SITE, 'img', f'act-{name}-{p.width}.webp'), 'WEBP', quality=80, method=6)
    return p.size

made = {}

# ---------------- 1. Colouring pages from the storyboard ----------------
pages = []
for fn, title, sub in [
    ('s_courage.png', 'Colour in Max', 'A pencil sketch from Rob’s storyboard. Max, Mr Ted and three Moonbeans.'),
    ('s_thingy.png', 'Colour in Moonbean', 'A pencil sketch from Rob’s storyboard. What colour are the bubbles?')]:
    im = page(); top = header(im, title, sub)
    sk = Image.open(os.path.join(SCR, fn)).convert('L')
    sk = sk.resize((sk.width * 2, sk.height * 2), Image.LANCZOS).filter(ImageFilter.SMOOTH_MORE)
    paste_fit(im, sk, (M, top + 20, W - M, H - M - 100))
    footer(im, 'From the Max and Moonbean storyboard.')
    pages.append(im)
made['colouring'] = (save_pdf(pages, 'max-colouring-pages.pdf'), preview(pages[0], 'colouring'))

# ---------------- 2. Moon maze ----------------
random.seed(7)
def maze(cols, rows):
    seen = [[False] * cols for _ in range(rows)]
    walls = {(c, r): {'N', 'S', 'E', 'W'} for r in range(rows) for c in range(cols)}
    stack = [(0, rows - 1)]; seen[rows - 1][0] = True
    opp = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    mv = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    while stack:
        c, r = stack[-1]
        nb = [(k, c + dx, r + dy) for k, (dx, dy) in mv.items() if 0 <= c + dx < cols and 0 <= r + dy < rows and not seen[r + dy][c + dx]]
        if not nb: stack.pop(); continue
        k, nc, nr = random.choice(nb)
        walls[(c, r)].discard(k); walls[(nc, nr)].discard(opp[k])
        seen[nr][nc] = True; stack.append((nc, nr))
    return walls
im = page(); top = header(im, 'Fly Max to the moon', 'Moonbean is waiting. Find the way from Max’s bubble to the moon.')
d = ImageDraw.Draw(im)
cols, rows = 11, 13
mx0, my0 = M + 60, top + 230
cell = min((W - 2 * M - 120) // cols, (H - my0 - M - 330) // rows)
wl = maze(cols, rows)
# moon behind the finish (top right)
fx, fy = mx0 + (cols - 1) * cell, my0
d.ellipse((fx - 30, fy - 210, fx + cell + 150, fy + 5), fill=(255, 246, 205), outline=(214, 196, 120), width=5)
paste_fit(im, BEAN_TOP, (fx - 10, fy - 230, fx + cell + 130, fy - 20))
for (c, r), ws in wl.items():
    x, y = mx0 + c * cell, my0 + r * cell
    for k in ws:
        if (c, r) == (cols - 1, 0) and k == 'N': continue      # exit
        if (c, r) == (0, rows - 1) and k == 'S': continue       # entrance
        seg = {'N': (x, y, x + cell, y), 'S': (x, y + cell, x + cell, y + cell), 'W': (x, y, x, y + cell), 'E': (x + cell, y, x + cell, y + cell)}[k]
        d.line(seg, fill=NIGHT, width=9)
paste_fit(im, MAX_BUBBLE, (mx0 - 70, my0 + rows * cell + 10, mx0 + cell + 260, H - M - 70))
d.text((mx0 + cell + 290, my0 + rows * cell + 70), 'Start here', font=font(40), fill=BLUE)
d.text((fx - 330, fy - 120), 'Finish', font=font(40), fill=BLUE)
footer(im)
made['maze'] = (save_pdf([im], 'max-moon-maze.pdf'), preview(im, 'maze'))

# ---------------- 3. Bubble-speak secret code ----------------
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
random.seed(11)
pats = []
import itertools
allp = [p for n in (1, 2, 3, 4) for p in itertools.combinations(range(6), n)]
random.shuffle(allp)
code = dict(zip(letters, allp[:26]))
def glyph(d, x, y, s, pat):
    pos = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
    for i, (cx, cy) in enumerate(pos):
        px, py = x + cx * s, y + cy * s
        if i in pat: d.ellipse((px + 3, py + 3, px + s - 3, py + s - 3), fill=BLUE)
        else: d.ellipse((px + s * .3, py + s * .3, px + s * .7, py + s * .7), outline=(200, 205, 222), width=3)
im = page(); top = header(im, 'Bubble-speak', 'Moonbean talks in bubbles. Use the key to read his secret message.')
d = ImageDraw.Draw(im)
s = 30; kx, ky = M + 10, top + 30; colw = (W - 2 * M) // 7
for i, L in enumerate(letters):
    cx = kx + (i % 7) * colw; cy = ky + (i // 7) * 170
    d.rounded_rectangle((cx, cy, cx + colw - 22, cy + 150), radius=22, fill=(240, 244, 252))
    d.text((cx + 18, cy + 40), L, font=font(56), fill=INK)
    glyph(d, cx + 92, cy + 30, s, code[L])
msg = ['MAX', 'IS', 'BRAVE']
y = ky + 4 * 170 + 90
d.text((M, y), 'The secret message', font=font(48), fill=INK); y += 100
gx = M
for word in msg:
    for ch in word:
        d.rounded_rectangle((gx, y, gx + 110, y + 230), radius=18, outline=(200, 205, 222), width=3)
        glyph(d, gx + 25, y + 18, s, code[ch])
        d.line((gx + 18, y + 200, gx + 92, y + 200), fill=INK, width=4)
        gx += 125
    gx += 70
y += 300
d.text((M, y), 'Now write your own bubble-speak message for a friend.', font=font(38, 'Regular'), fill=INK); y += 80
for i in range(3):
    d.line((M, y + i * 110, W - M, y + i * 110), fill=(210, 208, 216), width=3)
paste_fit(im, BEAN_BUBBLE, (W - M - 330, H - M - 420, W - M, H - M - 60))
ans = Image.new('RGBA', (520, 50), (255, 255, 255, 0)); ImageDraw.Draw(ans).text((0, 0), 'Answer: MAX IS BRAVE', font=font(30, 'Medium'), fill=GREY)
ans = ans.rotate(180); im.paste(ans, (M, H - M - 160), ans)
footer(im)
made['code'] = (save_pdf([im], 'max-bubble-speak-code.pdf'), preview(im, 'code'))

# ---------------- 4. My show-and-tell ----------------
im = page(); top = header(im, 'My show-and-tell', 'Max found Moonbean. What would you bring?')
d = ImageDraw.Draw(im)
y = top + 30
d.text((M, y), 'Draw it here', font=font(42), fill=INK)
box = (M, y + 70, W - M, y + 70 + 820)
d.rounded_rectangle(box, radius=34, outline=(200, 205, 222), width=5)
paste_fit(im, BEAN_TOP, (W - M - 230, box[3] - 300, W - M - 20, box[3] - 20))
y = box[3] + 60
for q in ['It is called', 'I found it', 'The best thing about it is', 'My friends should know']:
    d.text((M, y), q, font=font(38, 'Medium'), fill=INK)
    d.line((M + d.textlength(q, font=font(38, 'Medium')) + 20, y + 52, W - M, y + 52), fill=(200, 198, 206), width=3)
    y += 120
footer(im)
made['show'] = (save_pdf([im], 'max-show-and-tell.pdf'), preview(im, 'show'))

for k, (p, sz) in made.items():
    print(k, os.path.basename(p), round(os.path.getsize(p) / 1024), 'KB', 'preview', sz)
