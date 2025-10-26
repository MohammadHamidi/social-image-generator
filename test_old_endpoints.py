#!/usr/bin/env python3
"""
Test OLD endpoints (pre-layout engine)
Use this if the new /generate_post endpoint isn't deployed yet
"""

import requests
import json
from pathlib import Path

BASE_URL = "https://imageeditor.flowiran.ir"
OUTPUT_DIR = Path("./old_endpoint_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def test_gradient():
    """Test gradient generation"""
    print("\n" + "="*70)
    print("  Testing: POST /generate_gradient")
    print("="*70)

    config = {
        "width": 1080,
        "height": 1350,
        "top_color": [241, 114, 113],
        "bottom_color": [91, 197, 189],
        "direction": "vertical",
        "apply_dithering": True
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate_gradient",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            filepath = OUTPUT_DIR / "gradient_test.png"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Gradient generated: {filepath}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_text_layout():
    """Test text layout generation"""
    print("\n" + "="*70)
    print("  Testing: POST /generate_text")
    print("="*70)

    config = {
        "layout": "quote",
        "config": {
            "quote": "Every day is a new beginning",
            "author": "Unknown",
            "gradient_colors": {
                "top_color": [255, 200, 150],
                "bottom_color": [255, 150, 200]
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate_text",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            filepath = OUTPUT_DIR / "text_layout_test.png"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Text layout generated: {filepath}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_farsi_text():
    """Test Farsi text rendering"""
    print("\n" + "="*70)
    print("  Testing: POST /generate_text (Farsi)")
    print("="*70)

    config = {
        "layout": "quote",
        "config": {
            "quote": "هر روز یک شروع تازه است",
            "author": "نامشخص",
            "gradient_colors": {
                "top_color": [230, 240, 255],
                "bottom_color": [255, 230, 240]
            }
        }
    }

    try:
        response = requests.post(
            f"{BASE_URL}/generate_text",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            filepath = OUTPUT_DIR / "farsi_text_test.png"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Farsi text generated: {filepath}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Test old endpoints"""
    print("="*70)
    print("  🧪 Testing OLD Endpoints (Pre-Layout Engine)")
    print("="*70)
    print(f"\nTarget: {BASE_URL}")
    print(f"Output: {OUTPUT_DIR.absolute()}")

    results = []

    # Test gradient
    results.append(("Gradient Generation", test_gradient()))

    # Test text layout
    results.append(("Text Layout (English)", test_text_layout()))

    # Test Farsi
    results.append(("Text Layout (Farsi)", test_farsi_text()))

    # Summary
    print("\n" + "="*70)
    print("  Summary")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n✅ Old endpoints are working!")
        print("\n⚠️  However, these are NOT the new layout engine endpoints.")
        print("To use the new layouts, you need to deploy the latest code.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    print(f"\n📁 Output saved to: {OUTPUT_DIR.absolute()}")
    print("="*70)


if __name__ == "__main__":
    main()
