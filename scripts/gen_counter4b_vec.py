from pathlib import Path

T = 1.0   # clock period, ns
# (RST, EN) sampled at each rising edge: reset, count through the 15->0 wrap,
# hold, resume, reset while counting, resume, hold
SEQ = [(1, 0)]*2 + [(0, 1)]*20 + [(0, 0)]*3 + [(0, 1)]*5 + [(1, 1)]*2 + [(0, 1)]*4 + [(0, 0)]*2

HEADER = """radix 1 1 1 4
io i i i o
vname CLK RST EN COUNT<[3:0]>
tunit 1ns
trise 0.02
tfall 0.02
vih 0.8
vil 0.0
voh 0.6
vol 0.2

; time(ns) CLK RST EN COUNT
"""

rows, count, prev = [], 0, None
for k, (rst, en) in enumerate(SEQ + [(0, 0)]):
    t0 = k * T
    rows.append(f"{t0:.4f} 0 {rst} {en} X")                    # inputs change, CLK low
    if prev is not None:
        rows.append(f"{t0 + T/4:.4f} 0 {rst} {en} {prev:X}")   # check COUNT after edge k
    if k == len(SEQ):
        break
    rows.append(f"{t0 + T/2:.4f} 1 {rst} {en} X")              # rising edge k+1
    count = 0 if rst else ((count + 1) % 16 if en else count)
    prev = count

out = Path.home() / "simulation" / "stimuli"      # your own space: /vast/home/v/vwanjohi/simulation/stimuli
out.mkdir(parents=True, exist_ok=True)
vec = out / "counter4b.vec"
vec.write_text(f"; tb_counter4b: {len(SEQ)} edges, T = {T} ns, stop >= {(len(SEQ) + 1) * T:.1f} ns\n"
               + HEADER + "\n".join(rows) + "\n")
(out / "counter4b_vec.scs").write_text(f'vec_include "{vec}"\n')
print("wrote", vec, "and", out / "counter4b_vec.scs")
