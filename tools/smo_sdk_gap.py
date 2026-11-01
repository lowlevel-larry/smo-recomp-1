"""SDK gap inventory: the nn:: functions SMO's modules import against the runtime's HOST_OVERRIDE symbols.

For each mangled symbol a module imports (main and subsdk0 import from sdk), reports whether a HOST_OVERRIDE names it
exactly ('has'), whether an override names a symbol with the same nn:: qualified name but another signature
('signature differs': the SDK 7 and SDK 20 manglings disagree, a candidate for adapting that override), or neither
('missing': the game's own sdk code runs, which is the default and often fine). Also lists the overrides no SMO
module references.

Writes docs/smo-sdk-gap.md (symbol names only). Usage: smo_sdk_gap.py   (runs under .venv)
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'recomp'))
from nso import Nso  # noqa: E402

EXEFS = ROOT / 'build' / 'extracted' / 'smo-v141' / 'exefs'
OVERRIDE = re.compile(r'HOST_OVERRIDE\(\s*"([^"]+)"\s*,\s*(\w+)\s*\)')


def demangle(names):
    out = subprocess.run(['c++filt'], input='\n'.join(names), capture_output=True, text=True).stdout.splitlines()
    return dict(zip(names, out))


def qualified(demangled):
    """'nn::oe::Initialize' from 'nn::oe::Initialize()': the name without its parameter list."""
    depth, cut = 0, len(demangled)
    for i, ch in enumerate(demangled):
        if ch == '(' and depth == 0:
            cut = i
            break
        depth += ch == '<'
        depth -= ch == '>'
    return demangled[:cut]


def main():
    overrides = {}
    for path in sorted((ROOT / 'runtime').rglob('*.c*')):
        for sym, fn in OVERRIDE.findall(path.read_text(encoding='utf-8', errors='replace')):
            overrides[sym] = (fn, path.relative_to(ROOT).as_posix())
    imports = defaultdict(set)
    for name in ('main', 'subsdk0', 'sdk'):
        for sym, *_ in Nso(EXEFS / name).imports():
            imports[sym].add(name)
    exported = set()
    for name in ('main', 'subsdk0', 'sdk'):
        exported |= {s for s, *_ in Nso(EXEFS / name).exports()}
    referenced = set(imports) | exported
    dm = demangle(sorted(set(imports) | set(overrides)))
    by_name = defaultdict(list)
    for sym in overrides:
        by_name[qualified(dm[sym])].append(sym)

    rows = {'has': [], 'signature differs': [], 'missing': []}
    for sym in sorted(imports, key=lambda s: dm[s]):
        if not sym.startswith('_ZN2nn') and not sym.startswith('nn'):
            continue
        if sym in overrides:
            rows['has'].append((sym, overrides[sym]))
        elif by_name.get(qualified(dm[sym])):
            rows['signature differs'].append((sym, overrides[by_name[qualified(dm[sym])][0]]))
        else:
            rows['missing'].append((sym, None))
    unused = sorted((s for s in overrides if s not in referenced), key=lambda s: dm[s])
    other = sorted(s for s in imports if not s.startswith('_ZN2nn'))

    by_ns = defaultdict(lambda: [0, 0, 0])
    for i, key in enumerate(rows):
        for sym, _ in rows[key]:
            ns = '::'.join(qualified(dm[sym]).split('::')[:2])
            by_ns[ns][i] += 1

    lines = ['# Inventário nn:: do SMO 1.4.1 (SDK 7.3.2) vs HOST_OVERRIDE do runtime', '',
             'Gerado por `tools/smo_sdk_gap.py`. "tem": override com o mesmo símbolo; "assinatura difere": override para '
             'o mesmo nome qualificado com outra assinatura (SDK 20 do TotK), candidato a adaptar; "falta": nenhum '
             'override, roda o código do próprio `sdk` do jogo (o padrão; só vira trabalho se esse código precisar de '
             'serviço do Horizon que o runtime não emula).', '',
             f'- Imports nn:: dos módulos: {sum(len(v) for v in rows.values())} '
             f'(tem {len(rows["has"])}, assinatura difere {len(rows["signature differs"])}, falta {len(rows["missing"])})',
             f'- Overrides do runtime: {len(overrides)}; sem referência em nenhum módulo do SMO: {len(unused)}',
             f'- Imports não-nn (libc, NVN, etc.): {len(other)}', '',
             '## Por namespace', '', '| Namespace | tem | assinatura difere | falta |', '|---|---|---|---|']
    for ns, (a, b, c) in sorted(by_ns.items(), key=lambda kv: -sum(kv[1])):
        lines.append(f'| `{ns}` | {a} | {b} | {c} |')
    for key, title in (('has', 'Tem'), ('signature differs', 'Assinatura difere')):
        lines += ['', f'## {title}', '', '| Símbolo | Override |', '|---|---|']
        lines += [f'| `{dm[s]}` | `{fn}` ({path}) |' for s, (fn, path) in rows[key]]
    lines += ['', '## Falta (importados por main/subsdk0, sem override)', '']
    lines += [f'- `{dm[s]}`' for s, _ in rows['missing']]
    lines += ['', '## Overrides sem referência no SMO', '']
    lines += [f'- `{dm[s]}` ({overrides[s][1]})' for s in unused]
    (ROOT / 'docs' / 'smo-sdk-gap.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'has {len(rows["has"])}, signature differs {len(rows["signature differs"])}, missing {len(rows["missing"])}, '
          f'overrides {len(overrides)} ({len(unused)} unreferenced), other imports {len(other)}')


if __name__ == '__main__':
    main()
