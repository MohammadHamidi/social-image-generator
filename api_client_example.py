#!/usr/bin/env python3
"""
Example API Client for Social Image Generator
Demonstrates how to upload images and generate social media images using the API.
"""

import requests
import json
import os
from pathlib import Path

# Server configuration
BASE_URL = "http://localhost:5000"

def check_server_health():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Run: python run_server.py")
        return False

def upload_main_image(image_path):
    """Upload main image and return the URL"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None

    print(f"📤 Uploading main image: {image_path}")

    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/main", files=files)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Main image uploaded: {data['url']}")
        return data['url']
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return None

def upload_watermark_image(image_path):
    """Upload watermark image and return the URL"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None

    print(f"📤 Uploading watermark image: {image_path}")

    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/watermark", files=files)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Watermark image uploaded: {data['url']}")
        return data['url']
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return None

def generate_social_image(headline, subheadline, brand, main_image_url=None, watermark_image_url=None, background_color=[255, 255, 255]):
    """Generate social media image using the API"""
    print("🎨 Generating social media image...")

    payload = {
        "headline": headline,
        "subheadline": subheadline,
        "brand": brand,
        "background_color": background_color
    }

    if main_image_url:
        payload["main_image_url"] = main_image_url

    if watermark_image_url:
        payload["watermark_image_url"] = watermark_image_url

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("✅ Image generated successfully!")
        print(f"📥 Download URL: {data['download_url']}")
        print(f"📏 File size: {data['size']} bytes")

        # Download the generated image
        download_response = requests.get(data['download_url'])
        if download_response.status_code == 200:
            output_path = f"generated_social_image_{data['filename']}"
            with open(output_path, 'wb') as f:
                f.write(download_response.content)
            print(f"💾 Image saved locally: {output_path}")
            return output_path
        else:
            print("❌ Failed to download generated image")
            return None
    else:
        print(f"❌ Generation failed: {response.status_code}")
        print(response.text)
        return None

def demo_workflow():
    """Complete demo workflow"""
    print("🚀 Social Image Generator API Demo")
    print("=" * 50)

    # Check server
    if not check_server_health():
        return

    # Use existing images from assets/custom
    main_image_path = "assets/custom/main_section.png"
    watermark_image_path = "assets/custom/blueprint.png"

    # Upload images
    main_url = upload_main_image(main_image_path)
    watermark_url = upload_watermark_image(watermark_image_path)

    if not main_url:
        print("❌ Cannot proceed without main image")
        return

    print()

    # Generate image
    headline = "کت‌های زمستانی جدید"
    subheadline = "مجموعه‌ای از بهترین طراحی‌ها"
    brand = "Fashion Store"

    generated_path = generate_social_image(
        headline=headline,
        subheadline=subheadline,
        brand=brand,
        main_image_url=main_url,
        watermark_image_url=watermark_url,
        background_color=[255, 255, 255]
    )

    if generated_path:
        print()
        print("🎉 Demo completed successfully!")
        print(f"📁 Generated image: {generated_path}")
        print("You can now use this image for social media!")
    else:
        print("❌ Demo failed")

def show_api_usage():
    """Show API usage examples"""
    print("📚 API Usage Examples")
    print("=" * 30)

    print("1. Upload Main Image:")
    print("   curl -X POST -F 'file=@main.png' http://localhost:5000/upload/main")
    print()

    print("2. Upload Watermark Image:")
    print("   curl -X POST -F 'file=@watermark.png' http://localhost:5000/upload/watermark")
    print()

    print("3. Generate Image:")
    print('''   curl -X POST http://localhost:5000/generate \\
     -H "Content-Type: application/json" \\
     -d '{
       "headline": "کت‌های زمستانی جدید",
       "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
       "brand": "Fashion Store",
       "background_color": [255, 255, 255],
       "main_image_url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png",
       "watermark_image_url": "http://localhost:5000/uploads/watermark/20240101_120001_def456.png"
     }' ''')
    print()

    print("4. Check Server Health:")
    print("   curl http://localhost:5000/health")
    print()

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Social Image Generator API Client')
    parser.add_argument('--demo', action='store_true', help='Run complete demo workflow')
    parser.add_argument('--examples', action='store_true', help='Show API usage examples')

    args = parser.parse_args()

    if args.examples:
        show_api_usage()
    elif args.demo:
        demo_workflow()
    else:
        print("Social Image Generator API Client")
        print("Usage:")
        print("  python api_client_example.py --demo      # Run complete demo")
        print("  python api_client_example.py --examples  # Show API examples")
        print()
        print("Make sure the server is running:")
        print("  python run_server.py")

if __name__ == '__main__':
    main()
