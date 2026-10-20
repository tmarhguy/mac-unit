# inv_u FO4 delay (decoder sizing basis)

Testbench `proj1_lib/tb_fo4`: transient 0 to 1.2 ns, nominal corner, 27 C, VDD = 0.8 V. All stages are `inv_u` (PM0 4 fins, NM0 2 fins, l = 18n). Input: 0 to 0.8 V pulse, 20 ps edges. I0 drives N1; N1 feeds four `inv_u` (I1 to I4); I1 drives N2; N2 feeds four `inv_u` (I5 to I8). The measured stage is I1, N1 to N2: it has an FO4 load and an FO4-loaded driver. Schematic: `media/inv_u/tb_fo4_schematic.png`.

| Output | Definition | Value |
|---|---|---|
| tphl | N2 falling through 0.4 V minus N1 rising through 0.4 V | 54.66 ps |
| tplh | N2 rising through 0.4 V minus N1 falling through 0.4 V | 50.59 ps |
| FO4 delay (average) | (tphl + tplh) / 2 | 52.62 ps, about 53 ps |

Headline for the report: FO4 = 53 ps (two significant figures).

Estimate, not simulated: with the convention FO4 = 5 tau (inverter parasitic delay p = 1, electrical effort h = 4), tau is about 10.5 ps. Check this against the delay model the course handout uses before using it in the logical-effort sizing.

Notes:
- tplh is faster than tphl by about 4 ps, so the 4:2 inverter is slightly NMOS-favoured at this load and slew. This is read from the two numbers, not separately investigated.
- The crossing level is 0.4 V (VDD/2), not the 0.376 V of the read_path inverter.
- Single run, nominal corner, no wire load. Layout parasitics will make real FO4 slower.

Files: `media/inv_u/tb_fo4_ade_setup.png` (outputs setup, values not shown), `media/inv_u/tb_fo4_tran.png` (IN, N1, N2 with the scalar outputs), `media/inv_u/inv_u_schematic.png`.
