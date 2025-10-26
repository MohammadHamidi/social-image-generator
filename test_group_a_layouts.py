#!/usr/bin/env python3
"""
Integration test for Group A layouts
Tests split_image_text, product_showcase, and checklist layouts
"""

import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:5000"

def test_layout(name, json_path):
    """Test a layout by sending JSON to /generate_post endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Config: {json_path}")
    print('='*60)

    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Send request
    try:
        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=config,
            timeout=30
        )

        if response.status_code == 200:
            # Save the image
            output_dir = Path("test_outputs/group_a")
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{name}.png"
            with open(output_file, 'wb') as f:
                f.write(response.content)

            print(f"✅ SUCCESS: Image saved to {output_file}")
            print(f"   Size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Group A Layouts (split_image_text, product_showcase, checklist)")

    tests = [
        # Split Image Text
        ("split_image_text_basic", "examples/split_image_text/example_1_basic.json"),
        ("split_image_text_bullets", "examples/split_image_text/example_2_with_bullets.json"),
        ("split_image_text_farsi", "examples/split_image_text/example_3_farsi.json"),

        # Product Showcase
        ("product_showcase_basic", "examples/product_showcase/example_1_basic.json"),
        ("product_showcase_cta", "examples/product_showcase/example_2_with_cta.json"),

        # Checklist
        ("checklist_basic", "examples/checklist/example_1_basic.json"),
        ("checklist_checked", "examples/checklist/example_2_checked.json"),
        ("checklist_farsi", "examples/checklist/example_3_farsi.json"),
    ]

    results = []
    for name, path in tests:
        if os.path.exists(path):
            success = test_layout(name, path)
            results.append((name, success))
        else:
            print(f"\n⚠️  WARNING: {path} not found, skipping")
            results.append((name, False))

    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print('='*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All Group A layouts working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
