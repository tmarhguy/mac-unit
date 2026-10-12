# ADR-001: Bitcell Sizing (beta / gamma)

Date: 2026-10-02
Status: schematic-measured (post-layout TBD)

## Context

Part 1 needs a 6T cell that reads without flipping and writes
reliably at 0.8 V nominal (GPDK 18 nm), tileable for the Part 2 macro.

## Decision

Size by cell ratio `beta = (W/L)PD/(W/L)PG` for read stability and
pull-up ratio `gamma = (W/L)PU/(W/L)PG` for writability. Sweep beta
in schematic (1×, 1.5×, 2×), pick the design point, keep the cell
symmetric, then confirm with post-layout SNM/WM.

Schematic read-SNM at 0.8V (WL=VDD, BL=BLB=VDD, `scripts/check_snm_sweep.py`):
beta1 126.6mV, beta1.5 145.8mV, beta2 156.3mV. Selected beta=2, gamma=1
(PD 4fin, PU 2fin, PG 2fin, L=18nm). Raw: `results/part1/read-snm/beta*/raw.csv`.

## Consequences

- Chosen `(W/L)` table lives in `docs/sections/03-bitcell.adoc`.
- Post-layout butterfly + write-margin benches are mandatory;
  schematic-only SNM never promotes to results beyond the design section.
- Per-cell `C_BL` / `C_WL` become Part 2 line-load inputs.
