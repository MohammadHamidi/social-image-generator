#!/usr/bin/env python3
"""
LOCAL Server Test - Verify code works before deploying to production

This tests your LOCAL server (localhost:5000) to ensure all features work
before you deploy to production.

Usage:
1. Start your local server: python social_image_api.py
2. Run this script: python test_local_server.py
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime
import time

# LOCAL server URL
BASE_URL = "http://localhost:5000"

# Output directory for generated images
OUTPUT_DIR = Path("./local_test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print('='*70)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def check_server_running():
    """Check if local server is running"""
    print_header("STEP 1: Check if Local Server is Running")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Local server is running!")
            return True
        else:
            print_error(f"Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to local server!")
        print_info("Please start the server with: python social_image_api.py")
        return False
    except Exception as e:
        print_error(f"Error checking server: {str(e)}")
        return False


def test_health():
    """Test the /health endpoint"""
    print_header("STEP 2: Test /health Endpoint")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print_success("Health endpoint works!")
            print_info(f"Status: {data.get('status', 'unknown')}")
            print_info(f"Version: {data.get('version', 'unknown')}")

            if 'system' in data:
                print_info(f"Platform: {data['system'].get('platform', 'unknown')}")
                print_info(f"Generation Ready: {data['system'].get('generation_ready', False)}")

            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False


def test_layouts():
    """Test the /layouts endpoint - THIS IS THE NEW ENDPOINT"""
    print_header("STEP 3: Test /layouts Endpoint (NEW)")

    try:
        response = requests.get(f"{BASE_URL}/layouts", timeout=10)

        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            layouts = data.get('layouts', {})

            print_success(f"✅ /layouts endpoint works! Found {count} layouts")

            for layout_type, info in layouts.items():
                print_info(f"  • {layout_type}: {info.get('description', 'No description')}")

            return layouts
        elif response.status_code == 404:
            print_error("❌ /layouts endpoint returns 404!")
            print_error("This means you're running OLD code.")
            print_info("Solution: Make sure you're on the correct branch:")
            print_info("  git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
            print_info("  python social_image_api.py")
            return {}
        else:
            print_error(f"Layouts endpoint failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return {}

    except Exception as e:
        print_error(f"Layouts error: {str(e)}")
        return {}


def test_generate_post():
    """Test the /generate_post endpoint - THIS IS THE NEW ENDPOINT"""
    print_header("STEP 4: Test /generate_post Endpoint (NEW)")

    test_config = {
        "layout_type": "headline_promo",
        "content": {
            "headline": "Local Test",
            "subheadline": "Testing before production deploy"
        },
        "background": {
            "mode": "gradient",
            "gradient": {
                "colors": [[255, 200, 150], [255, 150, 200]],
                "direction": "vertical"
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=test_config,
            timeout=30
        )

        if response.status_code == 200:
            # Save test image
            filepath = OUTPUT_DIR / "test_generate_post.png"
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print_success("✅ /generate_post endpoint works!")
            print_info(f"Image saved to: {filepath}")
            print_info(f"Size: {len(response.content)} bytes")
            return True
        elif response.status_code == 404:
            print_error("❌ /generate_post endpoint returns 404!")
            print_error("This means you're running OLD code.")
            return False
        else:
            print_error(f"Generation failed: {response.status_code}")
            print_error(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_farsi_text():
    """Test Farsi text rendering"""
    print_header("STEP 5: Test Farsi/RTL Text Support")

    test_config = {
        "layout_type": "headline_promo",
        "content": {
            "headline": "فروش ویژه تابستان",
            "subheadline": "تخفیف تا ۵۰ درصد",
            "cta_text": "خرید کنید"
        },
        "background": {
            "mode": "gradient",
            "gradient": {
                "colors": [[230, 240, 255], [255, 230, 240]],
                "direction": "vertical"
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=test_config,
            timeout=30
        )

        if response.status_code == 200:
            filepath = OUTPUT_DIR / "test_farsi.png"
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print_success("✅ Farsi text works!")
            print_info(f"Image saved to: {filepath}")
            return True
        else:
            print_error(f"Farsi test failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_all_layouts():
    """Test all 7 layout types"""
    print_header("STEP 6: Test All Layout Types")

    layouts_to_test = [
        {
            "name": "headline_promo",
            "config": {
                "layout_type": "headline_promo",
                "content": {"headline": "Test"},
                "background": {"mode": "gradient", "gradient": {"colors": [[255,200,150], [255,150,200]], "direction": "vertical"}}
            }
        },
        {
            "name": "split_image_text",
            "config": {
                "layout_type": "split_image_text",
                "content": {"title": "Test", "description": "Test description"},
                "assets": {"hero_image_url": "https://picsum.photos/800/1000?random=1"},
                "background": {"mode": "solid_color", "color": [255, 255, 255]}
            }
        },
        {
            "name": "product_showcase",
            "config": {
                "layout_type": "product_showcase",
                "content": {"product_name": "Test Product", "price": "$99", "description": "Test"},
                "assets": {"hero_image_url": "https://picsum.photos/600/600?random=2"},
                "background": {"mode": "gradient", "gradient": {"colors": [[240,240,250], [255,255,255]], "direction": "vertical"}}
            }
        },
        {
            "name": "checklist",
            "config": {
                "layout_type": "checklist",
                "content": {"title": "Test List", "items": ["Item 1", "Item 2", "Item 3"]},
                "background": {"mode": "gradient", "gradient": {"colors": [[255,247,230], [255,255,255]], "direction": "vertical"}}
            }
        },
        {
            "name": "testimonial",
            "config": {
                "layout_type": "testimonial",
                "content": {"quote": "Great product!", "name": "Test User", "rating": 5},
                "background": {"mode": "gradient", "gradient": {"colors": [[250,250,255], [255,255,255]], "direction": "vertical"}}
            }
        },
        {
            "name": "overlay_text",
            "config": {
                "layout_type": "overlay_text",
                "content": {"text": "Test Overlay", "subtitle": "Subtitle"},
                "assets": {"background_image_url": "https://picsum.photos/1080/1350?random=3"},
                "options": {"text_position": "center", "overlay_opacity": 0.5}
            }
        },
        {
            "name": "caption_box",
            "config": {
                "layout_type": "caption_box",
                "content": {"title": "Test", "caption": "Test caption"},
                "assets": {"hero_image_url": "https://picsum.photos/1080/800?random=4"},
                "options": {"layout_style": "bottom_box", "image_ratio": 0.65}
            }
        }
    ]

    results = {}

    for layout in layouts_to_test:
        name = layout["name"]
        config = layout["config"]

        print(f"\n  Testing {name}...")

        try:
            response = requests.post(
                f"{BASE_URL}/generate_post",
                json=config,
                timeout=30
            )

            if response.status_code == 200:
                filepath = OUTPUT_DIR / f"test_{name}.png"
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print_success(f"{name}: OK ({len(response.content)} bytes)")
                results[name] = True
            else:
                print_error(f"{name}: Failed ({response.status_code})")
                print_error(f"  Error: {response.text[:200]}")
                results[name] = False

        except Exception as e:
            print_error(f"{name}: Error - {str(e)}")
            results[name] = False

    return results


def print_final_summary(all_passed):
    """Print final summary and next steps"""
    print_header("FINAL SUMMARY")

    if all_passed:
        print_success("🎉 ALL TESTS PASSED!")
        print("")
        print("✅ Your local code is working perfectly!")
        print("✅ All 7 layouts are functioning correctly")
        print("✅ Farsi/RTL text support works")
        print("✅ Both new endpoints (/layouts and /generate_post) work")
        print("")
        print("="*70)
        print("  READY FOR PRODUCTION DEPLOYMENT")
        print("="*70)
        print("")
        print("Your code is VERIFIED and ready to deploy!")
        print("")
        print("📋 Next Steps:")
        print("  1. Commit any remaining changes:")
        print("     git add .")
        print("     git commit -m 'Final verified version'")
        print("     git push")
        print("")
        print("  2. Deploy to production (choose one):")
        print("")
        print("     Option A - Direct deploy from feature branch:")
        print("       ssh your-server")
        print("       cd /path/to/app")
        print("       git fetch origin")
        print("       git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
        print("       git pull")
        print("       # Restart server (e.g., systemctl restart app)")
        print("")
        print("     Option B - Merge to main first:")
        print("       1. Create PR on GitHub")
        print("       2. Merge to main")
        print("       3. Deploy main branch")
        print("")
        print("  3. After deployment, test production:")
        print("     python test_production_deployment.py")
        print("")
        print(f"📁 Test images saved to: {OUTPUT_DIR.absolute()}")
    else:
        print_error("⚠️  SOME TESTS FAILED")
        print("")
        print("Your local code has issues that need to be fixed.")
        print("DO NOT deploy to production until all tests pass.")
        print("")
        print("Check the errors above and fix them first.")


def main():
    """Main test runner"""
    print("="*70)
    print("  🧪 LOCAL SERVER VERIFICATION")
    print("  Test code before deploying to production")
    print("="*70)
    print(f"\nTesting: {BASE_URL}")
    print(f"Output: {OUTPUT_DIR.absolute()}")

    # Check if server is running
    if not check_server_running():
        print("")
        print("="*70)
        print("  ❌ LOCAL SERVER NOT RUNNING")
        print("="*70)
        print("")
        print("Start your local server first:")
        print("  1. python social_image_api.py")
        print("  2. Wait for it to start (you'll see: 'Running on http://127.0.0.1:5000')")
        print("  3. Run this test again: python test_local_server.py")
        print("")
        return 1

    # Test health
    if not test_health():
        return 1

    # Test layouts endpoint (NEW)
    layouts = test_layouts()
    if not layouts:
        print("")
        print("="*70)
        print("  ❌ WRONG CODE VERSION")
        print("="*70)
        print("")
        print("Your local server is running OLD code without the layout engine.")
        print("")
        print("Solution:")
        print("  1. Stop the server (Ctrl+C)")
        print("  2. Make sure you're on the right branch:")
        print("     git status")
        print("     (should show: claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u)")
        print("")
        print("  3. If not, checkout the branch:")
        print("     git checkout claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
        print("")
        print("  4. Start server again:")
        print("     python social_image_api.py")
        print("")
        return 1

    # Test generate_post endpoint (NEW)
    if not test_generate_post():
        return 1

    # Test Farsi
    if not test_farsi_text():
        return 1

    # Test all layouts
    layout_results = test_all_layouts()

    # Check if all passed
    all_passed = all(layout_results.values())

    # Print summary
    print_final_summary(all_passed)

    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
