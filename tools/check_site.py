"""Site checker for kanavtyagi.github.io. Stdlib only.

Usage: python tools/check_site.py [--release]
Prints PASS/FAIL per check; exits 1 if any check fails.
Every function named test_* is a check. Each returns None (pass) or a string (failure detail).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "404.html"] + [f"projects/{s}.html" for s in ("crane", "xm23", "robo-heist", "lice", "coral")]
RELEASE = "--release" in sys.argv

ALLOWED_HOSTS = {"gc.zgo.at", "kanavtyagi.goatcounter.com", "www.youtube.com", "i.ytimg.com",
                 "github.com", "www.linkedin.com", "kanavtyagi.github.io"}
EVENTS = {"resume-download-nav", "resume-download-hero", "resume-download-contact",
          "resume-download-project", "email-click", "linkedin-click", "robo-heist-video"}
IDS = ["p-crane", "p-xm23", "p-robo", "p-lice", "p-coral", "x-drs", "x-npl"]
TOKENS = {"--page": "#131518", "--grid": "#1f2327", "--ink": "#e4e7eb", "--ink-muted": "#a4abb4",
          "--ink-faint": "#8c939d", "--ch1": "#f2c94c", "--ch2": "#5ec8f2", "--rule": "#2d3339",
          "--entry": "rgba(255,255,255,.03)", "--tape": "rgba(205,140,50,.6)", "--frame": "#e8ebee"}
FONT_FILES = ["plex-condensed-600", "plex-condensed-700", "caveat-500", "plex-sans", "plex-mono-400", "plex-mono-600"]  # plex-sans is variable (400-600)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children, self.text = tag, dict(attrs), parent, [], ""

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def find_all(self, pred):
        return [n for n in self.walk() if pred(n)]

    def all_text(self):
        return self.text + "".join(c.all_text() for c in self.children)


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [])
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.text += data


_cache = {}


def dom(page):
    if page not in _cache:
        b = Builder()
        b.feed((ROOT / page).read_text(encoding="utf-8"))
        _cache[page] = b.root
    return _cache[page]


def read(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---------------- Task 1 ----------------

def test_only_allowed_external_hosts():
    bad = []
    for page in PAGES:
        for n in dom(page).walk():
            for attr in ("src", "href"):
                v = n.attrs.get(attr) or ""
                if v.startswith(("http:", "https:", "//")):
                    host = urlparse(v if not v.startswith("//") else "https:" + v).hostname
                    if host not in ALLOWED_HOSTS:
                        bad.append(f"{page}: {v}")
    return "; ".join(bad) or None


def test_pages_use_notebook_css():
    bad = []
    for page in PAGES:
        d = dom(page)
        links = d.find_all(lambda n: n.tag == "link" and n.attrs.get("rel") == "stylesheet")
        styles = d.find_all(lambda n: n.tag == "style")
        if styles:
            bad.append(f"{page}: has <style>")
        if len(links) != 1:
            bad.append(f"{page}: {len(links)} stylesheet links")
            continue
        href = links[0].attrs.get("href", "")
        target = (ROOT / href.lstrip("/")) if href.startswith("/") else (ROOT / page).parent / href
        if target.resolve() != (ROOT / "notebook.css").resolve():
            bad.append(f"{page}: links {href}")
    return "; ".join(bad) or None


def test_goatcounter_events_kept():
    found = set()
    for page in PAGES:
        found |= {n.attrs["data-goatcounter-click"] for n in dom(page).walk() if n.attrs.get("data-goatcounter-click")}
    missing = EVENTS - found
    return f"missing {sorted(missing)}" if missing else None


def test_ids_and_labels_kept():
    d = dom("index.html")
    bad = []
    for i in IDS:
        m = d.find_all(lambda n, i=i: n.attrs.get("id") == i)
        if len(m) != 1 or not (m[0].attrs.get("data-label") or "").strip():
            bad.append(i)
    return f"bad ids {bad}" if bad else None


def test_home_h1_is_name():
    h1 = dom("index.html").find_all(lambda n: n.tag == "h1")
    if len(h1) != 1 or h1[0].all_text().strip() != "Kanav Tyagi":
        return f"h1s: {[h.all_text().strip() for h in h1]}"


def test_no_numbered_nav():
    n = dom("index.html").find_all(lambda n: "num" in n.classes)
    return f"{len(n)} .num elements" if n else None


def test_entries_have_links():
    d = dom("index.html")
    proj = d.find_all(lambda n: n.attrs.get("id") == "projects")
    if not proj:
        return "no #projects"
    entries = proj[0].find_all(lambda n: "entry" in n.classes)
    if len(entries) != 5:
        return f"{len(entries)} .entry elements in #projects (want 5)"
    bad = [e.attrs.get("id") for e in entries
           if not e.find_all(lambda n: n.tag == "a" and re.fullmatch(r"projects/[a-z0-9-]+\.html", n.attrs.get("href") or ""))]
    return f"entries without detail link: {bad}" if bad else None


def test_one_note_per_entry():
    bad = []
    for page in PAGES:
        d = dom(page)
        for box in d.find_all(lambda n: "entry" in n.classes or "log-item" in n.classes or n.tag == "section"):
            notes = box.find_all(lambda n: "note" in n.classes)
            if box.tag == "section":
                # notes belonging to nested entries/log items are counted on those
                notes = [x for x in notes if not _inside(x, box, ("entry", "log-item"))]
            limit = 3 if "hero" in box.classes else 1
            if len(notes) > limit:
                bad.append(f"{page}: <{box.tag} {box.attrs.get('id') or box.classes}> has {len(notes)} notes")
    return "; ".join(bad) or None


def _inside(node, stop, classes):
    p = node.parent
    while p is not None and p is not stop:
        if any(c in p.classes for c in classes):
            return True
        p = p.parent
    return False


def test_images_have_alt_and_size():
    bad = []
    for page in PAGES:
        for img in dom(page).find_all(lambda n: n.tag == "img"):
            if not (img.attrs.get("alt") or "").strip() or not img.attrs.get("width") or not img.attrs.get("height"):
                bad.append(f"{page}: {img.attrs.get('src')}")
    return "; ".join(bad) or None


def test_no_placeholders():
    if not RELEASE:
        return None
    bad = []
    for page in PAGES:
        for n in dom(page).walk():
            if "placeholder" in n.classes or "placeholder" in (n.attrs.get("src") or ""):
                bad.append(f"{page}: {n.tag} {n.attrs.get('src', '')}")
            src = n.attrs.get("src") or ""
            if n.tag == "img" and not src.startswith(("http", "//")) and not ((ROOT / page).parent / src).exists():
                bad.append(f"{page}: missing file {src}")
    return "; ".join(bad) or None


def test_skills_strings_quoted():
    """Every text:/where: string in the SKILLS data must not contain an unescaped single quote."""
    src = read("index.html")
    bad = []
    for line in re.findall(r"^\s*\{\s*text:.*$", src, re.M):
        if not re.fullmatch(r"\s*\{\s*text:\s*'(?:[^'\\]|\\.)*'\s*,\s*(?:ref|where):\s*'(?:[^'\\]|\\.)*'\s*\},?\s*", line):
            bad.append(line.strip()[:70])
    return f"malformed SKILLS lines: {bad}" if bad else None


def test_project_pages_have_spec():
    bad = [p for p in PAGES if p.startswith("projects/")
           if len(dom(p).find_all(lambda n: n.tag == "table" and "spec" in n.classes)) != 1]
    return f"pages without exactly one .spec table: {bad}" if bad else None


def test_hero_primary_is_resume():
    d = dom("index.html")
    hero = d.find_all(lambda n: "hero" in n.classes)
    if not hero:
        return "no .hero"
    btns = hero[0].find_all(lambda n: "btn" in n.classes)
    prim = [b for b in btns if "primary" in b.classes]
    if len(btns) != 2:
        return f"hero has {len(btns)} buttons (want 2)"
    if len(prim) != 1 or prim[0].attrs.get("data-goatcounter-click") != "resume-download-hero":
        return "hero primary button is not the resume download"


def test_hero_proof_links():
    d = dom("index.html")
    proof = d.find_all(lambda n: "proof" in n.classes)
    if len(proof) != 1:
        return f"{len(proof)} .proof elements (want 1)"
    links = [a.attrs.get("href") for a in proof[0].find_all(lambda n: n.tag == "a")]
    want = {"projects/crane.html", "#x-drs"}
    return None if want <= set(links) else f"proof links {links} missing {want - set(links)}"


def test_crane_has_diagram_and_tasks():
    d = dom("projects/crane.html")
    svgs = d.find_all(lambda n: n.tag == "svg" and n.attrs.get("role") == "img" and n.attrs.get("aria-labelledby"))
    tables = d.find_all(lambda n: n.tag == "table" and "tasks" in n.classes)
    bad = []
    if len(svgs) != 1: bad.append(f"{len(svgs)} labelled svg diagrams")
    if len(tables) != 1: bad.append(f"{len(tables)} .tasks tables")
    return "; ".join(bad) or None


# ---------------- Task 2 ----------------

def test_fonts_present_and_small():
    files = [ROOT / "fonts" / f"{f}.woff2" for f in FONT_FILES]
    missing = [f.name for f in files if not f.exists()]
    if missing:
        return f"missing {missing}"
    total = sum(f.stat().st_size for f in files)
    return f"fonts total {total} bytes > 204800" if total > 204800 else None


def test_font_faces_swap_and_fallbacks():
    faces = re.findall(r"@font-face\s*{([^}]*)}", read("fonts.css"))
    if len(faces) != len(FONT_FILES):
        return f"{len(faces)} @font-face rules in fonts.css (want {len(FONT_FILES)})"
    if any("font-display: swap" not in f for f in faces):
        return "an @font-face lacks font-display: swap"
    css = read("notebook.css")
    decls = re.findall(r"font-family\s*:\s*([^;}]+)", css)
    if not decls:
        return "no font-family in notebook.css"
    bad = [d for d in decls if not re.search(r"\b(serif|sans-serif|monospace|cursive)\s*$", d.strip())]
    return f"no generic fallback: {bad}" if bad else None


# ---------------- Task 3 ----------------

def _tokens():
    css = read("notebook.css")
    m = re.search(r":root\s*{([^}]*)}", css)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1))) if m else {}


def test_tokens_exact():
    t = _tokens()
    bad = [k for k, v in TOKENS.items() if t.get(k, "").replace(" ", "").lower() != v.replace(" ", "").lower()]
    return f"wrong/missing tokens {bad}" if bad else None


def _lum(hexv):
    hexv = hexv.lstrip("#")
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def test_no_old_palette():
    bad = []
    for f in PAGES + ["notebook.css"]:
        t = read(f).lower()
        for old in ("#1b1a18", "#f08a6c", "--coral", "--blue", "note coral", "note blue", "240, 138, 108", "27, 26, 24"):
            if old in t:
                bad.append(f"{f}: {old}")
    return "; ".join(bad) or None


def test_text_contrast():
    t = _tokens()
    if "--page" not in t:
        return "no --page token"
    bg = _lum(t["--page"].strip())
    bad = []
    for k in ("--ink", "--ink-muted", "--ink-faint", "--ch1", "--ch2"):
        if k not in t:
            bad.append(f"{k} missing")
            continue
        fg = _lum(t[k].strip())
        ratio = (max(fg, bg) + 0.05) / (min(fg, bg) + 0.05)
        if ratio < 4.5:
            bad.append(f"{k} {ratio:.2f}")
    return "; ".join(bad) or None


def test_focus_visible_rule():
    return None if ":focus-visible" in read("notebook.css") else "no :focus-visible rule"


def test_reduced_motion():
    return None if re.search(r"@media\s*\(prefers-reduced-motion:\s*reduce\)", read("notebook.css")) else "no reduced-motion block"


def test_note_rotation_limit():
    css = read("notebook.css")
    if not css:
        return "notebook.css missing"
    bad = [a for a in re.findall(r"rotate\(\s*(-?[\d.]+)deg", css) if abs(float(a)) > 3]
    return f"rotations over 3deg: {bad}" if bad else None


def main():
    only = [a for a in sys.argv[1:] if a.startswith("test_")]
    tests = [(n, f) for n, f in globals().items()
             if n.startswith("test_") and callable(f) and (not only or n in only)]
    failed = 0
    for name, fn in tests:
        try:
            res = fn()
        except Exception as e:  # a crash is a failure, not a pass
            res = f"error: {e!r}"
        if res:
            failed += 1
            print(f"FAIL {name}: {res}")
        else:
            print(f"PASS {name}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
