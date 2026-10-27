from pathlib import Path
import csv

OUT = Path("stimuli")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = """radix 1 1
vname D CLK
io i i

tunit 1ns
trise 0.02
tfall 0.02
vih 0.8
vil 0.0

; time(ns) D CLK
"""

def new_wave():
    events = {}

    def at(t, **changes):
        t = round(float(t), 6)
        events.setdefault(t, {}).update(changes)

    at(0, D=0, CLK=0)
    return events, at

def save(name, events, duration):
    state = {"D": 0, "CLK": 0}
    lines = [HEADER]

    for t in sorted(events):
        state.update(events[t])
        lines.append(
            f'{t:.6f} {state["D"]} {state["CLK"]}\n'
        )

    last_t = max(events)
    if last_t < duration:
        lines.append(
            f'{duration:.6f} {state["D"]} {state["CLK"]}\n'
        )

    (OUT / name).write_text("".join(lines))


# ==================================================
# TEST 1: FUNCTIONAL VERIFICATION + CLOCK-TO-Q
# ==================================================

events, at = new_wave()

for k in range(12):
    edge = 2 + 4*k
    bit = k % 2

    at(edge - 0.8, D=bit)
    at(edge, CLK=1)
    at(edge + 1, CLK=0)

    # D changes between clock edges; Q must hold
    at(edge + 1.5, D=1-bit)
    at(edge + 2, D=bit)

save("dff_function_tcq.vec", events, 50)


# ==================================================
# TESTS 2-5: SETUP AND HOLD TIME SWEEPS
# ==================================================

setup_ps = [
    1000, 500, 250, 150, 100,
    80, 60, 40, 30, 20, 10,
    0, -10, -20, -50
]

hold_ps = [
    0, 10, 20, 30, 40, 50,
    75, 100, 200, 500, 1000
]

trials = []

for mode, offsets in [
    ("setup", setup_ps),
    ("hold", hold_ps)
]:
    for direction in ("rise", "fall"):

        if mode == "setup":
            preload = 0 if direction == "rise" else 1
            before = 1 - preload
        else:
            before = 0 if direction == "rise" else 1
            preload = 1 - before

        events, at = new_wave()

        for k, offset in enumerate(offsets):
            base = 14 * k
            edge = base + 8

            # Establish the previous Q state
            at(base, D=preload, CLK=0)
            at(base + 2, CLK=1)
            at(base + 3, CLK=0)

            if mode == "setup":

                # D transition before target clock edge
                at(edge - offset/1000, D=before)
                at(edge, CLK=1)
                at(edge + 1, CLK=0)
                at(base + 10, D=preload)

                sample = edge + 0.8

            else:

                # D transition after target clock edge
                at(base + 6, D=before)
                at(edge, CLK=1)
                at(edge + offset/1000, D=1-before)
                at(edge + 1.5, CLK=0)

                sample = edge + 1.2

            trials.append([
                mode, direction, offset,
                edge, sample, before
            ])

        save(
            f"dff_{mode}_{direction}.vec",
            events,
            14 * len(offsets)
        )


# ==================================================
# TESTS 6-7: ENERGY PER CLOCK
# ==================================================

for mode in ("idle", "toggle"):
    events, at = new_wave()

    for k in range(24):
        edge = 2 + 4*k

        if mode == "toggle":
            at(edge - 1, D=k % 2)

        at(edge, CLK=1)
        at(edge + 2, CLK=0)

    save(
        f"dff_energy_{mode}.vec",
        events,
        100
    )


# ==================================================
# REFERENCE TABLE FOR SETUP/HOLD TRIALS
# ==================================================

with (OUT / "dff_trials.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "mode",
        "direction",
        "offset_ps",
        "clock_edge_ns",
        "sample_Q_at_ns",
        "expected_Q"
    ])
    writer.writerows(trials)


# ==================================================
# FINISH
# ==================================================

print("\nDFF VECTOR FILES CREATED:\n")

for file in sorted(OUT.glob("dff_*.vec")):
    print(file.resolve())

print("\nSetup/hold trials:", len(trials))
print("VDD = 0.8 V")
print("\nSUCCESS!")
