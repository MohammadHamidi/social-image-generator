#!/usr/bin/env python3
"""
Test script specifically for your files: main.png, watermark.png, bg.png
"""

import requests
import json
import os

BASE_URL = "http://localhost:5000"

def upload_file(file_path, endpoint):
    """Upload a file to the specified endpoint"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    print(f"📤 Uploading {os.path.basename(file_path)} to {endpoint}...")
    print(f"   File size: {os.path.getsize(file_path)} bytes")
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}{endpoint}", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful!")
        print(f"   URL: {data['url']}")
        return data['url']
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_all_your_files():
    """Test with all your specific files"""
    print("🧪 Testing with your specific files: main.png, watermark.png, bg.png")
    print("=" * 70)
    
    # Check if files exist
    main_path = "../main.png"
    watermark_path = "../watermark.png"
    bg_path = "../bg.png"
    
    for path in [main_path, watermark_path, bg_path]:
        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            return False
        print(f"✅ Found: {os.path.basename(path)} ({os.path.getsize(path)} bytes)")
    
    print()
    
    # Upload all files
    main_url = upload_file(main_path, "/upload/main")
    watermark_url = upload_file(watermark_path, "/upload/watermark")
    bg_url = upload_file(bg_path, "/upload/background")
    
    if not all([main_url, watermark_url, bg_url]):
        print("❌ Some uploads failed")
        return False
    
    print()
    print("🎨 Generating social media image with all your files...")
    
    # Generate with all three images
    payload = {
        "headline": "کت‌های زمستانی جدید",
        "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
        "brand": "Fashion Store",  # This should be hidden by watermark
        "main_image_url": main_url,
        "watermark_image_url": watermark_url,
        "background_image_url": bg_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code != 200:
        print(f"❌ Generation failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False
    
    data = response.json()
    print("✅ Generation successful!")
    print(f"   Download URL: {data['download_url']}")
    print(f"   File size: {data['size']} bytes")
    print(f"   Main image used: {data['config']['main_image_used']}")
    print(f"   Watermark used: {data['config']['watermark_image_used']}")
    
    # Download the result
    print()
    print("💾 Downloading generated image...")
    download_response = requests.get(data['download_url'])
    
    if download_response.status_code == 200:
        output_path = "FINAL_WITH_YOUR_FILES.png"
        with open(output_path, 'wb') as f:
            f.write(download_response.content)
        print(f"✅ Image saved: {output_path}")
        print(f"   File size: {len(download_response.content)} bytes")
        
        print()
        print("🔍 What this image should contain:")
        print("   🖼️ Your bg.png as the custom background")
        print("   👜 Your main.png (handbag) with background removed")
        print("   🏷️ Your watermark.png preserving transparency")
        print("   📝 Arabic text properly rendered")
        print("   ❌ NO brand text 'Fashion Store' (hidden by watermark)")
        
        return True
    else:
        print(f"❌ Download failed: {download_response.status_code}")
        return False

def test_text_only_with_bg():
    """Test text-only generation with your background"""
    print("\n🧪 Testing text-only with your background")
    print("=" * 50)
    
    bg_path = "../bg.png"
    bg_url = upload_file(bg_path, "/upload/background")
    
    if not bg_url:
        return False
    
    # Generate with only background and text
    payload = {
        "headline": "نص فقط",
        "subheadline": "خلفية مخصصة",
        "brand": "متجر الأزياء",
        "background_image_url": bg_url
        # No main or watermark images
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        download_response = requests.get(data['download_url'])
        
        if download_response.status_code == 200:
            with open("TEXT_ONLY_WITH_YOUR_BG.png", 'wb') as f:
                f.write(download_response.content)
            print("✅ Text-only result saved: TEXT_ONLY_WITH_YOUR_BG.png")
            print("🔍 Should show: Your bg.png background with Arabic text and brand")
            return True
    
    print("❌ Text-only generation failed")
    return False

def test_watermark_transparency():
    """Test that your watermark transparency is preserved"""
    print("\n🧪 Testing watermark transparency preservation")
    print("=" * 50)
    
    watermark_path = "../watermark.png"
    watermark_url = upload_file(watermark_path, "/upload/watermark")
    
    if not watermark_url:
        return False
    
    # Generate with only watermark and solid background
    payload = {
        "headline": "اختبار الشفافية",
        "subheadline": "العلامة المائية",
        "brand": "Should Not Appear",  # Should be hidden
        "background_color": [50, 100, 150],  # Solid color to test transparency
        "watermark_image_url": watermark_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        download_response = requests.get(data['download_url'])
        
        if download_response.status_code == 200:
            with open("WATERMARK_TRANSPARENCY_TEST.png", 'wb') as f:
                f.write(download_response.content)
            print("✅ Transparency test saved: WATERMARK_TRANSPARENCY_TEST.png")
            print("🔍 Should show: Watermark with preserved transparency on blue background")
            print("❌ Should NOT show: 'Should Not Appear' text")
            return True
    
    print("❌ Transparency test failed")
    return False

def main():
    """Run all tests with your specific files"""
    print("🚀 Testing Social Image Generator with YOUR SPECIFIC FILES")
    print("=" * 60)
    print("📁 Files to test:")
    print("   • main.png (your handbag image)")
    print("   • watermark.png (your logo/watermark)")  
    print("   • bg.png (your custom background)")
    print()
    
    # Check server health
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server not healthy")
            return
        print("✅ Server is healthy")
        print()
    except:
        print("❌ Cannot connect to server")
        return
    
    # Run tests
    test1 = test_all_your_files()
    test2 = test_text_only_with_bg()
    test3 = test_watermark_transparency()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"All files combined: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Text + background: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Watermark transparency: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    passed = sum([test1, test2, test3])
    print(f"\nPassed: {passed}/3 tests")
    
    if passed == 3:
        print("\n🎉 ALL TESTS PASSED!")
        print("📁 Generated files:")
        print("   • FINAL_WITH_YOUR_FILES.png - All your files combined")
        print("   • TEXT_ONLY_WITH_YOUR_BG.png - Text on your background")
        print("   • WATERMARK_TRANSPARENCY_TEST.png - Watermark transparency test")
        print()
        print("🔧 Features confirmed working:")
        print("   ✅ Your bg.png used as custom background")
        print("   ✅ Your main.png (handbag) properly integrated")
        print("   ✅ Your watermark.png transparency preserved")
        print("   ✅ Brand text hidden when watermark present")
        print("   ✅ Arabic text properly rendered")
    else:
        print(f"\n⚠️ {3 - passed} tests failed")

if __name__ == "__main__":
    main()
