"""Report what identifies an extracted SMO version: module sizes and build IDs, SDK and NVN versions, the audio
renderer revisions the code knows, relocation formats and the RomFS file formats. Prints facts only (no game bytes
beyond short version strings), for docs/smo-target.md.

Usage: smo_target_info.py [build/extracted/smo-v141]   (runs under .venv)
"""
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'recomp'))
from nso import DT_RELA, DT_RELR, Nso  # noqa: E402

MODULES = ('main', 'sdk', 'subsdk0', 'rtld')


def strings(image, pattern):
    return sorted({m.group().decode('ascii', 'replace') for m in re.finditer(pattern, bytes(image))})


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'build' / 'extracted' / 'smo-v141'
    exefs = out / 'exefs'
    nsos = {}
    for name in MODULES:
        nso = Nso(exefs / name)
        nsos[name] = nso
        relocs = '+'.join(t for t, k in (('RELA', DT_RELA), ('RELR', DT_RELR)) if k in nso.dyn) or 'none'
        print(f'{name}: file {(exefs / name).stat().st_size:,} B, image 0x{nso.size:x}, build {nso.build_id[:32]}, '
              f'text 0x{nso.text[1]:x}, relocs {relocs} ({len(nso.relocs)}), '
              f'imports {len(nso.imports())}, exports {len(nso.exports())}')
    for name, nso in nsos.items():
        sdk = strings(nso.image, rb'(?:NintendoSdk_nnSdk|SDK MW\+[A-Za-z]+\+[A-Za-z_]+)-[0-9][0-9_.A-Za-z-]*')
        if sdk:
            print(f'{name} SDK: {", ".join(sdk)}')
    for name, nso in nsos.items():
        nvn = strings(nso.image, rb'NVIDIA(?:_SDK)?[A-Za-z_]*-[0-9][0-9_.A-Za-z-]*|nvn[A-Za-z]*Version[A-Za-z]*')
        if nvn:
            print(f'{name} NVN strings: {", ".join(nvn[:12])}')
    procs = set()
    for nso in nsos.values():
        procs.update(strings(nso.image, rb'nvn[A-Z][A-Za-z0-9]+'))
    print(f'nvn proc names referenced: {len(procs)}')
    for name, nso in nsos.items():
        revs = strings(nso.image, rb'REV[0-9]{1,2}(?![0-9])')
        if revs:
            print(f'{name} audren revision tags: {", ".join(revs)}')
    for name, nso in nsos.items():
        libs = strings(nso.image, rb'SDK MW\+[^\0]{3,60}')
        print(f'{name} middleware: {len(libs)} entries' + (f' (e.g. {", ".join(libs[:6])})' if libs else ''))
    index = out / 'romfs' / 'index.json'
    if index.is_file():
        import json
        files = json.loads(index.read_text())['files']
        ext = collections.Counter(Path(f['path']).suffix.lower() or '(none)' for f in files)
        print('RomFS extensions: ' + ', '.join(f'{e} {n}' for e, n in ext.most_common(20)))
        tops = collections.Counter(f['path'].split('/')[0] for f in files)
        print('RomFS top dirs: ' + ', '.join(f'{d} {n}' for d, n in tops.most_common(20)))


if __name__ == '__main__':
    main()
