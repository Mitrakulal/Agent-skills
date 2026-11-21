---
name: laser-dxf-design
description: Design and export manufacturable 2D DXF files for laser cutting and engraving — mechanical plates, brackets, chassis, and decorative logo art. Use when the user asks for a laser-cut part, a DXF, an acrylic or metal plate, a 2D vector cut file, or a shop-ready cut package. Covers parametric hole layouts, layer and DXF-version conventions, pre-cut validation, previews, and a clean export (DXF + preview PNGs + DETAILS.md).
metadata:
  version: "1"
---

# Laser DXF Design

Produce 2D files a laser shop can cut without a phone call. There are two
families, and both end in the same export package:

- **Mechanical** — dimension-driven: plates, chassis, brackets, mounts.
  Holes and edges are toleranced; fit matters.
- **Decorative** — shape-driven: logos, art, ornaments. Contour quality and
  minimum feature size matter.

The rule for both: **the DXF is the deliverable, not the drawing.** A pretty
preview of a broken file is worse than useless.

## Non-negotiables

- Millimetres, 1:1, no scale factor. State the unit in `DETAILS.md`.
- Every cut profile is closed. No stray lines, no open contours, no
  zero-length entities.
- One source of truth for dimensions. Generate the DXF and the hole schedule
  from the same constants.
- Validate before export, then render the DXF itself and look at it.
- Export package is exactly: DXF + preview PNG + DXF-render PNG +
  `DETAILS.md`. No source code, no PDF, no temp files.
- Never hand-edit a DXF after validation. Fix the source and regenerate.

## Step 1 — Intake

Collect only what changes the geometry:

| Item | Why it matters |
|---|---|
| Part type | mechanical vs decorative |
| Overall size | plate outline / artboard |
| Material + thickness | minimum web, cut settings |
| Process | cut, engrave, or both; which face |
| Component holes | diameter, pitch, edge offsets |
| Corner radius | outline geometry |
| DXF version | R12 vs R2000 |
| Layer names / colours | shop template |
| Quantity / critical fit | tolerance and test-cut decision |

If the user supplies a drawing, treat it as a **claim**, not truth. Verify
critical dimensions against the physical part or the vendor drawing. Record
every unverified number in `DETAILS.md` under **Assumptions & risks**.

## Step 2 — Pick the DXF dialect

- **R12 (AC1009)** — maximum compatibility. `POLYLINE`/`VERTEX`, `CIRCLE`,
  `ARC`, `LINE`, `TEXT`. No `LWPOLYLINE`, no true colour, no `$INSUNITS`.
  Default for laser shops unless they ask otherwise.
- **R2000 (AC1015)** — `LWPOLYLINE`, `MTEXT`, colours, units. Use when the
  shop's software is modern or the source art already uses lwpolylines.

Never write `LWPOLYLINE` into an R12 file. If you need lwpolylines, export
R2000 and say so.

## Step 3 — Layers

Default convention:

| Layer | Colour | Contents |
|---|---|---|
| `CUT` | red (ACI 1) | outer profile, holes, slots |
| `ENGRAVE` | blue (ACI 5) | surface marking, text |
| `SCORE` | green (ACI 3) | fold / score lines (optional) |
| `FRAME` | cyan (ACI 4) | artboard / registration frame (optional) |
| `NOTES` | yellow (ACI 2) | non-output notes (optional) |

One purpose per layer. Never put cut geometry on layer `0`. If the shop
supplies a template, match its names and colours exactly.

## Step 4 — Mechanical design

### Model

- Use a parametric script (Python + `ezdxf` + `shapely` is the reference
  stack). Keep every dimension in one module.
- Origin at the part's bottom-left; part occupies `(0,0)` to `(W,H)`;
  +X right, +Y up.
- Outer profile: one closed polyline. Fillets: bulges in R12, arcs in R2000.
- Holes: one `CIRCLE` per hole. Slots: closed polyline with semicircular ends.
- Mirror stations by negating offsets, never by copying absolute
  coordinates — copies drift.

### Hole sizing

| Fastener | Plate hole | Notes |
|---|---|---|
| M2 | Ø2.2 | |
| M2.5 | Ø2.7 | |
| M3 | Ø3.2 | standard clearance |
| M4 | Ø4.3 | |
| M5 | Ø5.3 | |
| M3 heat-set insert | Ø4.0–4.2 | match insert datasheet |

The component's own hole (e.g. Ø3.0 on a PCB) is not the plate hole. Plate
hole = fastener + clearance. State both numbers in the schedule.

### Spacing

- Edge margin: `max(2 mm, 1.5 × thickness)`.
- Web between holes: `max(2 mm, 1.0 × thickness)` for acrylic; more for
  brittle material.
- Keep hole centres on a clean grid where possible; it makes the schedule
  readable and the part easy to inspect.

### Text

- Native `TEXT`/`MTEXT` is fine for engraving. Keep it on `ENGRAVE`.
- If the shop requires outlines, explode text to polylines before export and
  note it.
- Never put text on `CUT` unless the letters are meant to fall out.

### Kerf

Do not compensate by default — the shop's CAM applies kerf. If the user
explicitly asks for kerf compensation, offset the cut profile inward by
`kerf/2`, state the value, and keep the uncompensated source.

## Step 5 — Decorative design

- Convert filled art to **closed outlines**. Every filled region is one or
  more closed contours.
- Nested contours alternate: an outer contour cuts, an inner contour either
  falls out (cut) or is engraved. Decide per shape and document it.
- Minimum feature for 3 mm acrylic: **≥ 2 mm**; below that, engrave or add
  bridges. Islands under ~5 mm will fall out — bridge them (0.3–0.5 mm) or
  engrave them.
- Keep a consistent margin to the frame (10 mm is a good default).
- Simplify with a tolerance of 0.05–0.1 mm. Check for self-intersections and
  duplicate vertices after simplification.
- The preview must render the **DXF**, not the source art. Filled art and
  outline art look different; the shop cuts the outline.

## Step 6 — Validate

Run the bundled validator:

```bash
python scripts/validate_dxf.py part.dxf --cut CUT --engrave ENGRAVE \
  --expect-holes 32 --expect-size 140 200 --single-outline --min-web 2.0
```

It checks:

- file opens; `doc.audit()` clean
- entity counts by layer and type
- every cut entity closed; no `LINE`/`ARC` strays on `CUT`
- holes (circles) inside the outer profile (`--single-outline`)
- minimum cut-to-cut distance (`--min-web`)
- duplicate holes
- extents match `--expect-size`
- text on `CUT`
- zero-length entities

Then the manual gate: open `<part>_dxf_render.png` at 1:1, measure three
dimensions with a ruler or caliper, and compare to `DETAILS.md`. A render
that looks right at fit-to-screen can still be 5% off.

## Step 7 — Export package

Exactly four files, zipped together:

1. `<part>.dxf`
2. `<part>_preview.png` — annotated top view: dimensions, station labels,
   title, layer legend.
3. `<part>_dxf_render.png` — rendered from the DXF entities themselves.
4. `DETAILS.md` — the shop sheet.

No `.py`, no PDF, no source art, no intermediate renders. Keep the build
scripts in the working folder; they are not part of the deliverable.

### `DETAILS.md` template

```markdown
# <Part name> — laser cut package

- Date:
- Revision:
- Prepared by:

## Specification

- Overall size: W × H mm
- Material: <material>, <thickness> mm
- Process: cut / engrave / both
- DXF version: R12 (AC1009) / R2000 (AC1015)
- Units: millimetres, 1:1

## Layers

| Layer | Colour | Purpose |
|---|---|---|
| CUT | red | through-cut |
| ENGRAVE | blue | surface mark |

## Hole schedule

| Station | Component | Qty | Ø (mm) | X (mm) | Y (mm) | Pitch (mm) |
|---|---|---|---|---|---|---|

## Engraving

| Text | X | Y | Height (mm) |
|---|---|---|---|

## Cut notes

- Kerf: shop standard (not pre-compensated)
- Test cut: <yes/no>
- Masking / focus: <shop standard>

## Validation

- Entities: ...
- Holes: ... (expected ...)
- Outer profile: closed, single loop
- Extents: ... × ... mm
- Min cut-to-cut: ... mm
- Duplicates: 0
- Audit: 0 errors
- Render check: PASS

## Assumptions & risks

- ...

## File manifest

- `<part>.dxf`
- `<part>_preview.png`
- `<part>_dxf_render.png`
- `DETAILS.md`
```

## Step 8 — Delivery

- Filenames: lowercase, hyphens, no spaces.
- Tell the user what was verified and what is assumed. Do not bury a risk.
- For fit-critical parts, offer a 1:1 paper print before cutting.
- If the shop asks for R2000, different layer names, or nesting, re-export
  from the source. Never hand-edit the validated DXF.

## Reference cases

- `references/chassis-200x140.md` — 200 × 140 × 3 mm acrylic chassis, four
  clamp stations, two L298N stations, R12, 32 holes.
- `references/diya-logo-150.md` — 150 × 150 mm decorative diya logo,
  AC1015, `FRAME` + `LOGO`, nested contours and small-feature risks.

## Pitfalls

- R12 + `LWPOLYLINE` — invalid file. Use `POLYLINE` or export R2000.
- Bulge sign and direction — a fillet drawn the wrong way becomes a loop.
- Copying a mirrored station — coordinates drift; mirror offsets instead.
- Duplicate holes where stations overlap — the validator catches them.
- Text on `CUT` — the laser cuts the letters out.
- Filled art previewed as fill but exported as outlines — the shop cuts the
  outline, so check the render, not the art.
- Trusting a client drawing — verify the physical part.
- Measuring a photo without correcting perspective — use an orthographic
  vendor drawing or measure the part.
- R12 has no `$INSUNITS` — state mm in `DETAILS.md`.
