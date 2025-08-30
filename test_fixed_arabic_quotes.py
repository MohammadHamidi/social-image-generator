#!/usr/bin/env python3
"""
Test the fixed Arabic quote rendering
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_fixed_arabic_quotes():
    """Test Arabic quotes with the fixes"""
    print("🔧 TESTING FIXED ARABIC QUOTE RENDERING")
    print("=" * 45)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Test cases
        test_cases = [
            {
                "name": "Arabic Quote",
                "content": {
                    "quote": "العلم نور والجهل ظلام",
                    "author": "مثل عربي",
                    "brand": "النظام الحديث"
                },
                "output": "fixed_arabic_quote.png"
            },
            {
                "name": "Farsi Quote", 
                "content": {
                    "quote": "دانش نور است و نادانی تاریکی",
                    "author": "حکمت فارسی",
                    "brand": "سیستم جدید"
                },
                "output": "fixed_farsi_quote.png"
            },
            {
                "name": "Mixed Quote",
                "content": {
                    "quote": "Knowledge is power - العلم قوة",
                    "author": "Mixed Wisdom - حکمت مختلط",
                    "brand": "Bilingual System"
                },
                "output": "fixed_mixed_quote.png"
            }
        ]
        
        successful_tests = 0
        
        for test_case in test_cases:
            print(f"\n📝 Testing {test_case['name']}...")
            print(f"   Quote: {test_case['content']['quote']}")
            print(f"   Author: {test_case['content']['author']}")
            
            try:
                # Generate the quote layout
                img = generator.generate_quote_layout(**test_case['content'])
                
                # Save the result
                output_path = f"output/{test_case['output']}"
                img.save(output_path, 'PNG', quality=95)
                
                print(f"   ✅ Generated: {output_path}")
                successful_tests += 1
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n📊 Results: {successful_tests}/{len(test_cases)} tests passed")
        
        if successful_tests == len(test_cases):
            print("🎉 All Arabic quote tests passed!")
            print("📝 Check the output files to verify proper Arabic/Farsi rendering")
        
        return successful_tests == len(test_cases)
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

def test_arabic_article_fixed():
    """Test Arabic article with fixes"""
    print("\n🔧 TESTING FIXED ARABIC ARTICLE")
    print("=" * 35)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Arabic article with proper RTL content
        arabic_article = {
            "title": "نظام التصميم المحسن",
            "body": "يوضح هذا المقال التسلسل الهرمي المحسن للطباعة مع عنوان رئيسي مناسب ونص أساسي يحترم قيود العرض الأقصى. النص يحافظ على مقاييس قراءة مريحة ولا يمتد بشكل واسع جداً. التباعد بين الأسطر محسن للنص العربي.",
            "brand": "التميز في التصميم"
        }
        
        print("📝 Generating fixed Arabic article...")
        img = generator.generate_article_layout(**arabic_article)
        
        output_path = "output/fixed_arabic_article_layout.png"
        img.save(output_path, 'PNG', quality=95)
        
        print(f"✅ Generated: {output_path}")
        print("📝 Check if Arabic text now shows correctly with proper RTL alignment")
        
        return True
        
    except Exception as e:
        print(f"❌ Arabic article test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_before_after():
    """Show before/after comparison"""
    print("\n📊 BEFORE/AFTER COMPARISON")
    print("=" * 30)
    
    before_files = [
        "output/test_arabic_quote_full.png",
        "output/test_arabic_article_full.png"
    ]
    
    after_files = [
        "output/fixed_arabic_quote.png", 
        "output/fixed_arabic_article_layout.png"
    ]
    
    print("📁 Before (original issues):")
    for file in before_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (not found)")
    
    print("\n📁 After (fixed):")
    for file in after_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ⏳ {file} (will be generated)")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    print("🌍 TESTING FIXED ARABIC/FARSI RENDERING")
    print("=" * 45)
    
    compare_before_after()
    
    if test_fixed_arabic_quotes():
        test_arabic_article_fixed()
    
    print("\n🎉 Fixed Arabic testing completed!")
    print("\n📋 Key fixes applied:")
    print("1. Quote formatting now processes Arabic text correctly")
    print("2. Attribution formatting handles RTL text properly")
    print("3. Text alignment uses right-alignment for Arabic content")
    print("4. Text positioning adjusted for RTL languages")
    print("\n📝 Compare the new output files with the previous versions to see improvements")
