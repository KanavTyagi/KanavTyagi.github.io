# Graphite notebook redesign: design

Date: 2026-11-23
Site: kanavtyagi.github.io (repo `KanavTyagi/KanavTyagi.github.io`)
Branch: `project-pages` (local preview only; nothing goes live until Kanav says so)

## Intent and the why

The current site reads as a generic developer-portfolio template: dark navy with a teal
accent, `01. About` numbered nav, two-tone headings ("About **me**"), identical project
cards, system font, one centred column, and no physical hardware anywhere on the home page.

Kanav wants someone who finishes looking at the site to remember two things:

1. **He builds real hardware and enjoys it.** Not a list of coursework.
2. **He put real time into the site itself.** It should feel made by him, not filled into
   a template.

The chosen direction is an **engineering notebook, in the dark** ("graphite notebook"): the
site is his lab notebook at night, with a dark charcoal page, a faint grid, serif headings,
photos taped onto the page, handwritten margin notes, and small datasheet-style spec tables
inside project entries. Reference mockup: `.superpowers/brainstorm/mockups/dark-notebook.html`,
variant 1 (left).

## Goals

- First screen of the home page shows real hardware (a taped photo of the crane controller
  PCB) next to a personal headline, not a résumé sentence.
- Every page (home, 5 project pages, 404) shares one consistent notebook look.
- Personality comes from details: handwritten notes, taped photos, spec tables, slight
  rotations, varied layout between sections.
- Everything the site already does keeps working (see "Keep").
- Still loads fast and reads well on a phone.

## Non-goals

- No light theme and no theme switch (dark-only; Kanav asked for dark).
- No site generator, framework or build step (no Jekyll, React, npm).
- No new content beyond short handwritten notes and the spec tables, both built from facts
  already on the site or in his CV (`career-ops/cv.md`).
- No blog, no contact form.

## Anti-goals (failure even if it technically works)

- It still looks like a template, or like a template with stickers on it.
- The gimmick wins over the content: handwriting used for body text, so many notes and
  rotations that it's hard to read, or a joke that gets tiring.
- Any handwritten note or spec states something that isn't true.
- The site gets heavy or slow (big fonts, unoptimized photos, scripts).
- Placeholder photo boxes go live.

## Balance: professional core, fun edges

Roughly 80% professional, 20% fun by page area. Rules:

1. **Typed text carries every fact.** Someone reading only the typed text gets the full
   professional picture; handwritten notes add personality, never needed information.
2. **At most one handwritten note per section or project entry**, one line, small,
   rotated no more than 3°.
3. **Every note is true and about the work.** No jokes that undercut competence or care.
   "…usually on the 3rd revision" is the limit of self-deprecation.
4. **Fun never blocks anything:** no animations to wait for, no hidden content, no novelty
   navigation; everything readable and reachable on a phone.
5. **Serious things stay serious:** resume PDF, contact buttons and experience entries get
   no jokes.
6. **Easter eggs stay hidden:** HardFault 404, console message, status LED are rewards for
   the curious, not front-and-centre.

Test: a conservative hiring manager at a defence company should read "clear, competent,
detail-oriented"; a startup engineer should read "this person clearly enjoys this". If an
element would make the first one hesitate, it goes.

## Constraints

- GitHub Pages static hosting, served from `main` at the repo root. Plain HTML/CSS plus the
  small amount of vanilla JS the site already has.
- Kanav edits the site by hand, so the markup must stay readable and easy to change.
- Footer claims "Plain HTML and CSS: 0 dependencies, 0 warnings." That must stay true, so
  fonts are self-hosted (no Google Fonts requests) and nothing is loaded from a CDN except
  the existing GoatCounter analytics script.
- Phone width: 16px side gutter, no horizontal scrolling, nothing overlapping.
- Readability: body text contrast at least WCAG AA against the page; motion respects
  `prefers-reduced-motion`.

## Approaches considered

1. **Restyle the current site in place (chosen).** Keep plain HTML/CSS, one shared
   stylesheet for all pages, rework each section's markup into notebook layouts, keep all
   existing behaviour. Trade-off: the header/footer markup is duplicated in each of the 7
   HTML files; acceptable at this size.
2. **Move to Jekyll** (GitHub Pages' built-in generator) for shared layouts. Rejected: adds
   templating Kanav would have to learn, local preview needs Ruby, and it breaks the
   "0 dependencies" footer, for only 7 pages.
3. **Keep the old dark navy theme and just add notebook touches.** Rejected: notes and tape
   on the template look don't fix the "it looks like a template" problem.

Kanav picked approach 1, with a dark theme, and the "Graphite" variant over "Blueprint".

## The look (decided)

Palette (from the approved mockup):

| Token | Value | Use |
|---|---|---|
| page | `#1b1a18` | background |
| grid | `#2a2824`, 22px squares | faint graph-paper grid on the page |
| ink | `#e8e3d8` | headings, body text |
| ink-muted | `#a49c8c` | secondary text, nav |
| ink-faint | `#8f877a` | labels in spec tables, page numbers |
| coral pencil | `#f08a6c` | primary accent: handwritten notes, links, active states |
| blue pencil | `#8fc1ff` | secondary handwritten notes |
| rule | `#3a3730` | table lines, entry borders |
| entry | `rgba(255,255,255,.03)` | notebook entry boxes |
| tape | `rgba(232,200,120,.55)` | masking-tape strips on photos |
| photo frame | `#ece6d8` | instant-photo style border |

Type:

- **Fraunces** (serif): headings and entry titles.
- **Caveat** (handwriting): margin notes and photo captions only. Never body text, never
  the only place important information appears.
- **IBM Plex Sans**: body text.
- **IBM Plex Mono**: spec tables, labels, page numbers, status line.

All four are open-licence fonts, self-hosted as `woff2` in `/fonts/` with only the weights
used, plus their licence file. Target: all fonts together about 200 KB or less.

Signature elements:

- **Taped photos**: photo in a light instant-photo frame, rotated 2–3°, with a translucent
  tape strip, and a handwritten caption.
- **Margin notes**: short handwritten notes in coral or blue pencil, slightly rotated,
  sometimes with an arrow ("← hand-routed in KiCad, 2 layers").
- **Spec tables**: small two-column tables (label / value) with dashed rules, inside
  project entries.
- **Section headers**: serif title on a solid ink rule, with a small mono page number on
  the right ("p. 02").

## Page structure (decided)

### Home (`index.html`)

1. **Header**: plain text "Kanav Tyagi" on the left; links on the right: projects,
   experience, skills, contact, resume. The numbered `01.`–`05.` nav goes away. The current
   section is still highlighted while scrolling, now with a coral pencil underline.
2. **Hero**: his name stays the page's `<h1>` ("Kanav Tyagi", shown as a smaller line
   above the headline) so search results and screen readers still lead with it; then the
   big serif headline "I build hardware that works." (not a heading element) with the
   handwritten line "…usually on the 3rd revision"; a short intro, the current hero
   paragraph trimmed, with no new claims added (final-year Computer Engineering at
   Dalhousie, power electronics firmware at Leonardo DRS); the status line (open to new-grad
   roles, graduating April 2027) and its LED; buttons for projects and resume; the
   **crane controller PCB design** taped in as a printout, with the note
   "← hand-routed in KiCad, 2 layers" and a second short note that it's off to be made
   (e.g. "off to the fab →"). The board is designed but not yet manufactured, so this is a
   KiCad image (layout or 3D view), not a photo: it uses a plain white printout border and
   tape, not the instant-photo frame used for real photos. When the board arrives, a real
   photo of it replaces the printout and the "off to the fab" note goes.
3. **About**: the existing first-person text, kept.
4. **Projects**: notebook entries instead of identical cards. Each entry: title, date,
   a short description (the current card text trimmed to 1–2 sentences; the full story
   lives on the detail page), a spec table, one margin note, and a link to its detail
   page. The tag rows are dropped; the spec table replaces them. Keep each entry's
   `id="p-…"` and `data-label` attributes, which the skills feature relies on. Layout varies: Crane and
   Robo Heist are larger entries with a taped photo (crane PCB; Robo Heist team photo);
   XM23, LICE and Coral are compact entries (Coral gets its photo once supplied).
5. **Experience**: dated notebook log entries (Leonardo DRS, Marker/TA, CSIR NPL, B.Eng.).
6. **Skills**: same groups and the same clickable behaviour, restyled to fit the notebook.
7. **Contact**: same buttons and links.
8. **Footer**: same text.

### Project pages (`projects/*.html`, 5 pages)

Same content and structure as now (back link, title, meta line, overview, "What I/we
built", tools, previous/next), restyled as notebook pages. Each page gets its spec table
near the top. Photos are shown taped: Robo Heist team photo, crane PCB and coral station
when supplied. The Robo Heist video thumbnail link stays.

### 404 (`404.html`)

Keeps the HardFault joke and content, restyled in graphite.

## Spec table content (decided; all from existing facts)

| Project | Rows |
|---|---|
| Crane | MCU: ESP32, dual core · RTOS: FreeRTOS, pre-emptive · Link: ESP-NOW + watchdog · Board: 2-layer, KiCad |
| XM23 | Language: C, ~4,800 lines · ISA: XM23, 16-bit · Extras: cache simulator, debugger |
| Robo Heist | Brains: Arduino + Raspberry Pi Pico · Sensors: ultrasonic, encoders · Result: 2nd prize |
| LICE | Language: C · Display: VT100 terminal · Focus: pathfinding, obstacle avoidance |
| Coral | Sensors: temperature, pH, turbidity · Board: custom KiCad PCB · Housing: 3D-printed, waterproof |

## Keep (must still work after the redesign)

- Clickable skills that open "What I did with …" under the clicked row, the skill → item
  links and card highlighting, and the `SKILLS` data list in `index.html`.
- Project detail pages and previous/next navigation.
- Scroll progress bar under the header (restyled as a coral pencil line).
- Resume download links (nav, hero, contact, project pages) and the resume PDF.
- GoatCounter script and every existing `data-goatcounter-click` event name, unchanged, so
  analytics history stays comparable.
- The console "boot complete" message.
- Robo Heist video link and team photo.

## Photos

- Kanav will supply a **KiCad image of the crane controller PCB** (designed, being sent for
  manufacture; not built yet) and a **photo of the coral station**. He doesn't have many.
- Two treatments: **real photos** (coral station, Robo Heist team photo) get the
  instant-photo frame; **design images** (KiCad renders/layouts) get a plain white
  "printout" border. Never present a render as a photo of a built board.
- Each photo is resized to at most 1600px on the long side, saved as JPEG around quality
  80, with camera metadata removed, into `projects/img/`.
- Until a photo arrives, the build uses a clearly marked placeholder so layout can be
  checked locally. Placeholders must be replaced, or the photo slot removed, before
  anything is merged to `main`.

## Calls made on Kanav's behalf (he can change any of these)

- Dark-only, no light/dark switch (he didn't answer that question).
- Self-hosted fonts instead of Google Fonts.
- Hero headline "I build hardware that works." and the note "…usually on the 3rd
  revision" (Kanav kept this line). "Hand-routed in KiCad, 2 layers" confirmed true.
  "Happiest with a scope probe in one hand" removed at his request.
- Margin note wording: drafted from existing facts, listed in the build for Kanav to read
  and edit before going live.
- Crane and Robo Heist are the featured (larger) project entries because they have photos.
- Home project entries keep a trimmed 1–2 sentence description; tag rows are dropped.
- Name stays as the `<h1>`; the headline is visual only.
- The crane design image is shown as a taped printout, with an "off to the fab" note.
- The status LED line stays.

## Left to the builder

- Exact spacing, rotation angles, sizes and breakpoints, within the mockup's feel.
- Which existing CSS to delete versus rewrite; file names for the shared stylesheet.
- How the hero photo and notes stack on phones (photo below the text is fine).
- Exact wording of margin notes for XM23, LICE, Coral and the experience entries, as long
  as every note is true and short.

## Delivery

- All work on the `project-pages` branch, previewed locally at `http://127.0.0.1:8765`.
- Check home, all 5 project pages and the 404 at desktop width and at phone width (about
  375px) before calling it done.
- Merge to `main` (which publishes it) only when Kanav says so.
