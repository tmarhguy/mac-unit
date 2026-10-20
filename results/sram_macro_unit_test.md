# sram_macro full-macro test (2.5) -- first run, 66 ns

Testbench `tb_sram_macro` (see `sram_macro_schematic.md`), tclk = 1 ns, transient 0 to 66 ns, nominal. Images in `media/sram_macro/`: `tb_sram_macro_tran_control.png` (M, E, WE, CLK), `tb_sram_macro_tran_dout.png`, `tb_sram_macro_tran_din.png`, `tb_sram_macro_tran_addr.png`, `tb_sram_macro_ade_outputs_setup.png`.

Schedule read off the waveforms: WE high 0 to 16.25 ns (write 16 words, addresses 0..15, one per cycle), low 16.25 to 32.25 ns (read 16), high 32.25 to 48.25 ns (write complement), low 48.25 to 64.25 ns (read 16). ADDR<0> toggles every cycle, ADDR<3> every 8 cycles.

Check outputs (values not yet shown):
- err1 = max over 17 to 33 tclk of M * (|DOUT0 - E| + |DOUT1 - (0.8 - E)| + |DOUT2 - E| + |DOUT3 - (0.8 - E)|), spec < 0.1 V: first read pass (checkerboard).
- err2 = same over 49 to 65 tclk with the opposite polarity (DOUT0 expected at 0.8 - E, DOUT1 at E, ...), spec < 0.1 V: second read pass (complement).
- M is a narrow pulse that samples each cycle; E is the expected-bit square wave. The expected word is DOUT0 = DOUT2 = E, DOUT1 = DOUT3 = not E.

Observed from the DOUT waveforms (coarse, 66 ns on screen):
- Before the first read all four outputs sit high (latch start-up state).
- DOUT<3> and DOUT<1> are in phase, DOUT<2> and DOUT<0> are in phase and opposite to them: each word is 0101 or 1010, alternating every cycle (address), as the checkerboard requires.
- During the first read pass (17 to 32 ns) all outputs toggle every cycle; first transition at about 17.0 ns for a read whose clock edge is at 16.5 ns, i.e. about 0.5 ns CLK-to-DOUT (consistent with the 0.46 ns estimate; read off a 66 ns plot, so only roughly).
- While WE is high (32 to 49 ns) DOUT holds (bits 3 and 1 high, 2 and 0 low = the last word read, address 15), as the output latch should.
- In the second read pass (50 to 64 ns) the outputs toggle every cycle again; address 0 gives the complement of its first-pass value, which is why nothing changes at 49 ns (the held address-15 value equals the complement of address 0) and all four bits change together at 50 ns.
- After 64 ns the outputs hold again.

Not shown: the err1 and err2 values (the Value column is empty), so a numeric pass/fail is not yet recorded. Also not covered: 2.5(iii), the worst-case row read right after a write to the opposite value, and a minimum-period (T_CLK,min) search.

Open: run and record err1, err2; write the pass/fail table; add 2.5(iii); measure the worst-case access time and T_CLK,min from a period sweep.
