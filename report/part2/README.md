# Part 2 report and where the data is

- Report: `ESE5700_Proj1_Part2.pdf` (compiled) and `ESE5700_Proj1_Part2.tex` (source; needs `timing_diagram_2p2c.tex` and `img/small/`). Build: `latexmk -pdf ESE5700_Proj1_Part2.tex` or tectonic.
- All simulation screenshots (full size), results tables, CSVs, the Spectre netlist and the fin-count script are on the branch **`contribution-vwanjohi`** (open as PR #4 into `main`): https://github.com/tmarhguy/mac-unit/tree/contribution-vwanjohi
- Start with the index: https://github.com/tmarhguy/mac-unit/blob/contribution-vwanjohi/results/README.md (every folder and file, by block).
- Merging PR #4 brings `media/`, `results/`, `netlists/` and `scripts/` onto `main`.
- Not yet in the repo: the 16x4 array layout, DRC/LVS and extracted C_BL/C_WL (section 2 of the report), and the second decoder implementation.
