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
