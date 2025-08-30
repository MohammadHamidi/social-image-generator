#!/usr/bin/env python3
"""
Final comprehensive API test for all functionality
Tests both text layouts and image-based layouts through the API
"""

import requests
import json
import time
import os

# API base URL
BASE_URL = "http://localhost:5000"

def test_text_layouts_api():
    """Test all text layout types through API"""
    print("📡 TESTING TEXT LAYOUTS VIA API")
    print("=" * 40)
    
    text_tests = [
        {
            "layout_type": "quote",
            "content": {
                "quote": "The only impossible journey is the one you never begin",
                "author": "Tony Robbins", 
                "brand": "Success Mindset"
            }
        },
        {
            "layout_type": "article",
            "content": {
                "title": "The Power of Persistence",
                "body": "Success is not about avoiding failure, but about learning from it and persisting through challenges. Every setback is a setup for a comeback.",
                "brand": "Growth Academy"
            }
        },
        {
            "layout_type": "announcement",
            "content": {
                "title": "FLASH SALE",
                "description": "Limited time offer: 70% off all premium courses. Upgrade your skills today!",
                "cta": "GET DISCOUNT",
                "brand": "EduPlatform"
            }
        },
        {
            "layout_type": "list",
            "content": {
                "title": "Productivity Hacks",
                "items": [
                    "Start your day with the most important task",
                    "Use the Pomodoro Technique for focus",
                    "Eliminate distractions during work hours",
                    "Take regular breaks to maintain energy",
                    "Review and plan for the next day"
                ],
                "brand": "Productivity Pro"
            }
        },
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "This platform transformed my learning experience. The courses are engaging and the results speak for themselves.",
                "person_name": "Alex Chen",
                "person_title": "Software Developer",
                "brand": "Success Stories"
            }
        }
    ]
    
    for test in text_tests:
        print(f"\n📝 Testing {test['layout_type']} via API...")
        try:
            response = requests.post(f"{BASE_URL}/generate_text", json=test, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {data['filename']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ API server not running. Please start the server first.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            
        time.sleep(0.5)
    
    return True

def test_batch_generation_api():
    """Test batch generation through API"""
    print("\n🔄 TESTING BATCH GENERATION VIA API")
    print("=" * 40)
    
    batch_content = {
        "content": {
            # Works for all layouts
            "quote": "Innovation distinguishes between a leader and a follower",
            "author": "Steve Jobs",
            "title": "Leadership in Innovation",
            "body": "True leaders don't just manage teams; they inspire innovation and drive change. They see opportunities where others see obstacles.",
            "description": "Join our leadership workshop series and learn to lead with innovation.",
            "cta": "REGISTER NOW",
            "items": [
                "Think differently about problems",
                "Encourage creative solutions",
                "Lead by example",
                "Embrace failure as learning",
                "Foster team collaboration"
            ],
            "person_name": "Maria Garcia",
            "person_title": "Innovation Director",
            "brand": "Leadership Excellence"
        },
        "output_prefix": "api_batch_test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate_all_text", json=batch_content, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated {len(data['generated_files'])} layouts:")
            for file_info in data['generated_files']:
                print(f"   - {file_info['layout_type']}: {file_info['filename']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_original_image_generation_api():
    """Test original image generation functionality"""
    print("\n🖼️  TESTING ORIGINAL IMAGE GENERATION VIA API")
    print("=" * 50)
    
    # Test with uploaded images
    generate_request = {
        "headline": "Premium Leather Collection",
        "subheadline": "Handcrafted Excellence",
        "brand": "Fashion Store",
        "use_custom_images": True,
        "main_image": "main.png",
        "watermark_image": "watermark.png",
        "background_image": "bg.png"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", json=generate_request, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated original layout: {data['filename']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_info_endpoints():
    """Test information endpoints"""
    print("\n📋 TESTING API INFO ENDPOINTS")
    print("=" * 35)
    
    endpoints = [
        ("/", "Main API info"),
        ("/health", "Health check"),
        ("/text_layout_info", "Text layout info"),
        ("/files", "File listing")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")

def check_generated_files():
    """Check files in the generated directory"""
    print("\n📁 CHECKING GENERATED FILES")
    print("=" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/files", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total generated images: {data['total_generated']}")
            
            if data['total_generated'] > 0:
                print("📁 Recent generated files:")
                # Show last 10 files
                for file in data['generated_images'][-10:]:
                    print(f"   - {file}")
        else:
            print(f"❌ Failed to get file list: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking files: {e}")

def main():
    """Run comprehensive API tests"""
    print("🧪 FINAL COMPREHENSIVE API TEST")
    print("=" * 50)
    print("🚨 MAKE SURE API SERVER IS RUNNING: python3 social_image_api.py")
    print("=" * 50)
    
    # Test all functionality
    if test_text_layouts_api():
        test_batch_generation_api()
        test_original_image_generation_api()
        test_api_info_endpoints()
        check_generated_files()
        
        print("\n🎉 COMPREHENSIVE API TEST COMPLETED!")
        print("📝 All functionality tested through API endpoints")
        print("🔗 Visit http://localhost:5000 for API documentation")
    else:
        print("\n❌ API tests failed - please start the server first")
        print("💡 Run: python3 social_image_api.py")

if __name__ == "__main__":
    main()
