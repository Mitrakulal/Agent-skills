---
name: presentation-maker
description: Build interactive, click-to-reveal slide decks — one point popping in at a time with a spring animation, floating transparent PNG cut-outs, a big image stage, and live interactive demos. Use when the user asks for a presentation, slides, a deck, or a ppt, or wants an existing talk turned into a deck. Do not use for a static document, a report, or a slide file that must open in PowerPoint — the interactivity lives in a self-contained HTML deck (see "Medium rule").
metadata:
  version: "1"
---

# Presentation Maker

Build presentations the way a speaker actually presents them: one point at a
time, each point popping onto the slide as it is spoken, with real images
floating on the slide instead of boxed photos. The deck is a single
self-contained HTML file. It is not a PowerPoint file.

## Medium rule

The interactive mechanism — click-to-reveal, spring pops, live demos — only
exists in the HTML deck. A static `.pptx` cannot reproduce it. If the user
asks for a PowerPoint file, say so plainly, build the HTML deck as the
interactive version, and offer a static export only as a handout. Never claim
a `.pptx` will behave like the deck.

## What a deck built by this skill guarantees

- One click (or arrow key, Space, tap, swipe) reveals exactly one point. The
  audience never sees a point before it is spoken.
- Every revealed point pops in with a spring animation, never a fade or a
  slide-in from the side.
- Images are transparent PNG cut-outs floating on the slide, never photo
  rectangles, cards, or boxed pictures.
- The deck is one self-contained HTML file: it opens in any browser, works
  offline, and needs no build step and no server.
- Slides are reviewed one at a time. Never build the whole deck and present
  it for the first time at the end.

## Architecture

- One HTML file. Inline `<style>` and `<script>`, no external dependencies.
  Images are local files next to the HTML file, referenced by relative path,
  or inline SVG stand-ins when no image is available yet.
- Each slide is a `<section class="slide">`. Inside a slide, every point that
  reveals separately is an element with class `reveal`. Elements without that
  class are visible from the moment the slide appears.
- A tiny script owns all state: current slide index, current reveal step,
  and the chrome (dots, progress bar, counter). No framework, no library.
- Start from `template/deck.html` in this skill. It already implements the
  reveal system, the chrome, and every slide type below. Adapt it; do not
  rebuild the mechanism from scratch.

## The reveal system (the core mechanism)

This is the part that makes the deck feel the way it does. Implement it
exactly.

- Each slide declares its reveal steps in order: the elements with class
  `reveal`, in document order. A slide may have zero reveal steps.
- Forward (click, Right/Down arrow, Space, tap on the right, swipe left)
  advances exactly one step: the next `reveal` element pops in. When a slide
  has no more steps, forward moves to the next slide.
- Back (Left/Up arrow, Back button, swipe right) un-reveals one step. At
  step 0 of a slide, back moves to the previous slide at its last step.
- The pop animation: the element starts at `opacity: 0`, `transform:
  translateY(12px) scale(0.92)`, and animates to `opacity: 1`, `transform:
  none` over ~350 ms with an overshoot easing curve, e.g.
  `cubic-bezier(0.34, 1.56, 0.64, 1)`. The overshoot is the whole feel — a
  plain ease looks flat and a fade looks dead. The same pop is used for every
  reveal, including swapped stage images (below).
- Never reveal two points on one click. Never auto-advance. Never animate
  anything the user did not just ask for.
- A slide with zero reveal steps (title slide, big-word slide) advances to
  the next slide on the first click.

## Navigation and chrome

- Keyboard: Right/Down/Space forward, Left/Up back, `O` toggles the overview
  grid, `F` toggles fullscreen, `Home`/`End` jump to first/last slide.
- Mouse/touch: click anywhere (or the on-screen next/back controls) steps
  forward/back; swipe left/right steps forward/back.
- Slide dots along the bottom: one dot per slide, the current dot filled.
  Clicking a dot jumps to that slide at step 0.
- A thin progress bar across the top fills with slides + reveal steps, so
  the speaker always knows where they are in the talk.
- A slide counter in the deck bar (e.g. `4 / 12`). Hide it on the final
  slide when that slide is a single big word (see "Big-word slides").
- An overview grid (`O` key): a thumbnail grid of all slides; clicking one
  jumps to it.
- A fullscreen button. Keep the chrome quiet: dots, bar, counter, overview,
  fullscreen — nothing else. No extra HUD, no animation descriptions, no
  meta text about how the deck works.

## Slide types

### Title slide

- Zero reveal points: one click goes straight to slide 2.
- A logo or mark at the top (if the talk has one), the title, and one
  horizontal accent line under the title.
- One continuously moving element on that line: a small graphic that travels
  the line back and forth and loops forever. The movement lives on the line,
  not on the main image — the main image stays static.
- One static cut-out beside the title (the real object, the product, the
  speaker's own photo cut-out). On narrow screens (under ~900 px) the
  cut-out stacks above the title.
- Nothing else on the slide. No subtitle paragraph, no agenda on slide 1.

### Flow slide (the talk's roadmap)

- Left: the checkpoints of the talk, in order, each a short phrase
  (3–5 words). Each checkpoint is one reveal step.
- Right: one BIG image stage, about 300–380 px, with a drop shadow and no
  box, border, or card around it. Exactly one image shows at a time.
- The stage image matches the latest revealed checkpoint and swaps with the
  spring pop on each click. Back steps the stage image back. Never show
  small icons beside each checkpoint — one big image, swapping, is the
  whole point.
- Do not add a "How today runs" card or any second explanation of the flow.
  The checkpoints are the flow.

### Component / explainer slides

- A kicker line at the top: the section and the part number, e.g.
  `The kit · Part 2 of 7`. Keep kickers numbered consistently after every
  structural edit.
- Points pop in one per click. Keep each point to one line of plain words
  (a sentence at most). No invented specifications, numbers, or claims —
  every number on a slide comes from the user's real object, measurement,
  or source.
- The subject's cut-out floats on the slide, large enough to read, with a
  drop shadow. If labels point at parts of the image, sync the labels to
  the clicks: a label appears with the point that mentions it.
- When a before/after pair is needed, show both at the same display size,
  side by side, labelled BEFORE and AFTER. Check the orientation of the
  before image against the after image before shipping — a rotated board
  reads as a mistake, not a detail.

### Big-word slides

- Just the words, in huge type, centred on the slide. Two-tone: the
  framing words in white, the punch word in the accent colour.
- No kicker, no subtext, no points, no reveals. One click moves on.
- Use for section breaks (e.g. a single word like `DEMO` or `ASSEMBLY`)
  and for the final slide (e.g. `THANK YOU`). On the final slide, hide
  the slide counter so no number appears.

### Live demo slides

- The last reveal of an explainer slide may be a live interactive panel
  instead of a static point. Two patterns, both driven by the slide's own
  JavaScript, no server:
  - **Instrument panel:** a draggable object over a track or scene on the
    left, and a live readout window on the right streaming the numbers the
    object actually produces (e.g. sensor values), updating a few times a
    second, with a Play/Pause control. The numbers must come from the
    real geometry or the real device — simulate from the true measurements
    (e.g. the real low/high values), never invent a range that looks
    plausible.
  - **Brain loop:** three stages — SENSE (live numbers) → DECIDE (the
    decision in plain words, plus why) → DRIVE (the resulting action,
    shown as bars or motion). Play drives it; the object drifts, the
    system corrects. Draggable at any time.
- A demo panel is the last reveal of its slide so the speaker reaches it
  naturally and can stay on it as long as the demo needs.
- Verify a demo by simulation before shipping: run the numbers through
  the real geometry or logic and check the behaviour stays sane (the
  object never gets lost, the values never jump impossibly). Report the
  verification in one line to the user; do not claim a live check that
  was only a code read.

## PNG cut-outs

Images make or break the deck. The rule is cut-outs, not photos.

- Every image on a slide is a transparent PNG: the object with its
  background removed, floating on the slide with a drop shadow. Never a
  photo rectangle, never a card, never a picture inside a box.
- Making a cut-out: background removal with a lightweight model (e.g.
  `rembg` with the small `u2netp` model — do not use the 1 GB default
  model in a small VM, it gets killed). One image per fresh process,
  downscale to at most 1200 px on the long edge first, two threads.
- Traps: some clipart sites bake a checkerboard pattern into the pixels
  of a supposedly transparent PNG. Always check the corner alpha before
  trusting one — a fake transparent image shows its checkerboard on the
  slide. Luminance-threshold extraction works for black-on-white line
  icons; luminance-as-alpha works for white-on-black logos.
- When cutting a logo mark out of a full logo, find where the wordmark
  text actually starts (check with a zoomed view, not a column count —
  column counts mislead) and crop well left of it. A stray letter next to
  the mark reads as a mistake at any size.
- Name cut-outs by slide and order (`01-…`, `02-…`) and keep them in a
  `components/` folder next to the deck.
- If no cut-out exists yet, use a simple inline SVG stand-in in the
  template and mark it clearly as a stand-in. Never ship a stand-in as if
  it were the real image.

## Design rules

- Minimal beats maximal. One instance of each feature, no duplicates, no
  decoration for its own sake.
- Dark background, light text, one accent colour (orange in the reference
  deck — pick the accent from the user's own brand or topic, not from a
  preset). All body text the same light colour; the accent is for the
  punch word, the line, and the current dot only.
- No meta text about animations, no "click to reveal" hints on the slides,
  no extra HUD chrome. The speaker knows how it works; the audience
  should only feel it.
- Keep creative touches professional. A moving element on the title line
  is a touch; a staged multi-step reveal with teasing lines is a
  production. When the user says "simple", build exactly the simple form
  and confirm the concept in one line before adding any extra step, line,
  or effect.

## Build workflow

- Build one slide at a time and show it before moving on. The user
  reviews in one-line steers and corrects instantly — a full deck built
  in one go wastes the whole round trip.
- Content is frozen unless the user changes it. Never rewrite their words,
  never compress their points, never add a point they did not ask for.
- When the user describes a layout spatially, play it back in words and
  confirm it before building. After a repeated visual misread, stop
  rebuilding variants and play the layout back in words first, then build
  once.
- When the user says "Noo" they are restating their exact plan, not
  inviting debate: play it back verbatim against its constraints and
  confirm what holds.
- Verify every build the same way: open the deck, step through every
  reveal on every slide, and check the stage images swap, the counter and
  dots track, and the demo numbers stay sane. Screenshot the slides that
  changed. Report what you checked; do not claim a live check that was
  only a code read.

## Delivery

- Hand over the deck as a working link plus the single HTML file, in the
  same message that says it is ready. A file saved on the agent's machine
  has not reached anyone yet.
- Keep the deck's images next to the HTML file and reference them by
  relative path, so the folder stays portable: HTML + images + nothing else.
- If the user wants to share the deck publicly, publish it and hand over
  the plain-text copyable link. Edits reach viewers only when the deck is
  shared again, at the same URL — say so when handing it over.

## Installing this skill

- Paste the repository link (`https://github.com/Mitrakulal/Agent-skills`)
  to an agent and ask it to install the `presentation-maker` skill, or
  copy the `presentation-maker/` folder into the agent's skills
  directory. The skill is `SKILL.md` plus `template/deck.html`; nothing
  else is required.
- After installing, the agent builds decks by starting from
  `template/deck.html` and following this file. The template is a working
  deck — open it in a browser to see the mechanism before building on it.
