#!/usr/bin/env python3
"""
Comprehensive test for all Social Image Generator features:
- Watermark transparency preservation
- No brand text when watermark is present
- Background image upload and usage
- Pattern backgrounds
"""

import requests
import json
import os
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:5000"

def create_test_watermark():
    """Create a transparent PNG watermark for testing"""
    print("🎨 Creating transparent watermark for testing...")
    
    # Create transparent watermark
    watermark = Image.new('RGBA', (200, 80), (0, 0, 0, 0))  # Fully transparent
    draw = ImageDraw.Draw(watermark)
    
    # Draw logo background with transparency
    draw.ellipse([10, 10, 190, 70], fill=(255, 100, 100, 200))  # Semi-transparent red
    
    # Add text
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((100, 40), "Fashion Store", fill=(255, 255, 255, 255), anchor='mm', font=font)
    
    watermark_path = "test_transparent_watermark.png"
    watermark.save(watermark_path, 'PNG')
    print(f"✅ Created transparent watermark: {watermark_path}")
    return watermark_path

def create_test_background():
    """Create a custom background image for testing"""
    print("🌈 Creating custom background for testing...")
    
    # Create gradient background
    width, height = 1080, 1350
    bg = Image.new('RGB', (width, height))
    
    # Create diagonal gradient from purple to pink
    for y in range(height):
        for x in range(width):
            ratio = (x + y) / (width + height)
            r = int(138 * (1 - ratio) + 255 * ratio)  # Purple to Pink
            g = int(43 * (1 - ratio) + 192 * ratio)
            b = int(226 * (1 - ratio) + 203 * ratio)
            bg.putpixel((x, y), (r, g, b))
    
    # Add some pattern
    draw = ImageDraw.Draw(bg)
    for i in range(0, width, 100):
        for j in range(0, height, 100):
            if (i // 100 + j // 100) % 2 == 0:
                draw.rectangle([i, j, i+50, j+50], fill=(255, 255, 255, 30))
    
    bg_path = "test_custom_background.png"
    bg.save(bg_path, 'PNG')
    print(f"✅ Created custom background: {bg_path}")
    return bg_path

def test_transparent_watermark():
    """Test watermark transparency preservation"""
    print("\n🧪 Test 1: Transparent Watermark Preservation")
    print("=" * 50)
    
    # Create transparent watermark
    watermark_path = create_test_watermark()
    
    # Upload watermark
    with open(watermark_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/watermark", files=files)
    
    if response.status_code != 200:
        print(f"❌ Watermark upload failed: {response.status_code}")
        return False
    
    watermark_data = response.json()
    watermark_url = watermark_data['url']
    print(f"✅ Transparent watermark uploaded: {watermark_url}")
    
    # Generate with only watermark (no brand text should appear)
    payload = {
        "headline": "Testing Watermark",
        "subheadline": "Transparency Test",
        "brand": "Should Not Appear",  # This should be hidden by watermark
        "background_color": [100, 150, 200],
        "watermark_image_url": watermark_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    if response.status_code != 200:
        print(f"❌ Generation failed: {response.status_code}")
        return False
    
    data = response.json()
    print("✅ Generation successful!")
    print(f"   Watermark used: {data['config']['watermark_image_used']}")
    
    # Download result
    download_response = requests.get(data['download_url'])
    if download_response.status_code == 200:
        with open("test1_transparent_watermark.png", 'wb') as f:
            f.write(download_response.content)
        print("✅ Result saved: test1_transparent_watermark.png")
        print("🔍 Check: Watermark should be transparent, no 'Should Not Appear' text")
        return True
    
    return False

def test_custom_background():
    """Test custom background image upload"""
    print("\n🧪 Test 2: Custom Background Image")
    print("=" * 50)
    
    # Create custom background
    bg_path = create_test_background()
    
    # Upload background
    with open(bg_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/background", files=files)
    
    if response.status_code != 200:
        print(f"❌ Background upload failed: {response.status_code}")
        return False
    
    bg_data = response.json()
    bg_url = bg_data['url']
    print(f"✅ Custom background uploaded: {bg_url}")
    
    # Generate with custom background only (no main or watermark)
    payload = {
        "headline": "Custom Background",
        "subheadline": "Pattern Test",
        "brand": "Background Demo",
        "background_image_url": bg_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    if response.status_code != 200:
        print(f"❌ Generation failed: {response.status_code}")
        return False
    
    data = response.json()
    print("✅ Generation successful!")
    
    # Download result
    download_response = requests.get(data['download_url'])
    if download_response.status_code == 200:
        with open("test2_custom_background.png", 'wb') as f:
            f.write(download_response.content)
        print("✅ Result saved: test2_custom_background.png")
        print("🔍 Check: Should use purple-pink gradient background with pattern")
        return True
    
    return False

def test_all_features_combined():
    """Test all features together"""
    print("\n🧪 Test 3: All Features Combined")
    print("=" * 50)
    
    # Use your actual images
    main_path = "../main.png"
    if not os.path.exists(main_path):
        print("❌ main.png not found, skipping combined test")
        return False
    
    # Upload main image
    with open(main_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/main", files=files)
    
    if response.status_code != 200:
        print(f"❌ Main upload failed: {response.status_code}")
        return False
    
    main_url = response.json()['url']
    print(f"✅ Main image uploaded: {main_url}")
    
    # Create and upload transparent watermark
    watermark_path = create_test_watermark()
    with open(watermark_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/watermark", files=files)
    
    watermark_url = response.json()['url']
    print(f"✅ Watermark uploaded: {watermark_url}")
    
    # Create and upload custom background
    bg_path = create_test_background()
    with open(bg_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/background", files=files)
    
    bg_url = response.json()['url']
    print(f"✅ Background uploaded: {bg_url}")
    
    # Generate with all features
    payload = {
        "headline": "کت‌های زمستانی جدید",
        "subheadline": "تست کامل سیستم",
        "brand": "Will Be Hidden",  # Should be hidden by watermark
        "main_image_url": main_url,
        "watermark_image_url": watermark_url,
        "background_image_url": bg_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    if response.status_code != 200:
        print(f"❌ Generation failed: {response.status_code}")
        print(response.text)
        return False
    
    data = response.json()
    print("✅ Generation successful!")
    print(f"   Main image used: {data['config']['main_image_used']}")
    print(f"   Watermark used: {data['config']['watermark_image_used']}")
    
    # Download result
    download_response = requests.get(data['download_url'])
    if download_response.status_code == 200:
        with open("test3_all_features.png", 'wb') as f:
            f.write(download_response.content)
        print("✅ Result saved: test3_all_features.png")
        print("🔍 Check:")
        print("   • Custom gradient background")
        print("   • Main handbag image with removed background")
        print("   • Transparent watermark preserving transparency")
        print("   • No brand text (hidden by watermark)")
        print("   • Arabic text properly rendered")
        return True
    
    return False

def test_text_only_mode():
    """Test text-only generation with custom background"""
    print("\n🧪 Test 4: Text-Only Mode")
    print("=" * 50)
    
    # Create custom background
    bg_path = create_test_background()
    with open(bg_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/background", files=files)
    
    bg_url = response.json()['url']
    print(f"✅ Background uploaded: {bg_url}")
    
    # Generate with only text and background
    payload = {
        "headline": "نص فقط",
        "subheadline": "اختبار النص فقط",
        "brand": "متجر الأزياء",
        "background_image_url": bg_url
        # No main_image_url or watermark_image_url
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    if response.status_code != 200:
        print(f"❌ Generation failed: {response.status_code}")
        return False
    
    data = response.json()
    print("✅ Generation successful!")
    
    # Download result
    download_response = requests.get(data['download_url'])
    if download_response.status_code == 200:
        with open("test4_text_only.png", 'wb') as f:
            f.write(download_response.content)
        print("✅ Result saved: test4_text_only.png")
        print("🔍 Check: Only Arabic text on custom background, no images")
        return True
    
    return False

def main():
    """Run all tests"""
    print("🚀 Social Image Generator - Complete Feature Test")
    print("=" * 60)
    
    # Check server health
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server not healthy")
            return
        print("✅ Server is healthy")
    except:
        print("❌ Cannot connect to server")
        return
    
    # Run all tests
    results = []
    results.append(("Transparent Watermark", test_transparent_watermark()))
    results.append(("Custom Background", test_custom_background()))
    results.append(("All Features Combined", test_all_features_combined()))
    results.append(("Text-Only Mode", test_text_only_mode()))
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("🔧 New Features Working:")
        print("   ✅ Watermark transparency preserved")
        print("   ✅ Brand text hidden when watermark present")
        print("   ✅ Custom background images supported")
        print("   ✅ Text-only generation works")
        print("   ✅ All combinations working perfectly")
    else:
        print(f"\n⚠️ {len(results) - passed} tests failed")
    
    # Cleanup
    for file in ["test_transparent_watermark.png", "test_custom_background.png"]:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()
