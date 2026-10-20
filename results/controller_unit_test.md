# controller unit test (2.4)

Testbench `proj1_lib/tb_controller`: controller driving `decoder_predec` (cwl = 0.5 fF per wordline), loads of 500 aF on PRE_B, 600 aF on RD_EN, 1.3 fF on WR_EN (stand-ins; read from a small schematic label). Transient 0 to 4.5 ns, nominal, 27 C, VDD = 0.8 V, clock period 1 ns (CLK rises at 0.5, 1.5, 2.5, 3.5 ns). Address held at 0, DIN all ones. WE high in cycle 1 and 3 (write), low in cycle 2 and 4 (read), as read from the waveform. Images: `media/controller/tb_controller_ade_results.png`, `tb_controller_tran.png`, schematic `tb_controller_schematic.png`.

| Output | Meaning | Value | Spec | Result |
|---|---|---|---|---|
| wlen_w | WL_EN width, 0.4 V crossings | 133.5 ps | none | n/a |
| t_clk_wl | CLK rising to WL<0> rising | 355.8 ps | none | n/a |
| t_wl_rden | WL<0> rising to RD_EN rising | 95.84 ps | none | n/a |
| rden_w | RD_EN width, 0.4 V crossings | 135.7 ps | none | n/a |
| gap_pre_wr | PRE_B rising to WR_EN rising | 178.5 ps | > 0 | pass |
| m_wl_pre | WL<0> falling to PRE_B falling | 117.8 ps | > 0 | pass |
| m_rd_pre | RD_EN falling to PRE_B falling (second PRE_B fall, 0.4 V) | 30.42 ps | > 0 | pass |
| no_rd_wr | peak RD_EN, 0.5 to 1.5 ns (write cycle) | 3.398 mV | < 0.08 V | pass |
| no_wr_rd | peak WR_EN, 1.5 to 2.5 ns (read cycle) | 411.7 uV | < 0.08 V | pass |

Reading of the waveform (times approximate, read off the plot):
- PRE_B follows CLK: it rises with CLK and falls with CLK, so precharge releases (PRE_B high, assuming an active-low precharge) at each rising edge. WL_EN/WL fire about 0.36 ns after the edge, end before PRE_B falls, and the bitlines are precharged again after.
- WR_EN pulses only in the write cycles, RD_EN only in the read cycles (about 2.0 and 4.0 ns), each about 135 ps wide.
- RD_EN rises 96 ps after WL rises (target from the read-column test: about 80 ps).

Combined access estimate: t_clk_wl (355.8 ps) + t_acc1 (226 ps, read-column test) = about 582 ps, CLK edge to valid DOUT. Sum of two separate simulations at stand-in loads, not one run; DOUT valid defined at 0.4 V.

Checks against targets:
- WL_EN width 133.5 ps at 0.4 V crossings vs the write minimum of 100 to 120 ps at 50%: passes with about 13 ps over the upper end. The design value was 140 ps. WL<0> width itself is not measured.
- RD_EN-to-PRE_B margin is only 30 ps (m_rd_pre). That is the thinnest edge. At +20% C_BL the read delays grow, so this margin needs recovery (shorter RD_EN, earlier clock phase, or a longer clock half period).

Open items:
- Confirm PRE_B active-low polarity against the `precharge` cell. The margins above assume PRE_B low means precharge on.
- Margin analysis at +20% C_BL (rerun with cwl and bitline loads scaled).
- Rerun with extracted loads; WE/address sequence only covers address 0.
