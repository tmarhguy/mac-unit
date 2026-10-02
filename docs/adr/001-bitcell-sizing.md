# ADR-001: Bitcell Sizing (beta / gamma)

Date: 2026-10-02
Status: proposed (bench TBD)

## Context

Part 1 needs a 6T cell that reads without flipping and writes
reliably at 1.2 V nominal, tileable for the Part 2 macro.

## Decision

Size by cell ratio `beta = (W/L)PD/(W/L)PG` for read stability and
pull-up ratio `gamma = (W/L)PU/(W/L)PG` for writability. Sweep beta
in schematic (1×, 1.5×, 2×), pick the design point, keep the cell
symmetric, then confirm with post-layout SNM/WM.

## Consequences

- Chosen `(W/L)` table lives in `docs/sections/03-bitcell.adoc`.
- Post-layout butterfly + write-margin benches are mandatory;
  schematic-only SNM never promotes to results.
- Per-cell `C_BL` / `C_WL` become Part 2 line-load inputs.
