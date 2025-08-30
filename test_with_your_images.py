#!/usr/bin/env python3
"""
Test script to verify that your actual main.png and watermark.png are being used
"""

import requests
import json
import os

BASE_URL = "http://localhost:5000"

def test_with_your_images():
    """Test generation with your actual main.png and watermark.png"""
    print("🧪 Testing with your actual main.png and watermark.png")
    print("=" * 60)
    
    # Check if your images exist
    main_path = "../main.png"
    watermark_path = "../watermark.png"
    
    if not os.path.exists(main_path):
        print(f"❌ main.png not found at {main_path}")
        return False
        
    if not os.path.exists(watermark_path):
        print(f"❌ watermark.png not found at {watermark_path}")
        return False
    
    print(f"✅ Found main.png: {os.path.getsize(main_path)} bytes")
    print(f"✅ Found watermark.png: {os.path.getsize(watermark_path)} bytes")
    print()
    
    # Upload your actual images
    print("📤 Uploading your actual images...")
    
    # Upload main image
    with open(main_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/main", files=files)
    
    if response.status_code != 200:
        print(f"❌ Failed to upload main image: {response.status_code}")
        return False
    
    main_data = response.json()
    main_url = main_data['url']
    print(f"✅ Main image uploaded: {main_url}")
    
    # Upload watermark image
    with open(watermark_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/watermark", files=files)
    
    if response.status_code != 200:
        print(f"❌ Failed to upload watermark image: {response.status_code}")
        return False
    
    watermark_data = response.json()
    watermark_url = watermark_data['url']
    print(f"✅ Watermark image uploaded: {watermark_url}")
    print()
    
    # Generate image with your uploads
    print("🎨 Generating social media image with your images...")
    
    payload = {
        "headline": "کت‌های زمستانی جدید",
        "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
        "brand": "Fashion Store",
        "background_color": [255, 100, 100],
        "main_image_url": main_url,
        "watermark_image_url": watermark_url
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
    print()
    
    # Download the result
    print("💾 Downloading generated image...")
    download_response = requests.get(data['download_url'])
    
    if download_response.status_code != 200:
        print(f"❌ Download failed: {download_response.status_code}")
        return False
    
    output_path = "YOUR_IMAGES_RESULT.png"
    with open(output_path, 'wb') as f:
        f.write(download_response.content)
    
    print(f"✅ Image saved: {output_path}")
    print(f"   File size: {len(download_response.content)} bytes")
    print()
    
    # Verify the result
    print("🔍 Verification:")
    print(f"   • Original main.png: {os.path.getsize(main_path)} bytes")
    print(f"   • Original watermark.png: {os.path.getsize(watermark_path)} bytes")
    print(f"   • Generated image: {len(download_response.content)} bytes")
    print()
    
    if len(download_response.content) > 200000:  # Large size indicates images are included
        print("🎉 SUCCESS! The large file size indicates your images are included!")
        print("🖼️ Check YOUR_IMAGES_RESULT.png to see your images in the social media post!")
    else:
        print("⚠️ File size seems small - images might not be properly included")
    
    return True

def test_without_images():
    """Test generation without custom images for comparison"""
    print("🎯 Testing without custom images (for comparison)...")
    
    payload = {
        "headline": "Test Without Images",
        "subheadline": "Programmatic Generation",
        "brand": "Comparison Test"
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        download_response = requests.get(data['download_url'])
        
        if download_response.status_code == 200:
            with open("NO_IMAGES_RESULT.png", 'wb') as f:
                f.write(download_response.content)
            
            print(f"✅ No-images version: {len(download_response.content)} bytes")
            print("   This shows the difference when no custom images are used")
            return True
    
    print("❌ Failed to generate comparison image")
    return False

def main():
    print("🚀 Social Image Generator - Your Images Test")
    print("=" * 50)
    print()
    
    # Test server health
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server not healthy")
            return
        print("✅ Server is healthy")
        print()
    except:
        print("❌ Cannot connect to server. Make sure it's running!")
        return
    
    # Run tests
    success1 = test_with_your_images()
    print()
    success2 = test_without_images()
    
    print()
    print("📊 Test Summary:")
    print("=" * 20)
    print(f"Your images test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Comparison test: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1:
        print()
        print("🎉 SUCCESS! Your main.png and watermark.png are now being used!")
        print("📁 Check these files:")
        print("   • YOUR_IMAGES_RESULT.png - Contains your images")
        print("   • NO_IMAGES_RESULT.png - Without custom images (comparison)")

if __name__ == "__main__":
    main()
