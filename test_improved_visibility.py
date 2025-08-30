#!/usr/bin/env python3
"""
Test improved text visibility with shadows and better contrast
"""

import os
import sys
import json
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_social_generator import EnhancedSocialImageGenerator

def test_improved_text_layouts():
    """Test all text layouts with improved visibility"""
    print("🔥 TESTING IMPROVED TEXT VISIBILITY")
    print("=" * 50)
    
    # Create config with various background types for testing
    configs = [
        {
            "name": "Light Background",
            "config": {
                "canvas_width": 1080,
                "canvas_height": 1350,
                "background": {
                    "type": "solid",
                    "primary_color": [240, 240, 240]  # Light gray
                },
                "fonts": {
                    "headline_size": 48,
                    "subheadline_size": 32,
                    "brand_size": 24
                }
            }
        },
        {
            "name": "Dark Background",
            "config": {
                "canvas_width": 1080,
                "canvas_height": 1350,
                "background": {
                    "type": "solid",
                    "primary_color": [30, 30, 30]  # Dark gray
                },
                "fonts": {
                    "headline_size": 48,
                    "subheadline_size": 32,
                    "brand_size": 24
                }
            }
        },
        {
            "name": "Gradient Background",
            "config": {
                "canvas_width": 1080,
                "canvas_height": 1350,
                "background": {
                    "type": "gradient",
                    "primary_color": [120, 50, 200],
                    "secondary_color": [200, 50, 120],
                    "gradient_direction": "diagonal"
                },
                "fonts": {
                    "headline_size": 48,
                    "subheadline_size": 32,
                    "brand_size": 24
                }
            }
        }
    ]
    
    # Test content
    test_content = {
        "quote": {
            "quote": "The future belongs to those who believe in the beauty of their dreams",
            "author": "Eleanor Roosevelt",
            "brand": "Inspiration Daily"
        },
        "article": {
            "title": "Building Better Habits",
            "body": "Success is not about making dramatic changes overnight. It's about making small, consistent improvements every day. These tiny changes compound over time to create remarkable results.",
            "brand": "Growth Mindset"
        },
        "announcement": {
            "title": "LIMITED TIME OFFER",
            "description": "Get 60% off our premium courses this week only. Transform your skills and advance your career with expert-led training.",
            "cta": "CLAIM DISCOUNT",
            "brand": "SkillUp Academy"
        }
    }
    
    os.makedirs("output", exist_ok=True)
    
    for config_info in configs:
        print(f"\n🎨 Testing with {config_info['name']}...")
        
        # Save config
        config_path = f"config/test_{config_info['name'].lower().replace(' ', '_')}.json"
        with open(config_path, 'w') as f:
            json.dump(config_info['config'], f, indent=2)
        
        try:
            generator = EnhancedSocialImageGenerator(config_path)
            
            for layout_type, content in test_content.items():
                print(f"  📝 Creating {layout_type} layout...")
                
                img = generator.generate_text_layout(layout_type, content)
                
                output_name = f"improved_{config_info['name'].lower().replace(' ', '_')}_{layout_type}.png"
                output_path = f"output/{output_name}"
                img.save(output_path, 'PNG', quality=95)
                
                print(f"  ✅ Saved: {output_path}")
                
        except Exception as e:
            print(f"  ❌ Failed with {config_info['name']}: {e}")

def test_with_user_images():
    """Test with the user's provided images and improved visibility"""
    print("\n🖼️  TESTING WITH USER IMAGES + IMPROVED TEXT")
    print("=" * 50)
    
    # Check for user images
    main_files = [f for f in os.listdir("uploads/main/") if f == "main.png"]
    bg_files = [f for f in os.listdir("uploads/background/") if f == "bg.png"]
    watermark_files = [f for f in os.listdir("uploads/watermark/") if f == "watermark.png"]
    
    if not (main_files and watermark_files):
        print("❌ User images not found. Looking for alternatives...")
        main_files = os.listdir("uploads/main/")[:1]
        watermark_files = os.listdir("uploads/watermark/")[:1]
    
    if main_files and watermark_files:
        print(f"📁 Using: main={main_files[0]}, watermark={watermark_files[0]}")
        if bg_files:
            print(f"📁 Background: {bg_files[0]}")
        
        # Create config with user images
        image_config = {
            "canvas_width": 1080,
            "canvas_height": 1350,
            "background": {
                "type": "gradient",
                "primary_color": [40, 50, 60],
                "secondary_color": [60, 70, 80],
                "gradient_direction": "vertical"
            },
            "custom_images": {
                "use_custom_images": True,
                "main_image_path": f"uploads/main/{main_files[0]}",
                "blueprint_image_path": f"uploads/watermark/{watermark_files[0]}",
                "main_image_size": [450, 450],
                "blueprint_image_size": [120, 120],
                "main_image_position": [315, 550],
                "blueprint_image_position": [480, 250],
                "remove_background": True
            }
        }
        
        # Add background if available
        if bg_files:
            image_config["custom_images"]["background_image_path"] = f"uploads/background/{bg_files[0]}"
        
        # Save config
        config_path = "config/user_images_improved.json"
        with open(config_path, 'w') as f:
            json.dump(image_config, f, indent=2)
        
        try:
            generator = EnhancedSocialImageGenerator(config_path)
            
            # Test scenarios
            scenarios = [
                {
                    "name": "Product Hero Layout",
                    "method": "generate_enhanced_hero_layout",
                    "args": ["Premium Quality Bags", "Handcrafted Excellence", "Fashion Store"],
                    "filename": "improved_hero_with_images.png"
                },
                {
                    "name": "Quote with Product Background",
                    "method": "generate_text_layout",
                    "args": ["quote", {
                        "quote": "Style is a way to say who you are without having to speak",
                        "author": "Rachel Zoe",
                        "brand": "Fashion Store"
                    }],
                    "filename": "improved_quote_with_product.png"
                },
                {
                    "name": "Announcement with Product",
                    "method": "generate_text_layout",
                    "args": ["announcement", {
                        "title": "NEW COLLECTION",
                        "description": "Discover our latest handcrafted leather bags. Premium quality meets timeless design.",
                        "cta": "SHOP NOW",
                        "brand": "Fashion Store"
                    }],
                    "filename": "improved_announcement_with_product.png"
                }
            ]
            
            for scenario in scenarios:
                print(f"\n🎨 Testing: {scenario['name']}")
                try:
                    method = getattr(generator, scenario['method'])
                    img = method(*scenario['args'])
                    
                    output_path = f"output/{scenario['filename']}"
                    img.save(output_path, 'PNG', quality=95)
                    print(f"✅ Generated: {output_path}")
                    
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    
        except Exception as e:
            print(f"❌ Generator failed: {e}")
    else:
        print("❌ Required image files not found!")

def main():
    """Run improved visibility tests"""
    print("🔍 TESTING IMPROVED TEXT VISIBILITY FEATURES")
    print("=" * 60)
    
    test_improved_text_layouts()
    test_with_user_images()
    
    print("\n📊 IMPROVED VISIBILITY TEST SUMMARY")
    print("=" * 40)
    
    # List all generated files
    output_files = [f for f in os.listdir("output") if f.startswith('improved_') and f.endswith('.png')]
    print(f"📁 Generated {len(output_files)} improved visibility images:")
    for file in sorted(output_files):
        print(f"   - {file}")
    
    print("\n🎉 Improved visibility testing completed!")
    print("📝 Check the improved_* files in output/ for better text visibility")

if __name__ == "__main__":
    main()
