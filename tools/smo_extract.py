"""Extract Super Mario Odyssey (base 1.0.0 + one update) into build/extracted/ and verify it against known hashes.

The TotK extractor (tools/extract.py and the vendored MacNativeGames scripts) does the work; this script swaps in a
Program NCA picker that accepts SMO's title IDs (tools/smo_profile.py) and lists every code module the ExeFS holds.

Steps, each skipped when its verified output already exists:

1. ExeFS of the base game (1.0.0, kept for matching OdysseyDecomp's 1.0.0 addresses) -> extracted/smo-v0/exefs.
2. ExeFS of the update -> extracted/smo-v<ver>/exefs.
3. Update RomFS: hactool merges the base Program NCA with the update's BKTR section -> extracted/smo-v<ver>/romfs.
   The base RomFS on its own is not extracted: the merged image replaces it.

The first run writes tools/data/smo-expected-v<ver>.json (hashes and sizes only); later runs must match it.
Runs under .venv-py314. Key values are read by the tools from the keys file and never printed.

Usage: smo_extract.py [--config config.local.toml] [--version X.Y.Z]   (version: read from the update NACP)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402  (puts tools/vendor/macnativegames on sys.path)
import extract_exefs  # noqa: E402
import extract_romfs  # noqa: E402
import smo_profile as profile  # noqa: E402
from extract_exefs import common_tickets, container_entries, load_keys, nca_inventory, record_offset, require  # noqa: E402
from extract_update_romfs import copy_range, hactool_prod_keys  # noqa: E402

say = extract.say


def program_nca(records, update=False):
    """extract_exefs.program_nca with SMO's title IDs: (record, header) of the one Program NCA of a base or update."""
    programs = [(r, h) for r, h in records if r['content_type'] == 0]
    require(len(programs) == 1, 'Expected one Program NCA; combined packages are unsupported')
    record, hdr = programs[0]
    bktr = any(hdr[0x400 + i * 512 + 4] == 4 for i in range(4))
    metadata = [r for r, _ in records if r['content_type'] == 1]
    if update:
        require(record['title_id'] == profile.BASE_TITLE, f'Update belongs to another game, not {profile.NAME}')
        require(bktr, 'Expected a BKTR update, not a base game')
        require(all(r['title_id'] in (profile.BASE_TITLE, profile.UPDATE_TITLE) for r, _ in records),
                'Mixed-title update package')
    else:
        require(record['title_id'] == profile.BASE_TITLE and not bktr,
                f'Expected the {profile.NAME} base game; updates, DLC and other games are unsupported')
        require(len(metadata) <= 1 and all(r['title_id'] == profile.BASE_TITLE for r in metadata),
                'Expected base game metadata; updates, DLC and combined packages are unsupported')
    return record, hdr


# Every module that imports program_nca by name gets the SMO picker.
for module in (extract_exefs, extract_romfs, extract):
    module.program_nca = program_nca


def code_hashes(exefs):
    """{name: sha256} of every file in an ExeFS (code modules and main.npdm)."""
    return {p.name: extract.sha256(p) for p in sorted(exefs.iterdir()) if p.is_file()}


def extract_exefs_to(game, keys, out, logs, update):
    """Run the vendored ExeFS extractor in a child process (it exits on errors) with the SMO picker."""
    exefs = out / 'exefs'
    if exefs.exists():
        shutil.rmtree(exefs)
    out.mkdir(parents=True, exist_ok=True)
    stub = ('import sys; sys.path.insert(0, sys.argv.pop(1)); import smo_extract, extract_exefs; '
            'sys.argv = sys.argv[1:]; extract_exefs.main()')
    log = logs / f'extract_exefs-{out.name}.log'
    command = [sys.executable, '-c', stub, str(Path(__file__).resolve().parent), 'extract_exefs',
               str(game), '--keys', str(keys), '--output', str(exefs)] + (['--update'] if update else [])
    with log.open('wb') as f:
        code = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT).returncode
    require(code == 0, f'ExeFS extraction of {game.name} failed; see {extract.shown(log)}')
    return exefs


def display_version(nsp, keys_path, hactool, scratch):
    """The display version (e.g. '1.3.0') in the control NACP of an NSP. The file name is not trusted: an update named
    1.4.1 turned out to be 1.3.0."""
    keys = load_keys(keys_path)
    with nsp.open('rb') as f:
        _, entries = container_entries(f, nsp.stat().st_size)
        tickets = common_tickets(f, entries)
        controls = [r for r, _ in nca_inventory(f, entries, keys) if r['content_type'] == 2]
    require(len(controls) == 1, f'Expected one Control NCA in {nsp.name}')
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='nacp-', dir=scratch) as tmp:
        tmp = Path(tmp)
        title_keys = tmp / 'title.keys'
        fd = os.open(title_keys, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f:
            f.writelines(f'{rights.hex()} = {key.hex()}\n' for rights, key in tickets.items())
        hactool_keys = tmp / 'hactool.keys'
        hactool_prod_keys(keys_path, hactool_keys)
        nca = tmp / 'control.nca'
        copy_range(nsp, record_offset(controls[0]), controls[0]['size'], nca)
        subprocess.run([str(hactool), '-x', '-y', '--disablekeywarns', '--suppresskeys', '-k', str(hactool_keys),
                        f'--romfsdir={tmp / "romfs"}', str(nca)], env=dict(os.environ, MNG_TITLE_KEYS=str(title_keys)),
                       capture_output=True)
        nacp = tmp / 'romfs' / 'control.nacp'
        require(nacp.is_file(), f'Could not read the control NACP of {nsp.name}')
        return nacp.read_bytes()[0x3060:0x3070].rstrip(b'\0').decode('ascii')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--config', type=Path, default=profile.ROOT / 'config.local.toml')
    parser.add_argument('--version', help='display version of the update (default: read from its control NACP)')
    parser.add_argument('--hactool', type=Path, default=profile.ROOT / 'toolchain' / 'hactool' / 'hactool')
    args = parser.parse_args()

    config = tomllib.loads(args.config.read_text(encoding='utf-8'))
    given = config['input']
    base, keys = Path(given['base']), Path(given['keys'])
    updates = given.get('updates', [])
    require(len(updates) == 1, 'Name exactly one update in input.updates')
    update = Path(updates[0])
    work = profile.ROOT / config.get('work', {}).get('dir', 'build')
    extracted, logs = work / 'extracted', work / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    args.version = args.version or display_version(update, keys, args.hactool, work / 'tmp')
    say(f'Update {update.name}: version {args.version} (control NACP)')

    expected_file = profile.expected_path(args.version)
    expected = json.loads(expected_file.read_text()) if expected_file.is_file() else None
    record = {'game': profile.NAME, 'base_title': profile.BASE_TITLE, 'update_title': profile.UPDATE_TITLE,
              'display_version': args.version}

    say('Base game (1.0.0)')
    base_out = extracted / profile.version_dir('1.0.0')
    if not expected or not (base_out / 'exefs').is_dir() or code_hashes(base_out / 'exefs') != expected['base_exefs_sha256']:
        say('  extracting ExeFS')
        extract_exefs_to(base, keys, base_out, logs, update=False)
    record['base_exefs_sha256'] = code_hashes(base_out / 'exefs')
    say(f'  ExeFS: {", ".join(record["base_exefs_sha256"])}')

    say(f'Update {args.version}')
    out = extracted / profile.version_dir(args.version)
    if not expected or not (out / 'exefs').is_dir() or code_hashes(out / 'exefs') != expected['exefs_sha256']:
        say('  extracting ExeFS')
        extract_exefs_to(update, keys, out, logs, update=True)
    record['exefs_sha256'] = code_hashes(out / 'exefs')
    say(f'  ExeFS: {", ".join(record["exefs_sha256"])}')

    romfs = out / 'romfs'
    if not (expected and extract.romfs_verified(romfs, {'romfs': expected['romfs']})):
        say('  merging RomFS with the update')
        extract.merge_update_romfs(base, update, keys, args.hactool, romfs, logs)
    report = json.loads((romfs / 'index.json').read_text())
    record['romfs'] = {'size': report['romfs_size'], 'sha256': report['romfs_sha256'], 'files': len(report['files'])}
    say(f'  RomFS: {report["romfs_size"]:,} bytes, {len(report["files"]):,} files')

    if expected:
        for key in ('base_exefs_sha256', 'exefs_sha256', 'romfs'):
            require(record[key] == expected[key], f'{key} does not match {expected_file.name}')
        say(f'All hashes match {expected_file.name}')
    else:
        expected_file.write_text(json.dumps(record, indent=2) + '\n')
        say(f'Wrote {extract.shown(expected_file)} (first run: these hashes are the reference from now on)')


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        sys.exit(f'error: {error}')
