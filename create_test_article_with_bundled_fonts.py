#!/usr/bin/env python3
"""
Test creating the article that was showing ASCII patterns, now with bundled fonts
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_article_with_bundled_fonts():
    """Test the exact article that was showing ASCII patterns"""
    print("🔧 TESTING ARTICLE WITH BUNDLED FONTS")
    print("=" * 40)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        # Create generator
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        # Same content that was problematic
        content = {
            "title": "Design System Improvements",
            "body": "This article demonstrates the fixed typography hierarchy with proper H1 (72px) title, body text (32px) that respects max-width constraints (780px), and enhanced readability through better line spacing. The text no longer runs too wide and maintains comfortable reading measures.",
            "brand": "Design Excellence"
        }
        
        print("📝 Content to render:")
        print(f"   Title: {content['title']}")
        print(f"   Body: {content['body'][:50]}...")
        print(f"   Brand: {content['brand']}")
        
        print("\n🎨 Generating article with bundled fonts...")
        img = generator.generate_article_layout(**content)
        
        output_path = "output/bundled_fonts_article_test.png"
        img.save(output_path, 'PNG', quality=95)
        
        print(f"✅ Successfully generated: {output_path}")
        print("📝 This should now show proper text instead of ASCII patterns!")
        
        # Also test the original problematic function calls
        print("\n🔍 Testing step-by-step generation...")
        
        # Create fresh image
        test_img = generator._create_enhanced_background()
        test_img = generator._add_gradient_noise(test_img)
        test_img = generator._draw_scrim_overlay(test_img, 'medium')
        
        # Test the specific text rendering
        title_width, title_height = generator._draw_multiline_text(
            test_img, content['title'], generator.fonts['headline'],
            (generator.config['canvas_width'] // 2, 200),
            (255, 255, 255),
            max_width=780,
            alignment='center',
            add_shadow=True
        )
        
        print(f"   Title rendered: {title_width}x{title_height}")
        
        body_width, body_height = generator._draw_multiline_text(
            test_img, content['body'], generator.fonts['subheadline'],
            (generator.config['canvas_width'] // 2, 300),
            (255, 255, 255),
            max_width=780,
            alignment='left',
            justify=True,
            add_shadow=True
        )
        
        print(f"   Body rendered: {body_width}x{body_height}")
        
        step_output_path = "output/bundled_fonts_step_by_step.png"
        test_img.save(step_output_path, 'PNG', quality=95)
        
        print(f"✅ Step-by-step test: {step_output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Article test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_layouts_bundled():
    """Test all layout types with bundled fonts"""
    print("\n🎨 TESTING ALL LAYOUTS WITH BUNDLED FONTS")
    print("=" * 45)
    
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        
        generator = EnhancedSocialImageGenerator('config/design_system_config.json')
        
        layouts_to_test = [
            ("hero", {"title": "Docker Ready", "subtitle": "Self-contained font system", "brand": "Container Tech"}),
            ("quote", {"quote": "Bundled fonts ensure consistent rendering", "author": "DevOps Engineer", "brand": "System Design"}),
            ("article", {"title": "Container Typography", "body": "This demonstrates that the bundled font system works correctly in containerized environments. No more ASCII patterns or missing text rendering.", "brand": "Tech Solutions"}),
            ("announcement", {"title": "Service Ready", "description": "The social image generator is now Docker-ready with bundled fonts", "cta": "Deploy Now", "brand": "Cloud Services"}),
            ("testimonial", {"quote": "The Docker setup works perfectly with bundled fonts", "person_name": "Sarah Developer", "person_title": "Senior Engineer", "brand": "Tech Team"})
        ]
        
        successful_layouts = 0
        
        for layout_name, content in layouts_to_test:
            try:
                print(f"\n📝 Testing {layout_name} layout...")
                
                if layout_name == "hero":
                    img = generator.generate_enhanced_hero_layout(**content)
                elif layout_name == "quote":
                    img = generator.generate_quote_layout(**content)
                elif layout_name == "article":
                    img = generator.generate_article_layout(**content)
                elif layout_name == "announcement":
                    img = generator.generate_announcement_layout(**content)
                elif layout_name == "testimonial":
                    img = generator.generate_testimonial_layout(**content)
                
                output_path = f"output/bundled_fonts_{layout_name}.png"
                img.save(output_path, 'PNG', quality=95)
                
                print(f"   ✅ Generated: {output_path}")
                successful_layouts += 1
                
            except Exception as e:
                print(f"   ❌ Failed {layout_name}: {e}")
        
        print(f"\n📊 Layout Test Results: {successful_layouts}/{len(layouts_to_test)} successful")
        
        if successful_layouts == len(layouts_to_test):
            print("🎉 All layouts working with bundled fonts!")
            print("🐳 Ready for Docker deployment!")
        
        return successful_layouts == len(layouts_to_test)
        
    except Exception as e:
        print(f"❌ Layout testing failed: {e}")
        return False

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    if test_article_with_bundled_fonts():
        test_all_layouts_bundled()
    
    print("\n🎉 Bundled fonts testing completed!")
    print("📝 Compare output/bundled_fonts_* with the previous problematic images")
    print("🐳 Ready to build Docker image: docker build -t social-image-generator .")
