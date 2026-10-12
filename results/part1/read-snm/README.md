# Part 1 read-SNM results (schematic, VDD = 0.8 V)

Canonical β sweep. Each `beta*/` holds the verbatim Cadence export plus derived files.

- `raw.csv` — 4-col ViVA export `(X1,Y1,X2,Y2)`. One trace is normal `(sweep,out)`, the other mirrored `(out,sweep)`. Column order swaps between runs; `check_snm_sweep.py` auto-detects.
- `q.csv`, `qb.csv` — normalized `(sweep_v,output_v)` splits.
- `snm.json` — `snm_l_v/snm_r_v/snm_read_v`, intersections, disturb (low crossing), grid step, 4k/16k convergence.
- `butterfly.png/.svg` — clean plot: two VTCs + two max-squares + SNM label (matplotlib).

| β (PD fin, PG 2fin) | SNM_read | disturb | intersections mV |
|---|---|---|---|
| 1 (2) | 126.6 mV | 134.3 mV | 134.3, 410.0, 797.9 |
| 1.5 (3) | 145.8 mV | 96.6 mV | 96.6, 388.0, 798.6 |
| 2 (4, schematic candidate) | 156.3 mV | 77.1 mV | 77.1, 372.5, 798.8 |

Recompute: `python3 scripts/check_snm_sweep.py --all`

Benches: WL=VDD, BL=BLB=VDD. TB schematics: `media/part1/read_snm_q_tb_sch.png`, `read_snm_qb_tb_sch.png`; per-β cells `read_snm_q_sch_*.png`, `read_snm_qb_sch_*.png`; Cadence screenshots `read_snm_beta*.png`.

These values do not establish post-layout read SNM or write margin. See the [root README](../../../README.md) and [current handout](../../../docs/ese5700-project1.pdf) for the complete Part 1 scope.
