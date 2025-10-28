#!/usr/bin/env python3
"""
Test Upload and Generation Flow

This script demonstrates the proper workflow for:
1. Uploading images (main, watermark, background)
2. Using those images to generate Instagram posts
3. Handling both URL and filesystem paths correctly
"""

import requests
import json
import os
from PIL import Image, ImageDraw

# Configuration
API_BASE_URL = "http://localhost:5000"


def create_test_image(filename, size=(800, 800), color=(255, 100, 100), text="TEST"):
    """Create a simple test image"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)

    # Draw some text
    from PIL import ImageFont
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Draw text in center
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    draw.text(position, text, fill=(255, 255, 255), font=font)

    # Save
    img.save(filename, 'PNG')
    print(f"✅ Created test image: {filename}")
    return filename


def test_upload_endpoint(endpoint, filepath, image_type):
    """Test uploading an image to a specific endpoint"""
    print(f"\n📤 Testing upload to {endpoint}...")

    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f, 'image/png')}
        response = requests.post(f"{API_BASE_URL}{endpoint}", files=files)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful!")
        print(f"   Filename: {data['filename']}")
        print(f"   URL: {data['url']}")
        print(f"   Path: {data.get('path', 'N/A')}")
        print(f"   Size: {data['size']} bytes")
        return data
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None


def test_generation_with_uploaded_images(main_upload, watermark_upload):
    """Test generating a post using uploaded images"""
    print(f"\n🎨 Testing image generation with uploaded images...")

    # IMPORTANT: Use the 'path' field, not 'url' field
    # The 'path' field contains the filesystem path that AssetManager can load
    # The 'url' field is for serving the file via HTTP

    payload = {
        "layout_type": "headline_promo",
        "content": {
            "headline": "Summer Sale",
            "subheadline": "Up to 50% Off",
            "cta": "Shop Now"
        },
        "assets": {
            # Use 'path' from upload response for filesystem access
            "hero_image_url": main_upload.get('path') or main_upload['url'],
            "watermark_url": watermark_upload.get('path') or watermark_upload['url']
        },
        "background": {
            "mode": "gradient",
            "gradient": {
                "colors": [[255, 107, 107], [253, 187, 45]],
                "direction": "vertical"
            }
        },
        "options": {
            "remove_hero_background": False,
            "remove_watermark_background": True,
            "watermark_position": "bottom-right",
            "watermark_size": 100
        }
    }

    print(f"📋 Request payload:")
    print(f"   Hero image path: {payload['assets']['hero_image_url']}")
    print(f"   Watermark path: {payload['assets']['watermark_url']}")

    response = requests.post(
        f"{API_BASE_URL}/generate_post",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Generation successful!")
        print(f"   Layout: {data['layout_type']}")
        print(f"   Files generated: {data['total_slides']}")
        for file_info in data['generated_files']:
            print(f"   - {file_info['filename']} ({file_info['width']}x{file_info['height']})")
            print(f"     URL: {file_info['download_url']}")
        return data
    else:
        print(f"❌ Generation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None


def test_generation_with_url_paths(main_upload, watermark_upload):
    """Test what happens when using URL paths (this might fail without the fix)"""
    print(f"\n🧪 Testing generation with URL paths (old behavior)...")

    payload = {
        "layout_type": "headline_promo",
        "content": {
            "headline": "Test with URLs"
        },
        "assets": {
            # Using 'url' field instead of 'path' - this might not work
            "hero_image_url": main_upload['url'],
            "watermark_url": watermark_upload['url']
        },
        "background": {
            "mode": "solid_color",
            "color": [240, 240, 250]
        }
    }

    print(f"📋 Using URL paths:")
    print(f"   Hero: {payload['assets']['hero_image_url']}")
    print(f"   Watermark: {payload['assets']['watermark_url']}")

    response = requests.post(
        f"{API_BASE_URL}/generate_post",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        print(f"✅ Generation worked with URL paths!")
        print(f"   (Path resolution is working correctly)")
        return response.json()
    else:
        print(f"⚠️  Generation failed with URL paths: {response.status_code}")
        print(f"   This is expected if path resolution isn't working")
        return None


def main():
    """Run all tests"""
    print("="*60)
    print("🧪 UPLOAD AND GENERATION FLOW TEST")
    print("="*60)

    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print(f"⚠️  API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API")
        print(f"   Make sure the API is running at {API_BASE_URL}")
        return

    # Create test images
    print("\n📁 Creating test images...")
    os.makedirs('test_images', exist_ok=True)

    main_image = create_test_image('test_images/main.png',
                                   size=(800, 800),
                                   color=(100, 150, 255),
                                   text="MAIN")

    watermark_image = create_test_image('test_images/watermark.png',
                                        size=(200, 200),
                                        color=(255, 100, 150),
                                        text="LOGO")

    # Test uploads
    main_upload = test_upload_endpoint('/upload/main', main_image, 'main')
    if not main_upload:
        print("❌ Main upload failed, cannot continue")
        return

    watermark_upload = test_upload_endpoint('/upload/watermark', watermark_image, 'watermark')
    if not watermark_upload:
        print("❌ Watermark upload failed, cannot continue")
        return

    # Test generation with filesystem paths (should work)
    result1 = test_generation_with_uploaded_images(main_upload, watermark_upload)

    # Test generation with URL paths (should also work with enhanced path resolution)
    result2 = test_generation_with_url_paths(main_upload, watermark_upload)

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Upload main image: SUCCESS")
    print(f"✅ Upload watermark image: SUCCESS")
    print(f"{'✅' if result1 else '❌'} Generation with filesystem paths: {'SUCCESS' if result1 else 'FAILED'}")
    print(f"{'✅' if result2 else '⚠️ '} Generation with URL paths: {'SUCCESS' if result2 else 'FAILED (might need path resolution)'}")

    if result1 and result2:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Upload and generation flow is working correctly.")
    elif result1:
        print("\n⚠️  PARTIAL SUCCESS")
        print("   Filesystem paths work, but URL paths need improvement.")
        print("   Use the 'path' field from upload responses for best results.")
    else:
        print("\n❌ TESTS FAILED")
        print("   There are issues with the upload/generation flow.")


if __name__ == '__main__':
    main()
