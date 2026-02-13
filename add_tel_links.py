#!/usr/bin/env python3
"""Add tel: links to phone numbers in resources.html"""
import re
from pathlib import Path

# Read the HTML file
html_file = Path("we4free_website/resources.html")
content = html_file.read_text(encoding='utf-8')

# Pattern 1: "Call 1-XXX-XXX-XXXX" or "Call XXX-XXX-XXXX"
def add_tel_link_call(match):
    full_text = match.group(0)
    phone = match.group(1)
    # Clean phone for tel: link (remove spaces, dashes ok)
    tel_phone = phone.replace(' ', '')
    return f'<a href="tel:{tel_phone}">{full_text}</a>'

# Pattern 2: "Dial XXX"
def add_tel_link_dial(match):
    full_text = match.group(0)
    phone = match.group(1)
    tel_phone = phone.replace(' ', '')
    return f'<a href="tel:{tel_phone}">{full_text}</a>'

# Pattern 3: Standalone phone numbers (1-XXX-XXX-XXXX or XXX-XXX-XXXX)
def add_tel_link_standalone(match):
    # Check if already in a link
    before = content[max(0, match.start()-20):match.start()]
    if 'href="tel:' in before or '<a href=' in before:
        return match.group(0)  # Already a link, skip

    phone = match.group(0)
    tel_phone = phone.replace(' ', '')
    return f'<a href="tel:{tel_phone}">{phone}</a>'

# Apply patterns - be careful with existing links
# Pattern: "Call" followed by phone number
content = re.sub(r'(?<!href=")Call (1-\d{3}-\d{3}-\d{4}|\d{3}-\d{3}-\d{3}-\d{4}|1-\d{3}-[A-Z]+-\d{4})',
                lambda m: f'<a href="tel:{m.group(1).replace(" ", "")}" style="color: inherit; text-decoration: underline;">Call {m.group(1)}</a>' if 'href=' not in content[max(0, m.start()-30):m.start()] else m.group(0),
                content)

# Pattern: "Dial" followed by phone number
content = re.sub(r'(?<!href=")Dial (\d{3})',
                lambda m: f'<a href="tel:{m.group(1)}" style="color: inherit; text-decoration: underline;">Dial {m.group(1)}</a>' if 'href=' not in content[max(0, m.start()-30):m.start()] else m.group(0),
                content)

# Pattern: Standalone phone format "XXX-XXX-XXXX" or "1-XXX-XXX-XXXX" not already in links
# This is trickier - only target specific contexts
content = re.sub(r'(?<=>)(1-\d{3}-\d{3}-\d{4})(?=[<,;])',
                lambda m: f'<a href="tel:{m.group(1)}" style="color: inherit; text-decoration: underline;">{m.group(1)}</a>' if 'href=' not in content[max(0, m.start()-50):m.start()] else m.group(0),
                content)

print("✅ Added tel: links to phone numbers")
print(f"📝 Saving to {html_file}")

# Save the updated content
html_file.write_text(content, encoding='utf-8')

print("✅ Done!")
