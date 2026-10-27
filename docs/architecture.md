# Architecture and build order

Cadence GPDK 18 nm (`cds_ff_mpt`) at nominal 0.8 V. The live report site is a single-page Asciidoctor book built from [`docs/index.adoc`](index.adoc). One Gradescope PDF per part lives under [`report/part1/`](../report/part1/), [`report/part2/`](../report/part2/), and [`report/part3/`](../report/part3/).

## Built hierarchy

1. **6T bitcell (Part 1).** Symmetric cell, 0.72 µm × 0.54 µm = 0.39 µm², D = 28, DRC 0, LVS clean. Extracted $C_{BL}=180$ aF, $C_{WL}=90$ aF. Extracted read SNM 140 mV at 0.8 V (110 mV at 0.7 V, 70 mV at 0.5 V). Write margin 0.42 / 0.32 / 0.18 V. The 0.5 V write is the weak result. Schematic SNM CSVs remain in [`results/part1/read-snm/`](../results/part1/read-snm/).

2. **16×4 SRAM macro (Part 2).** Same cell tiled 64 times. 4-to-16 predecoder, nfin=8 write driver, 2:2 read path, output latch, delay-chain controller. Stand-in $C_{BL}=3.5$ fF. Schematic-level: $T_{CLK}=0.69$ ns, $t_{\mathrm{access}}=488$ ps, $P_{\mathrm{read}}=115.2$ µW, $P_{\mathrm{leak}}=3.99$ µW, area 54.6 µm² (est.), FOM $\approx 4.7\times10^{3}$. Notes: [`results/sram_macro_unit_test.md`](../results/sram_macro_unit_test.md), [`results/sram_macro_area_fom.md`](../results/sram_macro_area_fom.md).

3. **4-bit MAC (Part 3).** Two macros (W and X), 4×4 array multiplier, 12-bit ripple accumulator, 4-bit counter + `controller_mac`. TG master-slave DFFs. 17 cycles START→DONE. Schematic-level: selected $T_{CLK}=2.5$ ns, $t_{dot}=42.5$ ns, Test A $E_{dot}=8.870$ pJ, FOM$_{MAC}=1.1\times10^{5}$. Tests A/B/C all pass at 10 / 4.0 / 2.5 ns; at 2.0 ns B fails (0xC10 vs 0xE10); 1.75 ns and 1.5 ns all fail.

Site chapter order: overview → spec → Part 1 (sizing, read, write, SNM, layout) → Part 2 macro → Part 3 MAC → verification → about / authors.

## Operating points (do not mix)

| Block | Clock | Delay used in FOM | Energy / power |
|-------|-------|-------------------|----------------|
| Macro | 0.69 ns | $t_{\mathrm{access}}=488$ ps | $P_{\mathrm{read}}=115.2$ µW |
| MAC | **2.5 ns** | $t_{dot}=42.5$ ns | Test A 8.870 pJ |

Part 3 energy and FOM use 2.5 ns, not the 2.0 ns A/C-only pass. Area outside the Part 1 cell is $D\sum W_i L_i$ (est.).

## Site build

`make docs` runs [`scripts/build-docs.sh`](../scripts/build-docs.sh): Asciidoctor → `build/docs/index.html`, then stages `docs/images`, `media/cadence`, `media/part1`, selected Part 2 JPEGs from `report/part2/img/small/`, selected Part 3 PNGs from `report/part3/img/`, and the three report PDFs. `make docs-check` runs [`scripts/check-docs.py`](../scripts/check-docs.py) (alt text, unique IDs, `#overview` / `#about`, no missing assets). GitHub Pages deploys from `main` via [`.github/workflows/docs.yml`](../.github/workflows/docs.yml).
