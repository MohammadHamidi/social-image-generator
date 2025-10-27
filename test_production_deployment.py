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

import sys
import io
import requests
import json
import os
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# Deployed system URL
BASE_URL = "http://localhost:5000"

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
    print(f"[OK] {text}")


def print_error(text):
    """Print error message"""
    print(f"[ERROR] {text}")


def print_info(text):
    """Print info message"""
    print(f"[INFO] {text}")


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
    """Test the /text_layout_info endpoint"""
    print_header("TEST 2: Available Layouts")

    try:
        response = requests.get(f"{BASE_URL}/text_layout_info", timeout=10)

        if response.status_code == 200:
            data = response.json()
            layouts = data.get('text_layouts', {})

            print_success(f"Found {len(layouts)} available text layouts")

            for layout_type, info in layouts.items():
                print_info(f"  • {layout_type}: {info.get('description', 'No description')}")

            return layouts
        else:
            print_error(f"Text layout info endpoint failed: {response.status_code}")
            return {}

    except Exception as e:
        print_error(f"Text layout info error: {str(e)}")
        return {}


def test_layout(name, config, layout_type):
    """Test a specific layout configuration"""
    print(f"\n  Testing: {name}...")

    try:
        response = requests.post(
            f"{BASE_URL}/generate_text",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            # Check if response is JSON (metadata) or image
            try:
                data = response.json()
                if 'download_url' in data:
                    # It's a JSON response with download URL
                    download_url = f"{BASE_URL}{data['download_url']}"
                    image_response = requests.get(download_url, timeout=30)
                    if image_response.status_code == 200:
                        image_content = image_response.content
                    else:
                        print_error(f"{name}: Failed to download image from {download_url}")
                        return False
                else:
                    print_error(f"{name}: Unexpected JSON response format")
                    return False
            except ValueError:
                # Response is already an image
                image_content = response.content

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{layout_type}_{name}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(image_content)

            print_success(f"{name}: Image saved to {filepath} ({len(image_content)} bytes)")
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

    # Test 1: announcement
    print("\n[TEST] Testing announcement layout...")
    results['announcement'] = []

    results['announcement'].append(test_layout(
        "english",
        {
            "layout_type": "announcement",
            "content": {
                "title": "New Product Launch",
                "description": "Revolutionary innovation for your workflow that will transform how you work",
                "cta": "Learn More",
                "brand": "Innovation Co."
            },
            "background_color": [255, 255, 255]
        },
        "announcement"
    ))

    results['announcement'].append(test_layout(
        "farsi",
        {
            "layout_type": "announcement",
            "content": {
                "title": "راه‌اندازی محصول جدید",
                "description": "نوآوری انقلابی برای گردش کار شما که نحوه کار شما را متحول خواهد کرد",
                "cta": "بیشتر بدانید",
                "brand": "شرکت نوآوری"
            },
            "background_color": [240, 240, 250]
        },
        "announcement"
    ))

    # Gradient backgrounds
    results['announcement'].append(test_layout(
        "gradient_english",
        {
            "layout_type": "announcement",
            "content": {
                "title": "Summer Sale 2024",
                "description": "Amazing deals on premium products with up to 50% discount",
                "cta": "Shop Now",
                "brand": "Premium Store"
            },
            "background_color": [255, 200, 150]
        },
        "announcement"
    ))

    results['announcement'].append(test_layout(
        "gradient_farsi",
        {
            "layout_type": "announcement",
            "content": {
                "title": "فروش ویژه تابستان",
                "description": "تخفیفات شگفت‌انگیز بر روی محصولات باکیفیت تا ۵۰ درصد تخفیف",
                "cta": "همین الان خرید کنید",
                "brand": "فروشگاه پریمیوم"
            },
            "background_color": [255, 220, 180]
        },
        "announcement"
    ))

    # Test 2: article
    print("\n[TEST] Testing article layout...")
    results['article'] = []

    results['article'].append(test_layout(
        "english",
        {
            "layout_type": "article",
            "content": {
                "title": "The Future of Technology",
                "body": "Artificial intelligence is transforming every industry and changing how we work, communicate, and solve complex problems.",
                "brand": "Tech Insights"
            },
            "background_color": [250, 250, 255]
        },
        "article"
    ))

    results['article'].append(test_layout(
        "farsi",
        {
            "layout_type": "article",
            "content": {
                "title": "آینده فناوری",
                "body": "هوش مصنوعی در حال تبدیل هر صنعتی است و نحوه کار، ارتباط و حل مشکلات پیچیده ما را تغییر می‌دهد.",
                "brand": "بینش فناوری"
            },
            "background_color": [255, 250, 245]
        },
        "article"
    ))

    results['article'].append(test_layout(
        "gradient_english",
        {
            "layout_type": "article",
            "content": {
                "title": "Innovation in Design",
                "body": "Modern design principles focus on user experience, simplicity, and accessibility. Great design solves real problems and creates meaningful connections.",
                "brand": "Design Lab"
            },
            "background_color": [230, 240, 255]
        },
        "article"
    ))

    results['article'].append(test_layout(
        "gradient_farsi",
        {
            "layout_type": "article",
            "content": {
                "title": "نوآوری در طراحی",
                "body": "اصول طراحی مدرن بر تجربه کاربری، سادگی و دسترسی‌پذیری تمرکز دارد. طراحی عالی مشکلات واقعی را حل می‌کند و ارتباطات معنادار ایجاد می‌کند.",
                "brand": "آزمایشگاه طراحی"
            },
            "background_color": [250, 240, 250]
        },
        "article"
    ))

    # Test 3: list
    print("\n[TEST] Testing list layout...")
    results['list'] = []

    results['list'].append(test_layout(
        "english",
        {
            "layout_type": "list",
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
            "background_color": [255, 247, 230]
        },
        "list"
    ))

    results['list'].append(test_layout(
        "farsi",
        {
            "layout_type": "list",
            "content": {
                "title": "۵ نکته برای طراحی بهتر",
                "items": [
                    "ساده و تمیز نگه دارید",
                    "از تایپوگرافی یکنواخت استفاده کنید",
                    "با کاربران واقعی تست کنید",
                    "روی نیازهای کاربر تمرکز کنید",
                    "بر اساس بازخورد تکرار کنید"
                ],
                "brand": "استودیو طراحی"
            },
            "background_color": [240, 255, 240]
        },
        "list"
    ))

    results['list'].append(test_layout(
        "gradient_english",
        {
            "layout_type": "list",
            "content": {
                "title": "Success Strategies",
                "items": [
                    "Set clear goals",
                    "Stay organized",
                    "Never stop learning",
                    "Network effectively",
                    "Maintain work-life balance"
                ],
                "brand": "Life Coaching"
            },
            "background_color": [200, 220, 255]
        },
        "list"
    ))

    results['list'].append(test_layout(
        "gradient_farsi",
        {
            "layout_type": "list",
            "content": {
                "title": "استراتژی‌های موفقیت",
                "items": [
                    "اهداف روشن تعیین کنید",
                    "منظم بمانید",
                    "یادگیری را متوقف نکنید",
                    "به شبکه‌سازی موثر بپردازید",
                    "تعادل کار و زندگی را حفظ کنید"
                ],
                "brand": "مربی‌گری زندگی"
            },
            "background_color": [255, 200, 180]
        },
        "list"
    ))

    # Test 4: quote
    print("\n[TEST] Testing quote layout...")
    results['quote'] = []

    results['quote'].append(test_layout(
        "english",
        {
            "layout_type": "quote",
            "content": {
                "quote": "Success is not final, failure is not fatal.",
                "author": "Winston Churchill",
                "brand": "Inspiration Daily"
            },
            "background_color": [250, 250, 255]
        },
        "quote"
    ))

    results['quote'].append(test_layout(
        "farsi",
        {
            "layout_type": "quote",
            "content": {
                "quote": "موفقیت نهایی نیست، شکست کشنده نیست.",
                "author": "وینستون چرچیل",
                "brand": "الهام روزانه"
            },
            "background_color": [255, 255, 250]
        },
        "quote"
    ))

    results['quote'].append(test_layout(
        "gradient_english",
        {
            "layout_type": "quote",
            "content": {
                "quote": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs",
                "brand": "Motivation Hub"
            },
            "background_color": [200, 230, 255]
        },
        "quote"
    ))

    results['quote'].append(test_layout(
        "gradient_farsi",
        {
            "layout_type": "quote",
            "content": {
                "quote": "تنها راه انجام کارهای بزرگ، عاشق آنچه انجام می‌دهید است.",
                "author": "استیو جابز",
                "brand": "مرکز انگیزه"
            },
            "background_color": [255, 230, 200]
        },
        "quote"
    ))

    # Test 5: testimonial
    print("\n[TEST] Testing testimonial layout...")
    results['testimonial'] = []

    results['testimonial'].append(test_layout(
        "english",
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "This product completely transformed our business operations and increased our productivity by 300%.",
                "person_name": "Sarah Johnson",
                "person_title": "CEO, Tech Startup",
                "brand": "Product Reviews"
            },
            "background_color": [245, 250, 255]
        },
        "testimonial"
    ))

    results['testimonial'].append(test_layout(
        "farsi",
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "این محصول عملیات تجاری ما را کاملاً متحول کرد و بهره‌وری ما را ۳۰۰ درصد افزایش داد.",
                "person_name": "سارا احمدی",
                "person_title": "مدیر عامل، استارتاپ فناوری",
                "brand": "بررسی محصولات"
            },
            "background_color": [255, 250, 250]
        },
        "testimonial"
    ))

    results['testimonial'].append(test_layout(
        "gradient_english",
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "Outstanding quality and excellent customer service. Highly recommended for any business looking to scale.",
                "person_name": "Michael Chen",
                "person_title": "Operations Director",
                "brand": "Business Solutions"
            },
            "background_color": [180, 200, 255]
        },
        "testimonial"
    ))

    results['testimonial'].append(test_layout(
        "gradient_farsi",
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "کیفیت برجسته و خدمات مشتری عالی. برای هر کسب و کاری که به دنبال مقیاس‌پذیری است بسیار توصیه می‌شود.",
                "person_name": "میکائیل چن",
                "person_title": "مدیر عملیات",
                "brand": "راه‌حل‌های تجاری"
            },
            "background_color": [255, 220, 180]
        },
        "testimonial"
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
        print_info("\n⚠️  Could not fetch layout info, but continuing with predefined tests...")

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
