# Laser DXF Design

A skill that teaches an agent to design and export manufacturable 2D DXF
files for laser cutting and engraving — mechanical plates, brackets,
chassis, and decorative logo art. The output is a shop-ready package: the
DXF, two previews, and a details sheet. No source code in the package.

## What's inside

- `SKILL.md` — the complete workflow: intake, DXF dialect, layers,
  mechanical and decorative design, validation gates, export package, and
  handling design changes without hand-editing the DXF.
- `scripts/validate_dxf.py` — pre-cut validator: closed contours, hole
  counts, extents, minimum webs, duplicates, audit.
- `references/chassis-200x140.md` — worked mechanical example (acrylic
  chassis, 4 clamp stations, 2 L298N boards, R12).
- `references/diya-logo-150.md` — worked decorative example (150 × 150
  logo, AC1015, nested contours, small-feature risks).

## Install

Paste this repo link to your agent and ask it to install the
`laser-dxf-design` skill:

```
https://github.com/Mitrakulal/Agent-skills
```

Or copy the `laser-dxf-design/` folder into your agent's skills directory.

## Use

Ask for a laser-cut part, a DXF, an acrylic plate, a chassis, or a logo cut
file. The agent designs it, validates it, renders it, and hands back a zip
containing only the DXF, the previews, and `DETAILS.md`.

## One thing to know

The DXF is the deliverable. A preview that looks right is not proof — the
validator and a 1:1 render check are the gate. The skill never ships source
code in the export package.
