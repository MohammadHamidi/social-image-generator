#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for headline_promo layout

This script tests the new LayoutEngine architecture with the headline_promo layout.
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from layouts import get_layout_engine, list_available_layouts
from PIL import Image


def test_layout_registry():
    """Test that layouts are registered correctly."""
    print("=" * 60)
    print("Test 1: Layout Registry")
    print("=" * 60)

    try:
        layouts = list_available_layouts()
        print(f"✅ Found {len(layouts)} registered layout(s)")

        for layout_type, schema in layouts.items():
            print(f"  - {layout_type}: {schema.get('description', 'No description')}")

        return True
    except Exception as e:
        print(f"❌ Layout registry test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_minimal():
    """Test headline_promo with minimal content."""
    print("\n" + "=" * 60)
    print("Test 2: Headline Promo - Minimal (headline only)")
    print("=" * 60)

    try:
        # Get layout class
        HeadlinePromoLayout = get_layout_engine('headline_promo')

        # Create instance
        layout = HeadlinePromoLayout(
            content={'headline': 'Summer Sale'},
            background={
                'mode': 'gradient',
                'gradient': {
                    'colors': [[255, 107, 107], [253, 187, 45]],
                    'direction': 'vertical'
                }
            }
        )

        # Render
        images = layout.render()

        assert len(images) == 1, "Should return 1 image"
        assert isinstance(images[0], Image.Image), "Should return PIL Image"
        assert images[0].size == (1080, 1350), "Should be Instagram post size"

        # Save
        os.makedirs('test_output', exist_ok=True)
        images[0].save('test_output/headline_promo_minimal.png')

        print("✅ Minimal headline test PASSED")
        print(f"   Image size: {images[0].size}")
        print(f"   Saved to: test_output/headline_promo_minimal.png")
        return True

    except Exception as e:
        print(f"❌ Minimal headline test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_full():
    """Test headline_promo with all content fields."""
    print("\n" + "=" * 60)
    print("Test 3: Headline Promo - Full (headline + subheadline + CTA)")
    print("=" * 60)

    try:
        HeadlinePromoLayout = get_layout_engine('headline_promo')

        layout = HeadlinePromoLayout(
            content={
                'headline': 'Summer Sale',
                'subheadline': 'Up to 50% Off Everything',
                'cta': 'Shop Now'
            },
            background={
                'mode': 'gradient',
                'gradient': {
                    'colors': [[255, 107, 107], [253, 187, 45]],
                    'direction': 'vertical'
                }
            }
        )

        images = layout.render()
        os.makedirs('test_output', exist_ok=True)
        images[0].save('test_output/headline_promo_full.png')

        print("✅ Full headline test PASSED")
        print(f"   Saved to: test_output/headline_promo_full.png")
        return True

    except Exception as e:
        print(f"❌ Full headline test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_farsi():
    """Test headline_promo with Farsi content."""
    print("\n" + "=" * 60)
    print("Test 4: Headline Promo - Farsi Text")
    print("=" * 60)

    try:
        HeadlinePromoLayout = get_layout_engine('headline_promo')

        layout = HeadlinePromoLayout(
            content={
                'headline': 'فروش تابستانی',
                'subheadline': 'تا ۵۰٪ تخفیف روی همه محصولات',
                'cta': 'خرید کنید'
            },
            background={
                'mode': 'gradient',
                'gradient': {
                    'colors': [[78, 205, 196], [255, 107, 107]],
                    'direction': 'vertical'
                }
            }
        )

        images = layout.render()
        os.makedirs('test_output', exist_ok=True)
        images[0].save('test_output/headline_promo_farsi.png')

        print("✅ Farsi headline test PASSED")
        print(f"   Saved to: test_output/headline_promo_farsi.png")
        return True

    except Exception as e:
        print(f"❌ Farsi headline test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_from_example_files():
    """Test using example JSON files."""
    print("\n" + "=" * 60)
    print("Test 5: Generate from Example JSON Files")
    print("=" * 60)

    examples_dir = 'examples/headline_promo'

    if not os.path.exists(examples_dir):
        print(f"⚠️  Examples directory not found: {examples_dir}")
        return True  # Not a critical failure

    HeadlinePromoLayout = get_layout_engine('headline_promo')
    success_count = 0
    total_count = 0

    for filename in sorted(os.listdir(examples_dir)):
        if not filename.endswith('.json'):
            continue

        total_count += 1
        filepath = os.path.join(examples_dir, filename)

        print(f"\n  Processing: {filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            layout = HeadlinePromoLayout(
                content=data.get('content', {}),
                assets=data.get('assets', {}),
                background=data.get('background', {}),
                options=data.get('options', {})
            )

            images = layout.render()

            # Save with example name
            output_name = f"headline_promo_{filename.replace('.json', '.png')}"
            os.makedirs('test_output', exist_ok=True)
            images[0].save(f'test_output/{output_name}')

            print(f"  ✅ Generated: test_output/{output_name}")
            success_count += 1

        except Exception as e:
            print(f"  ❌ Failed: {e}")

    print(f"\n  Summary: {success_count}/{total_count} examples generated successfully")

    return success_count == total_count


def main():
    """Run all tests."""
    print("\n🧪 Testing Headline Promo Layout\n")

    results = []
    results.append(("Layout Registry", test_layout_registry()))
    results.append(("Minimal Headline", test_headline_promo_minimal()))
    results.append(("Full Content", test_headline_promo_full()))
    results.append(("Farsi Text", test_headline_promo_farsi()))
    results.append(("Example Files", test_from_example_files()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
