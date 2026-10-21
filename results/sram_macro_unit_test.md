# sram_macro full-macro test (2.5) -- first run, 66 ns

Testbench `tb_sram_macro` (see `sram_macro_schematic.md`), tclk = 1 ns, transient 0 to 66 ns, nominal. Images in `media/sram_macro/`: `tb_sram_macro_tran_control.png` (M, E, WE, CLK), `tb_sram_macro_tran_dout.png`, `tb_sram_macro_tran_din.png`, `tb_sram_macro_tran_addr.png`, `tb_sram_macro_ade_outputs_setup.png`.

Schedule read off the waveforms: WE high 0 to 16.25 ns (write 16 words, addresses 0..15, one per cycle), low 16.25 to 32.25 ns (read 16), high 32.25 to 48.25 ns (write complement), low 48.25 to 64.25 ns (read 16). ADDR<0> toggles every cycle, ADDR<3> every 8 cycles.

Check outputs (results: `media/sram_macro/tb_sram_macro_ade_results_err.png`):

| Output | Value | Spec | Result |
|---|---|---|---|
| err1 (first read pass, checkerboard) | 173.8 uV | < 0.1 V | pass |
| err2 (second read pass, complement) | 173.8 uV | < 0.1 V | pass |

Access time, from the added outputs (`media/sram_macro/tb_sram_macro_ade_results_access.png`):

| Output | Definition | Value |
|---|---|---|
| t_acc_f | DOUT<1> falling through 0.4 V (1st falling crossing) minus the 17th rising CLK crossing at 0.4 V | 463.7 ps |
| t_acc_r | DOUT<1> rising through 0.4 V (1st rising crossing) minus the 18th rising CLK crossing | 484.2 ps |

The 463.7 ps falling value agrees with the 464 ps built up from the controller (238.2 ps) plus the column (226 ps). The rising value is about 20 ps longer. These are DOUT<1> only, at one specific read each (the 17th and 18th clock edges, i.e. addresses 0 and 1 of the first read pass), at stand-in loads; the worst case over all four bits and all 16 addresses is not measured yet.

Design variables in this run: `tclk` = 1 ns, `cbw` = 0.62 fF. `cbw` is not defined anywhere I have seen; it is probably the bitline wire capacitance added to the 16 cells per column, because 16 x 180 aF + 0.62 fF = 3.50 fF, the stand-in C_BL used in every earlier test. Confirm.

Definitions:
- err1 = max over 17 to 33 tclk of M * (|DOUT0 - E| + |DOUT1 - (0.8 - E)| + |DOUT2 - E| + |DOUT3 - (0.8 - E)|), spec < 0.1 V: first read pass (checkerboard).
- err2 = same over 49 to 65 tclk with the opposite polarity (DOUT0 expected at 0.8 - E, DOUT1 at E, ...), spec < 0.1 V: second read pass (complement).
- M is a narrow pulse that samples each cycle; E is the expected-bit square wave. The expected word is DOUT0 = DOUT2 = E, DOUT1 = DOUT3 = not E.

Observed from the DOUT waveforms (coarse, 66 ns on screen):
- Before the first read all four outputs sit high (latch start-up state).
- DOUT<3> and DOUT<1> are in phase, DOUT<2> and DOUT<0> are in phase and opposite to them: each word is 0101 or 1010, alternating every cycle (address), as the checkerboard requires.
- During the first read pass (17 to 32 ns) all outputs toggle every cycle; first transition at about 17.0 ns for a read whose clock edge is at 16.5 ns, i.e. about 0.5 ns CLK-to-DOUT (consistent with the 0.46 ns estimate; read off a 66 ns plot, so only roughly).
- While WE is high (32 to 49 ns) DOUT holds (bits 3 and 1 high, 2 and 0 low = the last word read, address 15), as the output latch should.
- In the second read pass (50 to 64 ns) the outputs toggle every cycle again; address 0 gives the complement of its first-pass value, which is why nothing changes at 49 ns (the held address-15 value equals the complement of address 0) and all four bits change together at 50 ns.
- After 64 ns the outputs hold again.

Now recorded: err1 and err2 both pass with 173.8 uV against the 0.1 V limit (the two values are identical, which is plausible for a symmetric pattern and its complement but worth a glance). Not covered: 2.5(iii), the worst-case row read right after a write to the opposite value, and a minimum-period (T_CLK,min) search.

Open: worst-case access over all bits and addresses; add 2.5(iii); measure the worst-case access time and T_CLK,min from a period sweep.

## Worst-row run (22 ns): err3 and write times

Images: `tb_sram_macro_ade_results_err3_write_times.png` (passing values), `tb_sram_macro_ade_results_err3_unresolved_1p28.png` (earlier state of the same table, see below). Setup: transient 0 to 22 ns, tclk = 1 ns, cbw = 0.62 fF. The tab title is `COL<0> (sram_col)`, so the column was opened in the same session; new probes are /I0/COL<0>/Q<15:0>, /QB<15:0>, /I0/WL<15:0>, /I0/COL<0>/BLB (hierarchical nets inside the macro).

| Output | Meaning (expression is truncated in the screenshot) | Value | Spec | Result |
|---|---|---|---|---|
| err3 | same style of check as err1/err2 (M-weighted DOUT error), taken here to be the worst-row test 2.5(iii) | 173.8 uV | < 0.1 V | pass |
| t_wr1 | Q<15> rising through 0.335 V, window 2.4 to 3.4 tclk | 338.6 ps | none | n/a |
| t_wr0 | Q<15> falling through 0.335 V, window 4.4 to 5.4 tclk | 333.7 ps | none | n/a |

Notes:
- The reference edge for t_wr1 and t_wr0 is cut off in the screenshot; the values (about 335 ps) match CLK-to-WL (238.2 ps) plus the write time (96 ps) from the column tests (334 ps), so the reference is probably the rising CLK edge. 0.335 V is the cell's own inverter switching point (0.335 V from Part 1).
- Row 15 is assumed to be the worst-case row (the last wordline); not verified. Only Q is tracked (the handout also asks for the other node, QB, past its switching point).
- err3 is assumed to be 2.5(iii); its full expression is not visible.
- Unresolved: the other capture shows err3 = 1.28 with t_wr1 and t_wr0 empty. It is the same table before the delays were evaluated, or an earlier failing run; I do not know which. If it was a failing run (1.28 is above the 0.1 V limit), what changed to fix it should be noted.

Waveforms for the 22 ns run: `tb_sram_macro_worstrow_tran_22ns.png` (CLK, WE and the bitline-bar of COL<0>, 0 to 22 ns) and `tb_sram_macro_worstrow_tran_zoom_1p9_6ns.png` (zoom, 1.9 to 6 ns). WE changes every cycle (high, low, high, ...), so the macro alternates write and read cycles back to back; this supports reading err3 as the 2.5(iii) test (read right after a write), though the err3 expression itself is still truncated in the screenshots. COL<0>/BLB swings close to 0 V in some cycles and to about 0.4 V in others (read off the zoom: about 0 V near 2.8 to 3.1 ns, about 70 mV near 3.9 to 4.1 ns, about 0.4 V near 5.0 to 5.2 ns); which cycle is a write and which a read for this row, and the stored values, are not annotated, so no further reading is made. Two more screenshots (132, 133) repeat the ADE table already recorded above (err3 173.8 uV, t_wr1 338.6 ps, t_wr0 333.7 ps), so they were not saved again.

Row-15 waveform (`tb_sram_macro_worstrow_row15_waveform.png`, 22 ns): DOUT<0>, COL<0>/Q<15>, COL<0>/QB<15>, WL<15>, COL<0>/BLB. Read off the plot: WL<15> pulses once every clock cycle (about 22 pulses in 22 ns, a write and a read in alternate cycles); Q<15> and QB<15> are complementary and flip repeatedly, i.e. row 15 is written to alternating values; COL<0>/BLB shows the write and read discharges every cycle; DOUT<0> toggles with the stored value, behind the cell. This is the waveform the handout asks for in 2.5(iii). Exact write/read assignment per cycle and the cycle-by-cycle DOUT values are not annotated.

Row-15 control view (22 ns and zoom): `tb_sram_macro_row15_wl_bl_we_clk_dout_22ns.png`, `tb_sram_macro_row15_wl_bl_we_clk_dout_zoom_BEST.png` (1.5 to 6.8 ns, best for the report), `tb_sram_macro_row15_overzoomed_single_edge.png` (a single-edge zoom, kept in case). Traces: WL<15>, COL<0>/BL, COL<0>/BLB, WE, CLK, DOUT<0>.

Read off the zoom: WE is low around 1.3 to 2.3 ns and 3.3 to 4.3 ns, high around 2.3 to 3.3 ns, so with CLK rising at 1.5, 2.5, 3.5, 4.5, 5.5 ns the cycles alternate read (1.5), write (2.5), read (3.5), write (4.5), read (5.5). DOUT<0> changes only after the reads, at about 2.0 ns (falls), 4.0 ns (rises) and 6.0 ns (falls): about 0.5 ns after each read edge, and the value toggles every read. So each read returns the value written to the row in the cycle just before, and that value alternates: a read immediately after a write to the opposite value, as 2.5(iii) requires. WL<15> pulses in every cycle (read and write). BL and BLB swing in alternate cycles (the write drives one of them low; the read discharges one). The exact stored value per cycle is not annotated. Plots are about 0.5 ns CLK-to-DOUT, read roughly.

All-in-one 22 ns view: `tb_sram_macro_row15_all_signals_22ns_BEST.png` shows CLK, WE, WL<15>, COL<0>/BL, COL<0>/BLB, COL<0>/Q<15>, COL<0>/QB<15> and DOUT<0> together (one image for 2.5(iii); supersedes `tb_sram_macro_worstrow_row15_waveform.png`, which lacks CLK, WE and BL). Q<15> and QB<15> are complementary and each flips every other write (period about 4 ns), and DOUT<0> follows them after each read, as described above.

Write-time markers: `tb_sram_macro_write_time_markers.png`. Marker A is on CLK at 2.55538 ns, 448.458 mV (the rising edge of the write cycle at 2.5 ns); marker B is on Q<15> at 2.88868 ns, 305.508 mV (Q rising after the write of a 1). Delta: 333.2962 ps (dy 142.95 mV). This shows the reference edge for t_wr1 and t_wr0 is the rising CLK edge. The ADE values (338.6 ps and 333.7 ps) use the 0.4 V crossing on CLK and 0.335 V on Q; the markers sit at 0.448 V and 0.306 V, which is why 333.3 ps differs a little from 338.6 ps. Both are within about 2% of each other and of the 334 ps predicted from 238.2 + 96 ps.

## tclk sweep (66 ns checkerboard/complement bench): T_CLK,min

Image: `media/sram_macro/tb_sram_macro_tclk_sweep_results.png`; data `results/sram_macro_tclk_sweep.csv`. Design variables: tclk = 1n, 0.9n, 0.85n, 0.8n, 0.75n, 0.7n; cbw = 0.62 fF; transient 0 to 66n (not scaled with tclk; see below). The results view is filtered to "pass" (12 of 120 rows).

| tclk | err1 | err2 | Result |
|---|---|---|---|
| 1 ns | 173.8 uV | 173.8 uV | pass |
| 900 ps | 177.7 uV | 177.8 uV | pass |
| 850 ps | 187.7 uV | 187.7 uV | pass |
| 800 ps | 232.8 uV | 232.8 uV | pass |
| 750 ps | 496.9 uV | 496.2 uV | pass |
| 700 ps | 5.103 mV | 5.118 mV | pass |

All six points pass (limit 0.1 V). So T_CLK,min is at or below 0.70 ns; the failing period has not been found. The error rises as the period shortens and jumps 10x between 750 and 700 ps (0.5 mV to 5.1 mV), which suggests the failure edge is not far below 0.7 ns. Next points: 0.65, 0.6, 0.55, 0.5 ns.

Caveats:
- Only err1 and err2 (the 66 ns bench) are in this sweep. err3 (worst row, 22 ns bench) and the controller margins are not swept.
- The controller delays are fixed times (delay chains), not scaled with the clock, so the half-period shrinks while the pulse widths do not. If PRE_B falls with the CLK falling edge at 0.5 tclk (as it appears), the RD_EN-to-PRE_B margin (70 ps at 1 ns, `m_rd_pre`) would shrink by about (1 ns - tclk)/2, reaching zero near 0.86 ns and going negative below that. err1/err2 still pass down to 0.7 ns, so either that margin is not what fails first or this estimate is wrong. Measure m_rd_pre, m_wl_pre and the other controller margins across this sweep to settle it.
- The 66 ns stop time is fixed; the sources scale with tclk but the run length does not, so at shorter periods the run covers more cycles than intended (the windows in err1/err2 use VAR("tclk"), so they scale). The checks still cover their full windows.

## tclk sweep on the worst-row bench (22 ns): err3 and write times

Same sweep (tclk = 1n to 0.7n) on the worst-row bench (maestro `tb_sram_macro_t3`). Data: `results/sram_macro_tclk_sweep_err3.csv`; plot `media/sram_macro/tb_sram_macro_tclk_sweep_err3_plot.png` (err3, t_wr1, t_wr0 against tclk, plus an overlay of all signals that is not readable).

| tclk | err3 | t_wr1 | t_wr0 | Result |
|---|---|---|---|---|
| 1 ns | 173.8 uV | 338.6 ps | 333.7 ps | pass |
| 900 ps | 177.7 uV | 338.6 ps | 333.6 ps | pass |
| 850 ps | 187.7 uV | 338.7 ps | 333.6 ps | pass |
| 800 ps | 232.5 uV | 338.6 ps | 333.6 ps | pass |
| 750 ps | 496.6 uV | 338.5 ps | 333.7 ps | pass |
| 700 ps | 5.623 mV | 338.5 ps | 333.7 ps | pass |

err3 passes at every period down to 0.70 ns, like err1 and err2, so all three tests pass at 0.70 ns. err3 follows the same trend: flat near 0.2 mV, then 0.5 mV at 750 ps and 5.6 mV at 700 ps, a steep rise just above the failure edge. The write times do not depend on the clock period (about 338.6 ps and 333.7 ps at all six periods), as expected for a delay set by the controller and the column rather than by the clock.

T_CLK,min is therefore at or below 0.70 ns for all three tests. The failing period is still not found (next: 0.65, 0.6, 0.55, 0.5 ns).

## err3 versus tclk, 600 to 700 ps: where the worst-row test fails

Plot: `media/sram_macro/tb_sram_macro_tclk_sweep_err3_600_700ps.png` (err3 against tclk, 600 to 700 ps; y axis unlabelled, read as volts because 700 ps gives about 0.006 V, matching the 5.6 mV table value). Values below are read off the curve, only approximate; the plot has few sample points (kinks near 670, 680, 690 and 700 ps).

- err3 sits flat at about 1.28 V for tclk from 600 up to about 670 ps: the test fails completely (limit 0.1 V). This explains the earlier unexplained screenshot with err3 = 1.28: it was a run at a period in this failing range.
- It then drops steeply: about 0.6 V near 680 ps, about 0.03 V at 690 ps, about 0.006 V at 700 ps.
- With the 0.1 V limit, the test passes at 690 ps (about 30 mV) and fails at 680 ps (about 0.6 V). So T_CLK,min is between 680 and 690 ps for the worst-row test; the best passing period seen is about 690 ps, with only about 3x margin on the limit.
- Only err3 was swept below 700 ps; err1 and err2 (66 ns bench) have not been run below 700 ps, so the macro-wide T_CLK,min is the larger of the three, not yet known. The write times (t_wr1, t_wr0) are not drawn in this window.

## Access time versus tclk, about 680 to 700 ps

Plot: `media/sram_macro/tb_sram_macro_tclk_access_680_700ps.png` (t_acc1 and t_acc0 against tclk; the x axis is logarithmic, labelled as powers of ten: 10^-9.167 to 10^-9.155 s = about 681 to 700 ps, with a kink at 10^-9.1615 = about 689 ps, i.e. three sweep points near 680, 690 and 700 ps). Values read off the curves (approximate); the output definitions are not visible, taken as the read-1 and read-0 access times (CLK to DOUT), the same outputs as t_acc_r and t_acc_f.

| tclk | t_acc1 | t_acc0 |
|---|---|---|
| about 680 ps | about 500 ps | about 461.9 ps |
| about 690 ps | about 489 ps | about 461.8 ps |
| about 700 ps | about 486 ps | about 461.7 ps |

Read access barely changes with the period: t_acc0 moves by about 0.2 ps, and t_acc1 grows from about 486 to about 500 ps as the period shrinks to 680 ps (the period at which err3 already fails), so read-1 slows down as the clock approaches its limit. Compare 484.2 ps (rising) and 463.7 ps (falling) at 1 ns on DOUT<1>. Worst case so far: about 489 ps at 690 ps, the shortest period at which err3 passes.

## 680 ps (fails err3) against 690 ps (passes): overlay

Plot: `media/sram_macro/tb_sram_macro_680_vs_690ps_overlay.png` (1.7 to 5.4 ns; CLK, DOUT<0>, COL<0>/BLB, COL<0>/RD, PRE_B and RD_EN, the two periods overlaid and labelled 680p and 690p).

Read off the plot:
- The two runs track each other; the 680p clock edges drift earlier by about 10 ps per cycle, so the two curves separate over time (about 40 ps by 5 ns).
- DOUT<0> rises at about 2.9 ns in both runs. In the 680p run the rise stalls partway (a shoulder at roughly half swing near 2.85 ns) before completing; the 690p rise is a single clean edge. Both reach full swing, and both fall at about 4.3 ns.
- RD_EN (bottom panel) is a triangular, rounded pulse at about 2.8 to 3.0 ns and about 4.2 to 4.4 ns in both runs, much more rounded than the ideal pulses of the controller test, with the 680p pulse about 10 to 20 ps earlier. The RD node pulses (about 2.8 to 2.95 ns) follow it.
- COL<0>/BLB discharges to about 0.4 V in the cycle around 3.4 to 3.6 ns, shallower than in the write cycles.

What this suggests, and what it does not show: the hesitation on the 680p DOUT rise is the visible difference and is where the worst-row failure plausibly starts (the latch capturing late or from a not-yet-settled RD). It is a reading of a small feature, not a measurement; the err3 sampling instants and the failing cycle are not annotated, so the actual failing check cannot be pinned to this plot. To settle it, measure the RD_EN width and the RD settling time at 680 and 690 ps, and print err3 per cycle.
