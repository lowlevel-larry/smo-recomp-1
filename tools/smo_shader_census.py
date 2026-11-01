"""Census of every Maxwell shader in the extracted SMO RomFS and ExeFS, and an offline translation pass.

The SMO counterpart of tools/shader_census.py, whose parsers it reuses (SARC, BNSH, agl .sharcb, NSO images, job
files, the translation pass). The difference is the containers: SMO packs its RomFS files as Yaz0 (.szs) SARC
archives, decoded here with oead, where TotK uses zstd with dictionaries.

Reads build/extracted/<version>/ and writes build/<version>/shaders/ (code/, jobs.json, spv/, failures.txt), as
shader_census.py does. A shader is a startup shader when it comes from ShaderData/ (agl packages), SystemData/ or a
game module; the others (effects, layouts, models) are translated when met in play, or all with --all.

Runs under .venv (oead):  .venv/bin/python tools/smo_shader_census.py --version smo-v141 [--all] [--translate]
"""
import argparse
import json
import struct
import sys
import time
import types
from pathlib import Path

import oead

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
# shader_census imports compression.zstd (Python 3.14) at module level for TotK's packages; SMO has no zstd data, so a
# placeholder lets .venv (3.12, with oead) import its parsers.
if 'compression.zstd' not in sys.modules:
    try:
        import compression.zstd  # noqa: F401
    except ImportError:
        sys.modules['compression'] = types.ModuleType('compression')
        sys.modules['compression.zstd'] = types.ModuleType('compression.zstd')
import shader_census as sc  # noqa: E402

# RomFS directories whose shaders the game needs from the first frame on.
STARTUP_DIRS = ('ShaderData/', 'SystemData/')
# Directories that can hold shaders at all (agl packages, effects, layouts, system data, model archives).
SHADER_DIRS = STARTUP_DIRS + ('EffectData/', 'LayoutData/', 'ObjectData/', 'StageData/')
MAX_SIZE = 512 << 20


def yaz0(raw):
    if raw[:4] != b'Yaz0':
        return raw
    if struct.unpack_from('>I', raw, 4)[0] > MAX_SIZE:
        raise ValueError('unbounded Yaz0 file')
    return bytes(oead.yaz0.decompress(raw))


def inventory(romfs, exefs, everything):
    index = json.loads((romfs / 'index.json').read_text(encoding='utf-8'))
    if index.get('status') != 'pass':
        raise ValueError('RomFS has not passed integrity verification')
    shaders, rejected = {}, [0]

    def add(origin, name, found, startup):
        for key, stage, control, code in found:
            s = shaders.setdefault(key, dict(stage=stage, control=control, code=code, source=name, origin=origin,
                                             startup=startup))
            if startup and not s['startup']:
                s.update(source=name, origin=origin, startup=True)

    def visit(origin, name, data, startup, depth=0):
        if data[:4] == b'BAHS':
            add('sharcb', name, sc.sharcb_shaders(data, rejected), True)
            return
        if data[:4] == b'SARC':
            if depth > 4:
                return
            for member, raw in sc.sarc(data).items():
                visit(origin, name + '/' + member, yaz0(raw), startup, depth + 1)
            return
        pos = 0   # BFSHA, BNSH and resource files that embed complete BNSH files
        while (pos := data.find(b'BNSH\0\0\0\0', pos)) >= 0:
            size = struct.unpack_from('<I', sc.checked(data, pos + 28, 4))[0]
            add(origin, name, sc.bnsh_shaders(sc.checked(data, pos, size)), startup)
            pos += max(size, 8)

    dirs = SHADER_DIRS if everything else STARTUP_DIRS
    with (romfs / 'romfs.bin').open('rb') as stream:
        for row in sorted(index['files'], key=lambda r: r['path']):
            name = row['path']
            if not name.startswith(dirs):
                continue
            stream.seek(row['offset'])
            raw = stream.read(row['size'])
            if len(raw) != row['size']:
                raise ValueError('short RomFS read')
            data = yaz0(raw)
            if data[:4] in (b'SARC', b'FSHA', b'BNSH', b'BAHS') or b'BNSH\0\0\0\0' in data:
                visit('bnsh', name, data, name.startswith(STARTUP_DIRS))
    for module in sorted(exefs.iterdir()):
        if module.name in ('main', 'sdk', 'subsdk0', 'rtld'):
            visit('main', 'module:' + module.name, sc.nso_image(module), True)
    return shaders, rejected[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', default='smo-v141', help='build/extracted/<version> (default smo-v141)')
    ap.add_argument('--all', action='store_true', help='also effect, layout and model shaders')
    ap.add_argument('--translate', action='store_true', help='translate every shader and run spirv-val')
    args = ap.parse_args()
    extracted = ROOT / 'build' / 'extracted' / args.version
    out = ROOT / 'build' / args.version / 'shaders'
    t0 = time.perf_counter()
    shaders, rejected = inventory(extracted / 'romfs', extracted / 'exefs', args.all)
    jobs = sc.write_shaders(shaders, out, args.all)
    stages = {s: sum(1 for j in jobs.values() if j['job']['stage'] == s) for s in ('vs', 'ps', 'cs')}
    origins = {o: sum(1 for j in jobs.values() if j['origin'] == o) for o in ('sharcb', 'bnsh', 'main')}
    print(f'{len(shaders)} shaders found ({len(jobs)} written: {stages}; by origin {origins}; '
          f'{rejected} sharcb candidates without control magic) in {time.perf_counter() - t0:.1f} s')
    if args.translate:
        if not sc.XLATE.is_file():
            sys.exit(f'{sc.XLATE} not found: run tools/build_xlate.py')
        t0 = time.perf_counter()
        ok, failed, invalid = sc.translate(jobs, out)
        print(f'translated {ok} of {len(jobs)}: {failed} translator failures, {invalid} spirv-val errors '
              f'({time.perf_counter() - t0:.1f} s)' + (f'; see {out / "failures.txt"}' if failed or invalid else ''))


if __name__ == '__main__':
    main()
