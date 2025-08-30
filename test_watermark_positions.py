#!/usr/bin/env python3
"""
Test script to test different watermark positions for your logo
"""

import requests
import json
import os

BASE_URL = "http://localhost:5000"

def upload_files():
    """Upload the required files and return URLs"""
    print("📤 Uploading your files...")
    
    # Upload main image
    with open("../main.png", 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/main", files=files)
    main_url = response.json()['url']
    print(f"✅ Main image: {main_url}")
    
    # Upload watermark
    with open("../watermark.png", 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/watermark", files=files)
    watermark_url = response.json()['url']
    print(f"✅ Watermark: {watermark_url}")
    
    # Upload background
    with open("../bg.png", 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/background", files=files)
    bg_url = response.json()['url']
    print(f"✅ Background: {bg_url}")
    
    return main_url, watermark_url, bg_url

def test_watermark_position(position, main_url, watermark_url, bg_url):
    """Test a specific watermark position"""
    print(f"\n🎯 Testing watermark position: {position}")
    
    payload = {
        "headline": "كت‌های زمستانی جدید",
        "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
        "brand": "Fashion Store",  # Will be hidden by watermark
        "main_image_url": main_url,
        "watermark_image_url": watermark_url,
        "background_image_url": bg_url,
        "watermark_position": position
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        download_response = requests.get(data['download_url'])
        
        if download_response.status_code == 200:
            filename = f"watermark_{position.replace('-', '_')}.png"
            with open(filename, 'wb') as f:
                f.write(download_response.content)
            print(f"✅ Generated: {filename}")
            return True
    
    print(f"❌ Failed for position: {position}")
    return False

def main():
    """Test all watermark positions"""
    print("🎯 Testing Watermark Positions for Your Logo")
    print("=" * 50)
    
    # Check server
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server not healthy")
            return
        print("✅ Server is healthy")
    except:
        print("❌ Cannot connect to server")
        return
    
    # Upload files
    main_url, watermark_url, bg_url = upload_files()
    
    # Test different positions
    positions = [
        'bottom-right',   # Most common for logos
        'top-right',      # Header area
        'bottom-center',  # Footer center
        'bottom-left',    # Alternative corner
        'top-left'        # Alternative header
    ]
    
    print(f"\n🧪 Testing {len(positions)} different watermark positions...")
    results = []
    
    for position in positions:
        success = test_watermark_position(position, main_url, watermark_url, bg_url)
        results.append((position, success))
    
    # Summary
    print(f"\n📊 Position Test Results:")
    print("=" * 30)
    for position, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{position:15} : {status}")
    
    successful = sum(1 for _, success in results if success)
    print(f"\nGenerated {successful}/{len(positions)} position variants")
    
    if successful > 0:
        print(f"\n📁 Generated files:")
        for position, success in results:
            if success:
                filename = f"watermark_{position.replace('-', '_')}.png"
                print(f"   • {filename}")
        
        print(f"\n🔍 Position Guide:")
        print("   • bottom-right: Traditional logo placement (recommended)")
        print("   • top-right: Header area placement") 
        print("   • bottom-center: Footer center placement")
        print("   • bottom-left: Alternative corner")
        print("   • top-left: Alternative header")
        print()
        print("💡 Recommendation: Use 'bottom-right' for professional logo placement")
        print()
        print("🚀 To use a specific position in your API calls:")
        print('   Add: "watermark_position": "bottom-right" to your JSON payload')

if __name__ == "__main__":
    main()
