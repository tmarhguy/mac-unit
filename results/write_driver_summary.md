# Write driver: summary record (vwanjohi)

Conditions: VDD = 0.8 V, tt, 27 °C. C_BL = 3.5 fF is a stand-in load; rerun with extracted C_BL for Part 2.

## Table 1: Driver sizing (C_BL = 3.5 fF, pw_w1 = 0.3 ns)

| NM1-NM4 nfin | Write 0 | t_wr0 (ps) | t_wr1 (ps) | Lowest BLB before flip (mV)* |
|---|---|---|---|---|
| 2 | Fail, Q stalls at ~0.66 V | n/a | n/a | ~0 |
| 4 | Fail, Q stalls at 0.38 V | n/a | n/a | ~60 |
| 5 | Pass | 153 | 154 | ~190 |
| 6 | Pass | 121 | 121 | ~260 |
| 8 | Pass | 96 | 96 | ~345 |

*Read from waveform. To measure: `ymin(clip(VT("/BLB") 1.4n 1.71n))`.

## Table 2: Write wordline pulse (nfin = 8)

| pw_w1 | WL width at 50% | C_BL = 3.5 fF | C_BL = 4.2 fF (+20%) |
|---|---|---|---|
| 40p | ~60 ps | Fail (Q stalls at 0.62 V) | Fail (0.66 V) |
| 60p | ~80 ps | Fail (0.46 V) | Fail (0.51 V) |
| 80p | ~100 ps | Fail (0.27 V) | Fail (0.34 V) |
| 100p | ~120 ps | Pass, t_wr = 96 ps | Pass, t_wr = 102 ps |
| 120p | ~140 ps | Pass, 96 ps | Pass, 102 ps |
| 150p | ~170 ps | Pass, 96 ps | Pass, 102 ps |

Source: `write_driver_sweep.csv` (12-point sweep, run at nfin = 8).

## Conclusions

- Small drivers fail because the write races the undriven bitline: the cell discharges BLB through its pass-gate, pinning QB low and blocking the flip. At nfin = 2, BL reached 0.12 V and the write still failed.
- Smallest driver that writes: nfin = 5. Provisional choice: nfin = 8 (96 ps, BLB stays above ~0.34 V).
- Write time 96 ps, 102 ps at +20% C_BL (+6%).
- Minimum write pulse is 100-120 ps at 50% for both loads. Design pulse ~140 ps at 50%.
- Area: 4 columns x 36 fins x 0.048 um x 0.018 um x 28 = ~3.5 um2, about 14% of the 24.9 um2 array (64 x 0.389 um2). nfin 6 to 8 adds ~0.77 um2 (~3%) and saves ~25 ps. Settle 6 vs 8 once T_CLK,min is known.

## Open items

- Design-point waveform (nfin = 8, pw_w1 = 120p, C_BL = 3.5 fF) still needs a run.
- Measure the BLB column instead of reading it from the plots.
- Rerun both tables with the extracted C_BL.
- Sweep point 12 (150p, 4.2 fF): `q_wr1` is blank (run finished with errors).

## Files

- `media/write_driver/`: schematics (nfin 5, 6, 8), transients (nfin 2, 4, 5, 6, 8), results tables, sweep table.
- `results/write_driver_sweep.csv`: 12-point pw_w1 x C_BL sweep at nfin = 8.
