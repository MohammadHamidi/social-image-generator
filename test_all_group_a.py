#!/usr/bin/env python3
"""
Comprehensive test for ALL Group A layouts
Tests: split_image_text, product_showcase, checklist, testimonial, overlay_text, caption_box
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
            output_dir = Path("test_outputs/all_group_a")
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
    """Run all tests for Group A layouts"""
    print("🚀 Testing ALL Group A Layouts (6 layouts)")
    print("=" * 60)

    tests = [
        # A1: Split Image Text (3 tests)
        ("split_image_text_basic", "examples/split_image_text/example_1_basic.json"),
        ("split_image_text_bullets", "examples/split_image_text/example_2_with_bullets.json"),
        ("split_image_text_farsi", "examples/split_image_text/example_3_farsi.json"),

        # A2: Product Showcase (2 tests)
        ("product_showcase_basic", "examples/product_showcase/example_1_basic.json"),
        ("product_showcase_cta", "examples/product_showcase/example_2_with_cta.json"),

        # A3: Checklist (3 tests)
        ("checklist_basic", "examples/checklist/example_1_basic.json"),
        ("checklist_checked", "examples/checklist/example_2_checked.json"),
        ("checklist_farsi", "examples/checklist/example_3_farsi.json"),

        # A4: Testimonial (3 tests)
        ("testimonial_basic", "examples/testimonial/example_1_basic.json"),
        ("testimonial_photo_rating", "examples/testimonial/example_2_with_photo_rating.json"),
        ("testimonial_farsi", "examples/testimonial/example_3_farsi.json"),

        # A5: Overlay Text (3 tests)
        ("overlay_text_basic", "examples/overlay_text/example_1_basic.json"),
        ("overlay_text_box", "examples/overlay_text/example_2_text_box.json"),
        ("overlay_text_farsi", "examples/overlay_text/example_3_farsi.json"),

        # A6: Caption Box (3 tests)
        ("caption_box_bottom", "examples/caption_box/example_1_bottom.json"),
        ("caption_box_side", "examples/caption_box/example_2_side.json"),
        ("caption_box_farsi", "examples/caption_box/example_3_farsi.json"),
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
    print("SUMMARY - GROUP A LAYOUTS")
    print('='*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    # Group by layout type
    layout_groups = {
        "split_image_text": [],
        "product_showcase": [],
        "checklist": [],
        "testimonial": [],
        "overlay_text": [],
        "caption_box": []
    }

    for name, success in results:
        for layout_type in layout_groups.keys():
            if name.startswith(layout_type):
                layout_groups[layout_type].append((name, success))
                break

    # Print by layout type
    for layout_type, tests in layout_groups.items():
        if tests:
            passed_count = sum(1 for _, success in tests if success)
            total_count = len(tests)
            status = "✅" if passed_count == total_count else "⚠️"
            print(f"\n{status} {layout_type.upper()}: {passed_count}/{total_count} passed")
            for name, success in tests:
                status = "  ✅" if success else "  ❌"
                print(f"{status} {name}")

    print(f"\n{'='*60}")
    print(f"TOTAL: {passed}/{total} tests passed")
    print('='*60)

    if passed == total:
        print("\n🎉 ALL GROUP A LAYOUTS WORKING PERFECTLY!")
        print("Group A is 100% complete!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
