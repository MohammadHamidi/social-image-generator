#!/usr/bin/env python3
"""
Comprehensive test for all social image generator functionality
Tests both text layouts and image-based layouts with provided images
"""

import os
import sys
import json
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_social_generator import EnhancedSocialImageGenerator

def test_text_visibility_fix():
    """Test and fix text visibility issues"""
    print("🔍 DEBUGGING TEXT VISIBILITY ISSUES")
    print("=" * 50)
    
    # Test with both config and no config
    configs = [
        ("No Config", None),
        ("Text Config", "config/text_layouts_config.json"),
        ("Default Config", "config/default_config.json")
    ]
    
    content = {
        "quote": "THIS IS A TEST QUOTE TO CHECK VISIBILITY",
        "author": "Test Author",
        "brand": "Test Brand"
    }
    
    for config_name, config_path in configs:
        print(f"\n📋 Testing with {config_name}...")
        try:
            if config_path and os.path.exists(config_path):
                generator = EnhancedSocialImageGenerator(config_path)
            else:
                generator = EnhancedSocialImageGenerator()
            
            # Test quote layout
            img = generator.generate_text_layout('quote', content)
            output_path = f"output/debug_text_{config_name.lower().replace(' ', '_')}.png"
            img.save(output_path, 'PNG', quality=95)
            
            print(f"✅ Generated: {output_path}")
            
            # Print background config being used
            bg_config = generator.config.get('background', {})
            print(f"   Background: {bg_config.get('type', 'unknown')} - {bg_config.get('primary_color', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Failed with {config_name}: {e}")

def test_with_provided_images():
    """Test all layouts with the provided images"""
    print("\n🖼️  TESTING WITH PROVIDED IMAGES")
    print("=" * 50)
    
    # List uploaded files
    main_files = os.listdir("uploads/main/")
    bg_files = os.listdir("uploads/background/")
    watermark_files = os.listdir("uploads/watermark/")
    
    print(f"📁 Available files:")
    print(f"   Main: {main_files}")
    print(f"   Background: {bg_files}")
    print(f"   Watermark: {watermark_files}")
    
    if not (main_files and watermark_files):
        print("❌ Missing required image files!")
        return
    
    # Create configuration for testing with images
    test_config = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "background": {
            "type": "solid",
            "primary_color": [255, 255, 255]  # White background for testing
        },
        "custom_images": {
            "use_custom_images": True,
            "main_image_path": f"uploads/main/{main_files[0]}",
            "blueprint_image_path": f"uploads/watermark/{watermark_files[0]}",
            "main_image_size": [400, 400],
            "blueprint_image_size": [150, 150],
            "main_image_position": [340, 500],
            "blueprint_image_position": [465, 200],
            "remove_background": True
        }
    }
    
    # Add background image if available
    if bg_files:
        test_config["custom_images"]["background_image_path"] = f"uploads/background/{bg_files[0]}"
    
    # Save test config
    config_path = "config/test_with_images.json"
    with open(config_path, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print(f"\n🔧 Created test config: {config_path}")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Hero Layout with Images",
            "method": "generate_enhanced_hero_layout",
            "args": ["Product Showcase", "Latest Collection", "Fashion Store"]
        },
        {
            "name": "Quote with Custom Background",
            "method": "generate_text_layout",
            "args": ["quote", {
                "quote": "Style is a way to say who you are without having to speak",
                "author": "Rachel Zoe",
                "brand": "Fashion Store"
            }]
        }
    ]
    
    try:
        generator = EnhancedSocialImageGenerator(config_path)
        
        for scenario in scenarios:
            print(f"\n🎨 Testing: {scenario['name']}")
            try:
                method = getattr(generator, scenario['method'])
                img = method(*scenario['args'])
                
                output_name = scenario['name'].lower().replace(' ', '_')
                output_path = f"output/test_{output_name}.png"
                img.save(output_path, 'PNG', quality=95)
                
                print(f"✅ Generated: {output_path}")
                
            except Exception as e:
                print(f"❌ Failed: {e}")
                
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")

def test_all_text_layouts_with_dark_bg():
    """Test all text layouts with guaranteed dark background"""
    print("\n🌙 TESTING TEXT LAYOUTS WITH DARK BACKGROUND")
    print("=" * 50)
    
    # Create config with guaranteed dark background
    dark_config = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "background": {
            "type": "gradient",
            "primary_color": [20, 30, 40],  # Very dark
            "secondary_color": [40, 50, 60],  # Slightly lighter dark
            "gradient_direction": "diagonal"
        },
        "fonts": {
            "headline_size": 52,
            "subheadline_size": 36,
            "brand_size": 28
        }
    }
    
    config_path = "config/dark_test_config.json"
    with open(config_path, 'w') as f:
        json.dump(dark_config, f, indent=2)
    
    # Test content
    test_contents = {
        "quote": {
            "quote": "SUCCESS IS NOT FINAL, FAILURE IS NOT FATAL: IT IS THE COURAGE TO CONTINUE THAT COUNTS",
            "author": "Winston Churchill",
            "brand": "Daily Motivation"
        },
        "article": {
            "title": "THE POWER OF PERSISTENCE",
            "body": "In the journey of life, we encounter many obstacles and challenges. It is not the absence of failure that defines success, but the courage to rise again after each setback. Every great achievement in history has been the result of persistence and determination.",
            "brand": "Success Stories"
        },
        "announcement": {
            "title": "SPECIAL OFFER",
            "description": "Get 50% off on all premium courses. Limited time offer. Don't miss this opportunity to advance your skills.",
            "cta": "CLAIM NOW",
            "brand": "Learning Hub"
        },
        "list": {
            "title": "KEYS TO SUCCESS",
            "items": [
                "SET CLEAR GOALS AND OBJECTIVES",
                "DEVELOP A STRONG WORK ETHIC",
                "LEARN FROM FAILURES AND MISTAKES",
                "BUILD MEANINGFUL RELATIONSHIPS",
                "NEVER STOP LEARNING AND GROWING"
            ],
            "brand": "Success Academy"
        },
        "testimonial": {
            "quote": "This program completely transformed my approach to business. The results were beyond my expectations and the support was outstanding throughout the entire journey.",
            "person_name": "Sarah Johnson",
            "person_title": "CEO, Innovation Corp",
            "brand": "Success Stories"
        }
    }
    
    try:
        generator = EnhancedSocialImageGenerator(config_path)
        
        for layout_type, content in test_contents.items():
            print(f"\n📝 Testing {layout_type} layout...")
            try:
                img = generator.generate_text_layout(layout_type, content)
                output_path = f"output/dark_bg_{layout_type}.png"
                img.save(output_path, 'PNG', quality=95)
                print(f"✅ Generated: {output_path}")
                
            except Exception as e:
                print(f"❌ Failed {layout_type}: {e}")
                
    except Exception as e:
        print(f"❌ Generator failed: {e}")

def test_original_layouts():
    """Test the original hero/split/top_heavy/bottom_heavy layouts"""
    print("\n🏛️  TESTING ORIGINAL LAYOUTS")
    print("=" * 50)
    
    content = {
        'headline': 'کت‌های زمستانی جدید',
        'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
        'brand': 'Fashion Store'
    }
    
    try:
        # Test with original generator
        from social_image_generator import SocialImageGenerator
        
        generator = SocialImageGenerator()
        
        layouts = {
            'hero': generator.generate_hero_layout,
            'split': generator.generate_split_layout,
            'top_heavy': generator.generate_top_heavy_layout,
            'bottom_heavy': generator.generate_bottom_heavy_layout
        }
        
        for layout_name, layout_func in layouts.items():
            print(f"🎨 Testing {layout_name} layout...")
            try:
                img = layout_func(
                    content['headline'],
                    content['subheadline'],
                    content['brand']
                )
                output_path = f"output/original_{layout_name}.png"
                img.save(output_path, 'PNG', quality=95)
                print(f"✅ Generated: {output_path}")
                
            except Exception as e:
                print(f"❌ Failed {layout_name}: {e}")
                
    except Exception as e:
        print(f"❌ Original generator failed: {e}")

def create_text_with_contrast():
    """Create a simple test with high contrast to verify text rendering"""
    print("\n🔤 CREATING HIGH CONTRAST TEXT TEST")
    print("=" * 50)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple black background with white text
        img = Image.new('RGB', (1080, 1350), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Draw white text
        text = "THIS IS A VISIBILITY TEST"
        draw.text((100, 200), text, fill=(255, 255, 255), font=font)
        
        # Draw red text for extra visibility
        text2 = "RED TEXT FOR CONTRAST"
        draw.text((100, 300), text2, fill=(255, 0, 0), font=font)
        
        # Save
        output_path = "output/simple_contrast_test.png"
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Created simple test: {output_path}")
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")

def main():
    """Run comprehensive tests"""
    print("🧪 COMPREHENSIVE SOCIAL IMAGE GENERATOR TEST")
    print("=" * 60)
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Run all tests
    create_text_with_contrast()
    test_text_visibility_fix()
    test_all_text_layouts_with_dark_bg()
    test_with_provided_images()
    test_original_layouts()
    
    print("\n📊 TEST SUMMARY")
    print("=" * 30)
    
    # List all generated files
    output_files = [f for f in os.listdir("output") if f.endswith('.png')]
    print(f"📁 Generated {len(output_files)} test images:")
    for file in sorted(output_files):
        print(f"   - {file}")
    
    print("\n🎉 Comprehensive testing completed!")
    print("📝 Check the output directory for all generated images")
    print("🔍 Look for text visibility in each image")

if __name__ == "__main__":
    main()
