#!/usr/bin/env python3
"""
Test Arabic/Persian text rendering issues
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_arabic_text_issues():
    """Test various Arabic text rendering scenarios"""
    print("🔍 TESTING ARABIC/PERSIAN TEXT RENDERING")
    print("=" * 45)
    
    # Test texts
    test_texts = [
        ("Simple Arabic", "مرحبا"),
        ("Arabic Quote", "العلم نور والجهل ظلام"),
        ("Persian Text", "فارسی متن آزمایشی"),
        ("Mixed Text", "Hello مرحبا Persian فارسی"),
        ("Arabic with Numbers", "العدد ١٢٣ والرقم ٤٥٦"),
        ("Long Arabic", "هذا نص عربي طويل جداً لاختبار التفاف النص والمحاذاة الصحيحة في النظام الجديد")
    ]
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Create test image
        img = Image.new('RGB', (1080, 1350), (50, 60, 80))
        
        print("📝 Testing Arabic text processing...")
        
        y_pos = 100
        for i, (description, text) in enumerate(test_texts):
            print(f"\n🔤 Test {i+1}: {description}")
            print(f"   Original: {text}")
            
            try:
                # Test detection
                is_arabic = generator._is_arabic_text(text)
                print(f"   Arabic detected: {is_arabic}")
                
                # Test preparation
                prepared = generator._prepare_arabic_text(text)
                print(f"   Prepared: {prepared}")
                
                # Test rendering
                generator._draw_multiline_text(
                    img, text, generator.fonts['headline'],
                    (100, y_pos),
                    (255, 255, 255),
                    max_width=800
                )
                print(f"   ✅ Rendered at y={y_pos}")
                
                y_pos += 120
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Save test image
        output_path = "output/arabic_rendering_test.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"\n💾 Saved test: {output_path}")
        
    except Exception as e:
        print(f"❌ Arabic test failed: {e}")
        import traceback
        traceback.print_exc()

def test_arabic_libraries():
    """Test if Arabic processing libraries are available"""
    print("\n📚 TESTING ARABIC PROCESSING LIBRARIES")
    print("=" * 40)
    
    # Test arabic_reshaper
    try:
        import arabic_reshaper
        print("✅ arabic_reshaper available")
        
        # Test reshaping
        text = "مرحبا بالعالم"
        reshaped = arabic_reshaper.reshape(text)
        print(f"   Original: {text}")
        print(f"   Reshaped: {reshaped}")
        
    except ImportError:
        print("❌ arabic_reshaper not installed")
        print("   Install with: pip install arabic-reshaper")
    
    # Test bidi
    try:
        from bidi.algorithm import get_display
        print("✅ python-bidi available")
        
        # Test bidi
        text = "مرحبا بالعالم"
        display_text = get_display(text)
        print(f"   Original: {text}")
        print(f"   Display: {display_text}")
        
    except ImportError:
        print("❌ python-bidi not installed")
        print("   Install with: pip install python-bidi")

def create_proper_arabic_test():
    """Create a proper Arabic text test with libraries"""
    print("\n🛠️ CREATING PROPER ARABIC TEST")
    print("=" * 35)
    
    try:
        # Try to import Arabic libraries
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        print("✅ Arabic libraries available")
        
        # Test proper Arabic processing
        test_text = "العلم نور والجهل ظلام"
        print(f"Original: {test_text}")
        
        # Step 1: Reshape
        reshaped = arabic_reshaper.reshape(test_text)
        print(f"Reshaped: {reshaped}")
        
        # Step 2: Get display order
        display_text = get_display(reshaped)
        print(f"Display: {display_text}")
        
        # Create test image
        img = Image.new('RGB', (800, 400), (50, 60, 80))
        draw = ImageDraw.Draw(img)
        
        # Use bundled Arabic font
        font_path = "assets/fonts/NotoSansArabic-Bold.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 48)
        else:
            font = ImageFont.load_default()
        
        # Draw original (broken)
        draw.text((50, 50), test_text, font=font, fill=(255, 100, 100))
        draw.text((50, 20), "Original (Broken):", font=font, fill=(255, 255, 255))
        
        # Draw properly processed
        draw.text((50, 150), display_text, font=font, fill=(100, 255, 100))
        draw.text((50, 120), "Properly Processed:", font=font, fill=(255, 255, 255))
        
        # Save comparison
        output_path = "output/arabic_comparison.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Created comparison: {output_path}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing libraries: {e}")
        print("📦 Install required packages:")
        print("   pip install arabic-reshaper python-bidi")
        return False

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    test_arabic_libraries()
    test_arabic_text_issues()
    
    if create_proper_arabic_test():
        print("\n🎉 Arabic testing completed with proper processing!")
    else:
        print("\n⚠️  Arabic libraries need to be installed for proper text rendering")
    
    print("\n📋 Next steps:")
    print("1. Install: pip install arabic-reshaper python-bidi")
    print("2. Update generator to use proper Arabic processing")
    print("3. Test with: python3 test_arabic_rendering.py")
