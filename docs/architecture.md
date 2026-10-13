# Architecture and build order

The current project basis is Cadence GPDK 18 nm (`cds_ff_mpt`) at nominal 0.8 V. Measured Part 1 evidence is a symmetric 6T cell schematic and a three-point schematic read-SNM sweep. The [report](../ESE5700_Proj1_Part1.tex) also records the layout, extraction, and post-layout benches; numeric cells there stay blank until a Cadence run is filed. Raw exports are in the [results directory](../results/part1/read-snm/).

## Planned hierarchy

1. Record the tileable bitcell's PR-boundary area, Pegasus DRC/LVS, and per-cell BL/WL capacitance.
2. Record hold and read SNM, write margin, cell current, the 0.7 V and 0.5 V supply rows, and the functional write/read on the extracted cell.
3. Tile the validated cell into a 16 × 4 SRAM macro with decoder, precharge, write and sense circuitry.
4. Feed two macros into a 4 × 4 multiplier and 12-bit accumulator. A sequencer addresses the 16 word pairs.

Only the schematic read sweep currently has measured results. Later blocks must be verified before performance, area or timing can be reported.
