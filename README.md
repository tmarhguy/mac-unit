# ESE 5700 Project 1 — 6T SRAM bitcell

Tyrone Marhguy and Victor Wanjohi's Part 1 work toward an SRAM-fed 4-bit multiply-accumulate unit. The [current course handout](docs/ese5700-project1-current.pdf) specifies Cadence GPDK 18 nm, nominal 0.8 V and a post-layout 6T cell characterization. The repository currently contains the sized schematic, detailed read/write hand analysis, Cadence read testbenches, and a measured three-point *schematic* read-SNM sweep. Post-layout signoff and the remaining benches are still open.

## Read the report

- [Full Part 1 PDF](ESE5700_Proj1_Part1.pdf) and [LaTeX source](ESE5700_Proj1_Part1.tex)
- [Report website](https://tmarhguy.github.io/mac-unit/) and [AsciiDoc source](docs/index.adoc)
- [Raw Cadence sweep and derived SNM results](results/part1/read-snm/)

The PDF and site retain the original handwritten read derivation, Virtuoso testbench captures, and all three original ViVA butterflies. Cyan overlays show the computed maximum-square locations from each `snm.json` on the Cadence screenshots.

| β (PD / PG / PU fins) | Schematic read SNM at 0.8 V | Read-disturbed zero node |
|---|---:|---:|
| 1.0 (2 / 2 / 2) | 126.6 mV | 134.3 mV |
| 1.5 (3 / 2 / 2) | 145.8 mV | 96.6 mV |
| **2.0 (4 / 2 / 2)** | **156.3 mV** | **77.1 mV** |

β=2, γ=1 is the *schematic candidate*. The current handout also requires tileable layout and area, DRC/LVS, extraction and per-cell BL/WL capacitances, post-layout hold/read SNM, write margin and cell current, a 0.8/0.7/0.5 V supply table, functional waveforms, and each author's actual contributions. The report maps each missing item to its required evidence without supplying invented values.

## Reproduce the available result

```bash
python3 scripts/check_snm_sweep.py --all
make report
make docs
python3 scripts/check-docs.py build/docs
```

The data path is `results/part1/read-snm/beta*/raw.csv` → `q.csv` / `qb.csv` → `snm.json` and clean butterfly plots. The reported SNM is the smaller maximum-square side from the two butterfly lobes. The original Cadence captures and handwritten work remain in `media/part1/`.

## Later project stages

The handout's Parts 2 and 3 call for two 16 × 4 SRAM macros feeding a 4 × 4 multiplier, 12-bit accumulator and sequencer. Those are the project direction, not completed hardware in this repository. The maximum unsigned dot-product sum is 16 × 15 × 15 = 3600, which fits in 12 bits.
