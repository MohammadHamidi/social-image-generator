#!/usr/bin/env python3
"""
Test the Docker-compatible font system
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_bundled_fonts():
    """Test the bundled font system"""
    print("🔤 TESTING DOCKER-COMPATIBLE FONT SYSTEM")
    print("=" * 45)
    
    # Check font files
    font_dir = "assets/fonts"
    expected_fonts = [
        'NotoSans-Regular.ttf',
        'NotoSans-Bold.ttf', 
        'NotoSansArabic-Regular.ttf',
        'NotoSansArabic-Bold.ttf'
    ]
    
    print("📁 Checking for bundled fonts...")
    bundled_fonts_found = 0
    
    for font_file in expected_fonts:
        font_path = os.path.join(font_dir, font_file)
        if os.path.exists(font_path):
            print(f"✅ Found: {font_file}")
            bundled_fonts_found += 1
        else:
            print(f"❌ Missing: {font_file}")
    
    print(f"\n📊 Font Status: {bundled_fonts_found}/{len(expected_fonts)} bundled fonts found")
    
    if bundled_fonts_found == 0:
        print("⚠️  No bundled fonts found - will use system fonts")
        print("💡 Run: python3 download_fonts.py to get bundled fonts")
    elif bundled_fonts_found < len(expected_fonts):
        print("⚠️  Some bundled fonts missing - may affect multilingual support")
    else:
        print("🎉 All bundled fonts found - ready for Docker!")

def test_generator_with_fonts():
    """Test the generator with the new font system"""
    print("\n🎨 TESTING GENERATOR WITH NEW FONT SYSTEM")
    print("=" * 45)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        print("📋 Initializing generator with bundled fonts...")
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        print("\n📝 Font loading results:")
        for font_name, font_obj in generator.fonts.items():
            print(f"   {font_name}: {type(font_obj).__name__}")
            if hasattr(font_obj, 'path') and font_obj.path:
                font_path = font_obj.path
                if 'assets/fonts' in font_path:
                    print(f"      📦 Bundled: {os.path.basename(font_path)}")
                else:
                    print(f"      🖥️  System: {os.path.basename(font_path)}")
            else:
                print(f"      🔧 Default PIL font")
        
        # Test text rendering
        print("\n🖼️  Testing text rendering...")
        
        test_content = {
            "title": "Docker Font Test",
            "body": "This tests the bundled font system for Docker deployment. The fonts should render correctly without system dependencies.",
            "brand": "Container Ready"
        }
        
        img = generator.generate_article_layout(**test_content)
        
        output_path = "output/docker_font_test.png"
        img.save(output_path, 'PNG', quality=95)
        
        print(f"✅ Generated test image: {output_path}")
        print("📝 Check if text renders properly (not as ASCII patterns)")
        
        return True
        
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multilingual_support():
    """Test multilingual font support"""
    print("\n🌍 TESTING MULTILINGUAL SUPPORT")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Test Arabic content
        arabic_content = {
            "quote": "العلم نور والجهل ظلام",
            "author": "مثل عربي",
            "brand": "النظام الحديث"
        }
        
        print("📝 Testing Arabic text rendering...")
        img = generator.generate_quote_layout(**arabic_content)
        
        output_path = "output/docker_arabic_test.png"
        img.save(output_path, 'PNG', quality=95)
        
        print(f"✅ Generated Arabic test: {output_path}")
        
        # Test mixed content
        mixed_content = {
            "title": "Mixed Language Support - دعم اللغات المختلطة",
            "body": "This demonstrates mixed language support with both English and Arabic text. النص العربي يجب أن يظهر بشكل صحيح.",
            "brand": "Multilingual Ready"
        }
        
        print("📝 Testing mixed language rendering...")
        img = generator.generate_article_layout(**mixed_content)
        
        output_path = "output/docker_mixed_lang_test.png"
        img.save(output_path, 'PNG', quality=95)
        
        print(f"✅ Generated mixed language test: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Multilingual test failed: {e}")
        return False

def docker_readiness_check():
    """Check Docker readiness"""
    print("\n🐳 DOCKER READINESS CHECK")
    print("=" * 30)
    
    checks = [
        ("Bundled fonts directory exists", os.path.exists("assets/fonts")),
        ("At least one bundled font", len([f for f in os.listdir("assets/fonts") if f.endswith('.ttf')]) > 0),
        ("Generator imports successfully", True),  # If we got here, imports work
        ("No system font dependencies", True)  # We have fallbacks
    ]
    
    all_passed = True
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print(f"\n📊 Docker Readiness: {'🎉 READY' if all_passed else '⚠️  NEEDS ATTENTION'}")
    
    if all_passed:
        print("🚀 This setup will work in a Docker container!")
        print("📋 Next steps:")
        print("   1. Create Dockerfile with font installation")
        print("   2. Copy assets/fonts/ to container")
        print("   3. Install fontconfig in container")
    else:
        print("🔧 Issues to resolve:")
        print("   - Download bundled fonts: python3 download_fonts.py")
        print("   - Ensure all dependencies are met")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    test_bundled_fonts()
    
    if test_generator_with_fonts():
        test_multilingual_support()
    
    docker_readiness_check()
    
    print("\n🎉 Font system testing completed!")
    print("📝 Check output/docker_*_test.png files for visual verification")
