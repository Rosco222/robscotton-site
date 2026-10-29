"""Assemble the GitHub/Render repository: only the files the live pages use, plus robots.txt and sitemap.xml.
Usage: python3 make_dist.py <repo-folder>"""
import os, re, sys, glob, shutil, urllib.parse
REPO = sys.argv[1]; OUT = os.path.join(REPO, 'site'); TOOLS = os.path.join(REPO, 'tools')
SITE_URL = 'https://www.robscotton.com'
PAGES = ['index.html', 'splat.html', 'russell.html', 'russells-story.html', 'max.html', 'about.html', 'activities.html', 'gallery.html', 'contact.html', '404.html']
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT); os.makedirs(TOOLS, exist_ok=True)
need = set(PAGES) | {'assets/site.css', 'assets/site.js'}
for f in PAGES + ['assets/site.css', 'assets/site.js']:
    t = open(f).read()
    refs = re.findall(r'(?:href|src|data-full|data-src)="([^"#]+)"', t) + re.findall(r"url\(['\"]?([^'\")]+)", t)
    refs += [x.strip().split()[0] for s in re.findall(r'srcset="([^"]+)"', t) for x in s.split(',')]
    refs += re.findall(r"['\"]((?:img|audio|downloads|assets)/[^'\"]+)['\"]", t)
    for u in refs:
        if u.startswith(('http', 'mailto:', 'tel:', 'data:', '/')) and not u.startswith('/img'): continue
        p = os.path.normpath(urllib.parse.unquote(u.split('?')[0]).lstrip('/'))
        if f.startswith('assets/') and not os.path.exists(p): p = os.path.normpath(os.path.join('assets', p))
        if os.path.isfile(p): need.add(p)
for p in sorted(need):
    os.makedirs(os.path.join(OUT, os.path.dirname(p)), exist_ok=True); shutil.copy2(p, os.path.join(OUT, p))
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
urls = ''.join(f'  <url><loc>{SITE_URL}/{"" if p == "index.html" else p}</loc></url>\n' for p in PAGES if p != '404.html')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
for t in ['build.py', 'make_images.py', 'make_activities.py', 'make_dist.py']:
    shutil.copy2(t, os.path.join(TOOLS, t))
size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
print(len(need) + 2, 'files,', round(size / 1e6, 1), 'MB')
