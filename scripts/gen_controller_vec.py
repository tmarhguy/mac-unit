from pathlib import Path

T = 1.0   # clock period, ns
# per rising edge 1..60: inputs (sampled at the edge) and outputs expected after it
RST   = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
START = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
RUN   = [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0]
DONE  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
ACCEN = [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0]
COUNT = [0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,15,15,15,15,0,1,2,3,4,5,6,7,8,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,15,15,15,15]

HEADER = """radix 1 1 1 1 1 1 4
io i i i o o o o
vname CLK RST START RUN DONE ACC_EN COUNT<[3:0]>
tunit 1ns
trise 0.02
tfall 0.02
vih 0.8
vil 0.0
voh 0.6
vol 0.2

; time(ns) CLK RST START RUN DONE ACC_EN COUNT
"""

N = len(RST)
rows = []
for k in range(N + 1):
    t0 = k * T
    r, s = (RST[k], START[k]) if k < N else (0, 0)
    rows.append(f"{t0:.4f} 0 {r} {s} X X X X")                   # inputs change, CLK low
    if k > 0:                                                     # check outputs after edge k
        j = k - 1
        rows.append(f"{t0 + T/4:.4f} 0 {r} {s} {RUN[j]} {DONE[j]} {ACCEN[j]} {COUNT[j]:X}")
    if k < N:
        rows.append(f"{t0 + T/2:.4f} 1 {r} {s} X X X X")         # rising edge k+1

out = Path.home() / "simulation" / "stimuli"
out.mkdir(parents=True, exist_ok=True)
vec = out / "controller.vec"
vec.write_text(f"; tb_controller: {N} edges, T = {T} ns, stop >= {(N + 1) * T:.1f} ns\n"
               + HEADER + "\n".join(rows) + "\n")
print("wrote", vec)
