# Architecture and build order

The current project basis is Cadence GPDK 18 nm at nominal 0.8 V. Available Part 1 evidence is a symmetric 6T cell schematic and a three-point schematic read-SNM sweep. See the [report](../ESE5700_Proj1_Part1.tex) for analysis and the [results directory](../results/part1/read-snm/) for raw exports.

## Planned hierarchy

1. Complete a tileable bitcell layout; run DRC/LVS and parasitic extraction.
2. Rerun read and hold SNM, write margin, cell current, supply behavior and functional write/read on the extracted cell.
3. Tile the validated cell into a 16 × 4 SRAM macro with decoder, precharge, write and sense circuitry.
4. Feed two macros into a 4 × 4 multiplier and 12-bit accumulator. A sequencer addresses the 16 word pairs.

Only the schematic read sweep currently has measured results. Later blocks must be verified before performance, area or timing can be reported.
