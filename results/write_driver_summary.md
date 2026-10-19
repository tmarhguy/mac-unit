# Write driver and read path: summary record (vwanjohi)

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

## Read path (inverter on BLB, output RD)

Conditions: VDD = 0.8 V, tt, 27 C. VM is the input voltage where RD = BLB (DC sweep, 0 to 0.8 V).

| PM0 : NM0 fins | Switching point (VM) | BLB drop needed to flip RD | Est. read time (3.5 fF, 25 uA) |
|---|---|---|---|
| 2 : 2 | 0.376 V | 0.42 V | ~59 ps |
| 4 : 2 | 0.415 V | 0.39 V | ~54 ps |

Read time is estimated as C_BL x (VDD - VM) / I_read = 3.5 fF x drop / 25 uA. It is a hand estimate, not a simulated read.

PMOS strength: three measured switching points show a PMOS fin drives roughly half the current of an NMOS fin in this PDK. VM is 0.376 V at 2:2 (below VDD/2, so the NMOS wins), 0.415 V at 4:2 (close to VDD/2), and the cell's own inverter at 2:4 gives 0.335 V (the 2:4 figure is from the cell, not from this testbench). Doubling the PMOS to 4:2 therefore balances the inverter instead of skewing it. The small remaining offset (+15 mV from 0.4 V) means the PMOS is slightly stronger than a perfect match.

Files: `media/read_path/`: symbol, schematic (4:2), VTC and ADE outputs for 4:2 (`vm` = 415.1 mV), and the same three for 2:2 (`*_2to2.png`, `vm` = 376.3 mV).
