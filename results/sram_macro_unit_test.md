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
