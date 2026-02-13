#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download .htaccess to see what's blocking"""

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
REMOTE_DIR = "/home/u526066719/public_html"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    sftp = ssh.open_sftp()

    # Download .htaccess
    print("📥 Downloading .htaccess...\n")
    sftp.get(f"{REMOTE_DIR}/.htaccess", "downloaded_htaccess.txt")

    # Read and print it
    with open("downloaded_htaccess.txt", "r") as f:
        content = f.read()
        print("Current .htaccess content:")
        print("="*60)
        print(content)
        print("="*60)

    sftp.close()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    ssh.close()
