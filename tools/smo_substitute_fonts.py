"""Development stand-in for the Switch shared fonts: wrap a free TrueType font from this PC as the six nn::pl BFTTF
files, so the game can draw Latin text before the real fonts are extracted from the user's firmware
(tools/extract_fonts.py). Glyph shapes and metrics differ from the console's; this is never shipped.

Each slot gets a different font: the game loads all six into one font engine and selects them by their internal
names, so six copies of one font (one name) leave it without the later ones.

Output: build/substitute-fonts/*.bfttf. Run the game with TOTK_SHARED_FONTS=build/substitute-fonts.
Usage: smo_substitute_fonts.py [--font FILE ...]   (six TrueType/OpenType files, standard font first)
"""
import argparse
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAGIC = 0x7f9a0218
KEY = 0x49621806   # any key works: word 0 is MAGIC ^ key (runtime/ov_system.c ov_bfttf_size)
# Distinct families (Noto: OFL 1.1; Liberation: OFL 1.1), as Arch ships them.
DEFAULT_FONTS = ('/usr/share/fonts/noto/NotoSans-Regular.ttf', '/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
                 '/usr/share/fonts/noto/NotoSerif-Regular.ttf', '/usr/share/fonts/liberation/LiberationSerif-Regular.ttf',
                 '/usr/share/fonts/noto/NotoSansMono-Regular.ttf', '/usr/share/fonts/liberation/LiberationMono-Regular.ttf')
NAMES = ('0-standard', '1-chinese-simplified', '2-chinese-simplified-extension', '3-chinese-traditional', '4-korean',
         '5-nintendo-extension')


def bfttf(font):
    font += bytes(-len(font) % 4)
    words = struct.unpack(f'>{len(font) // 4}I', font)
    head = struct.pack('>II', MAGIC ^ KEY, len(font) ^ KEY)
    return head + struct.pack(f'>{len(words)}I', *(w ^ KEY for w in words))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--font', type=Path, nargs=6, default=[Path(p) for p in DEFAULT_FONTS])
    args = ap.parse_args()
    out = ROOT / 'build' / 'substitute-fonts'
    out.mkdir(parents=True, exist_ok=True)
    for name, font in zip(NAMES, args.font):
        data = font.read_bytes()
        if data[:4] not in (b'\0\1\0\0', b'OTTO'):
            raise SystemExit(f'{font} is not a single TrueType/OpenType font')
        (out / f'{name}.bfttf').write_bytes(bfttf(data))
        print(f'  {name}: {font.name} ({len(data):,} bytes)')
    print(f'{out.relative_to(ROOT)}: 6 stand-in fonts')


if __name__ == '__main__':
    main()
