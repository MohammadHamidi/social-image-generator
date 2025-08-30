#!/usr/bin/env python3
"""
Example script showing how to generate images with custom images instead of programmatic shapes.
"""

import sys
import os
sys.path.append('src')

from social_image_generator import SocialImageGenerator

def generate_with_custom_images():
    """Generate image using custom images for main content and blueprint/watermark"""

    # Create generator with custom images configuration
    config_path = "config/custom_images_example.json"
    generator = SocialImageGenerator(config_path)

    # Sample content
    content = {
        'headline': 'کت‌های زمستانی جدید',
        'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
        'brand': 'Fashion Store'
    }

    # Generate hero layout (will use custom images if available)
    print("Generating image with custom images...")
    img = generator.generate_hero_layout(
        content['headline'],
        content['subheadline'],
        content['brand']
    )

    # Save to root directory
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_path, 'social_image_custom.png')
    img.save(output_path, 'PNG', quality=95)
    print(f'Custom image generated and saved to: {output_path}')

def generate_fallback():
    """Generate image using default programmatic generation (fallback)"""

    # Create generator with default config (no custom images)
    generator = SocialImageGenerator()

    content = {
        'headline': 'کت‌های زمستانی جدید',
        'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
        'brand': 'Fashion Store'
    }

    print("Generating image with programmatic generation...")
    img = generator.generate_hero_layout(
        content['headline'],
        content['subheadline'],
        content['brand']
    )

    # Save to root directory
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_path, 'social_image_programmatic.png')
    img.save(output_path, 'PNG', quality=95)
    print(f'Programmatic image generated and saved to: {output_path}')

if __name__ == "__main__":
    print("Social Image Generator - Custom Images Demo")
    print("=" * 50)

    # Try custom images first
    try:
        generate_with_custom_images()
    except Exception as e:
        print(f"Custom images generation failed: {e}")
        print("Falling back to programmatic generation...")
        generate_fallback()

    print("\nDemo completed! Check the root directory for generated images.")
