#!/usr/bin/env python3
"""Build one self-contained Plasma Global Theme; no external KNS packages."""
import argparse
import gzip
import hashlib
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parent
VERSION = '1.2.0'
PACKAGE = ROOT / 'theme'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / f'SRCERY-Plasma-{VERSION}.tar.gz'
    with archive.open('wb') as dest, gzip.GzipFile(fileobj=dest, mode='wb', filename='', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            for path in sorted(PACKAGE.rglob('*')):
                if path.is_symlink():raise ValueError(f'Symlink in package: {path}')
                info = tar.gettarinfo(str(path), 'org.srcery.desktop/' + path.relative_to(PACKAGE).as_posix())
                info.uid = info.gid = 0
                info.uname = info.gname = ''
                info.mtime = 0
                info.mode = 0o755 if path.is_dir() else 0o644
                if path.is_file():
                    with path.open('rb') as source:tar.addfile(info, source)
                else:tar.addfile(info)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (args.output / (archive.name+'.sha256')).write_text(f'{digest}  {archive.name}\n')
    print(archive.name, archive.stat().st_size, digest)

if __name__ == '__main__':main()
