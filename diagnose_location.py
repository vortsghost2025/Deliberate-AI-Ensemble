#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check exactly where files are and their timestamps"""

import sys
import paramiko
from datetime import datetime

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

SSH_HOST = "88.223.85.164"
SSH_PORT = 65002
SSH_USER = "u526066719"
SSH_PASSWORD = "134679Rosebud!"

print("🔍 Checking file locations and timestamps...\n")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()

    # Check multiple possible directories
    possible_dirs = [
        "/home/u526066719/public_html",
        "/home/u526066719/domains/deliberateensemble.works/public_html",
        "/public_html",
        "/htdocs"
    ]

    for directory in possible_dirs:
        try:
            print(f"\n📁 Checking: {directory}")
            files = sftp.listdir(directory)
            print(f"   ✓ EXISTS - {len(files)} files found")

            # Show recent files with timestamps
            critical_files = ['sw.js', 'manifest.json', 'resources.html']
            print(f"\n   Recent critical files:")
            for cf in critical_files:
                try:
                    stat = sftp.stat(f"{directory}/{cf}")
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    print(f"      • {cf:<20} Modified: {mod_time} ({stat.st_size} bytes)")
                except:
                    print(f"      ✗ {cf} not found")

        except Exception as e:
            print(f"   ✗ Does not exist or not accessible")

    # Show current working directory
    print(f"\n📍 SFTP working directory: {sftp.getcwd()}")

    # Run a shell command to find where files really are
    stdin, stdout, stderr = ssh.exec_command("find /home/u526066719 -name 'sw.js' 2>/dev/null")
    found_files = stdout.read().decode().strip().split('\n')

    if found_files and found_files[0]:
        print(f"\n🔎 Found sw.js at these locations:")
        for f in found_files:
            if f:
                print(f"   • {f}")
    else:
        print(f"\n⚠️  sw.js not found anywhere in /home/u526066719/")

    sftp.close()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    ssh.close()
