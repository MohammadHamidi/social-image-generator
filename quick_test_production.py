#!/usr/bin/env python3
"""
Quick Production Test - Tests basic functionality of deployed system
Run this for a fast check: python quick_test_production.py
"""

import requests
import json

BASE_URL = "https://imageeditor.flowiran.ir"


def quick_test():
    """Quick test of production system"""
    print("🚀 Quick Production Test")
    print("="*60)

    # Test 1: Health
    print("\n1️⃣  Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Health check passed")
            data = response.json()
            print(f"   Status: {data.get('status')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # Test 2: Layouts
    print("\n2️⃣  Testing /layouts endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/layouts", timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"   ✅ Found {count} layouts")
            for layout in data.get('layouts', {}).keys():
                print(f"      • {layout}")
        else:
            print(f"   ❌ Layouts failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # Test 3: Generate a simple image
    print("\n3️⃣  Testing /generate_post endpoint...")
    try:
        test_config = {
            "layout_type": "headline_promo",
            "content": {
                "headline": "Test Post",
                "subheadline": "Production test"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 200, 150], [255, 150, 200]],
                    "direction": "vertical"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=test_config,
            timeout=30
        )

        if response.status_code == 200:
            # Save test image
            with open("test_output.png", "wb") as f:
                f.write(response.content)
            print(f"   ✅ Image generated successfully")
            print(f"   Saved to: test_output.png ({len(response.content)} bytes)")
        else:
            print(f"   ❌ Generation failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    print("\n" + "="*60)
    print("🎉 All quick tests passed!")
    print("="*60)


if __name__ == "__main__":
    quick_test()
