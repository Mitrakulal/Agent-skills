# Presentation Maker

A skill that teaches an agent to build interactive, click-to-reveal slide
decks — one point popping in at a time with a spring animation, floating
transparent PNG cut-outs, a big swapping image stage, and live interactive
demos. The mechanism from the Line Follower Workshop deck, as a reusable
skill. No line-follower content in here — just the mechanism.

## What's inside

- `SKILL.md` — the complete skill: the reveal system, slide types, PNG
  cut-out rules, design rules, build workflow, and delivery.
- `template/deck.html` — a minimal working deck that implements the
  mechanism. Open it in any browser to see it: title slide, flow slide
  with a swapping stage, component slide, big-word closer. Start every new
  deck from this file.

## Install

Paste this repo link to your agent and ask it to install the
`presentation-maker` skill:

```
https://github.com/Mitrakulal/Agent-skills
```

Or copy the `presentation-maker/` folder into your agent's skills
directory. The skill is `SKILL.md` plus `template/deck.html`; nothing else
is required.

## Use

Ask the agent for a presentation. It builds a self-contained HTML deck —
one file, works offline, click / arrow keys / Space / tap / swipe to step
through it, `O` for the overview grid, `F` for fullscreen.

## One thing to know

The interactivity lives in the HTML deck. A static `.pptx` cannot do
click-pop reveals or live demos — if you need a PowerPoint file, the deck
is the interactive version and the `.pptx` is only a static handout.
