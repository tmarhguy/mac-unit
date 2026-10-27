from pathlib import Path
import shutil, sys

VDD, RISE, END = 0.8, 0.02, 270.0
ROOT = Path.home() / 'mac_part3_stimuli'

TESTS = {
    'A': ([3,12,7,0,15,9,1,14,6,11,2,13,8,5,10,4],
          [9,2,15,7,4,12,0,11,13,1,8,6,3,14,5,10], 845),
    'B': ([15]*16, [15]*16, 3600),
    'C': ([5,10]*8, [10,5]*8, 800),
}

selected = sys.argv[1].upper() if len(sys.argv)>1 else 'B'
if selected not in TESTS:
    sys.exit('Usage: python3 scripts/make_mac_pwl.py A|B|C')

def write_pwl(file, changes, initial=0.0):
    file.parent.mkdir(parents=True, exist_ok=True)
    rows, previous = [(0.0, initial)], initial
    for t, new in sorted(changes):
        if new == previous:
            continue
        rows.extend([(t, previous), (t+RISE, new)])
        previous = new
    rows.append((END, previous))
    file.write_text(''.join(
        f'{t*1e-9:.12e} {v:.6f}\n' for t,v in rows
    ))

def high(bit):
    return VDD if bit else 0.0

common = ROOT / 'common'

write_pwl(common/'RST.pwl', [(4.5,0.0)], initial=VDD)
write_pwl(common/'START.pwl', [(164.5,VDD),(169.5,0.0)])
write_pwl(common/'WE_W.pwl', [(4.5,VDD),(84.5,0.0)])
write_pwl(common/'WE_X.pwl', [(84.5,VDD),(164.5,0.0)])

for bit in range(4):
    transitions = []
    for i in range(16):
        transitions += [
            (4.5+5*i, high((i>>bit)&1)),
            (84.5+5*i, high((i>>bit)&1))
        ]
    write_pwl(common/f'ADDR{bit}.pwl',
              transitions+[(164.5,0.0)])

for test, (weights, activations, expected) in TESTS.items():
    assert sum(w*x for w,x in zip(weights,activations)) == expected
    folder = ROOT/f'test_{test}'
    for bit in range(4):
        transitions = []
        for i in range(16):
            transitions.append(
                (4.5+5*i, high((weights[i]>>bit)&1))
            )
            transitions.append(
                (84.5+5*i, high((activations[i]>>bit)&1))
            )
        write_pwl(folder/f'DIN{bit}.pwl',
                  transitions+[(164.5,0.0)])

active = ROOT/'active'
active.mkdir(parents=True, exist_ok=True)

for bit in range(4):
    shutil.copyfile(
        ROOT/f'test_{selected}'/f'DIN{bit}.pwl',
        active/f'DIN{bit}.pwl'
    )

print('ACTIVE TEST:', selected)
print('EXPECTED ACC:', TESTS[selected][2])
print('PWL directory:', ROOT)

for sig in ['RST','START','WE_W','WE_X']:
    print(sig, common/f'{sig}.pwl')

for bit in range(4):
    print(f'ADDR<{bit}>', common/f'ADDR{bit}.pwl')
    print(f'DIN<{bit}>', active/f'DIN{bit}.pwl')
