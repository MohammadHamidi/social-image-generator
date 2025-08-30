#!/usr/bin/env python3
"""
Debug Arabic text visibility issues
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_simple_arabic_test():
    """Create a simple test to check if Arabic text is visible"""
    print("🔍 CREATING SIMPLE ARABIC VISIBILITY TEST")
    print("=" * 45)
    
    # Create test image with different backgrounds
    img = Image.new('RGB', (1080, 1350), (255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)
    
    # Test different fonts and colors
    font_tests = [
        ("System Default", ImageFont.load_default(), (0, 0, 0)),
        ("Arabic Font", "assets/fonts/NotoSansArabic-Bold.ttf", (255, 0, 0)),
        ("Latin Font", "assets/fonts/NotoSans-Bold.ttf", (0, 255, 0))
    ]
    
    y_pos = 50
    test_text = "العلم نور والجهل ظلام"
    
    print(f"Testing with text: {test_text}")
    
    for font_name, font_path, color in font_tests:
        print(f"\n📝 Testing {font_name}...")
        
        try:
            # Load font
            if isinstance(font_path, str) and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 48)
                print(f"   ✅ Loaded font: {os.path.basename(font_path)}")
            else:
                font = font_path  # Default font
                print(f"   ✅ Using default font")
            
            # Draw label
            draw.text((50, y_pos), f"{font_name}:", font=font, fill=(0, 0, 0))
            
            # Draw original text
            draw.text((50, y_pos + 40), f"Original: {test_text}", font=font, fill=color)
            
            # Draw with Arabic processing
            try:
                import arabic_reshaper
                from bidi.algorithm import get_display
                
                reshaped = arabic_reshaper.reshape(test_text)
                display_text = get_display(reshaped)
                
                draw.text((50, y_pos + 80), f"Processed: {display_text}", font=font, fill=color)
                print(f"   ✅ Processed text: {display_text}")
                
            except Exception as e:
                print(f"   ❌ Processing failed: {e}")
            
            y_pos += 150
            
        except Exception as e:
            print(f"   ❌ Font test failed: {e}")
    
    # Save test
    output_path = "output/arabic_visibility_test.png"
    img.save(output_path, 'PNG', quality=95)
    print(f"\n💾 Saved visibility test: {output_path}")

def test_arabic_with_backgrounds():
    """Test Arabic text with different background colors"""
    print("\n🎨 TESTING ARABIC WITH DIFFERENT BACKGROUNDS")
    print("=" * 50)
    
    backgrounds = [
        ("White", (255, 255, 255), (0, 0, 0)),       # Black text on white
        ("Black", (0, 0, 0), (255, 255, 255)),       # White text on black
        ("Blue", (50, 60, 80), (255, 255, 255)),     # White text on blue (our default)
        ("Red", (150, 50, 50), (255, 255, 255)),     # White text on red
    ]
    
    test_text = "النص العربي يجب أن يظهر بوضوح"
    
    for i, (bg_name, bg_color, text_color) in enumerate(backgrounds):
        print(f"📝 Testing {bg_name} background...")
        
        # Create image
        img = Image.new('RGB', (800, 200), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Load Arabic font
        try:
            font = ImageFont.truetype("assets/fonts/NotoSansArabic-Bold.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Process Arabic text
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            
            reshaped = arabic_reshaper.reshape(test_text)
            display_text = get_display(reshaped)
            
            # Draw text
            draw.text((50, 50), f"Original: {test_text}", font=font, fill=text_color)
            draw.text((50, 100), f"Processed: {display_text}", font=font, fill=text_color)
            
            # Save
            output_path = f"output/arabic_bg_test_{bg_name.lower()}.png"
            img.save(output_path, 'PNG', quality=95)
            print(f"   ✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")

def test_generator_arabic_step_by_step():
    """Test the generator's Arabic rendering step by step"""
    print("\n🔧 TESTING GENERATOR ARABIC STEP BY STEP")
    print("=" * 45)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Create base image
        img = generator._create_enhanced_background()
        print("✅ Created background")
        
        # Add effects
        img = generator._add_gradient_noise(img)
        img = generator._draw_scrim_overlay(img, 'medium')
        print("✅ Added effects")
        
        # Test Arabic text rendering
        arabic_text = "النص العربي للاختبار"
        print(f"Testing text: {arabic_text}")
        
        # Step 1: Text preparation
        prepared_text = generator._prepare_arabic_text(arabic_text)
        print(f"Prepared text: {prepared_text}")
        
        # Step 2: Draw text manually to debug
        draw = ImageDraw.Draw(img)
        font = generator.fonts['headline']
        
        # Test different positions and colors
        test_positions = [
            ((100, 100), (255, 255, 255), "White text"),
            ((100, 200), (255, 0, 0), "Red text"),
            ((100, 300), (0, 255, 0), "Green text"),
            ((100, 400), (0, 0, 0), "Black text"),
        ]
        
        for (x, y), color, description in test_positions:
            print(f"Drawing {description} at ({x}, {y})")
            
            # Draw original
            draw.text((x, y), f"Orig: {arabic_text}", font=font, fill=color)
            
            # Draw processed
            draw.text((x, y + 40), f"Proc: {prepared_text}", font=font, fill=color)
        
        # Step 3: Use the generator's multiline text function
        print("\nTesting generator's multiline text function...")
        
        text_width, text_height = generator._draw_multiline_text(
            img, arabic_text, font,
            (generator.config['canvas_width'] // 2, 600),
            (255, 255, 0),  # Yellow for visibility
            max_width=700,
            alignment='center',
            add_shadow=True
        )
        
        print(f"Multiline text rendered: {text_width}x{text_height}")
        
        # Save debug image
        output_path = "output/arabic_step_by_step_debug.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Saved debug image: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Step-by-step test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_font_arabic_support():
    """Check if our fonts actually support Arabic characters"""
    print("\n🔤 CHECKING FONT ARABIC SUPPORT")
    print("=" * 35)
    
    fonts_to_test = [
        "assets/fonts/NotoSansArabic-Bold.ttf",
        "assets/fonts/NotoSansArabic-Regular.ttf",
        "assets/fonts/NotoSans-Bold.ttf"
    ]
    
    arabic_chars = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر']
    
    for font_path in fonts_to_test:
        print(f"\n📝 Testing {os.path.basename(font_path)}...")
        
        if not os.path.exists(font_path):
            print(f"   ❌ Font file not found")
            continue
        
        try:
            font = ImageFont.truetype(font_path, 32)
            
            # Test individual characters
            for char in arabic_chars:
                try:
                    bbox = font.getbbox(char)
                    width = bbox[2] - bbox[0]
                    if width > 0:
                        print(f"   ✅ '{char}' supported (width: {width})")
                    else:
                        print(f"   ❌ '{char}' not supported (width: 0)")
                except:
                    print(f"   ❌ '{char}' failed to measure")
            
        except Exception as e:
            print(f"   ❌ Font loading failed: {e}")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    print("🔍 ARABIC TEXT VISIBILITY DEBUGGING")
    print("=" * 40)
    
    create_simple_arabic_test()
    test_arabic_with_backgrounds()
    test_generator_arabic_step_by_step()
    check_font_arabic_support()
    
    print("\n🎉 Arabic visibility debugging completed!")
    print("📁 Check the following files:")
    print("- output/arabic_visibility_test.png")
    print("- output/arabic_bg_test_*.png")
    print("- output/arabic_step_by_step_debug.png")
    print("\n📝 These will help identify if text is invisible, wrong color, or positioned incorrectly")
