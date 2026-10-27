"""Regenerate every site image at display-only resolution.

Rules
- Content images: capped at 1200 px on the long edge (480 / 800 / 1200 variants).
- Very tall documents (storyboards, style guides): capped at 960 px wide so they stay legible on screen.
- Page-header backgrounds: the colour wash is baked into the file, so the file itself is a faded,
  tinted image rather than clean artwork (960 / 1600 variants).
- No metadata is written. Colouring sheets in downloads/ are left at full print size.
"""
import os, json, sys
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
Image.MAX_IMAGE_PIXELS = None

SRC = '/mnt/user-data/uploads/For Claude/_claude_work/src'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'img_new'
os.makedirs(OUT, exist_ok=True)
CAP = 1200          # long-edge cap for artwork
TALL_W = 960        # width cap for very tall documents
manifest = {}

def save_variants(name, im, widths, alpha):
    W, H = im.size
    sizes = []
    for w in widths:
        w = min(w, W)
        if any(s[0] == w for s in sizes):
            continue
        h = round(H * w / W)
        r = im if w == W else im.resize((w, h), Image.LANCZOS)
        p = f'{OUT}/{name}-{w}.webp'
        r.save(p, 'WEBP', quality=78 if w >= 800 else 74, method=6)
        sizes.append((w, h, os.path.getsize(p)))
    manifest[name] = {'w': W, 'h': H, 'alpha': alpha, 'sizes': sizes}

def content(name, im, alpha):
    W, H = im.size
    if H / W > 2:                       # tall documents
        maxw = min(W, TALL_W)
    else:
        maxw = min(W, CAP, round(CAP * W / H))
    widths = [w for w in (480, 800) if w < maxw] + [maxw]
    if maxw < 480:
        widths = [maxw]
    scaled = im if maxw == W else im.resize((maxw, round(H * maxw / W)), Image.LANCZOS)
    save_variants(name, scaled, widths, alpha)

# ---------- ordinary artwork ----------
for f in sorted(os.listdir(SRC)):
    name, ext = os.path.splitext(f)
    if ext.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
        continue
    im = Image.open(os.path.join(SRC, f))
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    content(name, im, alpha)


# ---------- Russell paintings supplied October 2026 (RUSSELL For RobScotton.com) ----------
RSRC = '/mnt/user-data/uploads/For Claude/RUSSELL For RobScotton.com'
RUSSELL_NEW = {
    'russell-cover': 'RUSSELL COVER rgb reduced.jpg',
    'russell-cover-section': 'RUSSELL COVER for section.jpg',
    'russell-stars': 'RUSSELL counting stars.jpg',
    'russell-stars-2': 'RUSSELL counts stars 2.jpg',
    'russell-branch': 'RUSSELL on a branch cropped.jpg',
    'russell-swing': 'RUSSELL on swing.jpg',
    'russell-sleeps': 'RUSSELL sleeps.jpg',
    'russell-what-to-do': "what's a sheep to do?.jpg",
    # Russell and the Lost Treasure
    'russell-lt-reflecting': ' RUSSELL reflecting.jpg',
    'russell-lt-plan': 'RUSSELL 2 PAGE 9.jpg',
    'russell-lt-auntie-uncle': 'RUSSELL auntie and uncle.jpg',
    'russell-lt-shares': 'RUSSELL shares his treasure.jpg',
    'russell-lt-welding': 'RUSSELL welding.jpg',
    'russell-lt-determined': 'Russeell  determined1.jpg',
}
for name, f in RUSSELL_NEW.items():
    p = os.path.join(RSRC, f)
    if os.path.exists(p):
        content(name, Image.open(p).convert('RGB'), False)

# Seymour for the Splat page cast card
_sp = Image.open('/mnt/user-data/uploads/For Claude/Seymour/Semour Pose 1.png').convert('RGBA')
if True:
    content('seymour-pose', _sp.crop(_sp.getchannel('A').getbbox()), True)

# ---------- header backgrounds with the wash baked in ----------
def bake(name, im, widths=(960, 1600)):
    W, H = im.size
    top = min(W, max(widths))
    im = im if top == W else im.resize((top, round(H * top / W)), Image.LANCZOS)
    save_variants(name, im, widths, False)

def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Splat: grayscale, contrast 1.15, multiplied onto Splat yellow at 57%
eyes = Image.open(os.path.join(SRC, 'home-eyes.jpg')).convert('RGB').crop((330, 0, 1500, 640))
g = ImageEnhance.Contrast(ImageOps.grayscale(eyes).convert('RGB')).enhance(1.15)
yellow = Image.new('RGB', g.size, hex2rgb('F6B51F'))
from PIL import ImageChops
mult = ImageChops.multiply(yellow, g)
bake('hdr-splat', Image.blend(yellow, mult, 0.57))

# Russell: "Russell counts stars 2" (white border trimmed), set to the right with its own night sky
# extended to the left so the heading sits on sky and Russell stands clear of the text
import numpy as np
from scipy import ndimage
src = Image.open(os.path.join(RSRC, 'RUSSELL counts stars 2.jpg')).convert('RGB')
a = np.array(src).astype(int); nonw = a.min(axis=2) < 235
rows = np.where(nonw.mean(1) > .5)[0]; cols = np.where(nonw.mean(0) > .5)[0]
im = src.crop((cols[0] + 8, rows[0] + 8, cols[-1] - 8, rows[-1] - 8)); w, h = im.size
CW = int(h * 2.1)
edge = np.array(im.crop((0, 0, int(w * .08), h))).astype(float).mean(1)
edge = ndimage.gaussian_filter1d(edge, sigma=h * .05, axis=0, mode='nearest')
can = Image.fromarray(np.repeat(edge[:, None, :], CW, 1).astype('uint8'))
fw = int(w * .22)
mask = Image.new('L', (w, h), 255); mask.paste(Image.fromarray(np.tile(np.linspace(0, 255, fw)[None, :], (h, 1)).astype('uint8')), (0, 0))
can.paste(im, (CW - w, 0), mask)
bake('hdr-russell', can)

# Max: saturation 1.1, laid over night blue at 70%
mc = Image.open(os.path.join(SRC, 'max-cover.jpg')).convert('RGB')
mc = mc.resize((1600, round(mc.height * 1600 / mc.width)), Image.LANCZOS)
mc = ImageEnhance.Color(mc).enhance(1.1)
bake('hdr-max', Image.blend(Image.new('RGB', mc.size, hex2rgb('0B1733')), mc, 0.70))

json.dump(manifest, open(f'{OUT}/manifest.json', 'w'), indent=1)
tot = sum(os.path.getsize(os.path.join(OUT, x)) for x in os.listdir(OUT))
big = max((s[0], s[1], n) for n, m in manifest.items() for s in m['sizes'] if not n.startswith('hdr-'))
print(len(manifest), 'images,', round(tot / 1e6, 1), 'MB; largest content variant', big)
