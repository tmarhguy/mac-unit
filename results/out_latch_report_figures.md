# out_latch: table and figure for the report

## Table: EN pulse-width sweep

VDD = 0.8 V, nominal corner, 27 C, `cdout` = 1 fF (stand-in load), EN delay 300 ps. Tables keep an extra digit; headline numbers use two significant figures.

| pw_en | t_en_r | t_en_f | hold1 | hold0 | Result |
|---|---|---|---|---|---|
| 10p | eval err | eval err | -58.45 uV | 77.11 uV | Fail: latch never captures the 1 |
| 20p | 99.52 ps | 75.99 ps | 799.8 mV | 88.01 uV | Pass |
| 40p | 88.70 ps | 74.78 ps | 799.8 mV | 88.52 uV | Pass |
| 80p | 87.20 ps | 74.46 ps | 799.8 mV | 125.3 uV | Pass |
| 150p (design) | 87.27 ps | 74.47 ps | 799.2 mV | 1.250 mV | Pass |

Pass specs: `hold1` > 0.72 V, `hold0` < 0.08 V. Headline: `t_en_r` = 87 ps, `t_en_f` = 74 ps at the 150 ps design pulse.

## Figure: out_latch transient at pw_en = 150 ps

![out_latch transient at pw_en = 150 ps: RD, EN and DOUT](../media/out_latch/out_latch_tran_en_delay300p.png)

Caption: RD, EN and DOUT over 4.2 ns with a 150 ps EN pulse every 1 ns. DOUT is written only while EN is high (captures 0 at 0.3 ns, 1 at 1.3 ns, 0 at 2.3 ns, 1 at 3.3 ns) and holds its value while RD toggles with EN low. Scalar outputs on the plot: `t_en_r` 87.27 ps, `t_en_f` 74.47 ps, `hold1` 799.185 mV, `hold0` 1.250 mV.

Source files: sweep data `out_latch_pw_en_sweep.csv`; full record `out_latch_unit_test.md`.

## All pw_en traces (optional figure)

Best one for the report: `../media/out_latch/out_latch_pw_en_family_full_BEST.png`. It stacks RD, EN and DOUT for all five pw_en values (10p, 20p, 40p, 80p, 150p) over 0-4.2 ns with readable axes and labels. The 10p DOUT trace stays near 0 V and never captures the 1. This version is cropped to the plot area (no toolbar, tabs or status bar), so it can be used as is.

Other captures, kept in case they are needed (all in `media/out_latch/`):

| File | What it is |
|---|---|
| `out_latch_pw_en_family_full_BEST.png` | Full stack, readable, cropped to the plot (use this one) |
| `out_latch_pw_en_family_full_uncropped.png` | Same stack with the tool toolbar, tabs and status bar still showing |
| `out_latch_pw_en_family_full_vnc_overlay.png` | Same stack, but a VNC toolbar covers the left edge |
| `out_latch_pw_en_family_full_dark_unreadable.png` | Same full stack, dark with very small text |
| `out_latch_pw_en_family_partial_dout.png` | Scrolled view: EN (80p, 150p) and DOUT for all five values |
| `out_latch_pw_en_family_partial_rd_en.png` | Scrolled view: RD (80p, 150p) and EN for all five values |
