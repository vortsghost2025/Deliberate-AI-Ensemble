#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upload fixed .htaccess"""

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

print("⬆️  Uploading fixed .htaccess...\n")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()

    # Backup old .htaccess first
    print("📦 Backing up old .htaccess...")
    try:
        sftp.rename(f"{REMOTE_DIR}/.htaccess", f"{REMOTE_DIR}/.htaccess.backup")
        print("  ✓ Backed up to .htaccess.backup")
    except:
        print("  ⚠️  No existing .htaccess to backup")

    # Upload new .htaccess
    print("\n⬆️  Uploading new .htaccess with PWA MIME types...")
    sftp.put(".htaccess_new", f"{REMOTE_DIR}/.htaccess")
    print("  ✓ New .htaccess uploaded")

    print("\n✅ Done! Service Worker should now load properly.")
    print("\n🧪 Test it:")
    print("  1. Clear browser cache (Ctrl+Shift+Delete)")
    print("  2. Hard refresh (Ctrl+Shift+R)")
    print("  3. Visit: https://deliberateensemble.works/sw.js")
    print("  4. Should see JavaScript code, not an error")

    sftp.close()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    ssh.close()
