# decoder logical effort (2.2a), chosen 2-2 predecode, WL_EN to WL path

Path (4 gates): nand3_u, inv_2x, nand2_u (in row_pre), inv_drv.
Assumptions: tau = 10.5 ps (FO4 = 5 tau, FO4 = 52.6 ps); about 20 aF per fin (Part 1: 90 aF per cell over 4 pass-gate fins, about 22 aF per fin); p_inv = 1, p_nand2 = 2, p_nand3 = 3; C_WL = 0.5 fF (the simulated wordline load).

| Quantity | Value |
|---|---|
| G = g_nand3 g_inv g_nand2 g_inv | 5/3 x 1 x 4/3 x 1 = 20/9 = 2.22 |
| B (each literal reaches 2 predecode gates, each predecode output drives 4 row gates) | 2 x 4 = 8 |
| C_in (one nand3_u input: 4 PMOS + 6 NMOS fins) | 10 fins = 200 aF |
| H = C_WL / C_in | 500 / 200 = 2.5 |
| F = GBH | 44.4 |
| optimal N = log4 F | 2.74 |
| stage effort at N = 4, F^(1/4) | 2.58 |
| P | 3 + 1 + 2 + 1 = 7 |
| D = N F^(1/N) + P | 17.3 tau = 182 ps |
| simulated WL_EN to WL (rising) | 97 ps |

The prediction (182 ps) is about 1.9x the simulation (97 ps): the model with these assumed capacitances and parasitics is pessimistic for this design. The second implementation (flat NAND per row) and its numbers are not computed here; the user's notes were not available to the assistant, so that comparison is still open.

Correction to a mental estimate made earlier in the session: the stage-effort term is 4 x 2.58 = 10.3, and with P = 7 the total is 17.3 tau, not 10.3 tau.

## Correction (user review, 21 Oct)

The 182 ps prediction uses B = 8, the fan-out of an address literal, so it predicts the address-to-wordline path. The 97 ps simulated delay is WL_EN to wordline, a different path, so the earlier "predicted is about 1.9x the measured" comparison was not valid and was removed from the report. To compare: in tb_dec_pre hold WL_EN high and switch A<0> with a complementary AB<0>; repeat with A<2> for the other predecoder; quote the slower. For the flat decoder WL_EN enters at the row NAND2, two stages from the wordline, so compare address-to-wordline for both decoders. The decoder item in the handout's grading is "decoder design and logical-effort analysis, 1.5 pts" as a whole; how much the second implementation is worth inside it is not stated.

Other corrections recorded in the report: +20% C_BL must be tested in a bench with real bitlines (the t3 macro run with cbw = 1.32 fF, or tb_read_col with CBL = 4.2 fF), not in tb_controller, which has no bitlines; precharge recovery (user notes): 3 PMOS x 2 fins, BL reaches 99% of VDD in 142 ps at 3.5 fF, 845 mV peak, BLB near 690 mV during equalization; worst-case access is data dependent (read of 1), 488.3 ps on DOUT<1> and 488.9 ps on DOUT<0> at 0.69 ns; write power is measured with a checkerboard pattern rather than all-0/all-1 (state the deviation, not an estimate); the a3 width is corrected in the saved bench.

## Address-to-wordline measurement (A<0>, PA path)

106 ps (new row rising) and 112 ps (old row falling) against 182 ps predicted with B = 8: the model overestimates by about 1.6x. See `decoder_predec_unit_test.md`. A<2> (PB path) not yet measured.
