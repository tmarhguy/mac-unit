# sram_macro area and preliminary FOM (from the netlist)

Source: the Spectre netlist of `tb_sram_macro` pasted by the user (all subcircuits with fin counts, L = 18 nm). Area convention from Part 1: A = D * sum(W_i L_i), D = 28, one fin = 0.048 um wide, so 0.024192 um^2 per fin. The testbench-only parts (input buffers IB1/IB2, data gates, sources, DOUT loads) are excluded.

| Block | Instances | Fins each | Fins | Area (um^2) |
|---|---|---|---|---|
| Array, 64 cells | 64 | cell layout 0.389 um^2 | -- | 24.9 (tiled estimate, not laid out) |
| Row decoder | 1 | 520 | 520 | 12.6 |
| Controller | 1 | 426 | 426 | 10.3 |
| Write drivers | 4 | 36 | 144 | 3.5 |
| Precharge | 4 | 6 | 24 | 0.58 |
| Read paths (2:2) | 4 | 4 | 16 | 0.39 |
| Output latches | 4 | 24 | 96 | 2.3 |
| Periphery total | | | 1226 | 29.7 |
| Macro total | | | | 54.6 |

Cell fin counts: inv_u 6, inv_2x 12, inv_drv 9, nand2_u 8, nand3_u 30, out_latch 24, row_pre 17 (nand2_u + inv_drv). Controller = 23 inv_u (138) + 9 out_latch (216) + 4 inv_2x (48) + 3 nand2_u (24) = 426. Decoder = 4 nand3_u (120) + 4 nand2_u (32) + 8 inv_2x (96) + 16 row_pre (272) = 520. Column periphery = precharge 6 (3 PMOS x 2) + write driver 36 (four 8-fin NMOS + 2+2 inverter) + read path 4 + out_latch 24 = 70.

Periphery is 54% of the macro area (29.7 of 54.6 um^2). The controller's 426 fins are mostly its 9 input latches (216) and delay chains (15 inverters, 90).

FOM = Area x Power x T_CLK,min = 54.6 um^2 x 124.3 uW x 0.69 ns = 4.7e3 um^2 uW ns (write power, 690 ps). Still preliminary: the 24.9 um^2 array is tiled from the cell area, not laid out, and the write power is a checkerboard pattern rather than all-0 / all-1.
