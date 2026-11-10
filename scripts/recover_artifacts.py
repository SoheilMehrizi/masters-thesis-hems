"""Verify the supplied ZIP and recover original files without overwriting changes."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def recover():
    archive = ROOT / 'exports/custom_alameda_complete.zip'
    destination = ROOT / 'data/recovered'
    records = []
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP integrity failed')
        manifest = json.loads(z.read('PACKAGE_MANIFEST.json'))
        for name in z.namelist():
            target = (destination / name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError(f'Unsafe archive member: {name}')
            payload = z.read(name)
            digest = hashlib.sha256(payload).hexdigest()
            if name in manifest['files']:
                expected = manifest['files'][name]
                if digest != expected['sha256'] or len(payload) != expected['bytes']:
                    raise ValueError(f'Package manifest mismatch: {name}')
            elif name not in ('PACKAGE_MANIFEST.json', 'PACKAGE_README_FA.txt'):
                raise ValueError(f'Unlisted member: {name}')
            if target.exists() and target.read_bytes() != payload:
                raise ValueError(f'Refusing to overwrite modified artifact: {target}')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            records.append({'path': target.relative_to(ROOT).as_posix(), 'bytes': len(payload),
                            'sha256': digest, 'source': archive.relative_to(ROOT).as_posix(),
                            'package_manifest_verified': name in manifest['files']})
        missing = set(manifest['files']) - set(z.namelist())
        if missing:
            raise ValueError(f'Missing members: {missing}')
    report = {'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'files': records, 'note': 'Package integrity verifies consistency, not independent provenance authenticity.'}
    (ROOT / 'reports').mkdir(exist_ok=True)
    (ROOT / 'reports/dataset_manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'Recovered {len(records)} files; {len(manifest["files"])} package hashes verified.')

if __name__ == '__main__':
    recover()
