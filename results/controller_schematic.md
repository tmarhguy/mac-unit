# controller schematic (2.4), as drawn

Cell `proj1_lib/controller`. Inputs CLK, WE, ADDR<3:0>, DIN<3:0>. Outputs A<3:0>, AB<3:0>, D<3:0>, PRE_B, WL_EN, WR_EN, RD_EN. Schematic: `media/controller/controller_schematic.png` (cleanest of three captures; `controller_schematic_alt.png` is the same circuit, `controller_schematic_partial_view.png` is cut off at the right).

Blocks, read from the schematic (no simulation yet):

| Net | How it is made |
|---|---|
| CLKB, CLKBUF | CLK through `inv_u` (I0) to CLKB, then `inv_u` (I1) to CLKBUF |
| A<3:0>, D<3:0>, WE_L | `out_latch` cells LA, LD, LWE with EN = CLKB and RD = ADDR, DIN, WE. Transparent while CLK is low, holding while CLK is high |
| AB<3:0> | `inv_u` on A<3:0> |
| WE_LB | `inv_u` (I3) on WE_L |
| PRE_B | `inv_2x` (I4) on CLK, so PRE_B is the inverted clock |
| CLKD_B | CLKBUF through DLY1, a chain of 7 `inv_u` (inverting) |
| WL_EN | `nand2_u` (I6) of CLKBUF and CLKD_B, then `inv_2x` (I7). A one-shot: a pulse on each rising edge, width set by the DLY1 delay |
| WR_EN | `nand2_u` (I8) of WL_EN and WE_L, then `inv_2x` (I9): write cycles only |
| WLD | WL_EN through DLY2, a chain of 8 `inv_u` (non-inverting) |
| RD_EN | `nand2_u` (I11) of WLD and WE_LB, then `inv_u` (I12): WL_EN delayed by DLY2, read cycles only |

Matches the read-column result: RD_EN rises one chain delay after WL_EN and falls one chain delay after it, so its width equals the WL_EN width.

Open items:
- Simulate: WL_EN width (target about 140 ps at 50%), RD_EN lead over WL, WR_EN width, and the margin on each edge.
- Check PRE_B polarity. PRE_B is the inverted CLK, so if the precharge devices conduct while PRE_B is low, precharge is on while CLK is high, the same time the WL_EN pulse fires after the rising edge. The handout (2.2c) needs the wordline to rise after precharge releases. If the precharge is active-low, PRE_B probably needs to follow CLK (low while CLK is low, rising with it).
- Margin recovery if C_BL is 20% larger (longer DLY chains or a replica).
