"""Super Mario Odyssey game profile: title IDs, code modules and file names shared by the smo_* tools.

The TotK tools keep their constants; SMO tools import these instead, so upstream files stay untouched.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAME = 'Super Mario Odyssey'
BASE_TITLE = '0100000000010000'
UPDATE_TITLE = '0100000000010800'
# Code modules recompiled; rtld is extracted and hashed but not lifted.
EXEFS_CODE = ('main', 'sdk', 'subsdk0', 'rtld')
DATA = ROOT / 'tools' / 'data'
EXPECTED_GLOB = 'smo-expected-v*.json'


def expected_path(display_version):
    return DATA / f'smo-expected-v{display_version}.json'


def version_dir(display_version):
    """build/extracted/<dir> of a version: smo-v0 for 1.0.0, smo-v141 for 1.4.1."""
    return 'smo-v0' if display_version == '1.0.0' else 'smo-v' + display_version.replace('.', '')
