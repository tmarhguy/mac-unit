#!/usr/bin/env python3
"""Count fins per subcircuit (and flattened, for sram_macro) from a Spectre netlist.

usage: python3 scripts/count_fins.py netlists/tb_sram_macro.scs
Area convention (Part 1): A = D * sum(W_i L_i), D = 28, 1 fin = 0.048 um wide, L = 18 nm.
"""
import re, sys
from collections import defaultdict

text = open(sys.argv[1]).read().replace("\\\n", " ")
subs, cur = {}, None
for line in text.splitlines():
    line = line.strip()
    m = re.match(r"subckt (\S+)", line)
    if m:
        cur = m.group(1); subs[cur] = {"fins": 0, "children": defaultdict(int)}; continue
    if line.startswith("ends"):
        cur = None; continue
    if cur is None or not line or line.startswith("//"):
        continue
    nf = re.search(r"\bnfin=(\d+)", line)
    if nf:
        subs[cur]["fins"] += int(nf.group(1))
        continue
    m = re.match(r"\S+ \(.*\)\s+(\S+)$", line)
    if m and m.group(1) in subs:
        subs[cur]["children"][m.group(1)] += 1

memo = {}
def total(name):
    if name not in memo:
        s = subs[name]
        memo[name] = s["fins"] + sum(n * total(c) for c, n in s["children"].items())
    return memo[name]

K = 28 * 0.048 * 0.018  # um^2 per fin
for name in subs:
    print(f"{name:16s} {total(name):5d} fins  {total(name) * K:7.2f} um^2")
