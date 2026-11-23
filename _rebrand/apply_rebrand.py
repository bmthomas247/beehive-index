"""Apply The Ledger brand (Utah mark, black and gold) to utahhighschoolfootball.com's published files.

python _rebrand/apply_rebrand.py <site_root> [--dry] [--brand <brand dir>]
(run from the repo root: python _rebrand/apply_rebrand.py .)

* Patches every *.html under <site_root>: favicons + manifest links, page titles, share-card
  tags, JSON-LD names, the header logo, news-item icon/labels and the footer line.
* Black and gold: swaps the navy bar and amber accents inside the pages' own <style> blocks
  (SWAPS) and sets the gold variables (--sodium, --sodium-bright) in the brand style block.
* Copies the brand files in: brand/ (logos, icons, social images, tokens.css) plus the
  root files browsers ask for (favicon.ico, favicon.svg, apple-touch-icon.png,
  favicon-32.png, favicon-48.png, site.webmanifest).
* Never touches rankings data, stats logic or URLs. Running it twice changes nothing more.
"""
import os, re, sys, shutil, json, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DEFAULT = os.path.join(os.path.dirname(HERE), "brand")   # <repo>/brand, next to _rebrand/
SITE = "https://utahhighschoolfootball.com"
NAME = "The Ledger &middot; Utah High School Football"
OG_IMG = f"{SITE}/brand/social/og-card-1200x630.png"
OG_ALT = "The Ledger &middot; Utah High School Football. Power ratings, the player index and every roster in the state."
LOCKUP_W, LOCKUP_H = 136, 48           # horizontal lockup viewBox 136.402 x 48, shown 48 px tall

ICONS = (
    "<!-- The Ledger brand (Nov 2026): favicon (follows light/dark), PNG/ICO fallback for older\n"
    "     browsers, iOS home-screen icon and the web app manifest. Files live in /brand. -->\n"
    '<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
    '<link rel="manifest" href="/site.webmanifest">\n'
)

CSS = """<style id="ledger-brand">
/* The Ledger brand (Nov 2026). Header: the mark on narrower screens, the full lockup once the
   menu still fits beside it (app bar from 1320 px, program pages from 1280 px). */
.tb-brand .blogo,.px-brand img.blogo{width:48px;height:48px;flex:none}
.tb-brand .blockup,.px-brand img.blockup{display:none;width:auto;height:48px;flex:none}
@media (min-width:1320px){.tb-brand .blockup{display:block}.tb-brand .blogo{display:none}}
@media (min-width:1280px){.px-brand img.blockup{display:block}.px-brand img.blogo{display:none}}
.ledger-vh{position:absolute!important;width:1px!important;height:1px!important;margin:-1px;padding:0;border:0;
  overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
a.ledger-brand{display:inline-flex;align-items:center;line-height:0}
a.ledger-brand img{height:48px;width:auto}
/* Black and gold (Nov 18 2026). "html:root" outranks the page's own :root color blocks, wherever
   this block sits. The gold is the site's own (#E8A33D on black). Light mode: Gold Deep for text
   (#9A6206, 5.0:1 on white). Dark mode: neutral blacks. Black bars and panels always use #E8A33D. */
html:root{--sodium:#9A6206;--sodium-bright:#B87708}
@media (prefers-color-scheme: dark){html:root:not([data-theme="light"]){--sodium:#E8A33D;--sodium-bright:#F5BC63;--ink:#F3F3F6;--ink-2:#A6A6B2;--ink-3:#72727E;--ground:#08080A;--surface:#121216;--surface-2:#1A1A20;--line:#26262E;--line-soft:#1E1E25;--spine:#2C2C35}}
html:root[data-theme="dark"]{--sodium:#E8A33D;--sodium-bright:#F5BC63;--ink:#F3F3F6;--ink-2:#A6A6B2;--ink-3:#72727E;--ground:#08080A;--surface:#121216;--surface-2:#1A1A20;--line:#26262E;--line-soft:#1E1E25;--spine:#2C2C35}
nav.tabs.topbar,.px-top,.artface,.artcmp thead th,.rxhero,.rxnums div,.rxic,.rxp.gold,.rxlh,.c26>summary,#prtable tr.divrow td,#rktable tr.divrow td,.cw-ban,.rtoday,.rsign .sgcount,.rtc,.rchnav .rchn,.rsct,.rpti,.rptd[open] summary,.hdpp,.hpo-hero,.hgs-hero,.flagad.pwad,#v-tstats .tstab thead th,.pp-hero,.reelplay .rpbar,.cx-band,.mx-feat,.mx-th,.pxp-v .th{--sodium:#E8A33D;--sodium-bright:#E8A33D}
/* a selected tab can't be black on a black page: gold in dark mode */
@media (prefers-color-scheme: dark){html:root:not([data-theme="light"]) .pb-tabs button[aria-pressed="true"]{background:#E8A33D;color:#0E1116;border-color:#E8A33D}}
html:root[data-theme="dark"] .pb-tabs button[aria-pressed="true"]{background:#E8A33D;color:#0E1116;border-color:#E8A33D}
</style>
"""

MARK_ON_DARK = "/brand/logo/ledger-icon-color-on-dark.svg"   # full mark (THE LEDGER), 48 px
LOCKUP_ON_DARK = "/brand/logo/ledger-horizontal-color-on-dark.svg"
LOCKUP_ON_LIGHT = "/brand/logo/ledger-horizontal-color-on-light.svg"


def nav_brand(img_class_extra=""):
    return (f'<img class="blogo" src="{MARK_ON_DARK}" width="48" height="48" alt="" decoding="async">'
            f'<img class="blockup" src="{LOCKUP_ON_DARK}" width="{LOCKUP_W}" height="{LOCKUP_H}" alt="" decoding="async">'
            f'<b class="ledger-vh">{NAME}</b>')


def brand_title(t):
    if "The Ledger" in t:
        return t
    if t.rstrip().endswith("| Utah High School Football"):
        return t.rstrip()[: -len("Utah High School Football")] + NAME
    if t.startswith("Utah High School Football"):
        return "The Ledger &middot; " + t
    return t


RULES = []


def rule(fn):
    RULES.append(fn)
    return fn


@rule
def icons(s):
    if "The Ledger brand (Nov 2026): favicon" in s:
        return s, 0
    n = 0
    s, k = re.subn(r'<!-- The mark\.[\s\S]*?-->\s*', "", s); n += k
    s, k = re.subn(r'<link rel="(?:icon|shortcut icon|apple-touch-icon|manifest)"[^>]*>[ \t]*\n?', "", s); n += k
    m = re.search(r'<meta name="theme-color"[^>]*>\n?', s) or re.search(r'<meta name="viewport"[^>]*>\n?', s)
    if not m:
        raise ValueError("no theme-color or viewport meta to anchor the icon links")
    s = s[: m.end()] + ("" if s[m.end() - 1] == "\n" else "\n") + ICONS + s[m.end():]
    return s, n + 1


@rule
def titles(s):
    n = 0

    def t(m):
        nonlocal n
        new = brand_title(m.group(2))
        n += new != m.group(2)
        return m.group(1) + new + m.group(3)
    s = re.sub(r'(<title>)([^<]*)(</title>)', t, s, count=1)
    s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")([^"]*)(")', t, s)
    return s, n


@rule
def site_name(s):
    return re.subn(r'(<meta property="og:site_name" content=")Utah High School Football(")', r"\g<1>" + NAME + r"\2", s)


@rule
def share_card(s):
    n = 0
    s, k = re.subn(re.escape(f"{SITE}/share.png"), OG_IMG, s); n += k
    s, k = re.subn(r'content="Utah High School Football &mdash; The Ledger\. Power ratings, the player index and every roster in the state\."',
                   f'content="{OG_ALT}"', s); n += k
    if 'property="og:image"' not in s:
        tags = (f'<meta property="og:image" content="{OG_IMG}">\n<meta property="og:image:width" content="1200">\n'
                f'<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{OG_ALT}">\n')
        m = re.search(r'<meta property="og:url"[^>]*>\n?', s) or re.search(r'<meta property="og:description"[^>]*>\n?', s)
        if m:
            s = s[: m.end()] + ("" if s[m.end() - 1] == "\n" else "\n") + tags + s[m.end():]; n += 1
    s, k = re.subn(r'(<meta name="twitter:card" content=")summary(")', r"\1summary_large_image\2", s); n += k
    if 'name="twitter:image"' not in s and 'name="twitter:card"' in s:
        tw = (f'\n<meta name="twitter:site" content="@TheLedgerUT">\n<meta name="twitter:image" content="{OG_IMG}">\n'
              f'<meta name="twitter:image:alt" content="{OG_ALT}">')
        if 'name="twitter:site"' in s:
            tw = tw.replace('\n<meta name="twitter:site" content="@TheLedgerUT">', "")
        s = re.sub(r'(<meta name="twitter:card"[^>]*>)', lambda m: m.group(1) + tw, s, count=1); n += 1
    return s, n


@rule
def json_ld(s):
    n = 0
    s, k = re.subn(r'("@type":"WebSite",\s*"name":)"Utah High School Football"',
                   r'\1"The Ledger · Utah High School Football","alternateName":"Utah High School Football"', s); n += k
    s, k = re.subn(r'("publisher":\{"@type":"Organization",)"name":"Utah High School Football",',
                   r'\1"name":"The Ledger","alternateName":"Utah High School Football",'
                   f'"logo":"{SITE}/brand/icons/icon-512.png",', s); n += k
    return s, n


@rule
def header_logo(s):
    n = 0
    # the live app's top bar
    s, k = re.subn(r'<img class="blogo" src="/?logo-uhsfb\.webp"[^>]*>\s*<span>Utah High School <em>Football</em></span>',
                   lambda m: nav_brand(), s); n += k
    # the program pages' top bar
    s, k = re.subn(r'(<a class="px-brand" href="[^"]*">)<img src="/?logo-uhsfb\.webp"[^>]*>\s*<span>Utah High School <em>Football</em></span>',
                   lambda m: m.group(1) + nav_brand(), s); n += k
    # the plain header on the crawlable pages (light background, follows light/dark)
    s, k = re.subn(r'<a class="brand" href="([^"]*)">Utah High School <em>Football</em></a>',
                   lambda m: (f'<a class="brand ledger-brand" href="{m.group(1)}"><picture>'
                              f'<source media="(prefers-color-scheme: dark)" srcset="{LOCKUP_ON_DARK}">'
                              f'<img src="{LOCKUP_ON_LIGHT}" width="{LOCKUP_W}" height="{LOCKUP_H}" alt="{NAME}"></picture></a>'), s); n += k
    return s, n


@rule
def news_labels(s):
    n = 0
    s, k = re.subn(r'src="/?logo-uhsfb\.webp" alt="Utah High School Football"', 'src="/brand/icons/favicon-tile.svg" alt="The Ledger"', s); n += k
    for old, new in (("UHSFB Commitments", "The Ledger Commitments"), ("UHSFB Carousel", "The Ledger Carousel"),
                     ("UHSFB &middot;", "The Ledger &middot;")):
        s, k = re.subn(re.escape(old), new, s); n += k
    return s, n


@rule
def footers(s):
    n = 0
    s, k = re.subn(r'("foot"\)\.innerHTML\s*=\s*")Utah High School Football ·', r'\1The Ledger · Utah High School Football ·', s); n += k
    s, k = re.subn(r'<strong>Utah High School Football</strong>', f'<strong>{NAME}</strong>', s); n += k
    return s, n


@rule
def styles(s):
    if 'id="ledger-brand"' in s:  # already there: refresh it if this script's styles changed
        new = re.sub(r'<style id="ledger-brand">[\s\S]*?</style>\n', lambda m: CSS, s, count=1)
        return new, int(new != s)
    if "</head>" in s:
        return s.replace("</head>", CSS + "</head>", 1), 1
    # the live app page has no </head>: put it right under the icon links instead
    anchor = '<link rel="manifest" href="/site.webmanifest">\n'
    if anchor in s:
        return s.replace(anchor, anchor + CSS, 1), 1
    raise ValueError("no place to add the brand styles")


# Black and gold: color swaps inside the pages' own <style> blocks only (never scripts, data or
# school colors). Navy -> Ledger Black / charcoal, the gold stays the site's own #E8A33D.
SWAPS = [
    (r"#0B1F3A", "#0E1116"),   # navy bars and panels -> Ledger Black
    (r"#0f1a2b", "#0E1116"),
    (r"#14325C", "#24272E"),   # navy gradient partners -> charcoal
    (r"#13305a", "#24272E"),
    (r"#1b2a44", "#24272E"),
    (r"#13294b", "#1E2128"),
    (r"#132C4F", "#262A31"),   # bar hover
    (r"#3A4A5C", "#3A3E46"),
    (r"#1d2f52", "#24272E"),   # champions panel / records card gradients (added Nov 2026)
    (r"#2A4A7A", "#30343C"),
    (r"#071427", "#08090C"),
    (r"#081528", "#08090C"),
    (r"#0E2240", "#1E2128"),   # realignment banner
    (r"color:#B87708", "color:var(--sodium)"),   # amber text -> follows light/dark
]


def _neutral(m):
    """Any other dark navy or blue-slate (all channels <= 0x55, blue clearly above red) becomes a
    neutral charcoal of the same brightness, so panels the builder adds later turn black too.
    Brighter blues (school colors, chart colors like the 'pass' bar) are left alone."""
    h = m.group(0)
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    if max(r, g, b) > 0x55 or b - r < 0x18 or b < g:
        return h
    v = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return "#%02X%02X%02X" % (max(v - 3, 0), v, min(v + 5, 255))


@rule
def palette(s):
    n = 0

    def fix(m):
        nonlocal n
        if 'id="ledger-brand"' in m.group(1):
            return m.group(0)
        body = m.group(2)
        for old, new in SWAPS:
            body, k = re.subn(old, new, body, flags=re.I)
            n += k
        body2 = re.sub(r"#[0-9a-fA-F]{6}\b", _neutral, body)
        if body2 != body:
            n += sum(1 for a, b in zip(re.findall(r"#[0-9a-fA-F]{6}\b", body), re.findall(r"#[0-9a-fA-F]{6}\b", body2)) if a != b)
            body = body2
        return m.group(1) + body + m.group(3)

    s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", fix, s)
    return s, n


LEFTOVER = [("logo-uhsfb", r"logo-uhsfb"), ("share.png", r"/share\.png"), ("UHSFB", r"UHSFB"),
            ("old favicon PNG", r'href="favicon-(?:32|48)\.png"')]


def patch(s):
    out = {}
    for fn in RULES:
        s, k = fn(s)
        if k:
            out[fn.__name__] = k
    left = {name: len(re.findall(p, s)) for name, p in LEFTOVER if re.search(p, s)}
    return s, out, left


ROOT_FILES = {  # site root path: source inside the brand folder
    "favicon.ico": "icons/favicon.ico", "favicon.svg": "icons/favicon.svg",
    "apple-touch-icon.png": "icons/apple-touch-icon.png", "favicon-32.png": "icons/favicon-32.png",
    "favicon-48.png": "icons/favicon-48.png", "site.webmanifest": "icons/site.webmanifest",
}


def copy_assets(brand, site, dry):
    done = []
    for dirpath, _, files in os.walk(brand):
        for f in files:
            if f == "preview.html":
                continue
            src = os.path.join(dirpath, f)
            dst = os.path.join(site, "brand", os.path.relpath(src, brand))
            done.append(("brand/" + os.path.relpath(src, brand).replace(os.sep, "/"), src, dst))
    for rel, src in ROOT_FILES.items():
        done.append((rel, os.path.join(brand, src), os.path.join(site, rel)))
    report = []
    for rel, src, dst in done:
        state = "new" if not os.path.exists(dst) else ("same" if filecmp.cmp(src, dst, shallow=False) else "replaced")
        report.append((rel, state))
        if not dry and state != "same":
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    return report


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    site = os.path.abspath(args[0])
    dry = "--dry" in args
    brand = args[args.index("--brand") + 1] if "--brand" in args else BRAND_DEFAULT
    totals, changed, lefts = {}, 0, {}
    skipped = {}
    for dirpath, dirs, files in os.walk(site):
        dirs[:] = []   # top-level pages only: subfolders (t/ = blank tracking pages) are left alone
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            if re.match(r"google[0-9a-f]+\.html$", f):
                skipped[f] = "Google site-ownership file"
                continue
            raw = open(p, "rb").read()
            s = raw.decode("utf-8")
            if not re.search(r'<meta name="(?:viewport|theme-color)"', s):
                skipped[f] = "no page head to brand"
                continue
            new, out, left = patch(s)
            for k, v in out.items():
                totals[k] = totals.get(k, 0) + v
            if left:
                lefts[os.path.relpath(p, site)] = left
            if new != s:
                changed += 1
                if not dry:
                    with open(p, "w", encoding="utf-8", newline="") as fh:
                        fh.write(new)
    assets = copy_assets(brand, site, dry)
    print(json.dumps({"dry": dry, "html_files_changed": changed, "skipped": skipped, "changes_by_rule": totals,
                      "left_unchanged": lefts,
                      "assets": {k: sum(1 for _, s in assets if s == k) for k in ("new", "replaced", "same")},
                      "replaced_files": [r for r, s in assets if s == "replaced"]}, indent=1))


if __name__ == "__main__":
    main()
