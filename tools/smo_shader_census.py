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
# NVN control sections of SDK 7.3.2 are 0x7d1 bytes (TotK's NVN: 0x880 or 0x88c), with c1 and length at +0x700 and the
# stage at +0x714 as in the newer layout. Keys hash them padded with zeros to 0x880, as runtime/gfx_shader.c does.
CONTROL_SIZE = 0x7d1
CONTROL_KEY = 0x880


def sharcb_shaders(data, rejected):
    """shader_census.sharcb_shaders for SDK 7 packages: records <u64 code offset in the pool, u32 control size 0x7d1,
    i32 offset of the control from the record>."""
    if len(data) < 32 or data[:4] != b'BAHS':
        raise ValueError('expected an agl shader package')
    start, pool_size, pool = struct.unpack_from('<3I', data, 20)
    if not 32 <= start <= pool or pool + pool_size > len(data):
        raise ValueError('agl shader package layout outside the file')
    seen = set()
    at = start
    size = struct.pack('<I', CONTROL_SIZE)
    while (at := data.find(size, at, pool)) >= 0:
        record, at = at - 8, at + 4
        if record < start or record % 4:
            continue
        code_off = struct.unpack_from('<Q', data, record)[0]
        control_at = record + struct.unpack_from('<i', data, record + 12)[0]
        if not start <= control_at <= pool - CONTROL_SIZE or code_off >= pool_size:
            continue
        control = data[control_at:control_at + CONTROL_SIZE]
        if control[:4] != sc.CONTROL_MAGIC:
            rejected[0] += 1
            continue
        c1, length = struct.unpack_from('<II', control, 0x700)
        stage = sc.STAGE_IDS.get(struct.unpack_from('<I', control, 0x714)[0])
        if not stage or not 0 < length <= pool_size - code_off or c1 > length:
            continue
        control += bytes(CONTROL_KEY - CONTROL_SIZE)
        code = data[pool + code_off:pool + code_off + length]
        key = sc.digest(control + code)
        if key not in seen:
            seen.add(key)
            yield key, stage, control, code


def bnsh_shaders(data):
    """shader_census.bnsh_shaders for SDK 7 BNSH files (inside the .bfsha material archives): their control sections are
    0x7d1 bytes, which that reader skips as the SDK utility's older layout, so every model material shader
    (ShaderData/alRenderMaterial.bfsha and the other .bfsha) was missing from the inventory and translated in play.
    Keys pad the control with zeros to 0x880, as sharcb_shaders and runtime/gfx_shader.c control_view do."""
    if data[:4] != b'BNSH' or sc.checked(data, 12, 2) != b'\xff\xfe' or sc.checked(data, 96, 4) != b'grsc':
        raise ValueError('unsupported BNSH header')
    data = sc.checked(data, 0, struct.unpack_from('<I', data, 28)[0])
    count, variations = struct.unpack_from('<IQ', data, 124)
    sc.checked(data, variations, count * 64)
    seen = set()
    for i in range(count):
        program = struct.unpack_from('<Q', data, variations + i * 64 + 16)[0]
        sc.checked(data, program, 56)
        for stage, relative in [('vs', 8), ('ps', 40), ('cs', 48)]:
            offset = struct.unpack_from('<Q', data, program + relative)[0]
            if not offset:
                continue
            control_off, code_off, code_size, control_size = struct.unpack_from('<QQII', sc.checked(data, offset + 8, 24))
            if control_size < CONTROL_SIZE:
                continue
            control = sc.checked(data, control_off, CONTROL_SIZE)
            code = sc.checked(data, code_off, code_size)
            if control[:4] != sc.CONTROL_MAGIC:
                raise ValueError('NVN control section without its magic')
            c1, length = struct.unpack_from('<II', control, 0x700)
            actual = struct.unpack_from('<I', control, 0x714)[0]
            if actual != {'vs': 0, 'ps': 1, 'cs': 5}[stage] or not 0 <= c1 <= length <= len(code) or not length:
                raise ValueError('invalid NVN shader bounds or stage')
            control += bytes(CONTROL_KEY - CONTROL_SIZE)
            key = sc.digest(control + code[:length])
            if key not in seen:
                seen.add(key)
                yield key, stage, control, code[:length]


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
            add('sharcb', name, sharcb_shaders(data, rejected), True)
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
            add(origin, name, bnsh_shaders(sc.checked(data, pos, size)), startup)
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
