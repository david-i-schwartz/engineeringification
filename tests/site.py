"""Site checks: python3 tests/site.py SITE_FOLDER (default: this repository's top folder).
Serves the built site over http and checks, with Chromium standing in for each device:
the front page lists every tool, every tool has its icons and manifest, each tool opens on an iPhone-sized
and a desktop-sized window with no console errors, the Home Screen card shows on a phone, and a phone's
file preview (scripts off) points to the tool's web address. A real iPhone and iPad check is still needed."""
import functools, http.server, json, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..'))
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
CFG = json.load(open(os.path.join(SITE, 'site.json'), encoding='utf-8'))
FOLDERS = [a.get('folder') or a.get('code', '').lower() for a in CFG['apps']]
IPHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 26_1 like Mac OS X) AppleWebKit/605.1.15 '
          '(KHTML, like Gecko) Version/26.1 Mobile/15E148 Safari/604.1')
fails = []

def check(ok, what):
    print(('  ok   ' if ok else '  FAIL ') + what)
    if not ok:
        fails.append(what)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=SITE))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_address[1]}/'

def open_page(br, path, phone=True, js=True, scheme='light'):
    ctx = br.new_context(viewport={'width': 390, 'height': 844} if phone else {'width': 1280, 'height': 900},
                         user_agent=IPHONE if phone else None, has_touch=phone, is_mobile=phone,
                         java_script_enabled=js, color_scheme=scheme)
    pg = ctx.new_page(); errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'service' not in m.text.lower() else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(path if path.startswith(('http', 'file')) else BASE + path)
    pg.wait_for_timeout(800)
    return ctx, pg, errs

with sync_playwright() as p:
    br = p.chromium.launch()
    print('== the front page')
    ctx, pg, errs = open_page(br, '')
    check(pg.title() == CFG['title'], 'title is ' + CFG['title'])
    check(pg.locator('.app').count() == len(FOLDERS), f'it lists the {len(FOLDERS)} tool(s)')
    for f in FOLDERS:
        check(pg.evaluate(f"fetch('{f}/icon-192.png').then(r=>r.ok)"), f'{f}: icon')
        m = json.loads(pg.evaluate(f"fetch('{f}/manifest.webmanifest').then(r=>r.text())"))
        check(m['display'] == 'standalone' and m['start_url'] == './' and len(m['icons']) == 3, f'{f}: manifest ' + m['name'])
    check(not errs, 'no console errors: ' + '; '.join(errs[:3]))
    pg.screenshot(path=os.path.join(OUT, 'front-page.png')); ctx.close()

    for f in FOLDERS:
        print(f'== {f}')
        ctx, pg, errs = open_page(br, f + '/', phone=True, scheme='dark')
        card = pg.locator('#hh')
        check(card.count() == 1 and card.is_visible() and 'Put ' in card.inner_text(), 'phone: the Home Screen card shows')
        over = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
        check(over <= 0, f'phone: no sideways scrolling ({over}px)')
        check(not errs, 'phone, dark: no console errors: ' + '; '.join(errs[:3]))
        pg.screenshot(path=os.path.join(OUT, f'{f}-phone.png')); ctx.close()
        ctx, pg, errs = open_page(br, f + '/', phone=False)
        check(pg.locator('#hh').count() == 0 or not pg.locator('#hh').is_visible(), 'desktop: no Home Screen card')
        check(not errs, 'desktop, light: no console errors: ' + '; '.join(errs[:3]))
        pg.screenshot(path=os.path.join(OUT, f'{f}-desktop.png')); ctx.close()
        # Only tools made with HTML App Generator carry the file-preview note.
        if 'id="nojsNote"' in open(os.path.join(SITE, f, 'index.html'), encoding='utf-8').read():
            ctx, pg, errs = open_page(br, 'file://' + os.path.join(SITE, f, 'index.html'), js=False)
            href = pg.locator('#nojsNote a').get_attribute('href')
            check(href == CFG['base'] + f + '/', "file preview: the note links to the tool's web address: " + str(href))
            ctx.close()
        else:
            print('  --   file preview: not made with the generator, so it has no preview note')
    br.close()
srv.shutdown()
print('\n' + ('All checks passed.' if not fails else f'{len(fails)} checks failed.'))
sys.exit(1 if fails else 0)
