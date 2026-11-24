# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Recruiters and hiring managers** filling new-grad roles in embedded systems, firmware, and hardware engineering. They usually arrive from Kanav's resume or LinkedIn and decide quickly whether he is worth an interview.
- **Engineers doing technical screens**, who open the project pages to check what he actually built and how deep it goes.

The site exists to impress both groups (confirmed by Kanav). Other audiences, such as co-op coordinators or grad school admissions, are not confirmed.

## Product Purpose

The site is the personal portfolio of Kanav Tyagi, a final-year Computer Engineering student at Dalhousie University (graduating April 2027) who is looking for a new-grad role in embedded, firmware, or hardware engineering. Success means a recruiter or engineer leaves convinced that he is worth interviewing, then downloads his resume, emails him, or opens LinkedIn. GoatCounter tracks those clicks.

## Positioning

Kanav is not sure what sets him apart from his classmates. The angle below is **proposed from the evidence below and still needs his confirmation**:

> He already works like an embedded engineer, across the whole stack: he lays out the board, writes the firmware, and tunes the control loop. Each claim is backed by something you can see.

The evidence for it:

- Industry firmware work on power conversion for naval UPS systems at Leonardo DRS, done as a co-op. It covered tuning the PI loop on TI MCUs, checking it in PSIM first, and CAN bus between modules.
- His own two-layer KiCad PCB for the ESP32 crane controller, plus the FreeRTOS firmware behind it.
- A CPU emulator in about 4,800 lines of C (XM23) with interrupts, a cache simulator, and a debugger.
- A measurable result: 2nd prize, as part of a team, in the ECED 3901 design challenge.

The second thing visitors should remember: he enjoys building real hardware, and he put real time into this site himself. It is not a template.

## Operating Context

- Visitors usually come from his resume PDF or LinkedIn, on desktop or phone.
- Recruiters skim the home page. Engineers go deeper into the project detail pages under `projects/`.
- The resume download (`Kanav_Tyagi_Resume.pdf`) is a main action. The PDF is Kanav's own document, and it must agree with the site.

## Capabilities and Constraints

- **Stack:** static HTML and CSS, plus a small amount of plain JavaScript. There is no build step and no dependencies. Hosting is GitHub Pages (legacy Jekyll build from the `main` root). Repo: `KanavTyagi/KanavTyagi.github.io`.
- **Analytics:** GoatCounter is the only analytics. Clicks are tracked through `data-goatcounter-click` events on the resume, email, LinkedIn, and video links.
- **Pages:** the home page, five project detail pages, and the 404 page.
- **Home page features:** clickable skill pills that show what he did with each skill and link to the evidence.
- **Before merging:** run `python tools/check_site.py --release`. The `docs/`, `tools/`, and `.superpowers/` folders are kept off the live site through `_config.yml`.
- **Changes are tested on a branch first.** Nothing goes to `main` (live) without Kanav's explicit go-ahead.
- **Not yet decided:**
  - details for these skills: STM32, Assembly, UART/I2C, oscilloscopes and logic analyzers, MATLAB/Simulink, Linux, Git, SolidWorks;
  - whether to remove the old public `Kanav_Tyagi_Resume_2.pdf`.

## Brand Commitments

- **Engineering theme** (Kanav's request). The site should feel like the work of a hardware engineer.
- **Must not look like a generic, AI-generated site** (Kanav's request).
- **Voice:** first person, plain, and specific, like one engineer talking to another. Avoid buzzwords.
- **Only claim his own work:**
  - Team projects are labelled as team projects. Robo Heist was a team project (Group 19).
  - The coral station PCB was designed by someone else. Never say he designed or tested it.
  - The crane controller PCB is his.
- **Privacy:** no phone number on the site. The public email is kanavtyagi.172@gmail.com.

## Evidence on Hand

- **Crane controller board:** a 3D render made with KiCad, `projects/img/crane-pcb-render.jpg`. It comes from `RTOS/check_PCB_final/ESP32_Controller.kicad_pcb`. The board is designed but not yet built.
- **Robo Heist:**
  - team photo with the 2nd prize certificates: `projects/img/robo-heist-team.jpg`;
  - livestream of the run: https://www.youtube.com/watch?v=FZEagNN6bVo&t=23468s (the team's run starts at 6:31:08). The video does not allow embedding on other sites.
- **Coral station:** a photo of the test rig, `projects/img/coral-test-rig.jpg`. The PCB is not visible in it.
- **Real numbers:**
  - 85% accuracy on 15,000+ data points (CSIR NPL);
  - about 4,800 lines of C (XM23);
  - 2nd prize (Robo Heist).
- **What does not exist, and must not be invented:** testimonials, references, employer logos used as endorsements, photos of the built crane, coral PCB photos, and benchmarks or results not listed above.

## Product Principles

1. **Proof over adjectives.** Every claim points to something real: a board, a number, a video, or a page.
2. **Credit honestly.** Say what was his, what was the team's, and what is still in progress.
3. **Easy for recruiters to skim, deep enough for engineers.** The home page gets the point across in seconds, and the project pages hold up to a technical reader.
4. **Hand-made.** The site should show care and personality.
5. **Plain and fast.** No dependencies, quick to load, and it works on a phone.
