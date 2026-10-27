#!/usr/bin/env python3
from pathlib import Path
from decimal import Decimal, InvalidOperation
import sys

ROOT = Path(__file__).resolve().parent.parent
STIM = ROOT / "stimuli"
OUT = STIM / "timing"
OUT.mkdir(parents=True, exist_ok=True)

BASE_PERIOD = Decimal("10")  # Existing vectors use 10 ns

EXPECTED = {
    "A": (845, "34D"),
    "B": (3600, "E10"),
    "C": (800, "320"),
}

if len(sys.argv) < 2:
    sys.exit("Usage: python3 scripts/make_mac_timing_vec.py PERIOD_NS [A|B|C]")

try:
    period = Decimal(sys.argv[1])
except InvalidOperation:
    sys.exit("Clock period must be a number, e.g. 6, 4, 3.5")

if not period.is_finite() or period <= 0:
    sys.exit("Clock period must be positive and finite")

tests = [x.upper() for x in sys.argv[2:]] or ["A", "B", "C"]

if any(t not in EXPECTED for t in tests):
    sys.exit("Valid tests: A B C")

scale = period / BASE_PERIOD
tag = format(period.normalize(), "f").replace(".", "p")

def fmt(x):
    return format(x.normalize(), "f")

for test in tests:
    source = STIM / f"mac_top_{test}.vec"
    destination = OUT / f"mac_top_{test}_{tag}ns.vec"

    if not source.is_file():
        sys.exit(f"Missing original vector: {source}")

    output = []
    event_count = 0
    last_time = Decimal("0")
    previous_time = None

    for line in source.read_text().splitlines():
        fields = line.split()

        if not fields or line.lstrip().startswith(";"):
            output.append(line)
            continue

        try:
            time = Decimal(fields[0])
        except InvalidOperation:
            # Preserve vector headers, voltage levels,
            # radix, names, and transition settings.
            output.append(line)
            continue

        if len(fields) != 8:
            sys.exit(f"Unexpected vector row in {source}:\n{line}")

        if previous_time is not None and time < previous_time:
            sys.exit(f"Out-of-order event in {source}:\n{line}")

        previous_time = time
        new_time = time * scale

        # Scale ONLY the timestamp.
        # All 7 digital signal values remain identical.
        output.append(
            f"{fmt(new_time)} {' '.join(fields[1:])}"
        )

        event_count += 1
        last_time = new_time

    destination.write_text("\n".join(output) + "\n")

    expected_dec, expected_hex = EXPECTED[test]
    stop_time = last_time + 2 * period

    print(f"\nTEST {test} | CLOCK = {fmt(period)} ns")
    print(f"File: {destination}")
    print(f"Events: {event_count}")
    print(f"Expected ACC: {expected_dec} = 0x{expected_hex}")
    print(f"Suggested tran stop: {fmt(stop_time)}n")

print("\nDONE. Original vectors were NOT modified.")
