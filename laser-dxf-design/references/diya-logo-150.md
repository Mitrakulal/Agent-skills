# Worked example — 150 × 150 mm diya logo

Decorative mode. A diya (oil lamp) mark built from closed filled regions:
a bowl, a flame, and a ring of rays. Two variants exist: simple (15 logo
contours) and ornate (45 logo contours).

## Spec

| Item | Value |
|---|---|
| Artboard | 150 × 150 mm |
| Frame | 150 × 150 mm closed square on `FRAME` |
| DXF | AC1015 (R2000) |
| Layers | `FRAME` cyan (ACI 5), `LOGO` red (ACI 1) |
| Contours | simple: 15 logo + 1 frame; ornate: 45 logo + 1 frame |

## Geometry (simple)

- Logo extents: X 12.1–137.9, Y 10.0–118.9; 10 mm minimum margin to frame.
- 15 closed lwpolylines, all valid, all closed.
- One nested contour: the inner flame sits inside the outer flame (depth 1).
- Rays: 12 islands, each ~45–50 mm², narrowest ~2.8 mm.
- Union area: 6730 mm² of the 22 500 mm² frame.

## Process decision

- Frame: cut or engrave? Decide with the user. Cut = a loose 150 mm square;
  engrave = a registration border.
- Bowl/flame: cut through if the logo is a silhouette; engrave if it is a
  surface mark on a solid plate.
- Nested inner flame: cut through (falls out) or engrave. Never leave it
  ambiguous in the file.
- Rays: at ~2.8 mm wide they are cuttable in 3 mm acrylic but fragile.
  Below 2 mm, engrave or bridge.

## Validation

- All 16 (simple) / 46 (ornate) contours closed and valid.
- No self-intersections.
- Frame is exactly 150 × 150.
- Render the DXF itself; the supplied preview is an illustration, not proof
  of the cut geometry.

## Lessons

- Filled art exports as outlines. The preview shows fill; the laser cuts
  the outline. Always ship a DXF render, not the source art.
- Nested contours are islands: the inner flame is a separate piece. Decide
  cut vs engrave per nesting level.
- R2000 (`LWPOLYLINE`) is fine here; do not down-convert to R12 without
  converting lwpolylines to polylines.
- The ornate variant has 45 contours and features down to ~2.8 mm — check
  min feature before cutting.

## Files in this reference

- `diya-logo-150_preview.png` — illustrative preview.
