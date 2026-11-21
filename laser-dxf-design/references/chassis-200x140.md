# Worked example — 200 × 140 × 3 mm acrylic chassis

Mechanical mode. A four-motor robot chassis plate: four L-shaped metal
clamp stations and two L298N driver boards. Nothing else on the plate.

## Spec

| Item | Value |
|---|---|
| Outline | 140 mm (X) × 200 mm (Y) |
| Material | cast acrylic, 3 mm |
| Corners | R5 |
| Origin | bottom-left; FRONT = Y0, BACK = Y200 |
| DXF | R12 (AC1009), mm, 1:1 |
| Layers | `CUT` red, `ENGRAVE` blue |
| Holes | 32 total: 24 × Ø3.4 + 8 × Ø3.2 |

## Stations

### L-clamp × 4

- Base 40 × 20 mm; vertical face flush with the side edge; bend outboard.
- 10 mm from the plate end.
- 6 × Ø3.4 per clamp (24 total).
- Pattern: 3 across the 20 mm depth at 4 / 10 / 16 mm from the bend;
  2 along the 40 mm length at 5 / 35 mm from the clamp end.

### L298N × 2

- 44 × 47 mm clearance box (44 along X, 47 along Y).
- Centres at X 45 / 95, Y 162.5.
- 4 × Ø3.2 per board (8 total) at 37 × 37 mm pitch.
- Hole coordinates: X 26.5 / 63.5 / 76.5 / 113.5; Y 144 / 181.

## Validation

```
entities: 32 circles, 1 polyline
clamp holes: 24 × Ø3.4
L298N holes: 8 × Ø3.2
outer profile closed: true
all holes inside: true
duplicates: none
min hole-to-edge: 2.30 mm
min hole-to-hole: 2.60 mm
audit: 0 errors
RESULT: PASS
```

## Lessons

- The client PDF assumed a 4-hole clamp; the physical clamp has 6. The
  photo-derived pattern was used instead. A drawing is a claim.
- The L298N envelope is 44 × 47 mm, but the hole pitch came from the
  standard 43 × 43 board (37 × 37). Record the source of each number; do
  not let one drawing supply both.
- R12 + `POLYLINE` with bulges gives the R5 corners without arcs.
- Washers under M3 heads: the 2.3 mm edge web is the weak point in 3 mm
  acrylic.

## 250 mm variant (current)

Same design, plate length changed from 200 to 250 mm:

- rear clamp stations move to Y 200–240 (holes at Y 205 / 235);
- L298N centres move to Y 211.5 (holes at Y 193 / 230);
- title engraving becomes `CHASSIS 250x140x3`;
- hole sizes, pitches, layers and the 4-file export package are unchanged.

Everything else in this reference still applies.

## Files in this reference

- `chassis-200x140_preview.png` — annotated top view.
- `chassis-200x140_dxf-render.png` — render taken from the DXF itself.
