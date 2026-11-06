"""Fetch Cisco's prebuilt OpenH264 decoder for Windows: build/<ver>/openh264.dll.

The source (runtime/ov_movie.c) is BSD-2-Clause and links nothing of OpenH264 in; H.264 decoding only runs when this
.dll sits next to the exe and loads at run time (plat_lib_open), same design Firefox and Chromium use. Cisco's build
is free to redistribute and run (they cover the H.264 patent royalties for that exact binary; see
https://www.openh264.org/BINARY_LICENSE.txt), so this script downloads it from Cisco's own binary server instead of
compiling it from source or vendoring it in the repo.

Without it, SMO's MP4 cutscenes fall through to the library's own decoder path, which tries to open the Switch's
NVDEC hardware block and aborts (runtime/ov_movie.c h264_available comment).

  .venv\\Scripts\\python tools\\fetch_openh264.py [--version 2.4.1] [--out build\\smo-v141]
"""

import argparse
import bz2
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = '2.4.1'
URL = 'http://ciscobinary.openh264.org/openh264-{v}-win64.dll.bz2'


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--version', default=VERSION)
    p.add_argument('--out', type=Path, default=ROOT / 'build' / 'smo-v141')
    a = p.parse_args()

    url = URL.format(v=a.version)
    print(f'downloading {url}')
    with urllib.request.urlopen(url) as r:
        compressed = r.read()
    print(f'sha256 of the downloaded .bz2: {hashlib.sha256(compressed).hexdigest()}'
          ' (not checked against a pin; verify against https://github.com/cisco/openh264/releases if that matters to you)')

    data = bz2.decompress(compressed)
    a.out.mkdir(parents=True, exist_ok=True)
    target = a.out / 'openh264.dll'
    target.write_bytes(data)
    print(f'{target}: {len(data)} bytes (openh264-{a.version}-win64.dll)')


if __name__ == '__main__':
    main()
