#!/usr/bin/env python3
"""Build ordinary KPackage/KNewStuff archives without installer scripts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile

VERSION = '1.1.0'
ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--wallpaper-id', type=int)
    parser.add_argument('--style-id', type=int)
    parser.add_argument('--global-only', action='store_true', help='Keep already published component archives unchanged')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='srcery-native-') as temp:
        stage = Path(temp)
        packages = [
            ('SRCERY-Plasma-Style', 'share/plasma/desktoptheme/Srcery', 'Srcery'),
            ('SRCERY-Wallpaper', 'share/wallpapers/Srcery', 'Srcery'),
        ]
        if args.wallpaper_id and args.style_id:
            packages.append(('SRCERY-Global', 'share/plasma/look-and-feel/org.srcery.desktop', 'org.srcery.desktop'))
        if args.global_only:
            if not args.wallpaper_id or not args.style_id:
                parser.error('--global-only requires both Store ids')
            packages = [package for package in packages if package[0] == 'SRCERY-Global']
        hashes = []
        for name, source, folder in packages:
            target = stage / name / folder
            shutil.copytree(ROOT / source, target)
            metadata = target / 'metadata.json'
            data = json.loads(metadata.read_text())
            data['KPlugin']['Version'] = VERSION
            data['KPlugin']['Website'] = 'https://github.com/PROSHANTI/srcery-plasma'
            if name == 'SRCERY-Global':
                data['KPlugin']['Description'] = 'Srcery colors, Breeze-based Plasma style, logo splash and grey wallpaper. Iosevka is an optional separate font installation.'
                data['X-KPackage-Dependencies'] = [
                    f'kns://plasma-themes.knsrc/api.kde-look.org/{args.style_id}',
                    f'kns://wallpaper.knsrc/api.kde-look.org/{args.wallpaper_id}',
                ]
                defaults = target / 'contents/defaults'
                # Plasma 6.7 checks WM/font to detect font contents, but applies
                # General/font. Keep both so the Fonts checkbox is available.
                defaults.write_text(defaults.read_text().replace(
                    '[kdeglobals][WM]\n',
                    '[kdeglobals][WM]\nfont=Iosevka,12,-1,5,50,0,0,0,0,0\n'))
            if name == 'SRCERY-Plasma-Style':
                data['KPackageStructure'] = 'Plasma/Theme'
                (target / 'metadata.desktop').unlink()
            metadata.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            shutil.copytree(ROOT / 'LICENSES', target / 'LICENSES')
            shutil.copy2(ROOT / 'NOTICE', target / 'NOTICE')
            archive = args.output / f'{name}-{VERSION}.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                tar.add(target, arcname=folder)
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            hashes.append(f'{digest}  {archive.name}')
            print(archive.name, archive.stat().st_size, digest)
        all_archives = sorted(args.output.glob(f'SRCERY-*-{VERSION}.tar.gz'))
        hashes = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}' for p in all_archives]
        (args.output / 'SHA256SUMS-native.txt').write_text('\n'.join(hashes) + '\n')

if __name__ == '__main__':
    main()
