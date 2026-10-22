# nfin sizes: final values and how they were found

All devices are L = 18 nm. Final fin counts are read from the Spectre netlist `netlists/tb_sram_macro.scs` by `scripts/count_fins.py` (run `python3 scripts/count_fins.py netlists/tb_sram_macro.scs`); the sizes were chosen earlier in simulation, summarized here with where the evidence is.

## How the counts were obtained

1. The netlist lists every transistor with `nfin=`. The script sums fins per subcircuit and flattens the hierarchy (instances multiplied by their cell's fins).
2. Cross-checks against hand counts from the schematics: controller 426, decoder 520, write driver 36, out_latch 24, precharge 6, read_path 4, sram_6t 16, sram_col 326, sram_macro 2250 fins (54.4 um^2 if all fins are costed at D = 28; the report uses 54.6 um^2 because the 64 cells are costed at their laid-out area, 64 x 0.389 um^2, with periphery at fins).

## Final sizes (PMOS / NMOS, fins per device)

| Cell | PMOS | NMOS | Total fins | How it was chosen |
|---|---|---|---|---|
| sram_6t | pull-up 2 | pull-down 4, pass-gate 2 | 16 | Part 1: beta = 2 from the read-SNM sweep (beta 1, 1.5, 2) |
| write_driver | 2 (inverter) | 8 x 4 stack + 2 (inverter) | 36 | nfin sweep 2, 4, 5, 6, 8: 2 and 4 fail, 5 is the minimum that writes (153 ps), 8 gives 96 ps; 8 is provisional (nfin 6 vs 8 depends on T_CLK,min) |
| read_path | 2 | 2 | 4 | VM = 0.376 V at 2:2 vs 0.415 V at 4:2; 2:2 kept because 4:2 would add 8 fins and save only about 7 ps |
| out_latch | 2 (6 devices) | 2 (6 devices) | 24 | minimum size; unit test and pw_en sweep show it works from a 20 ps enable |
| precharge | 2 (3 devices) | -- | 6 | not swept in these records; checked only in the column and macro tests |
| inv_u | 4 | 2 | 6 | balanced unit inverter: a PMOS fin drives about half an NMOS fin, VM = 0.415 V; FO4 = 53 ps |
| inv_drv | 6 | 3 | 9 | 1.5 x inv_u, wordline driver |
| inv_2x | 8 | 4 | 12 | 2 x inv_u, predecode and enable drivers |
| nand2_u | 2 (2 devices) | 2 (2 devices) | 8 | half the strength of inv_u in both directions; whether this is intentional has not been confirmed |
| nand3_u | 4 (3 devices) | 6 (3 devices) | 30 | NMOS stack widened 3x to match inv_u's pull-down; PMOS equal to inv_u's |

## Block totals (fins)

Decoder 520 (4 nand3_u, 4 nand2_u, 8 inv_2x, 16 row_pre); controller 426 (23 inv_u, 9 out_latch, 4 inv_2x, 3 nand2_u); one column's periphery 70 (precharge 6, write driver 36, read path 4, latch 24), x4 = 280; cells 16 x 64 = 1024.

## Not recorded

The controller's delay chains are 7 inv_u (DLY1) and 8 inv_u (DLY2); the counts give the measured WL_EN width of 133.5 ps and RD_EN lead of 95.8 ps, but the tuning history (other chain lengths tried) was not captured. Likewise the precharge sizing and the decoder gate sizes were not swept in the records here.
