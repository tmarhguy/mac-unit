# read_col unit test (2.3)

Testbench `proj1_lib/tb_read_col`: transient, 0 to 6 ns, nominal corner, 27 C. VDD = 0.8 V, `CBL` = 3.5 fF (stand-in bitline load), `cdout` = 1 fF, `pw_w1` = 120p. Swept `rd_dly` (RD_EN delay, 1.48n to 1.68n in 40p steps) and `pw_rden` (RD_EN pulse width, 40p, 80p, 120p, 160p), 24 points. Full data: `read_col_sweep.csv` (all outputs, all points).

Sequence per run: write 1, read, write 0, read, write 1, read. Specs: `dout_c2`, `dout_c6`, `q_rd1`, `dout_g2` > 0.72 V (a stored 1); `dout_c4`, `q_rd0` < 0.08 V (a stored 0).

## Result

Every check passes except `dout_c6` at `pw_rden` = 40p, and that failure is the same at every `rd_dly` (the latch never captures the 1). `dout_g2` (minimum of DOUT over 1.4-2.0 ns) passes at all 24 points at 797-797.5 mV, so DOUT does not glitch even when RD_EN opens early. The reads do not disturb the cell (`q_rd1` 799.7 mV, `q_rd0` about 39 uV at every point).

## Table: access time grid (ps, WL to DOUT)

| rd_dly \ pw_rden | 40p | 80p | 120p | 160p | t_acc0 (read 0) |
|---|---|---|---|---|---|
| 1.48n | fail | 247 | 226 | 226 | 165 |
| 1.52n | fail | 235 | 235 | 235 | 205 |
| 1.56n | fail | 271 | 271 | 271 | 245 |
| 1.60n | fail | 311 | 311 | 311 | 285 |
| 1.64n | fail | 351 | 351 | 351 | 325 |
| 1.68n | fail | 391 | 391 | 391 | 365 |

"fail" at 40p means `dout_c6` fails and `t_acc1` does not evaluate (eval err). Cells show `t_acc1` unless stated.

## How to read it

- Opening RD_EN later only adds delay. From 1.52n on, both access times grow 40 ps for every 40 ps of `rd_dly`, because DOUT waits for the latch to open.
- Width: 120p is the right choice. At 1.48n, 80p passes but is about 22 ps slower (247.4 ps against 225.6 ps): X is only partly charged when the latch closes and the latch has to finish the transition on its own. 120p and 160p give the same 226 ps, so 120p is the shortest width that loses nothing.
- Delay: 1.48n is the best of the delays tested. RD_EN opens about 80 ps after WL, before RD has fully settled, but the long pulse lets the latch wait for RD. `dout_g2` confirms that opening this early causes no glitch. Earlier than 1.48n was not tested.

## Chosen read timing

`rd_dly` = 1.48n, `pw_rden` = 120p, about 140 ps wide at 50% (assuming 20 ps edges). The pulse closes at about 1.64n.

## Table: column read results (WL to DOUT, C_BL = 3.5 fF)

| Measurement | Value |
|---|---|
| BLB reaches the read inverter's switching point (t_blb) | 83 ps |
| RD crosses 0.4 V when the latch isn't loading it (t_rd) | 113 ps |
| DOUT valid, read 0 | 165 ps |
| DOUT valid, read 1 (column access time) | 226 ps |

`t_rd` is 113 ps for `rd_dly` 1.52n and later. At 1.48n it measures 140 ps because the latch is already loading RD.

## Does the read limit the wordline?

No. The bitline needs only about 83 ps of wordline time, so a read pulse of about 110 ps at 50% leaves margin. Scaling `t_blb` by +20% C_BL gives roughly 100 ps, which still fits (an estimate, not a simulation). The write's 140 ps pulse still sets WL_EN, so the nfin 6 vs 8 driver decision rests on write speed and T_CLK alone.

## What the controller needs for RD_EN

- Rise about 80 ps after the wordline at the cell. WL_EN is generated before the decoder, so that is about decoder delay + 80 ps after WL_EN.
- Stay high about 140 ps (50% width).
- Pulse in read cycles only.
- Close before precharge pulls BLB back up.

## Open items

- Capture the waveform at `rd_dly` = 1.48n, `pw_rden` = 120p for the report. The saved `media/read_col/read_col_tran.png` is the 1.48n run at 40p (it shows the failing third read), and the `read_col_rd_dly_sweep_*` plots are also 40p.
- Rerun with the extracted C_BL, and at +20% C_BL, to replace the 83 ps scaling estimate.
- Check the 1.44n and earlier `rd_dly` values to find where early opening stops working.

## Related files

- Data: `results/read_col_sweep.csv`, `results/read_col_dout_c6_sweep.csv` (subset)
- Setup: `media/read_col/read_col_ade_setup_dout_g2.png` (current), `read_col_ade_setup_pw_rden.png`, `read_col_ade_setup.png`
- Schematics and waveforms: `media/read_path/`, `media/read_col/`
