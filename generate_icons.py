#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate placeholder PWA icons for WE4Free"""

import sys
from PIL import Image, ImageDraw, ImageFont
import os

# Fix Windows UTF-8 encoding for emojis/checkmarks
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Icon sizes needed for PWA
SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Brand color (periwinkle/purple from theme)
BRAND_COLOR = (102, 126, 234)  # #667eea

OUTPUT_DIR = "we4free_website/icons"

def create_icon(size):
    """Create a single icon of given size"""
    # Create image with brand color background
    img = Image.new('RGB', (size, size), BRAND_COLOR)
    draw = ImageDraw.Draw(img)

    # Add white circle in center
    circle_margin = size // 8
    circle_bbox = [circle_margin, circle_margin, size - circle_margin, size - circle_margin]
    draw.ellipse(circle_bbox, fill=(255, 255, 255))

    # Add text "WE4" in center
    text = "WE4"

    # Try to use a system font, fallback to default
    try:
        # Calculate font size based on icon size
        font_size = size // 4
        # Try to load a bold font
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial Bold.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("seguisb.ttf", font_size)
                except:
                    font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (size - text_width) // 2 - bbox[0]
    y = (size - text_height) // 2 - bbox[1]

    # Draw text in brand color
    draw.text((x, y), text, fill=BRAND_COLOR, font=font)

    return img

def main():
    """Generate all icon sizes"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("[WE4Free Icon Generator]")
    print(f"Generating {len(SIZES)} icon sizes...")

    for size in SIZES:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        img = create_icon(size)
        img.save(filepath, "PNG", optimize=True)

        print(f"✓ Created {filename} ({size}x{size}px)")

    # Create emergency icon (96x96 for shortcuts)
    emergency_size = 96
    emergency_file = os.path.join(OUTPUT_DIR, "emergency-96x96.png")

    # Create red version for emergency
    img = Image.new('RGB', (emergency_size, emergency_size), (211, 47, 47))  # Red
    draw = ImageDraw.Draw(img)

    # White circle
    margin = emergency_size // 8
    draw.ellipse([margin, margin, emergency_size - margin, emergency_size - margin], fill=(255, 255, 255))

    # Draw "🚨" or "SOS" text
    text = "SOS"
    try:
        font_size = emergency_size // 4
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (emergency_size - text_width) // 2 - bbox[0]
    y = (emergency_size - text_height) // 2 - bbox[1]
    draw.text((x, y), text, fill=(211, 47, 47), font=font)

    img.save(emergency_file, "PNG", optimize=True)
    print(f"✓ Created emergency-96x96.png (red emergency icon)")

    print(f"\n✅ All icons generated in {OUTPUT_DIR}/")
    print(f"Total files: {len(SIZES) + 1}")

if __name__ == "__main__":
    main()
