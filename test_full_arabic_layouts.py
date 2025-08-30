#!/usr/bin/env python3
"""
Test full Arabic layouts to identify rendering issues
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_arabic_quote_layout():
    """Test Arabic quote layout specifically"""
    print("🔍 TESTING ARABIC QUOTE LAYOUT")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Arabic quote content
        arabic_content = {
            "quote": "العلم نور والجهل ظلام",
            "author": "مثل عربي",
            "brand": "النظام الحديث"
        }
        
        print("📝 Arabic content:")
        print(f"   Quote: {arabic_content['quote']}")
        print(f"   Author: {arabic_content['author']}")
        print(f"   Brand: {arabic_content['brand']}")
        
        print("\n🎨 Generating Arabic quote layout...")
        img = generator.generate_quote_layout(**arabic_content)
        
        output_path = "output/test_arabic_quote_full.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Generated: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Arabic quote failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_farsi_content():
    """Test Persian/Farsi content"""
    print("\n🔍 TESTING FARSI/PERSIAN CONTENT")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Farsi content
        farsi_content = {
            "quote": "دانش نور است و نادانی تاریکی",
            "author": "حکمت فارسی",
            "brand": "سیستم جدید"
        }
        
        print("📝 Farsi content:")
        print(f"   Quote: {farsi_content['quote']}")
        print(f"   Author: {farsi_content['author']}")
        print(f"   Brand: {farsi_content['brand']}")
        
        print("\n🎨 Generating Farsi quote layout...")
        img = generator.generate_quote_layout(**farsi_content)
        
        output_path = "output/test_farsi_quote_full.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Generated: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Farsi quote failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_arabic_article():
    """Test Arabic article layout"""
    print("\n🔍 TESTING ARABIC ARTICLE LAYOUT")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Arabic article content
        arabic_article = {
            "title": "تحسينات النظام التصميمي",
            "body": "هذا المقال يوضح التسلسل الهرمي للطباعة المحسن مع عنوان رئيسي مناسب، ونص أساسي يحترم قيود العرض الأقصى، وقابلية قراءة محسنة من خلال تباعد أفضل للأسطر. النص لم يعد يمتد بشكل واسع جداً ويحافظ على مقاييس قراءة مريحة.",
            "brand": "التميز في التصميم"
        }
        
        print("📝 Arabic article content:")
        print(f"   Title: {arabic_article['title']}")
        print(f"   Body: {arabic_article['body'][:50]}...")
        print(f"   Brand: {arabic_article['brand']}")
        
        print("\n🎨 Generating Arabic article layout...")
        img = generator.generate_article_layout(**arabic_article)
        
        output_path = "output/test_arabic_article_full.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Generated: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Arabic article failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mixed_language_content():
    """Test mixed language content"""
    print("\n🔍 TESTING MIXED LANGUAGE CONTENT")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Mixed content
        mixed_content = {
            "title": "Design System - نظام التصميم",
            "body": "This article demonstrates mixed language support with both English and Arabic text. النص العربي يجب أن يظهر بشكل صحيح مع النص الإنجليزي في نفس المحتوى.",
            "brand": "Multilingual System"
        }
        
        print("📝 Mixed language content:")
        print(f"   Title: {mixed_content['title']}")
        print(f"   Body: {mixed_content['body'][:50]}...")
        print(f"   Brand: {mixed_content['brand']}")
        
        print("\n🎨 Generating mixed language layout...")
        img = generator.generate_article_layout(**mixed_content)
        
        output_path = "output/test_mixed_language_full.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Generated: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mixed language failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_arabic_processing():
    """Analyze what's happening with Arabic text processing"""
    print("\n🔬 ANALYZING ARABIC TEXT PROCESSING")
    print("=" * 40)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        test_text = "العلم نور والجهل ظلام"
        print(f"Original text: {test_text}")
        
        # Step by step processing
        print("\n🔄 Step-by-step processing:")
        
        # Step 1: Detection
        is_arabic = generator._is_arabic_text(test_text)
        print(f"1. Arabic detected: {is_arabic}")
        
        # Step 2: Reshaping
        reshaped = arabic_reshaper.reshape(test_text)
        print(f"2. Reshaped: {reshaped}")
        
        # Step 3: Bidi
        display_text = get_display(reshaped)
        print(f"3. Display text: {display_text}")
        
        # Step 4: Generator's preparation
        prepared = generator._prepare_arabic_text(test_text)
        print(f"4. Generator prepared: {prepared}")
        
        # Check if they match
        if display_text == prepared:
            print("✅ Generator processing matches manual processing")
        else:
            print("❌ Generator processing differs from manual processing")
        
        # Test formatting
        formatted_quote = generator._format_quote_text(test_text, is_arabic)
        print(f"5. Formatted quote: {formatted_quote}")
        
        formatted_author = generator._format_attribution("مؤلف عربي", is_arabic)
        print(f"6. Formatted attribution: {formatted_author}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    print("🌍 COMPREHENSIVE ARABIC/FARSI TEXT TESTING")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Arabic Quote", test_arabic_quote_layout),
        ("Farsi Content", test_farsi_content),
        ("Arabic Article", test_arabic_article),
        ("Mixed Language", test_mixed_language_content),
        ("Processing Analysis", analyze_arabic_processing)
    ]
    
    successful_tests = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                successful_tests += 1
                print(f"✅ {test_name} completed successfully")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print(f"\n📊 TEST RESULTS: {successful_tests}/{len(tests)} tests passed")
    
    if successful_tests == len(tests):
        print("🎉 All Arabic/Farsi tests passed!")
    else:
        print("⚠️  Some tests failed - check the outputs to identify issues")
    
    print("\n📁 Generated files:")
    print("- output/test_arabic_quote_full.png")
    print("- output/test_farsi_quote_full.png") 
    print("- output/test_arabic_article_full.png")
    print("- output/test_mixed_language_full.png")
    print("\n📝 Please check these images to see if Arabic/Farsi text renders correctly")
