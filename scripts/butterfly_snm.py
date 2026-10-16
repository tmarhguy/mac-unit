#!/usr/bin/env python3
"""Measure SRAM static noise margin from two inverter DC transfer curves.

Each CSV supplies (input voltage, output voltage). The second curve is
mirrored across y=x before the two curves are overlaid. The script finds the
three intersections, then fits the largest axis-aligned square wholly between
the curves in each of the two lobes. SNM is the smaller square side.

The curves are linearly interpolated on a uniform voltage grid. The returned
square side is a grid estimate, not a certified continuous-curve bound;
increase --samples and check convergence before quoting a measurement.
Only use measured DC curves with the same bias conditions. No measurement is
inferred from a schematic or an illustrative curve.
"""

import argparse
import bisect
import csv
import json
import math
from pathlib import Path


def read_curve(path):
    points = []
    with open(path, newline="", encoding="utf-8-sig") as stream:
        for line, row in enumerate(csv.reader(stream), 1):
            if not row or all(not cell.strip() for cell in row):
                continue
            try:
                x, y = float(row[0]), float(row[1])
            except (ValueError, IndexError):
                if line == 1:
                    continue  # optional header
                raise ValueError(f"{path}:{line}: expected two numeric columns")
            if not (math.isfinite(x) and math.isfinite(y)):
                raise ValueError(f"{path}:{line}: voltage must be finite")
            points.append((x, y))
    if len(points) < 3:
        raise ValueError(f"{path}: need at least three voltage pairs")
    points.sort()
    if any(points[i][0] == points[i - 1][0] for i in range(1, len(points))):
        raise ValueError(f"{path}: duplicate input voltages; export one output per sweep point")
    return points


def mirror(curve):
    # A plateau becomes a vertical segment after mirroring. Keep its midpoint
    # for interpolation; lobe geometry is governed by the sloped transitions.
    groups = {}
    for x, y in curve:
        groups.setdefault(y, []).append(x)
    result = sorted((y, sum(xs) / len(xs)) for y, xs in groups.items())
    if len(result) < 3:
        raise ValueError("second curve has too few distinct output voltages")
    return result


def interpolate(curve, x):
    xs = [point[0] for point in curve]
    i = bisect.bisect_right(xs, x)
    if i == 0 or i == len(xs) + 1:
        raise ValueError("interpolation outside measured voltage range")
    if i == len(xs):
        if x == xs[-1]:
            return curve[-1][1]
        raise ValueError("interpolation outside measured voltage range")
    x0, y0 = curve[i - 1]
    x1, y1 = curve[i]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def intersections(xs, difference):
    roots = []
    for i in range(len(xs) - 1):
        a, b = difference[i], difference[i + 1]
        if a == 0:
            roots.append(xs[i])
        elif a * b < 0:
            roots.append(xs[i] - a * (xs[i + 1] - xs[i]) / (b - a))
    if difference[-1] == 0:
        roots.append(xs[-1])
    return [root for i, root in enumerate(roots) if i == 0 or root - roots[i - 1] > 1e-10]


def range_tables(values, operation):
    levels = [values]
    width = 2
    while width <= len(values):
        half = width // 2
        previous = levels[-1]
        levels.append([operation(previous[i], previous[i + half])
                       for i in range(len(values) - width + 1)])
        width *= 2
    return levels


def range_query(levels, left, right, operation):
    length = right - left + 1
    power = length.bit_length() - 1
    span = 1 << power
    return operation(levels[power][left], levels[power][right - span + 1])


def fit_lobe(xs, first, second, lo, hi):
    start = bisect.bisect_left(xs, lo)
    stop = bisect.bisect_right(xs, hi) - 1
    if stop - start < 2:
        raise ValueError("lobe has too few sampled points; increase --samples")
    upper = [max(first[i], second[i]) for i in range(start, stop + 1)]
    lower = [min(first[i], second[i]) for i in range(start, stop + 1)]
    upper_min = range_tables(upper, min)
    lower_max = range_tables(lower, max)
    step = xs[1] - xs[0]

    def feasible(k):
        side = k * step
        for left in range(len(upper) - k):
            right = left + k
            top = range_query(upper_min, left, right, min)
            bottom = range_query(lower_max, left, right, max)
            if top - bottom >= side - 1e-12:
                return left, bottom
        return None

    low, high = 0, len(upper) - 1
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid) is None:
            high = mid - 1
        else:
            low = mid
    found = feasible(low)
    if found is None or low == 0:
        raise ValueError("no positive square found in a lobe")
    left, bottom = found
    return {"side_v": low * step, "x_v": xs[start + left], "y_v": bottom}


def write_svg(path, curve_a, curve_b, squares, bounds):
    x0, x1, y0, y1 = bounds
    width, height, margin = 760, 760, 72
    scale_x = (width - 2 * margin) / (x1 - x0)
    scale_y = (height - 2 * margin) / (y1 - y0)

    def px(x):
        return margin + (x - x0) * scale_x

    def py(y):
        return height - margin - (y - y0) * scale_y

    def path_for(points):
        return " ".join(("M" if i == 0 else "L") + f"{px(x):.2f},{py(y):.2f}"
                        for i, (x, y) in enumerate(points))

    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<path d="M {margin},{height-margin} H {width-margin} M {margin},{height-margin} V {margin}" stroke="black" fill="none"/>',
             f'<path d="{path_for(curve_a)}" stroke="#1461a0" stroke-width="2" fill="none"/>',
             f'<path d="{path_for(curve_b)}" stroke="#bb4733" stroke-width="2" fill="none"/>']
    for square in squares:
        x, y, side = square["x_v"], square["y_v"], square["side_v"]
        lines.append(f'<rect x="{px(x):.2f}" y="{py(y+side):.2f}" width="{side*scale_x:.2f}" height="{side*scale_y:.2f}" fill="none" stroke="#202020" stroke-width="1.5"/>')
    lines += [f'<text x="{width/2}" y="{height-18}" text-anchor="middle" font-family="sans-serif">Input voltage (V)</text>',
              f'<text transform="translate(20,{height/2}) rotate(-90)" text-anchor="middle" font-family="sans-serif">Output voltage (V)</text>',
              f'<text x="{margin}" y="35" font-family="sans-serif" font-size="16">SNM = {min(s["side_v"] for s in squares):.4g} V</text>',
              '</svg>']
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_png(path, curve_a, curve_b, squares, bounds):
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise SystemExit("--png needs Pillow; use --svg or install Pillow") from exc
    x0, x1, y0, y1 = bounds
    width, height, margin = 900, 900, 85
    scale_x = (width - 2 * margin) / (x1 - x0)
    scale_y = (height - 2 * margin) / (y1 - y0)

    def point(x, y):
        return (margin + (x - x0) * scale_x,
                height - margin - (y - y0) * scale_y)

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.line([point(x0, y0), point(x1, y0)], fill="black", width=2)
    draw.line([point(x0, y0), point(x0, y1)], fill="black", width=2)
    draw.line([point(*p) for p in curve_a], fill="#1461a0", width=3)
    draw.line([point(*p) for p in curve_b], fill="#bb4733", width=3)
    for square in squares:
        x, y, side = square["x_v"], square["y_v"], square["side_v"]
        draw.rectangle([point(x, y + side), point(x + side, y)],
                       outline="#202020", width=2)
    draw.text((margin, 25), f'SNM = {min(s["side_v"] for s in squares):.4g} V', fill="black")
    draw.text((width // 2 - 60, height - 45), "Input voltage (V)", fill="black")
    draw.text((8, height // 2), "Output voltage (V)", fill="black")
    image.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("curve_a", type=Path, help="CSV: sweep input, first inverter output")
    parser.add_argument("curve_b", type=Path, help="CSV: sweep input, second inverter output")
    parser.add_argument("--samples", type=int, default=4001, help="common voltage-grid points (default: 4001)")
    parser.add_argument("--svg", type=Path, help="butterfly plot with fitted squares")
    parser.add_argument("--png", type=Path, help="PNG butterfly plot with fitted squares (requires Pillow)")
    parser.add_argument("--json", type=Path, help="machine-readable measurements")
    args = parser.parse_args()
    if args.samples < 101:
        parser.error("--samples must be at least 101")

    a = read_curve(args.curve_a)
    b = mirror(read_curve(args.curve_b))
    left, right = max(a[0][0], b[0][0]), min(a[-1][0], b[-1][0])
    if left >= right:
        parser.error("the curves have no common input-voltage range after mirroring")
    xs = [left + (right - left) * i / (args.samples - 1) for i in range(args.samples)]
    ys_a = [interpolate(a, x) for x in xs]
    ys_b = [interpolate(b, x) for x in xs]
    roots = intersections(xs, [u - v for u, v in zip(ys_a, ys_b)])
    if len(roots) != 3:
        parser.error(f"expected three butterfly intersections; found {len(roots)}. Check CSV columns and monotonic sweep data")
    squares = [fit_lobe(xs, ys_a, ys_b, roots[i], roots[i + 1]) for i in (0, 1)]
    result = {"snm_v": min(square["side_v"] for square in squares),
              "lobes": squares, "intersections_v": roots,
              "grid_step_v": xs[1] - xs[0],
              "curve_a": str(args.curve_a), "curve_b": str(args.curve_b)}
    if args.svg or args.png:
        values = [y for curve in (a, b) for _, y in curve]
        bounds = (left, right, min(values), max(values))
        if args.svg:
            write_svg(args.svg, a, b, squares, bounds)
        if args.png:
            write_png(args.png, a, b, squares, bounds)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
