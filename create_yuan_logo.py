#!/usr/bin/env python3
"""
Create Yuan Payment Logo

Generates a simple, professional logo for Yuan Payment with:
- Red circle background (#C8102E)
- Gold "¥" symbol in the center
- "Yuan Payment" text below in Chinese red
- Size: 400x400px, transparent background
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_yuan_logo(output_path):
    """Create Yuan Payment logo."""
    
    # Canvas size
    size = 400
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    chinese_red = (200, 16, 46)  # #C8102E
    gold = (255, 215, 0)  # #FFD700
    white = (255, 255, 255)
    
    # Draw red circle background
    circle_radius = 180
    center_x, center_y = size // 2, size // 2
    
    draw.ellipse(
        [(center_x - circle_radius, center_y - circle_radius),
         (center_x + circle_radius, center_y + circle_radius)],
        fill=chinese_red
    )
    
    # Draw gold ¥ symbol
    try:
        # Try to load a bold font for the symbol
        font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
        if os.path.exists(font_path):
            symbol_font = ImageFont.truetype(font_path, 120)
        else:
            # Fallback to default
            symbol_font = ImageFont.load_default()
            # Scale up for visibility
            symbol_size = 200
    except:
        symbol_font = ImageFont.load_default()
        symbol_size = 200
    
    # Draw ¥ symbol
    symbol = "¥"
    bbox = draw.textbbox((0, 0), symbol, font=symbol_font)
    symbol_width = bbox[2] - bbox[0]
    symbol_height = bbox[3] - bbox[1]
    
    # Center the symbol
    symbol_x = center_x - symbol_width // 2
    symbol_y = center_y - symbol_height // 2 - 20
    
    draw.text(
        (symbol_x, symbol_y),
        symbol,
        font=symbol_font,
        fill=gold
    )
    
    # Draw "YUAN" text below
    try:
        if os.path.exists(font_path):
            text_font = ImageFont.truetype(font_path, 36)
        else:
            text_font = ImageFont.load_default()
    except:
        text_font = ImageFont.load_default()
    
    yuan_text = "YUAN"
    bbox = draw.textbbox((0, 0), yuan_text, font=text_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y + 60
    
    draw.text(
        (text_x, text_y),
        yuan_text,
        font=text_font,
        fill=white
    )
    
    # Draw "PAYMENT" text below
    payment_text = "PAYMENT"
    bbox = draw.textbbox((0, 0), payment_text, font=text_font)
    text_width = bbox[2] - bbox[0]
    
    text_x = center_x - text_width // 2
    text_y = text_y + text_height + 5
    
    draw.text(
        (text_x, text_y),
        payment_text,
        font=text_font,
        fill=white
    )
    
    # Save logo
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"✅ Created Yuan Payment logo: {output_path}")
    print(f"   Size: {size}x{size}px")
    print(f"   Colors: Red (#C8102E), Gold (#FFD700)")
    
    return img

if __name__ == "__main__":
    output_path = "uploads/watermark/yuan-payment-logo.png"
    create_yuan_logo(output_path)

