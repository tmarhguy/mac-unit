# Architecture and build order

The current project basis is Cadence GPDK 18 nm (`cds_ff_mpt`) at nominal 0.8 V. The [report](../ESE5700_Proj1_Part1.tex) records a 0.72 µm × 0.54 µm cell (0.39 µm², 3900 F², D = 28), Pegasus DRC with 0 violations, LVS clean with comparison match, and the extracted stability numbers. Schematic read-SNM exports remain in the [results directory](../results/part1/read-snm/).

## Planned hierarchy

1. Keep this cell: 0.39 µm², Quantus net parasitics $C_{BL}=497.8$ aF, $C_{WL}=938.9$ aF. The 0.5 V write margin, 0.18 V, is the weak result.
2. File the functional write/read waveforms, then tile the cell into a 16 × 4 SRAM macro with decoder, precharge, write and sense circuitry.
3. Feed two macros into a 4 × 4 multiplier and 12-bit accumulator. A sequencer addresses the 16 word pairs.

Part 1 area, DRC/LVS, extraction, and the supply table are recorded on this cell. Part 2 and Part 3 are not built yet, so their performance, area, and timing stay unreported.
