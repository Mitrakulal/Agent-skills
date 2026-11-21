#!/usr/bin/env python3
"""Pre-flight validator for 2D laser-cut DXF files.

Usage:
    python validate_dxf.py part.dxf --cut CUT --engrave ENGRAVE --expect-holes 32
    python validate_dxf.py part.dxf --cut CUT --single-outline \
        --expect-size 140 200 --min-web 2.0

Checks:
    - file opens and DXF audit is clean
    - entity counts by layer and type
    - every cut entity is closed (no LINE/ARC strays, no open polylines)
    - text is not on the cut layer
    - hole (CIRCLE) count matches --expect-holes
    - extents match --expect-size
    - single outer contour and all other contours inside it (--single-outline)
    - minimum cut-to-cut distance (--min-web)
    - duplicate contours

Requires: ezdxf, shapely
    pip install ezdxf shapely

Exit code 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import ezdxf
from ezdxf import bbox
from ezdxf import path as ezpath
from shapely.geometry import Polygon

FLATTEN = 0.05
TOL = 1e-6


def polygon_of(entity):
    """Flatten a path-like DXF entity into a Shapely polygon."""
    try:
        p = ezpath.make_path(entity)
        pts = [(v.x, v.y) for v in p.flattening(FLATTEN)]
    except Exception:
        return None
    if len(pts) < 3:
        return None
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    poly = Polygon(pts)
    if not poly.is_valid:
        poly = poly.buffer(0)
    if poly.is_empty:
        return None
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda g: g.area)
    return poly


def closed(entity):
    t = entity.dxftype()
    if t == "CIRCLE":
        return True
    if t == "LWPOLYLINE":
        if entity.closed:
            return True
        pts = list(entity.get_points("xy"))
        return len(pts) > 2 and pts[0] == pts[-1]
    if t == "POLYLINE":
        if entity.is_closed:
            return True
        pts = list(entity.points())
        return len(pts) > 2 and pts[0][:2] == pts[-1][:2]
    if t == "SPLINE":
        return bool(entity.closed)
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate a 2D DXF before laser cutting.")
    ap.add_argument("dxf", type=Path)
    ap.add_argument("--cut", default="CUT", help="cut layer name (default CUT)")
    ap.add_argument("--engrave", default="ENGRAVE", help="engrave layer name (default ENGRAVE)")
    ap.add_argument("--expect-holes", type=int, default=None,
                    help="expected number of CIRCLE entities on the cut layer")
    ap.add_argument("--expect-size", nargs=2, type=float, metavar=("W", "H"), default=None,
                    help="expected extents width and height in mm")
    ap.add_argument("--single-outline", action="store_true",
                    help="require one outer cut contour and every other cut contour inside it")
    ap.add_argument("--min-web", type=float, default=0.0,
                    help="minimum allowed cut-to-cut distance in mm")
    ap.add_argument("--tol", type=float, default=0.1,
                    help="size tolerance in mm (default 0.1)")
    args = ap.parse_args(argv)

    fails = []
    notes = []

    try:
        doc = ezdxf.readfile(args.dxf)
    except Exception as exc:
        print(f"FAIL: cannot read {args.dxf}: {exc}")
        return 1

    msp = doc.modelspace()
    print(f"file: {args.dxf.name}")
    print(f"version: {doc.dxfversion}")
    insunits = doc.header.get("$INSUNITS", None)
    print(f"units: {insunits if insunits not in (None, 0) else 'not set (state mm in DETAILS.md)'}")

    auditor = doc.audit()
    errors = len(auditor.errors)
    fixes = len(auditor.fixes)
    print(f"audit: {errors} errors, {fixes} fixes")
    if errors:
        fails.append(f"DXF audit reports {errors} error(s)")

    layers = [(l.dxf.name, l.dxf.color) for l in doc.layers]
    print("layers:", ", ".join(f"{n} (ACI {c})" for n, c in layers))

    counts = Counter((e.dxf.layer, e.dxftype()) for e in msp)
    print("entities:")
    for (layer, typ), n in sorted(counts.items()):
        print(f"  {layer:12s} {typ:12s} {n}")

    cut = [e for e in msp if e.dxf.layer == args.cut]
    if not cut:
        fails.append(f"no entities on cut layer '{args.cut}'")

    strays = [e for e in cut if e.dxftype() in ("LINE", "ARC")]
    open_polys = [e for e in cut
                  if e.dxftype() in ("LWPOLYLINE", "POLYLINE", "SPLINE") and not closed(e)]
    if strays:
        fails.append(f"{len(strays)} open LINE/ARC entit(ies) on cut layer")
    if open_polys:
        fails.append(f"{len(open_polys)} open polyline/spline entit(ies) on cut layer")

    text_on_cut = [e for e in cut if e.dxftype() in ("TEXT", "MTEXT")]
    if text_on_cut:
        fails.append(f"{len(text_on_cut)} text entit(ies) on cut layer")

    polys = []
    for e in cut:
        if e.dxftype() in ("LINE", "ARC", "TEXT", "MTEXT"):
            continue
        poly = polygon_of(e)
        if poly is not None and poly.area > TOL:
            polys.append((e, poly))
        elif closed(e):
            fails.append(f"zero-area closed {e.dxftype()} on cut layer")

    circles = [e for e in cut if e.dxftype() == "CIRCLE"]
    print(f"holes (CIRCLE on cut): {len(circles)}")
    if args.expect_holes is not None and len(circles) != args.expect_holes:
        fails.append(f"hole count {len(circles)} != expected {args.expect_holes}")

    dup = 0
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            a, b = polys[i][1], polys[j][1]
            if abs(a.area - b.area) < 0.01 and a.symmetric_difference(b).area < 0.01:
                dup += 1
    if dup:
        fails.append(f"{dup} duplicate/overlapping contour pair(s)")

    try:
        ext = bbox.extents(msp)
        w = ext.extmax.x - ext.extmin.x
        h = ext.extmax.y - ext.extmin.y
        print(f"extents: {ext.extmin.x:.3f},{ext.extmin.y:.3f} -> "
              f"{ext.extmax.x:.3f},{ext.extmax.y:.3f}  ({w:.3f} x {h:.3f} mm)")
        if args.expect_size:
            ew, eh = args.expect_size
            if abs(w - ew) > args.tol or abs(h - eh) > args.tol:
                fails.append(f"size {w:.3f} x {h:.3f} mm != expected {ew} x {eh} mm "
                             f"(tol {args.tol})")
    except Exception as exc:
        notes.append(f"extents unavailable: {exc}")

    if args.single_outline and polys:
        outer = max(polys, key=lambda p: p[1].area)
        print(f"outer contour area: {outer[1].area:.1f} mm^2")
        for e, p in polys:
            if p is outer[1]:
                continue
            if not outer[1].contains(p):
                fails.append(f"{e.dxftype()} at ({p.centroid.x:.1f},{p.centroid.y:.1f}) "
                             f"is not inside the outer contour")

    if len(polys) > 1:
        best = min(
            ((polys[i][1].boundary.distance(polys[j][1].boundary), polys[i][0], polys[j][0])
             for i in range(len(polys)) for j in range(i + 1, len(polys))),
            key=lambda t: t[0],
        )
        print(f"min cut-to-cut: {best[0]:.3f} mm")
        if args.min_web > 0 and best[0] < args.min_web:
            fails.append(f"min cut-to-cut {best[0]:.3f} mm < {args.min_web} mm")

    engrave = [e for e in msp if e.dxf.layer == args.engrave]
    print(f"engrave entities: {len(engrave)}")

    for n in notes:
        print(f"note: {n}")
    if fails:
        print("\nRESULT: FAIL")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
