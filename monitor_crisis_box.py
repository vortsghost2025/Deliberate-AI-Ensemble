#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WE4Free Crisis Box Uptime Monitor
Checks that the emergency crisis box is visible and sticky
"""
import requests
from bs4 import BeautifulSoup
import time
import sys
from datetime import datetime

# Force UTF-8 encoding for output on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

URL = "https://deliberateensemble.works/resources.html"
CHECK_INTERVAL = 300  # 5 minutes
ALERT_EMAIL = None  # Set to email address for alerts

def check_crisis_box():
    """Check if crisis box exists and has correct styling"""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if crisis box exists
        crisis_box = soup.find('div', {'id': 'crisis-box'})
        if not crisis_box:
            return False, "Crisis box div not found in HTML"

        # Check if it has sticky positioning
        style = crisis_box.get('style', '')
        if 'position: sticky' not in style and 'position:sticky' not in style:
            return False, "Crisis box is not sticky"

        # Check if emergency numbers are present
        emergency_numbers = ['911', '988', '1-800-668-6868']
        for number in emergency_numbers:
            if number not in response.text:
                return False, f"Emergency number {number} not found"

        # Check if tel: links exist
        tel_links = soup.find_all('a', href=lambda x: x and x.startswith('tel:'))
        if len(tel_links) < 3:
            return False, f"Expected at least 3 tel: links, found {len(tel_links)}"

        return True, "All checks passed"

    except requests.RequestException as e:
        return False, f"HTTP error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def send_alert(message):
    """Send alert (placeholder for email/SMS service)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert = f"""
    [WE4Free ALERT] {timestamp}

    Crisis Box Health Check FAILED

    {message}

    URL: {URL}
    """
    print(alert)
    # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
    # or SMS service (Twilio)

def monitor(continuous=False):
    """Run health check, optionally in continuous mode"""
    consecutive_failures = 0

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        success, message = check_crisis_box()

        if success:
            print(f"[{timestamp}] [OK] Crisis box health check PASSED")
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            print(f"[{timestamp}] [FAIL] Crisis box health check FAILED: {message}")

            if consecutive_failures >= 3:
                send_alert(message)

        if not continuous:
            break

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print(f"Starting continuous monitoring (checking every {CHECK_INTERVAL}s)")
        print(f"Monitoring URL: {URL}\n")
        try:
            monitor(continuous=True)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
    else:
        print("Running single health check...")
        print(f"URL: {URL}\n")
        monitor(continuous=False)
        print("\nTip: Use --continuous for ongoing monitoring")
