#!/usr/bin/env python3
"""
Production Deployment Test Script
Tests the deployed Instagram image generator at https://imageeditor.flowiran.ir/

This script will:
1. Check system health
2. List available layouts
3. Test each layout type with sample requests
4. Save generated images to local directory
5. Provide comprehensive test results
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime

# Deployed system URL
BASE_URL = "https://imageeditor.flowiran.ir"

# Output directory for generated images
OUTPUT_DIR = Path("./production_test_outputs")
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


def test_health():
    """Test the /health endpoint"""
    print_header("TEST 1: System Health Check")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print_success(f"System is healthy!")
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
    """Test the /layouts endpoint"""
    print_header("TEST 2: Available Layouts")

    try:
        response = requests.get(f"{BASE_URL}/layouts", timeout=10)

        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            layouts = data.get('layouts', {})

            print_success(f"Found {count} available layouts")

            for layout_type, info in layouts.items():
                print_info(f"  • {layout_type}: {info.get('description', 'No description')}")

            return layouts
        else:
            print_error(f"Layouts endpoint failed: {response.status_code}")
            return {}

    except Exception as e:
        print_error(f"Layouts error: {str(e)}")
        return {}


def test_layout(name, config, layout_type):
    """Test a specific layout configuration"""
    print(f"\n  Testing: {name}...")

    try:
        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{layout_type}_{name}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            print_success(f"{name}: Image saved to {filepath} ({len(response.content)} bytes)")
            return True
        else:
            print_error(f"{name}: Failed with status {response.status_code}")
            print_error(f"  Error: {response.text[:200]}")
            return False

    except Exception as e:
        print_error(f"{name}: Error - {str(e)}")
        return False


def test_all_layouts():
    """Test all layout types with sample configurations"""
    print_header("TEST 3: Layout Generation Tests")

    results = {}

    # Test 1: headline_promo
    print("\n📋 Testing headline_promo layout...")
    results['headline_promo'] = []

    results['headline_promo'].append(test_layout(
        "basic",
        {
            "layout_type": "headline_promo",
            "content": {
                "headline": "Summer Sale 2024",
                "subheadline": "Up to 50% off everything",
                "cta_text": "Shop Now"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 200, 150], [255, 150, 200]],
                    "direction": "diagonal"
                }
            }
        },
        "headline_promo"
    ))

    results['headline_promo'].append(test_layout(
        "farsi",
        {
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
        },
        "headline_promo"
    ))

    # Test 2: split_image_text
    print("\n📋 Testing split_image_text layout...")
    results['split_image_text'] = []

    results['split_image_text'].append(test_layout(
        "basic",
        {
            "layout_type": "split_image_text",
            "content": {
                "title": "Premium Features",
                "description": "Everything you need in one place",
                "bullets": ["Fast Performance", "Easy to Use", "Secure"]
            },
            "assets": {
                "hero_image_url": "https://picsum.photos/800/1000?random=1"
            },
            "background": {
                "mode": "solid_color",
                "color": [255, 255, 255]
            }
        },
        "split_image_text"
    ))

    # Test 3: product_showcase
    print("\n📋 Testing product_showcase layout...")
    results['product_showcase'] = []

    results['product_showcase'].append(test_layout(
        "basic",
        {
            "layout_type": "product_showcase",
            "content": {
                "product_name": "Smart Watch Pro",
                "price": "$299",
                "description": "Advanced fitness tracking with 7-day battery life",
                "cta_text": "Buy Now"
            },
            "assets": {
                "hero_image_url": "https://picsum.photos/600/600?random=2"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[240, 240, 250], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        },
        "product_showcase"
    ))

    # Test 4: checklist
    print("\n📋 Testing checklist layout...")
    results['checklist'] = []

    results['checklist'].append(test_layout(
        "basic",
        {
            "layout_type": "checklist",
            "content": {
                "title": "5 Tips for Better Design",
                "items": [
                    "Keep it simple and clean",
                    "Use consistent typography",
                    "Test with real users",
                    "Focus on user needs",
                    "Iterate based on feedback"
                ],
                "brand": "Design Studio"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 247, 230], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        },
        "checklist"
    ))

    # Test 5: testimonial
    print("\n📋 Testing testimonial layout...")
    results['testimonial'] = []

    results['testimonial'].append(test_layout(
        "basic",
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "This product changed my life! The quality is outstanding.",
                "name": "Sarah Johnson",
                "title": "Marketing Director",
                "rating": 5
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[250, 250, 255], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        },
        "testimonial"
    ))

    # Test 6: overlay_text
    print("\n📋 Testing overlay_text layout...")
    results['overlay_text'] = []

    results['overlay_text'].append(test_layout(
        "basic",
        {
            "layout_type": "overlay_text",
            "content": {
                "text": "Every day is a new beginning",
                "subtitle": "Make it count"
            },
            "assets": {
                "background_image_url": "https://picsum.photos/1080/1350?random=3"
            },
            "options": {
                "text_position": "center",
                "overlay_opacity": 0.5
            }
        },
        "overlay_text"
    ))

    # Test 7: caption_box
    print("\n📋 Testing caption_box layout...")
    results['caption_box'] = []

    results['caption_box'].append(test_layout(
        "basic",
        {
            "layout_type": "caption_box",
            "content": {
                "title": "New Collection",
                "caption": "Discover our latest summer collection featuring bold colors",
                "brand": "Fashion Studio"
            },
            "assets": {
                "hero_image_url": "https://picsum.photos/1080/800?random=4"
            },
            "options": {
                "layout_style": "bottom_box",
                "image_ratio": 0.65
            }
        },
        "caption_box"
    ))

    return results


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")

    total_tests = 0
    passed_tests = 0

    for layout_type, tests in results.items():
        layout_passed = sum(tests)
        layout_total = len(tests)
        total_tests += layout_total
        passed_tests += layout_passed

        status = "✅" if layout_passed == layout_total else "⚠️"
        print(f"{status} {layout_type}: {layout_passed}/{layout_total} passed")

    print(f"\n{'='*70}")
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print_success("🎉 All tests passed! Production system is working perfectly!")
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) failed")

    print(f"\n📁 Generated images saved to: {OUTPUT_DIR.absolute()}")
    print('='*70)


def main():
    """Main test runner"""
    print_header("🚀 Production Deployment Test Suite")
    print_info(f"Testing: {BASE_URL}")
    print_info(f"Output: {OUTPUT_DIR.absolute()}")

    # Test 1: Health check
    if not test_health():
        print_error("\n❌ System health check failed. Aborting tests.")
        return 1

    # Test 2: List layouts
    layouts = test_layouts()
    if not layouts:
        print_error("\n❌ No layouts available. Aborting tests.")
        return 1

    # Test 3: Generate images with each layout
    results = test_all_layouts()

    # Print summary
    print_summary(results)

    return 0


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
