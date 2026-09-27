#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick deployment script for WE4Free website"""
import paramiko
import os
import sys
from pathlib import Path

# Force UTF-8 encoding for output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# SSH credentials
SSH_HOST = "88.223.85.164"
SSH_PORT = 65002
SSH_USER = "u526066719"
SSH_PASSWORD = os.environ.get("HOSTINGER_SSH_PASSWORD", "")
if not SSH_PASSWORD:
    sys.exit("HOSTINGER_SSH_PASSWORD is not set. Export it before running this script.")
# CORRECT PATH - domain-specific public_html
REMOTE_DIR = "/home/u526066719/domains/deliberateensemble.works/public_html"
LOCAL_DIR = "we4free_website"

print("Deploying WE4Free to deliberateensemble.works...")

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect
    print("🔌 Connecting to server...")
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)

    # Create SFTP client
    sftp = ssh.open_sftp()

    local_path = Path(LOCAL_DIR)

    # 1. Upload all HTML files
    html_files = list(local_path.glob("*.html"))
    print(f"\n📄 Uploading {len(html_files)} HTML file(s)...")
    for html_file in html_files:
        remote_file = f"{REMOTE_DIR}/{html_file.name}"
        print(f"  ✓ {html_file.name}")
        sftp.put(str(html_file), remote_file)

    # 2. Upload Service Worker and Manifest
    pwa_files = ["sw.js", "manifest.json", "db.js", "integrity.js", "self_healing.js", "channel_router.js", "conflict_resolver.js", "integrity.manifest.json"]
    print(f"\n🚀 Uploading PWA files...")
    for pwa_file in pwa_files:
        local_file = local_path / pwa_file
        if local_file.exists():
            remote_file = f"{REMOTE_DIR}/{pwa_file}"
            print(f"  ✓ {pwa_file}")
            sftp.put(str(local_file), remote_file)
        else:
            print(f"  ⚠️  {pwa_file} not found, skipping")

    # 3. Create icons directory and upload icons
    icons_dir = local_path / "icons"
    if icons_dir.exists():
        icon_files = list(icons_dir.glob("*.png"))
        print(f"\n🎨 Uploading {len(icon_files)} icon file(s)...")

        # Create remote icons directory
        try:
            sftp.mkdir(f"{REMOTE_DIR}/icons")
            print("  ✓ Created /icons directory")
        except IOError:
            # Directory already exists
            pass

        for icon_file in icon_files:
            remote_file = f"{REMOTE_DIR}/icons/{icon_file.name}"
            print(f"  ✓ {icon_file.name}")
            sftp.put(str(icon_file), remote_file)
    else:
        print(f"\n⚠️  Icons directory not found, skipping")

    sftp.close()

    print("\n" + "="*60)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print(f"📦 Deployed: {len(html_files)} HTML + 2 PWA files + {len(icon_files) if icons_dir.exists() else 0} icons")
    print("\n🌐 Live URLs:")
    print("  • Homepage: https://deliberateensemble.works")
    print("  • Resources: https://deliberateensemble.works/resources.html")
    print("  • Emergency: https://deliberateensemble.works/emergency.html")
    print("\n🧪 Test PWA:")
    print("  1. Open DevTools → Application → Service Workers")
    print("  2. Check manifest: Application → Manifest")
    print("  3. Try offline: DevTools → Network → Offline checkbox")
    print("="*60)

except Exception as e:
    print(f"Deployment failed: {e}")

finally:
    ssh.close()
