#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify gradient and Farsi text fixes
"""

import sys
import os
from PIL import Image

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_social_generator import EnhancedSocialImageGenerator

def test_gradient_generation():
    """Test gradient background generation"""
    print("=" * 60)
    print("Test 1: Gradient Generation")
    print("=" * 60)

    try:
        generator = EnhancedSocialImageGenerator()

        # Update config for gradient
        generator.config['background'] = {
            'type': 'gradient',
            'primary_color': [255, 107, 107],  # #FF6B6B (Red)
            'secondary_color': [78, 205, 196],  # #4ECDC4 (Teal)
            'gradient_direction': 'vertical'
        }

        img = generator._create_enhanced_background()

        # Check if image was created
        assert img is not None, "Image should not be None"
        assert img.size == (1080, 1350), f"Expected (1080, 1350), got {img.size}"

        # Check if it's a gradient (not solid color)
        # Get pixels from top and bottom
        pixels = img.load()
        top_pixel = pixels[540, 100]  # Middle x, near top
        bottom_pixel = pixels[540, 1250]  # Middle x, near bottom

        # They should be different for a gradient
        assert top_pixel != bottom_pixel, \
            f"Gradient not working! Top pixel {top_pixel} == Bottom pixel {bottom_pixel}"

        # Save test image
        os.makedirs('test_output', exist_ok=True)
        img.save('test_output/test_gradient.png')

        print("✅ Gradient generation: PASSED")
        print(f"   Top pixel (RGB): {top_pixel}")
        print(f"   Bottom pixel (RGB): {bottom_pixel}")
        print(f"   Saved to: test_output/test_gradient.png")
        return True
    except Exception as e:
        print(f"❌ Gradient generation: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_farsi_text_rendering():
    """Test Farsi text rendering"""
    print("\n" + "=" * 60)
    print("Test 2: Farsi Text Rendering")
    print("=" * 60)

    try:
        generator = EnhancedSocialImageGenerator()

        # Update config for gradient
        generator.config['background'] = {
            'type': 'gradient',
            'primary_color': [255, 107, 107],  # Red
            'secondary_color': [78, 205, 196],  # Teal
            'gradient_direction': 'vertical'
        }

        # Test Farsi text detection
        farsi_text = "موفقیت از خود شما آغاز می‌شود"
        is_farsi = generator._is_arabic_text(farsi_text)
        assert is_farsi, "Farsi text should be detected as Arabic/RTL"

        # Test text preparation
        prepared = generator._prepare_arabic_text(farsi_text)
        assert prepared is not None, "Prepared text should not be None"
        assert len(prepared) > 0, "Prepared text should not be empty"

        # Generate a quote layout
        img = generator.generate_quote_layout(
            quote="موفقیت از خود شما آغاز می‌شود",
            author="تیم فلوایران",
            brand="Flowiran"
        )

        assert img is not None, "Generated image should not be None"
        assert img.size == (1080, 1350), f"Expected (1080, 1350), got {img.size}"

        # Save test image
        os.makedirs('test_output', exist_ok=True)
        img.save('test_output/test_farsi_quote.png')

        print("✅ Farsi text rendering: PASSED")
        print(f"   Farsi detection: {is_farsi}")
        print(f"   Original text: {farsi_text}")
        print(f"   Prepared text length: {len(prepared)} chars")
        print(f"   Saved to: test_output/test_farsi_quote.png")
        return True
    except Exception as e:
        print(f"❌ Farsi text rendering: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mixed_content():
    """Test mixed English and Farsi content"""
    print("\n" + "=" * 60)
    print("Test 3: Mixed Content")
    print("=" * 60)

    try:
        generator = EnhancedSocialImageGenerator()

        # Update config for gradient
        generator.config['background'] = {
            'type': 'gradient',
            'primary_color': [253, 187, 45],   # Golden
            'secondary_color': [255, 107, 107],  # Red
            'gradient_direction': 'vertical'
        }

        # Test with English quote
        img = generator.generate_quote_layout(
            quote="Success starts with you",
            author="Flowiran Team",
            brand="Flowiran"
        )

        assert img is not None, "Generated image should not be None"

        # Save test image
        os.makedirs('test_output', exist_ok=True)
        img.save('test_output/test_english_quote.png')

        print("✅ Mixed content: PASSED")
        print(f"   Saved to: test_output/test_english_quote.png")
        return True
    except Exception as e:
        print(f"❌ Mixed content: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 Running Social Image Generator Tests\n")

    results = []
    results.append(("Gradient Generation", test_gradient_generation()))
    results.append(("Farsi Text Rendering", test_farsi_text_rendering()))
    results.append(("Mixed Content", test_mixed_content()))

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
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)
