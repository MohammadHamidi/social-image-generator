#!/usr/bin/env python3
"""
Test script for text layout API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_text_layout_info():
    """Test text layout info endpoint"""
    print("📋 Testing text layout info endpoint...")
    
    response = requests.get(f"{BASE_URL}/text_layout_info")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Text layout info retrieved successfully")
        print(f"📊 Available layouts: {list(data['text_layouts'].keys())}")
        print(f"🔧 Features: {data['features']}")
        return True
    else:
        print(f"❌ Failed to get text layout info: {response.status_code}")
        return False

def test_quote_layout():
    """Test quote layout generation"""
    print("\n💬 Testing quote layout...")
    
    content = {
        "layout_type": "quote",
        "content": {
            "quote": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "brand": "Motivation Hub"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Quote layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        print(f"🔗 Download URL: {data['download_url']}")
        return True
    else:
        print(f"❌ Failed to generate quote layout: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_article_layout():
    """Test article layout generation"""
    print("\n📄 Testing article layout...")
    
    content = {
        "layout_type": "article",
        "content": {
            "title": "The Power of Artificial Intelligence",
            "body": "Artificial Intelligence is revolutionizing industries across the globe. From healthcare to finance, AI technologies are enabling unprecedented efficiency and innovation. Machine learning algorithms can now process vast amounts of data to uncover patterns and insights that were previously impossible to detect.",
            "brand": "Tech Today"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Article layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        return True
    else:
        print(f"❌ Failed to generate article layout: {response.status_code}")
        return False

def test_announcement_layout():
    """Test announcement layout generation"""
    print("\n📢 Testing announcement layout...")
    
    content = {
        "layout_type": "announcement",
        "content": {
            "title": "Big Sale Event!",
            "description": "Don't miss our biggest sale of the year. Save up to 70% on selected items. Limited time offer valid until the end of this month.",
            "cta": "Shop Now",
            "brand": "Fashion Store"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Announcement layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        return True
    else:
        print(f"❌ Failed to generate announcement layout: {response.status_code}")
        return False

def test_list_layout():
    """Test list layout generation"""
    print("\n📝 Testing list layout...")
    
    content = {
        "layout_type": "list",
        "content": {
            "title": "5 Essential Skills for 2024",
            "items": [
                "Digital literacy and computer skills",
                "Critical thinking and problem solving",
                "Emotional intelligence and empathy",
                "Adaptability and continuous learning",
                "Communication and collaboration"
            ],
            "brand": "Career Development"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ List layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        return True
    else:
        print(f"❌ Failed to generate list layout: {response.status_code}")
        return False

def test_testimonial_layout():
    """Test testimonial layout generation"""
    print("\n👥 Testing testimonial layout...")
    
    content = {
        "layout_type": "testimonial",
        "content": {
            "quote": "This service exceeded all our expectations. The quality is outstanding and the support team is incredibly responsive. We couldn't be happier with our decision.",
            "person_name": "Dr. Maria Rodriguez",
            "person_title": "Director of Operations, TechCorp",
            "brand": "Customer Reviews"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Testimonial layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        return True
    else:
        print(f"❌ Failed to generate testimonial layout: {response.status_code}")
        return False

def test_batch_generation():
    """Test batch generation of all text layouts"""
    print("\n🔄 Testing batch generation...")
    
    content = {
        "content": {
            # Quote content
            "quote": "Innovation distinguishes between a leader and a follower.",
            "author": "Steve Jobs",
            
            # Article content
            "title": "Future of Remote Work",
            "body": "The shift to remote work has fundamentally changed how we approach productivity and collaboration. Companies are discovering new ways to maintain culture and efficiency in distributed teams.",
            
            # Announcement content
            "description": "Join our webinar series on remote work best practices and productivity tips.",
            "cta": "Register Free",
            
            # List content
            "items": [
                "Set up a dedicated workspace",
                "Establish clear boundaries",
                "Use productivity tools effectively",
                "Maintain regular communication"
            ],
            
            # Testimonial content
            "person_name": "Alex Thompson",
            "person_title": "Remote Team Lead",
            
            # Common
            "brand": "Remote Work Pro"
        },
        "output_prefix": "api_test"
    }
    
    response = requests.post(f"{BASE_URL}/generate_all_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Batch generation completed successfully")
        print(f"📊 Generated {len(data['generated_files'])} layouts:")
        for file_info in data['generated_files']:
            print(f"  - {file_info['layout_type']}: {file_info['filename']}")
        return True
    else:
        print(f"❌ Failed to generate batch layouts: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_multilingual():
    """Test multilingual support with Arabic text"""
    print("\n🌍 Testing multilingual support...")
    
    content = {
        "layout_type": "quote",
        "content": {
            "quote": "العلم نور والجهل ظلام",
            "author": "مثل عربي",
            "brand": "الحكمة اليومية"
        }
    }
    
    response = requests.post(f"{BASE_URL}/generate_text", json=content)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Arabic text layout generated successfully")
        print(f"📁 Filename: {data['filename']}")
        return True
    else:
        print(f"❌ Failed to generate Arabic layout: {response.status_code}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Testing Text Layout API Endpoints")
    print("=" * 50)
    
    tests = [
        test_text_layout_info,
        test_quote_layout,
        test_article_layout,
        test_announcement_layout,
        test_list_layout,
        test_testimonial_layout,
        test_batch_generation,
        test_multilingual
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            time.sleep(0.5)  # Brief pause between tests
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API server. Make sure it's running on localhost:5000")
            break
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed successfully!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
