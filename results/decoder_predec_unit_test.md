# decoder_predec unit test (4-to-16 row decoder with WL_EN)

Testbench `proj1_lib/tb_dec_pre`: transient 0 to 0.8 ns, nominal corner, 27 C, VDD = 0.8 V. `cwl` = 0.5 fF on each of the 16 wordlines (Part 1 gives 4 x 90 aF = 360 aF per row, plus wire). WL_EN: pulse 0 to 0.8 V, delay 200 ps, 20 ps edges, width 300 ps, period 1 ns. Address inputs are DC sources set by `a0` to `a3` (volts) with complements 0.8 - a. Schematics: `media/decoder_predec/`.

Design: PA<j> = WL_EN and (A<1:0> = j) through `nand3_u` + `inv_2x`; PB<m> = (A<3:2> = m) through `nand2_u` + `inv_2x`; `row_pre` (`nand2_u` + `inv_drv`) per row, WL<4m + j> = PA<j> and PB<m>. Path WL_EN to WL: `nand3_u`, `inv_2x`, `nand2_u`, `inv_drv`.

Output definitions use the sum of all 16 wordlines as "the selected wordline" (only one should be high):
- `t_en_r` / `t_en_f`: sum crossing 0.4 V (rising / falling) minus WL_EN crossing 0.4 V (rising / falling).
- `wl_one` = ymax(sum), spec < 1 V (two rows high would give about 1.6 V).
- `wl_hi` = ymax(sum), spec > 0.72 V (the selected row reaches high).

## Results so far: address 0 only (a0 = a1 = a2 = a3 = 0)

| Output | Value | Spec | Result |
|---|---|---|---|
| t_en_r | 97.42 ps | none | n/a |
| t_en_f | 101 ps | none | n/a |
| wl_one | 824 mV | < 1 V | pass |
| wl_hi | 824 mV | > 0.72 V | pass |

Headline at address 0: WL_EN to WL is about 97 ps rising and 101 ps falling (two significant figures). The 824 mV peak is 24 mV above VDD, an overshoot on the selected wordline (the sum of the other 15 rows is near 0).

Source: `media/decoder_predec/tb_dec_pre_ade_results_addr0.png`.

## Open items

- Only address 0 has been run. Sweep `a0` to `a3` over {0, 0.8} for all 16 addresses and record the worst-case `t_en_r` and `t_en_f` (the path through `nand3_u` differs by address, so delays will differ).
- The sum-of-wordlines measurement cannot show which row went high. Confirm from the WL<k> waveforms that WL<address> is the one that fires at each address.
- `cwl` = 0.5 fF is a stand-in; rerun with the extracted wordline load.
- Delay is to the 0.4 V crossing of the wordline, not to the cell. The cell sees WL rise through `inv_drv`; use the WL waveform at the cell for read and write timing.
