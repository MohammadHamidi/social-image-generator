#!/usr/bin/env python3
"""
Test script for new text-based layout features
Demonstrates quote, article, announcement, list, and testimonial layouts
"""

import os
import sys
import json
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_social_generator import EnhancedSocialImageGenerator

def test_text_layouts():
    """Test all text-based layout types"""
    print("🧪 Testing Text-Based Layout Features")
    print("=" * 50)
    
    # Load configuration and content
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'text_layouts_config.json')
    content_path = os.path.join(os.path.dirname(__file__), 'config', 'sample_text_content.json')
    
    # Initialize generator
    generator = EnhancedSocialImageGenerator(config_path)
    
    # Load sample content
    with open(content_path, 'r', encoding='utf-8') as f:
        sample_content = json.load(f)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Test each layout type
    layout_tests = [
        ('quote', sample_content['quote_content']),
        ('article', sample_content['article_content']),
        ('announcement', sample_content['announcement_content']),
        ('list', sample_content['list_content']),
        ('testimonial', sample_content['testimonial_content'])
    ]
    
    print("🎨 Generating text layouts...")
    
    for layout_type, content in layout_tests:
        try:
            print(f"  📝 Creating {layout_type} layout...")
            
            # Generate image
            img = generator.generate_text_layout(layout_type, content)
            
            # Save image
            output_path = os.path.join(output_dir, f"text_layout_{layout_type}.png")
            img.save(output_path, 'PNG', quality=95)
            
            print(f"  ✅ Saved: {output_path}")
            
        except Exception as e:
            print(f"  ❌ Failed to generate {layout_type}: {e}")
    
    # Test batch generation
    print("\n🔄 Testing batch generation...")
    try:
        # Use quote content as base for all layouts (just for demo)
        base_content = {
            # Quote layout
            'quote': 'The best time to plant a tree was 20 years ago. The second best time is now.',
            'author': 'Chinese Proverb',
            
            # Article layout
            'title': 'Sustainable Living Tips',
            'body': 'Small changes in our daily habits can make a significant impact on the environment. Start with reducing waste, conserving energy, and choosing sustainable products. Every action counts towards a better future.',
            
            # Announcement layout
            'description': 'Join us for our upcoming sustainability workshop where you will learn practical tips for eco-friendly living.',
            'cta': 'Register Now',
            
            # List layout
            'items': [
                'Reduce plastic consumption',
                'Use renewable energy sources',
                'Support local businesses',
                'Practice mindful consumption',
                'Educate others about sustainability'
            ],
            
            # Testimonial layout
            'person_name': 'Emma Watson',
            'person_title': 'Environmental Activist',
            
            # Common
            'brand': 'Green Living'
        }
        
        generator.generate_all_text_layouts(base_content, "batch_test")
        print("✅ Batch generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Batch generation failed: {e}")
    
    print("\n📊 Test Summary:")
    print("- Text layouts: quote, article, announcement, list, testimonial")
    print("- Features: multi-line text wrapping, justified alignment, various typography")
    print("- Output directory: output/")
    print("\n🎉 Text layout testing completed!")

def test_multilingual_support():
    """Test text layouts with Arabic/Farsi content"""
    print("\n🌍 Testing Multilingual Support")
    print("=" * 30)
    
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'text_layouts_config.json')
    generator = EnhancedSocialImageGenerator(config_path)
    
    # Arabic/Farsi content
    arabic_content = {
        'quote': 'العلم نور والجهل ظلام',
        'author': 'مثل عربي',
        'title': 'التكنولوجيا الحديثة',
        'body': 'تغير التكنولوجيا الحديثة طريقة عيشنا وعملنا. الذكاء الاصطناعي والتعلم الآلي يفتحان آفاقاً جديدة للابتكار والتطوير في جميع المجالات.',
        'description': 'انضم إلينا في ورشة العمل القادمة حول التكنولوجيا',
        'cta': 'سجل الآن',
        'items': [
            'استخدم التكنولوجيا بحكمة',
            'تعلم المهارات الجديدة',
            'شارك المعرفة مع الآخرين'
        ],
        'person_name': 'أحمد محمد',
        'person_title': 'مطور برمجيات',
        'brand': 'تقنية المستقبل'
    }
    
    try:
        print("📝 Generating Arabic content layouts...")
        
        # Test Arabic quote
        img = generator.generate_text_layout('quote', arabic_content)
        output_path = os.path.join(generator.output_dir, "arabic_quote_layout.png")
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Arabic quote saved: {output_path}")
        
        # Test Arabic article
        img = generator.generate_text_layout('article', arabic_content)
        output_path = os.path.join(generator.output_dir, "arabic_article_layout.png")
        img.save(output_path, 'PNG', quality=95)
        print(f"✅ Arabic article saved: {output_path}")
        
        print("🎉 Multilingual testing completed!")
        
    except Exception as e:
        print(f"❌ Multilingual testing failed: {e}")

if __name__ == "__main__":
    test_text_layouts()
    test_multilingual_support()
