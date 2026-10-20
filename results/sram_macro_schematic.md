# sram_macro top-level schematic (as drawn)

Image: `media/sram_macro/sram_macro_schematic.png`. Ports: CLK, WE, ADDR<3:0>, DIN<3:0> in; DOUT<3:0> out; VDD, VSS. Matches the Part 2 interface (CLK, WE, ADDR[3:0], DIN[3:0], DOUT[3:0]).

Instances:
- I0 `controller`: CLK, WE, ADDR, DIN in; outputs A<3:0>, AB<3:0>, D<3:0>, PRE_B, RD_EN, WL_EN, WR_EN.
- I1 `decoder_predec`: A, AB, WL_EN in; WL<15:0> out.
- COL<3:0> `sram_col` (four instances, one per bit): D, PRE_B, RD_EN, WL<15:0>, WR_EN in; DOUT out. The 16 cells, precharge, write driver, read path and output latch of a column are presumably inside `sram_col`; its schematic was not seen.

Open items: sram_col schematic and its contents; full-macro tests (2.5); sizes of the input buffering used in 2.5.

## tb_sram_macro (full-macro testbench)

Images: `media/sram_macro/tb_sram_macro_sources.png` (DUT, sources, DIN inverter), `tb_sram_macro_buffers_and_data_gates.png` (buffers and the data-pattern gates), `tb_sram_macro_schematic.png` (earlier, smaller whole-schematic capture; the first version of this note misread the buffers as 6-stage chains, which is wrong).

Sources (all 0 to 0.8 V, 20 ps edges, `tclk` = clock period; values read from the legible captures):

| Source | Period | Delay | Width / note |
|---|---|---|---|
| clk_s | tclk | tclk/2 | tclk/2 - 20p |
| a0_s | 2 tclk | 1.25 tclk | tclk - 20p |
| a1_s | 4 tclk | 2.25 tclk | 2 tclk - 20p |
| a2_s | 8 tclk | 4.25 tclk | 4 tclk - 20p |
| a3_s | 16 tclk | 8.25 tclk | 8 tclk - 20p |
| we_s | 32 tclk | 16.25 tclk | v1 = 0.8 V, v2 = 0 (starts high, drops low) |
| ph_s | 200 tclk | 32.25 tclk | width 100 tclk |
| M, E | tclk | 1.35 tclk, tclk | purpose not legible (sampling/marker pulses, probably) |

Address: a0..a3 form a binary counter, a0 toggling every tclk, so the address steps through all 16 values over 16 cycles; changes fall at 1.25 tclk etc., while CLK is low.
WE: starts high (write) for the first 16 cycles, then low (read) for 16, repeating every 32 cycles: write all 16 words, then read all 16.
Input buffering: IB1<0:5> and IB2<0:5> are two `inv_u` stages (a non-inverting buffer) on each of the six inputs clk_s, we_s, a3_s..a0_s (one `inv_u` per bit, 6 bits), giving CLK, WE, ADDR realistic drive. DIN goes through one `inv_u` (IDIN).
Load: 1 fF on each DOUT.

Data pattern (logic read from the gates): x1 = NAND(a0_s, ph_s); x2 = NAND(a0_s, x1); x3 = NAND(ph_s, x1); X = NAND(x2, x3) = a0 XOR ph. xb = NOT X, xbb = NOT xb = X. DIN<3:0> = inverters of {xb, xbb, xb, xbb} = {X, xb, X, xb}: alternating bits. So the word is 0101 or 1010 depending on X = a0 XOR ph: alternating by row through a0, and ph flipping at 32.25 tclk complements every word. That is the checkerboard of 2.5(i), then the complement overwrite of 2.5(ii) in the next 16 write cycles after ph flips (ph_s is high from 32.25 tclk, i.e. from the second 32-cycle period).

Not covered by this bench: 2.5(iii), the worst-case row read immediately after a write to the opposite value. Which bit order DIN[3:0] has (bit 3 first) is assumed.

Open: run it and capture waveforms and a pass/fail table.
