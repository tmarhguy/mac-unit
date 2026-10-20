#!/usr/bin/env python3
"""Check a 4-column Cadence read-SNM export and compute SNM_read.

Raw CSV layout (Virtuoso ViVA export):
  col1,col2 = first trace (X,Y), col3,col4 = second trace (X,Y).
  One trace is the normal VTC (X=sweep 0->VDD), the other is the
  mirrored VTC (X=output VDD->0, Y=sweep). Column order swaps
  between runs (beta1 vs beta1p5/beta2), so this script auto-detects
  which pair is normal (X starts near 0) and splits to q.csv/qb.csv.

Computes SNM_L/SNM_R via scripts/butterfly_snm.py maximum-square
method: SNM_read = min(SNM_L, SNM_R). Checks convergence at
4001 vs 16001 grid points and draws a minimal butterfly + squares
plot (matplotlib PNG + SVG): two curves + two squares + SNM label.

Usage:
  python3 scripts/check_snm_sweep.py results/part1/read-snm/beta1/raw.csv
  python3 scripts/check_snm_sweep.py --all
  python3 scripts/check_snm_sweep.py raw.csv --out-dir out/ --beta 1 --vdd 0.8
"""

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import butterfly_snm as bsnm


def read_raw(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(v) for v in r] for r in reader if r and any(c.strip() for c in r)]
    if len(rows) < 10:
        raise ValueError(f"{path}: too few rows ({len(rows)})")
    if any(len(r) != 4 for r in rows):
        raise ValueError(f"{path}: expected 4 columns (X1,Y1,X2,Y2)")
    cols = list(zip(*rows))
    return header, rows, cols


def split_raw(header, rows, cols):
    sweeps = [i for i, c in enumerate(cols) if abs(c[0]) < 1e-9]
    if len(sweeps) != 2:
        raise ValueError(f"expected 2 sweep columns starting at 0, got {sweeps}")
    pairs = [(0, 1), (2, 3)]
    normal = mirrored = None
    for xi, yi in pairs:
        if xi in sweeps:
            normal = (xi, yi)
        else:
            mirrored = (xi, yi)
    if normal is None or mirrored is None:
        raise ValueError("could not identify normal vs mirrored trace pair")
    a = [(cols[normal[0]][k], cols[normal[1]][k]) for k in range(len(rows))]
    # mirrored pair is (x=out, y=sweep) -> raw curve is (sweep, out)
    b = [(cols[mirrored[1]][k], cols[mirrored[0]][k]) for k in range(len(rows))]
    # sanity: sweeps monotonic increasing, outputs decreasing overall
    for name, curve in (("q", a), ("qb", b)):
        xs = [p[0] for p in curve]
        if not all(x2 > x1 for x1, x2 in zip(xs, xs[1:])):
            raise ValueError(f"{name} sweep not strictly increasing")
        if not (curve[0][1] > curve[-1][1]):
            raise ValueError(f"{name} output should fall with sweep")
    maxdiff = max(abs(p[1] - q[1]) for p, q in zip(a, b))
    return a, b, maxdiff, normal, mirrored


def compute_snm(a, b, samples):
    ma = bsnm.mirror(b)
    left = max(a[0][0], ma[0][0])
    right = min(a[-1][0], ma[-1][0])
    if left >= right:
        raise ValueError("no common voltage range after mirroring")
    xs = [left + (right - left) * i / (samples - 1) for i in range(samples)]
    ys_a = [bsnm.interpolate(a, x) for x in xs]
    ys_b = [bsnm.interpolate(ma, x) for x in xs]
    roots = bsnm.intersections(xs, [u - v for u, v in zip(ys_a, ys_b)])
    if len(roots) != 3:
        raise ValueError(f"expected 3 butterfly intersections, got {len(roots)}: {roots}")
    squares = [bsnm.fit_lobe(xs, ys_a, ys_b, roots[i], roots[i + 1]) for i in (0, 1)]
    return xs, ys_a, ys_b, roots, squares, ma


def plot_butterfly(out_png, out_svg, a, ma, squares, snm_v, beta_label):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=300)
    ax.plot([p[0] for p in a], [p[1] for p in a], linewidth=2, label="VTC Q")
    ax.plot([p[0] for p in ma], [p[1] for p in ma], linewidth=2, label="VTC QB (mirrored)")
    for sq in squares:
        rect = patches.Rectangle((sq["x_v"], sq["y_v"]), sq["side_v"], sq["side_v"],
                                 linewidth=1.5, edgecolor="black", facecolor="none")
        ax.add_patch(rect)
    ax.set_xlabel("Input voltage (V)")
    ax.set_ylabel("Output voltage (V)")
    ax.set_title(f"Read butterfly β={beta_label} — SNM_read={snm_v*1000:.1f} mV")
    ax.legend(frameon=True, fontsize=9, loc="best")
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    fig.savefig(out_png, dpi=300)
    fig.savefig(out_svg)
    plt.close(fig)


def process(raw_path, out_dir, beta_label, vdd_nom=0.8, tol_v=0.02):
    raw_path = Path(raw_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    header, rows, cols = read_raw(raw_path)
    a, b, maxdiff, normal, mirrored = split_raw(header, rows, cols)

    # voltage check: sweep should span ~0..VDD
    sweep_max = max(p[0] for p in a)
    out_max = max(p[1] for p in a)
    if abs(sweep_max - vdd_nom) > 0.05 or abs(out_max - vdd_nom) > 0.05:
        print(f"warning: sweep/output max {sweep_max:.3f}/{out_max:.3f}V vs nominal VDD {vdd_nom}V",
              file=sys.stderr)

    # convergence: 4001 vs 16001
    _, _, _, roots4, sq4, _ = compute_snm(a, b, 4001)
    snm4 = min(s["side_v"] for s in sq4)
    xs, ys_a, ys_b, roots, squares, ma = compute_snm(a, b, 16001)
    snm = min(s["side_v"] for s in squares)
    if abs(snm - snm4) > tol_v * 0.05 + 1e-4:
        print(f"warning: SNM not converged: 4k={snm4*1000:.2f}mV 16k={snm*1000:.2f}mV",
              file=sys.stderr)

    # write q/qb splits
    for name, curve in (("q", a), ("qb", b)):
        with open(out_dir / f"{name}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["sweep_v", "output_v"])
            w.writerows(curve)

    try:
        raw_rel = str(raw_path.resolve().relative_to(ROOT))
    except ValueError:
        raw_rel = str(raw_path)
    result = {
        "beta": beta_label,
        "vdd_nom_v": vdd_nom,
        "snm_v": snm,
        "snm_l_v": squares[0]["side_v"],
        "snm_r_v": squares[1]["side_v"],
        "snm_read_v": snm,
        "lobes": squares,
        "intersections_v": roots,
        "disturb_v": roots[0],
        "grid_step_v": xs[1] - xs[0],
        "snm_4k_v": snm4,
        "max_q_qb_diff_v": maxdiff,
        "raw": raw_rel,
    }
    with open(out_dir / "snm.json", "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    plot_butterfly(out_dir / "butterfly.png", out_dir / "butterfly.svg",
                   a, ma, squares, snm, beta_label)
    print(f"{raw_path}: SNM_L={squares[0]['side_v']*1000:.2f}mV "
          f"SNM_R={squares[1]['side_v']*1000:.2f}mV "
          f"SNM_read={snm*1000:.2f}mV disturb={roots[0]*1000:.1f}mV "
          f"(4k={snm4*1000:.2f}mV)")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("raw", nargs="?", type=Path, help="4-col raw Cadence CSV")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--beta", default=None, help="beta label, e.g. 1, 1.5, 2")
    ap.add_argument("--vdd", type=float, default=0.8)
    ap.add_argument("--all", action="store_true", help="process all beta dirs under results/part1/read-snm")
    args = ap.parse_args()

    if args.all:
        base = ROOT / "results" / "part1" / "read-snm"
        labels = {"beta1": "1", "beta1p5": "1.5", "beta2": "2"}
        results = {}
        for d in sorted(base.iterdir()):
            if d.is_dir() and (d / "raw.csv").exists():
                results[d.name] = process(d / "raw.csv", d, labels.get(d.name, d.name), args.vdd)
        print(json.dumps({k: v["snm_read_v"] for k, v in results.items()}, indent=2))
        return

    if not args.raw:
        ap.error("provide RAW csv or --all")
    raw = args.raw
    out = args.out_dir or raw.parent
    beta = args.beta or raw.parent.name.replace("beta", "").replace("p", ".")
    process(raw, out, beta, args.vdd)


if __name__ == "__main__":
    main()
