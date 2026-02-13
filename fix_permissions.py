#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix file permissions on server"""

import sys
import paramiko

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

SSH_HOST = "88.223.85.164"
SSH_PORT = 65002
SSH_USER = "u526066719"
SSH_PASSWORD = "134679Rosebud!"
REMOTE_DIR = "/home/u526066719/domains/deliberateensemble.works/public_html"

print("🔧 Fixing file permissions...\n")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()

    # Fix permissions for critical files
    critical_files = [
        'sw.js',
        'manifest.json',
        'emergency.html',
        'resources.html',
        'index.html',
        '.htaccess'
    ]

    print("📝 Setting file permissions to 644 (readable by web server)...\n")

    for file in critical_files:
        path = f"{REMOTE_DIR}/{file}"
        try:
            sftp.chmod(path, 0o644)  # rw-r--r--
            print(f"  ✓ {file} → 644")
        except Exception as e:
            print(f"  ✗ {file} → Failed: {e}")

    # Fix icons directory and files
    print("\n🎨 Setting icons directory permissions...\n")
    try:
        sftp.chmod(f"{REMOTE_DIR}/icons", 0o755)  # rwxr-xr-x
        print(f"  ✓ /icons/ → 755")

        # Fix each icon file
        icons = sftp.listdir(f"{REMOTE_DIR}/icons")
        for icon in icons:
            sftp.chmod(f"{REMOTE_DIR}/icons/{icon}", 0o644)
            print(f"  ✓ icons/{icon} → 644")
    except Exception as e:
        print(f"  ✗ Icons failed: {e}")

    print("\n✅ Permissions fixed!")
    print("\n🧪 Now try these URLs:")
    print("  • https://deliberateensemble.works/sw.js")
    print("  • https://deliberateensemble.works/manifest.json")
    print("\nShould load JavaScript/JSON instead of 404")

    sftp.close()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    ssh.close()
