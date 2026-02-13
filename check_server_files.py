#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check what files are actually on the server"""

import sys
import paramiko

# Fix Windows UTF-8 encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# SSH credentials
SSH_HOST = "88.223.85.164"
SSH_PORT = 65002
SSH_USER = "u526066719"
SSH_PASSWORD = "134679Rosebud!"
REMOTE_DIR = "/home/u526066719/public_html"

print("🔍 Checking server files...\n")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()

    # List all files in public_html
    print(f"📁 Files in {REMOTE_DIR}:\n")
    files = sftp.listdir(REMOTE_DIR)

    for file in sorted(files):
        try:
            stat = sftp.stat(f"{REMOTE_DIR}/{file}")
            size = stat.st_size
            if size < 1024:
                size_str = f"{size}B"
            elif size < 1024*1024:
                size_str = f"{size/1024:.1f}KB"
            else:
                size_str = f"{size/(1024*1024):.1f}MB"
            print(f"  {'📄' if '.' in file else '📁'} {file:<30} {size_str:>10}")
        except:
            print(f"  📁 {file}")

    # Check for specific files we need
    print("\n🎯 Checking critical files:")
    critical_files = ['sw.js', 'manifest.json', 'emergency.html', 'resources.html']

    for cf in critical_files:
        path = f"{REMOTE_DIR}/{cf}"
        try:
            stat = sftp.stat(path)
            print(f"  ✓ {cf} ({stat.st_size} bytes)")
        except:
            print(f"  ✗ {cf} MISSING")

    # Check icons directory
    print("\n🎨 Checking icons directory:")
    try:
        icons = sftp.listdir(f"{REMOTE_DIR}/icons")
        print(f"  ✓ /icons/ exists with {len(icons)} files")
        for icon in sorted(icons):
            print(f"    • {icon}")
    except:
        print(f"  ✗ /icons/ directory NOT FOUND")

    sftp.close()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    ssh.close()
