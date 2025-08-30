#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from social_image_generator import SocialImageGenerator

def test_all_layouts():
    """Test all layout generation"""
    print("Testing social image generator...")
    
    # Test content with both English and Farsi
    test_contents = [
        {
            'headline': 'New Winter Collection',
            'subheadline': 'Premium Quality Coats',
            'brand': 'Fashion Store'
        },
        {
            'headline': 'کت‌های زمستانی جدید',
            'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
            'brand': 'فروشگاه مد'
        }
    ]
    
    generator = SocialImageGenerator()
    
    for i, content in enumerate(test_contents):
        print(f"\nGenerating test set {i+1}...")
        generator.generate_all_layouts(content, f"test_{i+1}")
    
    print("\nAll tests completed! Check the output directory.")

if __name__ == "__main__":
    test_all_layouts()
