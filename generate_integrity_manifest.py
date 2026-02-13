#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate integrity.manifest.json with SHA-256 hashes"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Files to hash
FILES_TO_HASH = [
    'index.html',
    'resources.html',
    'emergency.html',
    'sw.js',
    'manifest.json',
    'db.js',
    'integrity.js',
    'self_healing.js'
]

BASE_DIR = Path('we4free_website')

def compute_sha256(file_path):
    """Compute SHA-256 hash of file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_manifest():
    """Generate integrity manifest"""
    manifest = {
        'version': '1.0.0',
        'generated': datetime.utcnow().isoformat() + 'Z',
        'algorithm': 'SHA-256',
        'files': {}
    }

    print('[WE4Free Integrity] Generating manifest...\n')

    for filename in FILES_TO_HASH:
        file_path = BASE_DIR / filename
        if not file_path.exists():
            print(f'  ⚠️  {filename} - NOT FOUND, skipping')
            continue

        sha256 = compute_sha256(file_path)
        size = file_path.stat().st_size

        manifest['files'][f'/{filename}'] = {
            'sha256': sha256,
            'size': size,
            'added': datetime.utcnow().isoformat() + 'Z'
        }

        print(f'  ✓ {filename:<20} {sha256[:16]}... ({size} bytes)')

    # Write manifest
    output_path = BASE_DIR / 'integrity.manifest.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f'\n✅ Manifest generated: {output_path}')
    print(f'   {len(manifest["files"])} files hashed')
    print(f'   Version: {manifest["version"]}')

if __name__ == '__main__':
    generate_manifest()
