# Graphite Notebook Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle kanavtyagi.github.io (home, 5 project pages, 404) as a dark "graphite engineering notebook" without losing any existing behaviour.

**Architecture:** Plain static HTML. One shared stylesheet `notebook.css` at the repo root replaces the inline `<style>` in `index.html`, `projects/project.css`, and the inline styles in `404.html`. Self-hosted fonts in `fonts/`. A stdlib-only Python checker `tools/check_site.py` is the test suite; visual/phone checks run in the browser against the local preview server.

**Tech Stack:** HTML5, CSS (custom properties, grid/flex), existing vanilla JS in `index.html`, Python 3 stdlib (checker, Pillow already installed for images), GitHub Pages (Jekyll "legacy" build from `main`).

**Spec:** `docs/superpowers/specs/2026-11-23-graphite-notebook-redesign-design.md`

## Global Constraints

- Work only on branch `project-pages`. Do not push to `main`; merging/publishing happens only when Kanav says so.
- No external requests except the existing GoatCounter script `//gc.zgo.at/count.js` and `https://kanavtyagi.goatcounter.com/count`. No Google Fonts, no CDNs.
- Dark-only: no light theme, no theme switch.
- Palette (exact): page `#1b1a18`, grid `#2a2824` at 22px, ink `#e8e3d8`, ink-muted `#a49c8c`, ink-faint `#8f877a`, coral `#f08a6c`, blue `#8fc1ff`, rule `#3a3730`, entry `rgba(255,255,255,.03)`, tape `rgba(232,200,120,.55)`, photo frame `#ece6d8`.
- Fonts: Fraunces (headings), Caveat (notes/captions only), IBM Plex Sans (body), IBM Plex Mono (specs/labels). Self-hosted woff2, total ≤ 200 KB.
- Balance rules: at most one handwritten note per section or project entry; notes one line, rotation ≤ 3°; every note true; no notes on resume/contact; facts always in typed text.
- Phone: 16px side gutter, no horizontal scroll, nothing overlapping at 375px width.
- Body text contrast ≥ 4.5:1 against the page; `prefers-reduced-motion` disables animations.
- Keep unchanged: every `data-goatcounter-click` name (`resume-download-nav`, `resume-download-hero`, `resume-download-contact`, `resume-download-project`, `email-click`, `linkedin-click`, `robo-heist-video`), the `SKILLS` data and skill-panel JS, ids `p-crane p-xm23 p-robo p-lice p-coral x-drs x-npl` with their `data-label`s, the console "boot complete" message, footer text.
- Never present a KiCad render as a photo: design images use `.printout`, real photos use `.photo`.

## Review Focus

- Phone width (375px): hero printout and notes overlapping the intro or causing sideways scroll; expected: they stack below the text, no overflow. Pinned by Task 7 `overflow check`.
- A photo file missing or not yet supplied: layout must not collapse; expected: reserved space from `width`/`height`, alt text shown. Pinned by Task 1 `test_images_have_alt_and_size`.
- Keyboard-only visitor: project entries and skill pills reachable with Tab with a visible focus ring. Pinned by Task 1 `test_entries_have_links` and Task 3 `test_focus_visible_rule`.
- Fonts fail or load slowly: text must render in fallback fonts immediately. Pinned by Task 2 `test_font_faces_swap_and_fallbacks`.
- Placeholder images reaching `main`. Pinned by Task 1 `test_no_placeholders` (run with `--release`).

---

### Task 1: Checker script and publish exclusions

**Files:**
- Create: `tools/check_site.py`
- Create: `_config.yml`

**Interfaces:**
- Produces: `python tools/check_site.py [--release]`; prints `PASS name` / `FAIL name: detail` per check, exits 1 on any FAIL. Pages checked: `index.html`, `404.html`, `projects/{crane,xm23,robo-heist,lice,coral}.html`. Later tasks add checks to this file as functions named `test_*`, auto-discovered.

- [ ] **Step 1: Write the checker with these tests** (stdlib `html.parser`, `re`, `pathlib`):
  - `test_only_allowed_external_hosts`: every `src`/`href` starting `http`/`//` has host in `{gc.zgo.at, kanavtyagi.goatcounter.com, www.youtube.com, i.ytimg.com, github.com, www.linkedin.com, kanavtyagi.github.io}`; `mailto:` allowed.
  - `test_pages_use_notebook_css`: each page has exactly one `<link rel="stylesheet">` and it resolves to `notebook.css` at repo root; no `<style>` element in any page.
  - `test_goatcounter_events_kept`: the union of `data-goatcounter-click` values across pages ⊇ the 7 names in Global Constraints.
  - `test_ids_and_labels_kept`: `index.html` has the 7 ids with non-empty `data-label`.
  - `test_home_h1_is_name`: `index.html` has exactly one `<h1>` with text `Kanav Tyagi`.
  - `test_no_numbered_nav`: no element with class `num` in `index.html`.
  - `test_entries_have_links`: every `.entry` in `index.html` `#projects` contains an `<a href="projects/<slug>.html">`.
  - `test_one_note_per_entry`: every `.entry` and every `<section>` contains ≤ 1 element with class `note` (hero section allowed 3).
  - `test_images_have_alt_and_size`: every `<img>` has non-empty `alt`, `width`, `height`.
  - `test_no_placeholders` (only with `--release`): no element with class `placeholder` and no `img` src containing `placeholder`.
- [ ] **Step 2: Create `_config.yml`** with `exclude: [docs, tools, .superpowers]` so GitHub Pages' Jekyll build doesn't publish them.
- [ ] **Step 3: Run** `python tools/check_site.py` — Expected: FAIL on `test_pages_use_notebook_css`, `test_home_h1_is_name`, `test_no_numbered_nav`, `test_entries_have_links` (site not restyled yet); the rest PASS.
- [ ] **Step 4: Commit** `git add tools/check_site.py _config.yml && git commit -m "Add site checker and exclude docs/tools from Pages"`

### Task 2: Self-hosted fonts

**Files:**
- Create: `fonts/fraunces-500.woff2`, `fonts/fraunces-700.woff2`, `fonts/caveat-500.woff2`, `fonts/plex-sans-400.woff2`, `fonts/plex-sans-600.woff2`, `fonts/plex-mono-400.woff2`, `fonts/plex-mono-600.woff2`, `fonts/OFL.txt`
- Create: `fonts.css` (the `@font-face` rules; imported by `notebook.css`)
- Modify: `tools/check_site.py` (add tests)

**Interfaces:**
- Produces: font-family names `"Fraunces"`, `"Caveat"`, `"IBM Plex Sans"`, `"IBM Plex Mono"`.

- [ ] **Step 1: Add tests** `test_fonts_present_and_small` (the 7 files exist, total ≤ 204800 bytes) and `test_font_faces_swap_and_fallbacks` (every `@font-face` in `fonts.css` has `font-display: swap`; every `font-family` declaration in `notebook.css` ends with a generic family `serif|sans-serif|monospace|cursive`).
- [ ] **Step 2: Run checker** — Expected: both FAIL.
- [ ] **Step 3: Get the fonts.** Ask Kanav before downloading (name the files, source and approximate size). Source: latin-subset woff2 files from the Google Fonts CSS2 API for the weights above, saved into `fonts/`; licence text from the google/fonts GitHub repo `ofl/fraunces/OFL.txt` (one combined `OFL.txt` noting all four families). Write `fonts.css` with one `@font-face` per file, `font-display: swap`.
- [ ] **Step 4: Run checker** — Expected: both PASS.
- [ ] **Step 5: Commit** `git add fonts fonts.css tools/check_site.py && git commit -m "Self-host notebook fonts"`

### Task 3: Shared stylesheet `notebook.css`

**Files:**
- Create: `notebook.css`
- Modify: `tools/check_site.py`

**Interfaces:**
- Consumes: `fonts.css` (via `@import "fonts.css";` first line).
- Produces (class names later tasks use): `.wrap` (max-width 960px container), `.site-header` / `.site-nav` (links get `.active` from JS), `.progress`, `.page-head` (serif title + mono page number `.pno`), `.hero`, `.hero-name` (the h1), `.headline`, `.intro`, `.status` + `.led`, `.btn` / `.btn.primary`, `.note` (+ modifiers `.note.coral`, `.note.blue`, `.note.arrow-left`), `.taped` wrapper with `.tape`, `.photo` (instant-photo frame `#ece6d8`, bottom border 26px), `.printout` (plain white border 6px), `figcaption.caption` (Caveat), `.entry` (+ `.entry.featured`), `.spec` (two-column table, dashed `--rule` lines, labels `--ink-faint`), `.log` / `.log-item` (experience), `.skills` / `.skill-result` (same selectors the existing JS uses), `.match`, `.flash`, `.site-footer`.
- Custom properties named exactly: `--page --grid --ink --ink-muted --ink-faint --coral --blue --rule --entry --tape --frame`.

- [ ] **Step 1: Add tests** `test_tokens_exact` (each custom property above has the exact Global Constraints value), `test_text_contrast` (WCAG contrast of `--ink`, `--ink-muted`, `--ink-faint`, `--coral` against `--page` each ≥ 4.5), `test_focus_visible_rule` (`notebook.css` contains a `:focus-visible` rule), `test_reduced_motion` (contains `@media (prefers-reduced-motion: reduce)`), `test_note_rotation_limit` (every `rotate(` in `notebook.css` ≤ 3deg in absolute value).
- [ ] **Step 2: Run checker** — Expected: the 5 new tests FAIL.
- [ ] **Step 3: Write `notebook.css`.** Page background: `--page` plus two `linear-gradient` grid lines of `--grid` at 22px. Body font IBM Plex Sans, headings Fraunces, `.note`/`.caption` Caveat, `.spec`/`.pno`/`.status` IBM Plex Mono. `.progress` is a 3px coral bar under the header driven by the existing `clip-path` JS. Active nav link: coral underline. At `max-width: 720px` the hero becomes one column, `.taped` items lose absolute positioning and sit below the intro, gutters 16px, `.site-nav` scrolls horizontally if needed. Match the reference mockup `.superpowers/brainstorm/mockups/dark-notebook.html` variant 1.
- [ ] **Step 4: Run checker** — Expected: the 5 new tests PASS.
- [ ] **Step 5: Commit** `git add notebook.css tools/check_site.py && git commit -m "Add graphite notebook stylesheet"`

### Task 4: Home page

**Files:**
- Modify: `index.html` (replace the `<style>` block with `<link rel="stylesheet" href="notebook.css">`; restructure markup; keep the `<script>` blocks, adjusting only selectors that change)

**Interfaces:**
- Consumes: Task 3 class names.
- Produces: unchanged ids/labels/event names (Global Constraints).

- [ ] **Step 1: Run checker** — Expected: the four Task 1 FAILs still failing.
- [ ] **Step 2: Header:** "Kanav Tyagi" (text, links to top) + links `projects, experience, skills, contact` (to `#…`) + `resume` (download, `resume-download-nav`). No numbers. Keep `.progress`.
- [ ] **Step 3: Hero:** `<h1 class="hero-name">Kanav Tyagi</h1>`; `<p class="headline">I build hardware that works.</p>`; `.note.coral` "…usually on the 3rd revision"; `.intro` = current hero paragraph trimmed to 2 sentences, no new claims; `.status` line unchanged; buttons View projects / Download resume (`resume-download-hero`) / Get in touch. Right side: `.taped` > `img.printout` `src="projects/img/crane-pcb-design.png"` (placeholder until supplied, class `placeholder`, alt "KiCad layout of the handheld crane controller PCB", width/height set) with `.note.blue.arrow-left` "← hand-routed in KiCad, 2 layers" and `.note.coral` "off to the fab →".
- [ ] **Step 4: About:** `.page-head` "About" `p. 01`; current two paragraphs unchanged.
- [ ] **Step 5: Projects** (`.page-head` "Projects" `p. 02`). Order crane, xm23, robo, lice, coral. Each `article.entry` keeps its `id`/`data-label`; crane and robo are `.entry.featured` with a `.taped` image (crane: same design image, robo: `projects/img/robo-heist-team.jpg` as `.photo`). Title links to the detail page. Copy:

  | Entry | Date line | Description | Spec rows | Note |
  |---|---|---|---|---|
  | crane | Fall 2026 · in progress | A remote-controlled crane running FreeRTOS on a dual-core ESP32, driven from a handheld ESP32 remote whose PCB I designed. | MCU: ESP32, dual core · RTOS: FreeRTOS, pre-emptive · Link: ESP-NOW + watchdog · Board: 2-layer, KiCad | limit switches → ISR → PWM off. no waiting. |
  | xm23 | Winter 2025 | A 16-bit CPU emulator in C with interrupts, memory-mapped devices, a configurable cache and a debugger. | Language: C, ~4,800 lines · ISA: XM23, 16-bit · Extras: cache simulator, debugger | nested interrupts + tail-chaining, in C |
  | robo | Winter 2025 · 2nd prize | Our team's autonomous robot worked through a secured arena, past simulated RFID and laser-tripwire security, and took 2nd prize. | Brains: Arduino + Raspberry Pi Pico · Sensors: ultrasonic, encoders · Result: 2nd prize | 2nd prize, Group 19 ✓ |
  | lice | Fall 2024 | Autonomous rover software in C that plans paths and avoids obstacles in a simulated lunar ice cave. | Language: C · Display: VT100 terminal · Focus: pathfinding, obstacle avoidance | all drawn with VT100 escape codes |
  | coral | Winter 2024 | A reef monitoring station with temperature, pH and turbidity sensors on custom KiCad PCBs, in a waterproof 3D-printed housing. | Sensors: temperature, pH, turbidity · Board: custom KiCad PCB · Housing: 3D-printed, waterproof | temp · pH · turbidity → logged + sent wirelessly |

- [ ] **Step 6: Experience** (`.page-head` "Experience" `p. 03`) as `.log` with the 4 current items (dates, titles, text unchanged; keep `id="x-drs"`/`id="x-npl"` + labels). Notes: DRS `.note` "tuned the PI loop, checked it in PSIM first"; NPL `.note` "85% accuracy on 15,000+ data points". No notes on the other two.
- [ ] **Step 7: Skills** (`p. 04`), **Contact** (`p. 05`), footer: same content and attributes, new classes only. Update the nav-highlight JS selector from `nav a[href^="#"]` to `.site-nav a[href^="#"]` if the markup changed.
- [ ] **Step 8: Run checker** — Expected: all tests PASS (without `--release`).
- [ ] **Step 9: Browser check** at `http://127.0.0.1:8765/`: click "C / C++" → panel opens under its row, crane/xm23/lice/robo entries get `.match`; scroll → nav underline moves and progress bar fills; console shows `[  OK  ] boot complete`.
- [ ] **Step 10: Commit** `git add index.html && git commit -m "Home page: graphite notebook layout"`

### Task 5: Project pages

**Files:**
- Modify: `projects/crane.html`, `projects/xm23.html`, `projects/robo-heist.html`, `projects/lice.html`, `projects/coral.html`
- Delete: `projects/project.css`

**Interfaces:**
- Consumes: Task 3 classes; spec rows from Task 4 table.

- [ ] **Step 1: In each page** replace the stylesheet link with `<link rel="stylesheet" href="../notebook.css">`; header uses `.site-header` (name links to `../index.html`, links "all projects" → `../index.html#projects` and resume `resume-download-project`); add the project's `.spec` table directly under the meta line; keep overview, "What I/we built", tools, pager and footer content unchanged.
- [ ] **Step 2: Images.** Robo Heist: team photo as `.taped` `.photo` with the existing caption as `figcaption.caption`; video link unchanged. Crane: `.taped .printout` with the design image + caption "KiCad layout. off to the fab." Coral: `.taped .photo` `projects/img/coral-station.jpg` (placeholder until supplied) caption "Coral monitoring station prototype".
- [ ] **Step 3: Delete** `projects/project.css`.
- [ ] **Step 4: Run checker** — Expected: all PASS.
- [ ] **Step 5: Browser check** each page: back link, previous/next work; Robo Heist video link opens at `t=23468s`.
- [ ] **Step 6: Commit** `git add -A projects && git commit -m "Project pages: graphite notebook layout"`

### Task 6: 404 page

**Files:**
- Modify: `404.html`

- [ ] **Step 1:** Remove the inline `<style>`; link `/notebook.css` (absolute, since 404 can be served at any path); keep the HardFault text, the "jump to reset vector (home)" link and the GoatCounter script; render the dump in IBM Plex Mono on the graphite page.
- [ ] **Step 2: Run checker** — Expected: all PASS. Browser: `http://127.0.0.1:8765/404.html` styled correctly.
- [ ] **Step 3: Commit** `git add 404.html && git commit -m "404: graphite notebook styling"`

### Task 7: Photos and final verification

**Files:**
- Create: `projects/img/crane-pcb-design.png` (or `.jpg`), `projects/img/coral-station.jpg`
- Modify: `index.html`, `projects/crane.html`, `projects/coral.html` (remove `placeholder` classes, set real `width`/`height`)

- [ ] **Step 1: Get the images from Kanav** (KiCad image of the crane controller PCB; coral station photo). Resize to ≤ 1600px long side, JPEG quality ~80 (PNG kept for a flat KiCad layout if smaller), strip metadata with Pillow (`ImageOps.exif_transpose`, save without exif).
- [ ] **Step 2: Wire them in** and set `width`/`height` to the real pixel size.
- [ ] **Step 3: Run** `python tools/check_site.py --release` — Expected: all PASS, including `test_no_placeholders`.
- [ ] **Step 4: Overflow check** in the browser at 1440px and at 375px width for all 7 pages, running `document.documentElement.scrollWidth <= innerWidth` — Expected: `true` everywhere; take a screenshot of the home hero at both widths and confirm no note overlaps text.
- [ ] **Step 5: Commit** `git add -A projects index.html && git commit -m "Add crane design image and coral photo"`; push the branch (`git push`) — **not** `main`. Tell Kanav it's ready to review; merge only on his go-ahead.
