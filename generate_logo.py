#!/usr/bin/env python3
"""
Generate Yuan Payment Logo
Creates a 400x400px logo with Chinese-themed design
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_yuan_payment_logo():
    """Generate Yuan Payment logo with Chinese theme"""

    # Create output directory if it doesn't exist
    output_dir = "/app/uploads/watermark"
    os.makedirs(output_dir, exist_ok=True)

    # Create 400x400 canvas with transparent background
    size = 400
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    chinese_red = (200, 16, 46, 255)  # #C8102E
    gold = (255, 215, 0, 255)  # #FFD700

    # Draw red circle background
    circle_padding = 20
    circle_bbox = [circle_padding, circle_padding, size - circle_padding, size - circle_padding]
    draw.ellipse(circle_bbox, fill=chinese_red)

    # Draw Yuan symbol (¥) in gold
    yuan_symbol = "¥"

    # Try to use a nice font, fallback to default
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "arial.ttf"
    ]

    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 180)
            print(f"✅ Using font: {font_path}")
            break
        except:
            continue

    if font is None:
        print("⚠️  Using default font")
        font = ImageFont.load_default()

    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), yuan_symbol, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the Yuan symbol
    text_x = (size - text_width) // 2 - bbox[0]
    text_y = (size - text_height) // 2 - bbox[1] - 20  # Slight adjustment up

    # Draw Yuan symbol with slight shadow for depth
    shadow_offset = 3
    draw.text((text_x + shadow_offset, text_y + shadow_offset), yuan_symbol, font=font, fill=(0, 0, 0, 100))
    draw.text((text_x, text_y), yuan_symbol, font=font, fill=gold)

    # Add "Yuan Payment" text below
    text_font = None
    for font_path in font_paths:
        try:
            text_font = ImageFont.truetype(font_path, 32)
            break
        except:
            continue

    if text_font is None:
        text_font = ImageFont.load_default()

    text = "Yuan Payment"
    bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2 - bbox[0]
    text_y = size - 80

    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, font=text_font, fill=(0, 0, 0, 100))
    draw.text((text_x, text_y), text, font=text_font, fill=chinese_red)

    # Save the logo
    output_path = os.path.join(output_dir, "yuan-payment-logo.png")
    img.save(output_path, "PNG")

    print(f"✅ Yuan Payment logo created successfully!")
    print(f"   Path: {output_path}")
    print(f"   Size: {size}x{size}px")
    print(f"   Colors: Chinese Red (#C8102E) and Gold (#FFD700)")

    return output_path

if __name__ == "__main__":
    generate_yuan_payment_logo()
