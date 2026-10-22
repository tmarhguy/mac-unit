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

## Waveform at address 0

![decoder_predec transient at address 0: WL_EN and all 16 wordlines](../media/decoder_predec/tb_dec_pre_tran_addr0.png)

Caption: WL_EN and WL<15:0> for address 0 (nominal, `cwl` = 0.5 fF). Only WL<0> rises (about 300 ps, 97 ps after WL_EN crosses 0.4 V) and falls (about 620 ps after WL_EN falls at 520 ps). The other 15 rows stay at 0 V with only small coupling glitches: tens to about 150 uV on twelve rows and about 2 mV on WL<4>, WL<8> and WL<12>. Those three share PA<0> with WL<0> (rows 4m + 0), which is the expected place for a glitch. Scalar outputs on the plot: `t_en_r` 97.42 ps, `t_en_f` 101.02 ps, `wl_one` and `wl_hi` 823.96 mV. Times are read off the plot except the scalar outputs. The y-axis range shown for WL<0> is auto-scaled and larger than the 824 mV peak.

This confirms the right row fires at address 0. The other 15 addresses are not yet checked.

## All 16 addresses: level checks

Sweep of `a0` to `a3` over {0, 0.8 V} (16 points, a3 varying fastest; address = a0 + 2 a1 + 4 a2 + 8 a3), same testbench and `cwl` = 0.5 fF. Data: `decoder_predec_address_sweep.csv`.

Result: at all 16 addresses `wl_one` = 824 mV (spec < 1 V) and `wl_hi` = 824 mV (spec > 0.72 V), both pass. So exactly one wordline goes high at every address and none overlap. Source: the ADE results table filtered to "pass" (32 of 336 rows: 2 outputs x 16 points).

Delays: `t_en_r` = 97.42 ps and `t_en_f` = 101 ps at all 16 addresses (the table shows no variation). That is expected for this bench: WL_EN is pulsed while the address is static, and WL_EN always enters the same pin of the same `nand3_u`, so the switching path is the same for every address.

Row identity: the added output `wl_idx` is the sum over k of k times the peak of WL<k>, divided by the 0.824 V peak, i.e. the index of the row that fired. It rounds to the applied address at all 16 points (values 0.059, 8.009, 4.034, 11.98, 2.063, 10.01, 6.037, 13.99, 1.061, 9.01, 5.035, 12.98, 3.064, 11.01, 7.039, 14.99 for addresses 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15). The worst deviation is 0.06, from coupling glitches on the other rows. So the correct row fires at every address. Screenshots: `media/decoder_predec/tb_dec_pre_ade_wl_idx_results.png`, `tb_dec_pre_ade_wl_idx_setup.png`. The expression is read from a screenshot where it is truncated; check it in ADE.

What this does not show: (1) which row fires: resolved by `wl_idx` above; (2) the delay from an address input to the wordline (the path the handout's 2.2a asks about). That path enters `nand3_u` on pins B and C, which can differ from pin A, and needs a bench where the address changes with WL_EN already high or with the enable tied high.

## Open items

- The 16-address sweep has run: level checks pass and the WL_EN-to-WL delay is the same at every address. Still needed: the address-input-to-WL delay (address changing, enable already high).
- `cwl` = 0.5 fF is a stand-in; rerun with the extracted wordline load.
- Delay is to the 0.4 V crossing of the wordline, not to the cell. The cell sees WL rise through `inv_drv`; use the WL waveform at the cell for read and write timing.

## Address-to-wordline delay (A<0> switching, WL_EN held high)

Images: `tb_dec_pre_addr_to_wl_ade.png` (outputs), `tb_dec_pre_addr_to_wl_tran.png` (waveform, plot 23:41:09). Setup: WL_EN held high, A<0> pulsed (period about 2 ns) with its complement on AB<0>, cwl = 0.5 fF, 0 to 4 ns. This is the PA path (WL<0> and WL<1>).

| Output | Definition (0.4 V crossings) | Value |
|---|---|---|
| t_ar | WL<1> rising minus A<0> rising | 106.2 ps (new row rising) |
| t_af | WL<0> falling minus A<0> rising | 112.4 ps (old row falling) |
| t_br | WL<0> rising minus A<0> falling | 105.9 ps |
| t_bf | WL<1> falling minus A<0> falling | 112.4 ps |
| wl_one / wl_hi | peak of the summed wordlines | 1.016 V (spec < 1 V flagged, > 0.72 V pass) |
| wl_idx | | 1.094 (between rows 0 and 1 during the swap) |
| t_en_f | WL_EN falling delay | eval err (WL_EN does not switch in this bench) |

Slower address-to-wordline delay: 112 ps. Logical-effort prediction 182 ps (B = 8): overestimates by about 1.6x (1.7x against the 106 ps edge). The old and new rows overlap briefly while the address changes (summed peak 1.02 V), so the < 1 V static check does not hold during a switch, which is why WL_EN gates the wordlines; the controller changes the address while CLK is low and the enable is off.

Expression details are truncated in the screenshot (definitions above are read from the visible parts of the expressions). Still to do: A<2> (PB path) and quote the slower; the flat decoder.
