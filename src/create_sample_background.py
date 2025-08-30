from PIL import Image, ImageDraw
import math

def create_swirly_pattern(width=1080, height=1350):
    """Create a sample swirly background pattern"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Create swirly pattern with circles and curves
    for i in range(0, width + 200, 40):
        for j in range(0, height + 200, 40):
            # Calculate wave-like positions
            x = i + 30 * math.sin(j / 100.0)
            y = j + 30 * math.cos(i / 100.0)
            
            # Draw overlapping circles of different sizes
            radius = 15 + 10 * math.sin((i + j) / 50.0)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(240, 240, 240), outline=(220, 220, 220))
    
    # Add some larger decorative elements
    for i in range(5):
        x = (i * width // 4) + 100
        y = (i * height // 6) + 150
        draw.ellipse([x-50, y-50, x+50, y+50], 
                    fill=(250, 250, 250), outline=(200, 200, 200))
    
    return img

if __name__ == "__main__":
    pattern = create_swirly_pattern()
    pattern.save('assets/backgrounds/swirly_pattern.png')
    print("Sample background pattern created!")
