"""Coverage oracle for the SMO lift: list every site the lifter must treat specially and check it treats all of them.

Categories, found by scanning each module's .text (every word, not only discovered functions):
  svc        SVC #imm (Horizon system calls)
  mrs/msr    system register reads and writes, by register name (tpidrro_el0, tpidr_el0, cntpct_el0, cntfrq_el0, ...)
  excl       exclusive loads/stores and pairs (LDXR/LDAXR/STXR/STLXR/LDXP/LDAXP/STXP/STLXP)
  x18        any instruction that names x18/w18 (the platform register Horizon reserves)
  jumptable  jump tables the generator resolved, from generated/<ver>/<mod>/manifest.json

A site counts as handled when the lifter accepts its word and does not turn it into an undefined-instruction trap.
The report goes to stdout and to build/<ver>/scan_sites.json; the exit code is 1 if any site is not handled.

Usage: smo_scan_sites.py [--exefs build/extracted/smo-v141/exefs] [--gen generated/smo-v141]   (runs under .venv)
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import capstone
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'recomp'))
from layout import read as read_layout  # noqa: E402
from lifter import Lifter, Unsupported  # noqa: E402
from nso import Nso  # noqa: E402

MODULES = ('main', 'sdk', 'subsdk0')


def categories(w, text):
    """Category names of one instruction word (text: its disassembly)."""
    out = []
    if (w & 0xFFE0001F) == 0xD4000001:
        out.append('svc')
    if (w & 0xFFF00000) == 0xD5300000:
        out.append('mrs ' + text.split(',')[-1].strip())
    if (w & 0xFFF00000) == 0xD5100000:
        out.append('msr ' + text.split()[1].rstrip(','))
    if (w & 0x3F000000) == 0x08000000 and not (w >> 23) & 1:
        out.append('excl ' + text.split()[0])
    if 'x18' in text or 'w18' in text:
        out.append('x18 ' + text.split()[0])
    return out


def scan(name, nso, base, md):
    lo, size = nso.text
    words = np.frombuffer(bytes(nso.image[lo:lo + size]), dtype='<u4')
    uniq, first, counts = np.unique(words, return_index=True, return_counts=True)
    lifter = Lifter(base, 'c')
    sites = defaultdict(lambda: [0, 0, 0, Counter()])   # category -> [occurrences, distinct, unhandled occurrences, lowering]
    for w, i, n in zip(uniq.tolist(), first.tolist(), counts.tolist()):
        insn = next(md.disasm(w.to_bytes(4, 'little'), base + lo + i * 4), None)
        if insn is None:
            continue
        cats = categories(w, f'{insn.mnemonic} {insn.op_str}')
        if not cats:
            continue
        try:
            ins = lifter.lift(w, base + lo + i * 4)
            handled = not (ins.kind == 'trap' and ins.code.startswith('rt_udf'))
            lowering = ins.code.split('(')[0].strip()[:40] if ins.code else ins.kind
        except Unsupported:
            handled, lowering = False, 'Unsupported'
        for cat in cats:
            e = sites[cat]
            e[0] += n
            e[1] += 1
            e[2] += 0 if handled else n
            e[3][lowering if cat.startswith(('svc', 'mrs', 'msr')) else ins_kind(handled)] += n
    return sites


def ins_kind(handled):
    return 'handled' if handled else 'unhandled'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--exefs', type=Path, default=ROOT / 'build' / 'extracted' / 'smo-v141' / 'exefs')
    ap.add_argument('--gen', type=Path, default=ROOT / 'generated' / 'smo-v141')
    ap.add_argument('--out', type=Path, default=ROOT / 'build' / 'smo-v141' / 'scan_sites.json')
    args = ap.parse_args()
    bases = {n: b for n, b, _ in read_layout(args.gen)}
    md = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
    report, bad = {}, 0
    for name in MODULES:
        sites = scan(name, Nso(str(args.exefs / name)), bases[name], md)
        manifest = json.loads((args.gen / name / 'manifest.json').read_text())
        st = manifest['stats']
        report[name] = {cat: {'occurrences': e[0], 'distinct': e[1], 'unhandled': e[2], 'lowering': dict(e[3])}
                        for cat, e in sorted(sites.items())}
        report[name]['jumptable'] = {'tables': st['jump_tables'], 'targets': st['jump_table_targets'],
                                     'all_label_fallbacks': st['all_label_fallbacks'], 'br_dispatch': st['br_dispatch'],
                                     'unsupported': st['unsupported']}
        print(f'== {name}')
        groups = defaultdict(lambda: [0, 0])
        for cat, e in sites.items():
            g = groups[cat.split()[0]]
            g[0] += e[0]
            g[1] += e[2]
        for g, (n, u) in sorted(groups.items()):
            print(f'  {g:6} {n:8} sites, {u} unhandled')
        for cat, e in sorted(sites.items()):
            if cat.startswith(('mrs', 'msr', 'svc')) or e[2]:
                print(f'    {cat:28} {e[0]:7}  {", ".join(f"{k} {v}" for k, v in e[3].most_common(3))}')
        print(f'  jump tables {st["jump_tables"]} ({st["jump_table_targets"]} targets), all-label fallbacks '
              f'{st["all_label_fallbacks"]}, br via dispatch {st["br_dispatch"]}, unsupported {st["unsupported"]}')
        bad += sum(e[2] for e in sites.values()) + st['unsupported']
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1) + '\n')
    print(f'coverage: {"100%" if not bad else f"{bad} unhandled sites"}; report {args.out.relative_to(ROOT)}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
