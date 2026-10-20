# sram_macro top-level schematic (as drawn)

Image: `media/sram_macro/sram_macro_schematic.png`. Ports: CLK, WE, ADDR<3:0>, DIN<3:0> in; DOUT<3:0> out; VDD, VSS. Matches the Part 2 interface (CLK, WE, ADDR[3:0], DIN[3:0], DOUT[3:0]).

Instances:
- I0 `controller`: CLK, WE, ADDR, DIN in; outputs A<3:0>, AB<3:0>, D<3:0>, PRE_B, RD_EN, WL_EN, WR_EN.
- I1 `decoder_predec`: A, AB, WL_EN in; WL<15:0> out.
- COL<3:0> `sram_col` (four instances, one per bit): D, PRE_B, RD_EN, WL<15:0>, WR_EN in; DOUT out. The 16 cells, precharge, write driver, read path and output latch of a column are presumably inside `sram_col`; its schematic was not seen.

Open items: sram_col schematic and its contents; full-macro tests (2.5); sizes of the input buffering used in 2.5.
