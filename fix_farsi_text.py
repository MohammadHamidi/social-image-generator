#!/usr/bin/env python3
"""
Fix Farsi Text Rendering Issues
This script tests and fixes Farsi/Persian text rendering in the Social Image Generator.
"""

import sys
import os

# Add src to path
sys.path.append('src')

def test_arabic_reshaper():
    """Test if arabic_reshaper is working properly"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        # Test Farsi text
        test_text = "موفقیت پایان راه نیست؛ شکست هم مهلک نیست."
        print(f"✅ Original Farsi text: {test_text}")
        
        # Test reshaping
        reshaped = arabic_reshaper.reshape(test_text)
        print(f"✅ Reshaped text: {reshaped}")
        
        # Test display
        display_text = get_display(reshaped)
        print(f"✅ Display text: {display_text}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_font_loading():
    """Test if Farsi fonts are loading properly"""
    try:
        from PIL import ImageFont
        
        # Check font directory
        font_dir = os.path.join('assets', 'fonts')
        if not os.path.exists(font_dir):
            print(f"❌ Font directory not found: {font_dir}")
            return False
            
        print(f"✅ Font directory found: {font_dir}")
        
        # List available fonts
        font_files = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]
        print(f"✅ Available fonts: {font_files}")
        
        # Check for Farsi fonts
        farsi_fonts = [f for f in font_files if 'IRANYekan' in f or 'NotoSansArabic' in f]
        if farsi_fonts:
            print(f"✅ Farsi fonts found: {farsi_fonts}")
            
            # Test loading a Farsi font
            test_font_path = os.path.join(font_dir, farsi_fonts[0])
            try:
                font = ImageFont.truetype(test_font_path, 32)
                print(f"✅ Successfully loaded font: {farsi_fonts[0]}")
                return True
            except Exception as e:
                print(f"❌ Failed to load font {farsi_fonts[0]}: {e}")
                return False
        else:
            print("❌ No Farsi fonts found!")
            return False
            
    except Exception as e:
        print(f"❌ Font test error: {e}")
        return False

def test_text_generation():
    """Test if text generation works with Farsi"""
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        # Create a simple config
        config = {
            'canvas_width': 1080,
            'canvas_height': 1350,
            'fonts': {
                'headline_size': 48,
                'subheadline_size': 32,
                'brand_size': 24
            },
            'design_system': {
                'colors': {
                    'text': {
                        'primary': [255, 255, 255],
                        'secondary': [203, 213, 225],
                        'muted': [148, 163, 184]
                    }
                },
                'shadows': {
                    'text': {
                        'offset': 2,
                        'blur': 4,
                        'color': [0, 0, 0, 153]
                    }
                }
            }
        }
        
        # Save config temporarily
        config_path = 'temp_test_config.json'
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        try:
            # Initialize generator
            generator = EnhancedSocialImageGenerator(config_path)
            
            # Test Farsi text generation
            content = {
                'quote': 'موفقیت پایان راه نیست؛ شکست هم مهلک نیست.',
                'author': 'Winston Churchill',
                'brand': 'Inspiration Daily'
            }
            
            print("🔄 Testing Farsi text generation...")
            img = generator.generate_text_layout('quote', content)
            
            # Save test image
            output_path = 'test_farsi_quote.png'
            img.save(output_path, 'PNG')
            print(f"✅ Test image saved: {output_path}")
            
            return True
            
        finally:
            # Clean up temp config
            if os.path.exists(config_path):
                os.remove(config_path)
                
    except Exception as e:
        print(f"❌ Text generation test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🔍 Testing Farsi Text Rendering...\n")
    
    # Test 1: Arabic reshaper
    print("1. Testing Arabic Reshaper...")
    reshaper_ok = test_arabic_reshaper()
    print()
    
    # Test 2: Font loading
    print("2. Testing Font Loading...")
    font_ok = test_font_loading()
    print()
    
    # Test 3: Text generation
    print("3. Testing Text Generation...")
    generation_ok = test_text_generation()
    print()
    
    # Summary
    print("📊 Test Results:")
    print(f"   Arabic Reshaper: {'✅ PASS' if reshaper_ok else '❌ FAIL'}")
    print(f"   Font Loading: {'✅ PASS' if font_ok else '❌ FAIL'}")
    print(f"   Text Generation: {'✅ PASS' if generation_ok else '❌ FAIL'}")
    
    if all([reshaper_ok, font_ok, generation_ok]):
        print("\n🎉 All tests passed! Farsi text should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        
        if not reshaper_ok:
            print("\n💡 To fix Arabic Reshaper:")
            print("   pip install arabic-reshaper python-bidi")
            
        if not font_ok:
            print("\n💡 To fix Font Loading:")
            print("   - Ensure assets/fonts/ directory exists")
            print("   - Download IRANYekan or NotoSansArabic fonts")
            print("   - Check file permissions")

if __name__ == "__main__":
    main()
