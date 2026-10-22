# Part 2 data index (branch `contribution-vwanjohi`)

Everything measured for Part 2 is in this branch (PR #4 into `main`). The compiled report and its source are on `main` under `report/part2/`; a longer, less edited draft is in `report/part2_long_draft/`.

## Images, by block (`media/`)

| Folder | Files | What |
|---|---|---|
| `media/controller/` | 16 | controller: schematics (v1 to v3), tb_controller, ADE results, waveforms |
| `media/decoder_predec/` | 15 | 4-to-16 decoder: schematic, tb_dec_pre, 16-address checks, address-to-wordline delay |
| `media/inv_2x/` | 1 | 2x inverter (8:4) |
| `media/inv_drv/` | 1 | wordline driver inverter (6:3) |
| `media/inv_u/` | 5 | unit inverter and the FO4 testbench (tb_fo4) with results |
| `media/nand2_u/` | 1 | 2-input NAND (2/2 fins) |
| `media/nand3_u/` | 1 | 3-input NAND (4 PMOS, 6 NMOS) |
| `media/out_latch/` | 18 | output latch: schematic, testbench, pw_en sweep, unit-test waveforms |
| `media/precharge/` | 5 | precharge schematic, testbench, ADE outputs and transients |
| `media/read_col/` | 19 | read column bench: rd_dly x pw_rden sweep, waveforms at 1.48n/120p, ADE setup and results |
| `media/read_path/` | 9 | read path (inverter on BLB): symbol, schematic, VTC, switching-point outputs (2:2 and 4:2) |
| `media/row_pre/` | 1 | per-row gate (NAND2 + driver) |
| `media/sram_macro/` | 35 | full macro: top-level and testbench schematics, sram_col, 66 ns and 22 ns runs, period sweeps, power, standby |
| `media/write_driver/` | 11 | write driver: schematics and transients for nfin 2, 4, 5, 6, 8; ADE outputs |

Image names say what they show; names ending `_BEST` mark the clearest capture, `_nfin2/4/5/6/8` the fin count, `_v2`/`_v3` design versions kept for the record.

## Results and records (`results/`)

| File | Contents |
|---|---|
| `results/controller_schematic.md` | controller as drawn |
| `results/controller_unit_test.md` | controller timing, before/after, margins on each edge |
| `results/decoder_logical_effort.md` | logical-effort numbers and corrections |
| `results/decoder_predec_address_sweep.csv` | 16-address data |
| `results/decoder_predec_unit_test.md` | decoder tests: delays, 16-address checks, wl_idx, address-to-wordline delay |
| `results/inv_u_fo4.md` | FO4 delay of inv_u (52.6 ps) |
| `results/nfin_sizes.md` | final nfin per cell and how each was found |
| `results/out_latch_pw_en_sweep.csv` | pw_en sweep data |
| `results/out_latch_report_figures.md` | table and figure chosen for the report |
| `results/out_latch_unit_test.md` | output latch unit test and pw_en sweep |
| `results/read_col_dout_c6_sweep.csv` | subset of the above (dout_c6) |
| `results/read_col_sweep.csv` | full 24-point rd_dly x pw_rden sweep, all outputs |
| `results/read_col_unit_test.md` | read column test (2.3): grid, chosen timing, waveforms |
| `results/sram_macro_area_fom.md` | exact area from the netlist and preliminary FOM |
| `results/sram_macro_schematic.md` | macro, sram_col, testbench decoding, netlist cross-checks, corrections |
| `results/sram_macro_tclk_power_sweep.csv` | final sweep 700 to 600 ps: errors, access, write/read/standby power |
| `results/sram_macro_tclk_sweep.csv` | err1/err2 vs clock period (1 to 0.7 ns) |
| `results/sram_macro_tclk_sweep_err3.csv` | err3 and write times vs clock period |
| `results/sram_macro_unit_test.md` | full-macro tests, sweeps, power, standby (all runs in order) |
| `results/write_driver_summary.md` | write-driver and read-path summary, tables, rationale for read_path 2:2 |
| `results/write_driver_sweep.csv` | 12-point pw_w1 x C_BL write sweep (nfin 8) |

## Netlist and scripts

- `netlists/tb_sram_macro.scs`: Spectre netlist of the macro and its testbench (all subcircuits, fin counts).
- `scripts/count_fins.py`: fin counts per cell and flattened area from the netlist (`python3 scripts/count_fins.py netlists/tb_sram_macro.scs`).

## Report

- `report/part2/` on `main`: `ESE5700_Proj1_Part2.tex`, `.pdf`, `timing_diagram_2p2c.tex`, resized figures in `img/small/` (full-size originals are the `media/` files above).
- `report/part2_long_draft/` (this branch): the earlier 25-page draft with every figure, `.tex` and `.pdf`.
