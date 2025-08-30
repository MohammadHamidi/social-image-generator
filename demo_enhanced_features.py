#!/usr/bin/env python3
"""
Demo script showcasing the enhanced Social Image Generator features:
- Background removal for custom images
- Advanced color control
- Multiple gradient types
- Layout-specific color schemes
"""

import sys
import os
sys.path.append('src')

from enhanced_social_generator import EnhancedSocialImageGenerator
import json

def create_sample_configs():
    """Create sample configuration files for different use cases"""

    # Modern gradient theme
    modern_config = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "background": {
            "type": "gradient",
            "primary_color": [67, 56, 202],      # Indigo
            "secondary_color": [147, 51, 234],   # Purple
            "gradient_direction": "diagonal"
        },
        "layout_colors": {
            "hero": {
                "headline_color": [255, 255, 255],
                "subheadline_color": [229, 231, 235],
                "brand_color": [156, 163, 175],
                "text_panel_bg": [0, 0, 0, 120]
            }
        },
        "custom_images": {
            "use_custom_images": True,
            "remove_background": True,
            "background_removal_method": "auto",
            "main_image_size": [600, 400],
            "main_image_position": [240, 450]
        }
    }

    # High contrast theme
    contrast_config = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "background": {
            "type": "solid",
            "primary_color": [17, 24, 39]  # Dark gray
        },
        "layout_colors": {
            "hero": {
                "headline_color": [255, 255, 255],
                "subheadline_color": [249, 250, 251],
                "brand_color": [34, 197, 94],  # Green accent
                "text_panel_bg": [55, 65, 81, 200]
            }
        },
        "custom_images": {
            "use_custom_images": True,
            "remove_background": True,
            "background_removal_method": "edge_detection",
            "edge_threshold": 40
        }
    }

    # Warm gradient theme
    warm_config = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "background": {
            "type": "gradient",
            "primary_color": [251, 146, 60],    # Orange
            "secondary_color": [239, 68, 68],   # Red
            "gradient_direction": "radial"
        },
        "layout_colors": {
            "hero": {
                "headline_color": [255, 255, 255],
                "subheadline_color": [254, 249, 195],
                "brand_color": [255, 237, 213],
                "text_panel_bg": [120, 53, 15, 180]
            }
        },
        "custom_images": {
            "use_custom_images": True,
            "remove_background": True,
            "background_removal_method": "color_threshold",
            "color_tolerance": 25
        }
    }

    return {
        'modern': modern_config,
        'contrast': contrast_config,
        'warm': warm_config
    }

def demo_background_removal_methods():
    """Demonstrate different background removal methods"""
    print("🔧 Testing Background Removal Methods")
    print("=" * 50)

    # Sample content
    content = {
        'headline': 'Enhanced Generator',
        'subheadline': 'With Background Removal',
        'brand': 'Demo Studio'
    }

    methods = ['auto', 'edge_detection', 'color_threshold']

    for method in methods:
        print(f"Testing {method} method...")

        config = {
            "custom_images": {
                "use_custom_images": True,
                "remove_background": True,
                "background_removal_method": method,
                "main_image_path": "assets/custom/main_section.png",
                "blueprint_image_path": "assets/custom/blueprint.png"
            }
        }

        try:
            # Create generator with temporary config
            with open('temp_config.json', 'w') as f:
                json.dump(config, f)

            generator = EnhancedSocialImageGenerator('temp_config.json')
            img = generator.generate_enhanced_hero_layout(
                content['headline'],
                content['subheadline'],
                content['brand']
            )

            # Save with method name
            output_path = f"output/demo_{method}_removal.png"
            os.makedirs('output', exist_ok=True)
            img.save(output_path, 'PNG')
            print(f"✓ Saved: {output_path}")

        except Exception as e:
            print(f"✗ Failed {method}: {e}")
        finally:
            # Cleanup temp file
            if os.path.exists('temp_config.json'):
                os.remove('temp_config.json')

    print()

def demo_gradient_backgrounds():
    """Demonstrate different gradient types"""
    print("🎨 Testing Gradient Backgrounds")
    print("=" * 40)

    content = {
        'headline': 'Gradient Backgrounds',
        'subheadline': 'Multiple Direction Types',
        'brand': 'Design Studio'
    }

    gradient_types = ['horizontal', 'vertical', 'diagonal', 'radial']

    for gradient_type in gradient_types:
        print(f"Generating {gradient_type} gradient...")

        config = {
            "background": {
                "type": "gradient",
                "primary_color": [59, 130, 246],   # Blue
                "secondary_color": [147, 51, 234], # Purple
                "gradient_direction": gradient_type
            }
        }

        try:
            # Create temporary config
            with open('temp_config.json', 'w') as f:
                json.dump(config, f)

            generator = EnhancedSocialImageGenerator('temp_config.json')
            img = generator.generate_enhanced_hero_layout(
                content['headline'],
                content['subheadline'],
                content['brand']
            )

            # Save with gradient type name
            output_path = f"output/demo_gradient_{gradient_type}.png"
            img.save(output_path, 'PNG')
            print(f"✓ Saved: {output_path}")

        except Exception as e:
            print(f"✗ Failed {gradient_type}: {e}")
        finally:
            if os.path.exists('temp_config.json'):
                os.remove('temp_config.json')

    print()

def demo_color_themes():
    """Demonstrate different color themes"""
    print("🌈 Testing Color Themes")
    print("=" * 30)

    content = {
        'headline': 'Custom Color Themes',
        'subheadline': 'Professional Styling',
        'brand': 'Theme Demo'
    }

    configs = create_sample_configs()

    for theme_name, config in configs.items():
        print(f"Generating {theme_name} theme...")

        try:
            # Create temporary config
            with open('temp_config.json', 'w') as f:
                json.dump(config, f, indent=2)

            generator = EnhancedSocialImageGenerator('temp_config.json')
            img = generator.generate_enhanced_hero_layout(
                content['headline'],
                content['subheadline'],
                content['brand']
            )

            # Save with theme name
            output_path = f"output/demo_theme_{theme_name}.png"
            img.save(output_path, 'PNG')
            print(f"✓ Saved: {output_path}")

        except Exception as e:
            print(f"✗ Failed {theme_name}: {e}")
        finally:
            if os.path.exists('temp_config.json'):
                os.remove('temp_config.json')

    print()

def demo_custom_images_with_removal():
    """Demonstrate custom images with background removal"""
    print("🖼️  Testing Custom Images with Background Removal")
    print("=" * 55)

    content = {
        'headline': 'Custom Images',
        'subheadline': 'Background Removed',
        'brand': 'Image Studio'
    }

    # Check if custom images exist
    main_image_path = "assets/custom/main_section.png"
    blueprint_path = "assets/custom/blueprint.png"

    if not os.path.exists(main_image_path):
        print(f"⚠️  Custom image not found: {main_image_path}")
        print("Please add your custom images to assets/custom/ to test this feature")
        return

    config = {
        "background": {
            "type": "gradient",
            "primary_color": [99, 102, 241],
            "secondary_color": [168, 85, 247],
            "gradient_direction": "diagonal"
        },
        "custom_images": {
            "use_custom_images": True,
            "main_image_path": main_image_path,
            "blueprint_image_path": blueprint_path,
            "remove_background": True,
            "background_removal_method": "auto",
            "main_image_size": [500, 400],
            "blueprint_image_size": [150, 100],
            "main_image_position": [290, 500],
            "blueprint_image_position": [750, 300]
        },
        "layout_colors": {
            "hero": {
                "headline_color": [255, 255, 255],
                "subheadline_color": [243, 244, 246],
                "brand_color": [209, 213, 219]
            }
        }
    }

    try:
        with open('temp_config.json', 'w') as f:
            json.dump(config, f, indent=2)

        generator = EnhancedSocialImageGenerator('temp_config.json')
        img = generator.generate_enhanced_hero_layout(
            content['headline'],
            content['subheadline'],
            content['brand']
        )

        output_path = "output/demo_custom_images_removed_bg.png"
        img.save(output_path, 'PNG')
        print(f"✓ Saved: {output_path}")

    except Exception as e:
        print(f"✗ Failed: {e}")
    finally:
        if os.path.exists('temp_config.json'):
            os.remove('temp_config.json')

    print()

def create_comparison_image():
    """Create before/after comparison"""
    print("📊 Creating Before/After Comparison")
    print("=" * 40)

    content = {
        'headline': 'Before vs After',
        'subheadline': 'Enhancement Comparison',
        'brand': 'Demo'
    }

    # Original version (simple)
    simple_config = {
        "background": {
            "type": "solid",
            "primary_color": [255, 100, 100]
        }
    }

    # Enhanced version
    enhanced_config = {
        "background": {
            "type": "gradient",
            "primary_color": [236, 72, 153],
            "secondary_color": [124, 58, 237],
            "gradient_direction": "radial"
        },
        "layout_colors": {
            "hero": {
                "headline_color": [255, 255, 255],
                "subheadline_color": [248, 250, 252],
                "brand_color": [203, 213, 225],
                "text_panel_bg": [15, 23, 42, 160]
            }
        }
    }

    try:
        # Generate simple version
        with open('temp_config.json', 'w') as f:
            json.dump(simple_config, f)

        simple_gen = EnhancedSocialImageGenerator('temp_config.json')
        simple_img = simple_gen.generate_enhanced_hero_layout(
            content['headline'], content['subheadline'], content['brand']
        )
        simple_img.save("output/demo_before_enhancement.png", 'PNG')

        # Generate enhanced version
        with open('temp_config.json', 'w') as f:
            json.dump(enhanced_config, f)

        enhanced_gen = EnhancedSocialImageGenerator('temp_config.json')
        enhanced_img = enhanced_gen.generate_enhanced_hero_layout(
            content['headline'], content['subheadline'], content['brand']
        )
        enhanced_img.save("output/demo_after_enhancement.png", 'PNG')

        print("✓ Created comparison images:")
        print("  - demo_before_enhancement.png")
        print("  - demo_after_enhancement.png")

    except Exception as e:
        print(f"✗ Failed: {e}")
    finally:
        if os.path.exists('temp_config.json'):
            os.remove('temp_config.json')

def main():
    """Run all demos"""
    print("🚀 Enhanced Social Image Generator - Demo")
    print("=" * 50)
    print()

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Run demos
    demo_gradient_backgrounds()
    demo_color_themes()
    demo_background_removal_methods()
    demo_custom_images_with_removal()
    create_comparison_image()

    print("🎉 All demos completed!")
    print("Check the 'output' directory for generated images.")
    print()
    print("📝 Next Steps:")
    print("1. Add your custom images to assets/custom/")
    print("2. Modify configs in demo to match your brand")
    print("3. Run individual demos or create your own configs")

if __name__ == "__main__":
    main()
