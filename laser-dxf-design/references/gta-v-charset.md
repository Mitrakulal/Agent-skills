# Worked example — GTA V unique character set

Decorative/text mode. One outline per unique letter in **grand theft auto**
(11 letters) plus the two-piece V logo. The letters come from the official
logo SVG's white fills; the V comes from the supplied raster reference.

## Spec

| Item | Value |
|---|---|
| Letters | `g r a n d t h e f u o` (11 unique; `t` and `a` repeat in the phrase) |
| Letter box | 15 × 10 mm each |
| V box | 20 × 20 mm |
| V actual | 20.00 × 17.06 mm, two pieces |
| Material | 3 mm acrylic |
| DXF | R12 (AC1009), mm, 1:1 |
| Layers | `CUT` red only |
| Layout | 4 × 3 grid, 20 mm cells, 25 mm pitch, 5 mm margin |
| Overall | 105 × 80 mm; piece extents 88.74 × 63.53 mm |

## Source handling

- Letters: official `Grand_Theft_Auto_V_Logo.svg`, white fill paths.
  Path IDs: `g`=`path630`, `a`=`path612`, `n`=`polygon600`, `d`=`path458`,
  `t`=`polygon622`, `e`=`path598`, `f`=`polygon160`, `u`=`polygon624`,
  `o`=`path596`.
- `r` and `h` are merged in `path610`; split at the row baselines
  (`r` below 188.32, `h` above 218.32).
- The SVG's `r` is mirrored relative to the reference; flip it about its
  own centre.
- V: threshold the purple pixels from the JPEG. The white slash separates
  two components; do **not** close it. Left component 144 × 123 px, right
  120 × 169 px, union 197 × 168 px.
- Place both V pieces with one transform from the union bbox so the gap and
  relative positions survive. Do not fit each V piece to its own box.

## Sizes

| Piece | Bounding box (mm) | Counters |
|---|---|---|
| g | 5.39 × 9.99 | 1 |
| r | 7.07 × 10.00 | 1 |
| a | 7.04 × 10.00 | 1 |
| n | 6.93 × 10.00 | 0 |
| d | 5.59 × 10.00 | 1 |
| t | 7.24 × 10.00 | 0 |
| h | 6.90 × 10.00 | 0 |
| e | 7.03 × 10.00 | 1 |
| f | 7.47 × 10.00 | 0 |
| u | 6.89 × 10.00 | 0 |
| o | 7.15 × 10.00 | 1 |
| V left | 14.52 × 12.28 | 0 |
| V right | 12.08 × 17.06 | 0 |

V overall 20.00 × 17.06 mm; the gap between the pieces is 0.76 mm at this
scale. The V is width-limited.

## Process decisions

- Letters and counters cut through; counters fall out.
- The V is **two pieces**, not one piece with an engraved slash. The white
  slash in the reference is a real gap. There is no `ENGRAVE` layer.
- The `r` has an open slot about 0.53 mm wide; it is part of the outline,
  not a closed counter.
- Minimum counter 0.62 mm (`g`); minimum wall 0.73 mm (`o`). These are at
  the limit for 3 mm acrylic — test-cut. If the `o` ring fails, omit or
  engrave its counter, or enlarge the glyph; do not silently thicken it.

## Validation

- 13 pieces: 11 unique letters + 2 V pieces.
- 19 closed `CUT` polylines: 13 outer outlines + 6 counters.
- 0 `ENGRAVE` entities; 0 `LINE` entities.
- All letters ≤ 15 × 10 mm; V overall ≤ 20 × 20 mm.
- Min hole 0.62 mm; min stroke 0.73 mm; min inter-piece gap 11.48 mm.
- DXF audit: 0 errors; bundled validator: PASS; DXF render check: PASS.
- Reference-vs-DXF side-by-side checked at the same height.

## Lessons

- Official vector beats a lookalike font. The lettering is the brand; a
  generic bold font is a different design.
- Split merged paths before fitting. `r` + `h` in one path would have been
  scaled as a group and both glyphs would be wrong.
- A per-glyph 15 × 10 mm box includes ascenders and descenders. Letters
  with them (`g`, `d`, `h`, `t`, `f`) have a smaller x-height and read
  smaller than x-height-only letters (`a`, `e`, `o`); state the tradeoff
  instead of stretching.
- A white slash may be a gap, not a mark. Two-piece logos need a placement
  note and a check that the gap is wide enough to survive kerf.
- Hairline counters are the real risk, not the outer silhouette. Measure
  them and flag a test cut.
- Rebuild the full chain after any geometry change. The first zip in this
  job was stale (old DXF and pre-simplification previews); a stale package
  is a wrong part.
- Render from the DXF, not the source art, and compare it to the reference.

## Files in this reference

No logo image is shipped with this reference; the dimensions and source
handling above are the reusable part.
