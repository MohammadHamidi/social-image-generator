#!/usr/bin/env python3
"""
Instagram Carousel Generator for Yuan Payment Style Posts

This script generates complete Instagram carousel posts with:
- Multiple slides (typically 5-10 slides)
- Consistent branding across all slides
- Mixed layouts (headline, checklist, product showcase, etc.)
- Farsi text support
- Custom images and logos

Usage:
    python generate_instagram_carousel.py carousel_config.json
"""

import requests
import json
import sys
import time
from pathlib import Path

BASE_URL = "http://localhost:5000"

def generate_carousel(config_file):
    """Generate a complete Instagram carousel from configuration file."""
    
    print("📊 Instagram Carousel Generator")
    print("="*60)
    
    # Load configuration
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    carousel_posts = config.get('carousel_posts', [])
    metadata = config.get('metadata', {})
    
    print(f"Campaign: {metadata.get('campaign_name', 'Unnamed')}")
    print(f"Total Slides: {len(carousel_posts)}")
    print(f"="*60)
    
    generated_slides = []
    
    # Generate each slide
    for slide_data in carousel_posts:
        slide_num = slide_data.get('slide', 0)
        layout_type = slide_data.get('layout_type', '')
        
        print(f"\n🎨 Generating Slide {slide_num}/{len(carousel_posts)}")
        print(f"   Layout: {layout_type}")
        
        # Prepare generation request
        generation_request = {
            "layout_type": layout_type,
            "content": slide_data.get('content', {}),
            "assets": slide_data.get('assets', {}),
            "background": slide_data.get('background', {}),
            "options": slide_data.get('options', {})
        }
        
        try:
            # Generate slide
            response = requests.post(
                f"{BASE_URL}/generate_post",
                json=generation_request,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    file_info = result['generated_files'][0]
                    
                    # Download the generated slide
                    download_url = f"{BASE_URL}{file_info['download_url']}"
                    img_response = requests.get(download_url, timeout=10)
                    
                    # Save with sequential naming
                    output_filename = f"carousel_slide_{slide_num:02d}_{layout_type}.png"
                    output_path = Path('generated_carousel') / output_filename
                    output_path.parent.mkdir(exist_ok=True)
                    
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    generated_slides.append({
                        'slide': slide_num,
                        'layout': layout_type,
                        'filename': output_filename,
                        'size': len(img_response.content)
                    })
                    
                    print(f"   ✅ Saved: {output_filename}")
                else:
                    print(f"   ❌ Generation failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Small delay between slides
        time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ CAROUSEL GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total Slides Generated: {len(generated_slides)}/{len(carousel_posts)}")
    print(f"Output Directory: generated_carousel/")
    print(f"\nFiles:")
    for slide in generated_slides:
        print(f"  {slide['slide']}. {slide['filename']} ({slide['size']//1024}KB)")
    
    # Save post caption
    if 'post_caption' in metadata:
        caption_file = Path('generated_carousel') / 'post_caption.txt'
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(metadata['post_caption'])
        print(f"\n📝 Caption saved: post_caption.txt")
    
    print(f"\n🎉 Ready to upload to Instagram!")
    print(f"   Upload order: slide_01, slide_02, slide_03...")
    
    return generated_slides

def generate_simple_carousel(title, slides_content):
    """
    Quick helper to generate a carousel from simple content.
    
    Args:
        title: Main carousel title
        slides_content: List of dicts with 'headline' and 'description'
    """
    carousel_config = {
        "carousel_posts": [
            # Cover slide
            {
                "slide": 1,
                "layout_type": "headline_promo",
                "content": {
                    "headline": title,
                    "subheadline": "بکشید برای اطلاعات بیشتر ←",
                },
                "background": {
                    "mode": "gradient",
                    "gradient": {
                        "colors": [[220, 38, 38], [185, 28, 28]],
                        "direction": "vertical"
                    }
                },
                "options": {
                    "text_color": [255, 255, 255],
                    "text_position": "center"
                }
            }
        ]
    }
    
    # Add content slides
    for idx, content in enumerate(slides_content, start=2):
        carousel_config["carousel_posts"].append({
            "slide": idx,
            "layout_type": "split_image_text",
            "content": {
                "title": content.get('headline', ''),
                "description": content.get('description', ''),
                "bullets": content.get('bullets', [])
            },
            "assets": content.get('assets', {}),
            "background": {
                "mode": "solid_color",
                "color": [255, 255, 255]
            }
        })
    
    # Add CTA slide
    carousel_config["carousel_posts"].append({
        "slide": len(slides_content) + 2,
        "layout_type": "headline_promo",
        "content": {
            "headline": "آماده شروع هستید؟",
            "cta": "تماس با ما"
        },
        "background": {
            "mode": "gradient",
            "gradient": {
                "colors": [[220, 38, 38], [185, 28, 28]],
                "direction": "vertical"
            }
        },
        "options": {
            "text_color": [255, 255, 255],
            "text_position": "center"
        }
    })
    
    # Save config
    config_path = Path('generated_carousel') / 'carousel_config.json'
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(carousel_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Config saved: {config_path}")
    return generate_carousel(config_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Generate from config file
        config_file = sys.argv[1]
        generate_carousel(config_file)
    else:
        # Example: Quick carousel generation
        print("📝 Example: Generating quick carousel...")
        
        generate_simple_carousel(
            title="راهنمای واردات از چین",
            slides_content=[
                {
                    "headline": "سرعت و هزینه",
                    "description": "مقایسه روش‌های مختلف",
                    "bullets": ["سریع", "ارزان", "امن"]
                },
                {
                    "headline": "تشخیص فروشندگان معتبر",
                    "description": "چگونه فروشندگان خوب را پیدا کنیم",
                    "bullets": ["بررسی نظرات", "تاریخچه فروش", "گواهینامه‌ها"]
                },
                {
                    "headline": "هزینه‌های پنهان",
                    "description": "هزینه‌هایی که باید بدانید",
                    "bullets": ["گمرک", "حمل", "بیمه"]
                }
            ]
        )

