# sram_macro top-level schematic (as drawn)

Image: `media/sram_macro/sram_macro_schematic.png`. Ports: CLK, WE, ADDR<3:0>, DIN<3:0> in; DOUT<3:0> out; VDD, VSS. Matches the Part 2 interface (CLK, WE, ADDR[3:0], DIN[3:0], DOUT[3:0]).

Instances:
- I0 `controller`: CLK, WE, ADDR, DIN in; outputs A<3:0>, AB<3:0>, D<3:0>, PRE_B, RD_EN, WL_EN, WR_EN.
- I1 `decoder_predec`: A, AB, WL_EN in; WL<15:0> out.
- COL<3:0> `sram_col` (four instances, one per bit): D, PRE_B, RD_EN, WL<15:0>, WR_EN in; DOUT out. The 16 cells, precharge, write driver, read path and output latch of a column are presumably inside `sram_col`; its schematic was not seen.

Open items: sram_col schematic and its contents; full-macro tests (2.5); sizes of the input buffering used in 2.5.

## tb_sram_macro (full-macro testbench, as drawn)

Image: `media/sram_macro/tb_sram_macro_schematic.png` (text is small; values below are partly read from it and should be checked in the schematic).
- DUT: `sram_macro` with a load capacitor on DOUT<3:0> (value not legible).
- Stimulus: eight pulse sources (clk_s, a0_s to a3_s, we_s, and a data phase ph_s plus two further sources), with periods and delays written as multiples of `tclk` (for example 2*tclk, 4*tclk, 8*tclk, 16*tclk, 32*tclk, with fractional delays such as tclk/2 and 1.25*tclk), 20 ps edges, 0 to 0.8 V. This is a binary counter pattern: it steps the address through all 16 words on successive cycles.
- Input buffering (handout 2.5 asks for realistic input strength): two `inv_u` chains, IB1 and IB2, each of 6 bits wide (named <0:5>), buffer the clock, WE and address sources into CLK, WE, ADDR. This models the input drive instead of ideal sources.
- Data pattern: a small network of `nand2_u` and `inv_u` gates (N1 to N4, IX1, IX2) builds the DIN bits from the address and phase signals (nets x1, x2, x3, xb, xbb), so that DIN depends on the address, as a checkerboard needs. The exact function is not legible here.

Open: confirm the DIN pattern gives checkerboard 0101 / 1010 alternating by row, the complement overwrite and the worst-case-row read, and run it; no results yet.
