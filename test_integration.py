#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Test - End-to-End System Verification

This script tests the complete system:
1. Server startup
2. API endpoints
3. Layout rendering
4. Gradient generation
5. Farsi text rendering
"""

import sys
import os
import time
import subprocess
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:5000"
SERVER_PROCESS = None


def start_server():
    """Start the Flask server in the background."""
    global SERVER_PROCESS

    print("🚀 Starting Flask server...")

    # Start server
    SERVER_PROCESS = subprocess.Popen(
        [sys.executable, "social_image_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, 'FLASK_ENV': 'development'}
    )

    # Wait for server to start
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                print("✅ Server started successfully")
                return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)

    print("❌ Server failed to start")
    return False


def stop_server():
    """Stop the Flask server."""
    global SERVER_PROCESS

    if SERVER_PROCESS:
        print("\n🛑 Stopping server...")
        SERVER_PROCESS.terminate()
        try:
            SERVER_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            SERVER_PROCESS.kill()
        print("✅ Server stopped")


def test_health_endpoint():
    """Test /health endpoint."""
    print("\n" + "=" * 60)
    print("Test 1: Health Endpoint")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data['status'] == 'healthy', "Server not healthy"

        print("✅ Health endpoint working")
        print(f"   Status: {data['status']}")
        return True
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False


def test_layouts_endpoint():
    """Test /layouts endpoint."""
    print("\n" + "=" * 60)
    print("Test 2: Layouts Endpoint")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/layouts")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert 'layouts' in data, "Missing 'layouts' field"
        assert 'count' in data, "Missing 'count' field"
        assert data['count'] > 0, "No layouts registered"

        print("✅ Layouts endpoint working")
        print(f"   Registered layouts: {data['count']}")
        for name, schema in data['layouts'].items():
            print(f"   - {name}: {schema.get('description', 'No description')}")

        return True
    except Exception as e:
        print(f"❌ Layouts endpoint failed: {e}")
        return False


def test_gradient_endpoint():
    """Test gradient generation (verify fixes)."""
    print("\n" + "=" * 60)
    print("Test 3: Gradient Generation (Verify Fixes)")
    print("=" * 60)

    try:
        # Test gradient generation
        payload = {
            "colors": ["#FF6B6B", "#4ECDC4"],
            "gradient_type": "linear",
            "direction": "vertical",
            "width": 1080,
            "height": 1350,
            "use_hsl_interpolation": True,
            "add_noise": True,
            "noise_intensity": 0.02,
            "apply_dither": False
        }

        response = requests.post(
            f"{BASE_URL}/generate_gradient",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data['success'] == True, "Gradient generation failed"
        assert 'download_url' in data, "Missing download_url"

        print("✅ Gradient generation working")
        print(f"   File: {data['filename']}")
        print(f"   Size: {data['size']} bytes")
        print(f"   Dimensions: {data['dimensions']['width']}x{data['dimensions']['height']}")

        # Verify the file exists
        download_url = data['download_url']
        file_response = requests.get(f"{BASE_URL}{download_url}")
        assert file_response.status_code == 200, "Generated file not accessible"

        print(f"   ✅ File accessible at {download_url}")

        return True
    except Exception as e:
        print(f"❌ Gradient generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_minimal():
    """Test headline_promo with minimal content."""
    print("\n" + "=" * 60)
    print("Test 4: headline_promo Layout - Minimal")
    print("=" * 60)

    try:
        payload = {
            "layout_type": "headline_promo",
            "content": {
                "headline": "Summer Sale"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 107, 107], [253, 187, 45]],
                    "direction": "vertical"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data['success'] == True, "Generation failed"
        assert data['layout_type'] == 'headline_promo', "Wrong layout type"
        assert len(data['generated_files']) == 1, "Expected 1 file"

        file_info = data['generated_files'][0]

        print("✅ headline_promo minimal generation working")
        print(f"   File: {file_info['filename']}")
        print(f"   Size: {file_info['size_bytes']} bytes")
        print(f"   Dimensions: {file_info['width']}x{file_info['height']}")

        return True
    except Exception as e:
        print(f"❌ headline_promo minimal failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_full():
    """Test headline_promo with full content."""
    print("\n" + "=" * 60)
    print("Test 5: headline_promo Layout - Full Content")
    print("=" * 60)

    try:
        payload = {
            "layout_type": "headline_promo",
            "content": {
                "headline": "Summer Sale",
                "subheadline": "Up to 50% Off Everything",
                "cta": "Shop Now"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 107, 107], [253, 187, 45]],
                    "direction": "vertical"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data['success'] == True, "Generation failed"

        print("✅ headline_promo full content working")
        print(f"   File: {data['generated_files'][0]['filename']}")

        return True
    except Exception as e:
        print(f"❌ headline_promo full content failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_headline_promo_farsi():
    """Test headline_promo with Farsi text (verify fixes)."""
    print("\n" + "=" * 60)
    print("Test 6: headline_promo Layout - Farsi Text (Verify Fixes)")
    print("=" * 60)

    try:
        payload = {
            "layout_type": "headline_promo",
            "content": {
                "headline": "فروش تابستانی",
                "subheadline": "تا ۵۰٪ تخفیف روی همه محصولات",
                "cta": "خرید کنید"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[78, 205, 196], [255, 107, 107]],
                    "direction": "vertical"
                }
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data['success'] == True, "Generation failed"

        print("✅ Farsi text rendering working")
        print(f"   File: {data['generated_files'][0]['filename']}")
        print("   ✅ RTL text processing successful")

        return True
    except Exception as e:
        print(f"❌ Farsi text rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_invalid_layout_type():
    """Test error handling for invalid layout type."""
    print("\n" + "=" * 60)
    print("Test 7: Error Handling - Invalid Layout Type")
    print("=" * 60)

    try:
        payload = {
            "layout_type": "nonexistent_layout",
            "content": {
                "headline": "Test"
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert 'error' in data, "Missing error field"
        assert 'available_layouts' in data, "Missing available_layouts field"

        print("✅ Error handling working")
        print(f"   Error message: {data['error']}")
        print(f"   Available layouts shown: {len(data['available_layouts'])}")

        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_missing_required_content():
    """Test validation for missing required content."""
    print("\n" + "=" * 60)
    print("Test 8: Validation - Missing Required Content")
    print("=" * 60)

    try:
        payload = {
            "layout_type": "headline_promo",
            "content": {
                # Missing required 'headline' field
            }
        }

        response = requests.post(
            f"{BASE_URL}/generate_post",
            json=payload,
            timeout=30
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert 'error' in data, "Missing error field"

        print("✅ Validation working")
        print(f"   Error message: {data['error']}")

        return True
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("🧪 Integration Test Suite - Complete System Verification")
    print("=" * 60)

    # Start server
    if not start_server():
        print("\n❌ Cannot proceed without server")
        return 1

    try:
        # Run all tests
        results = []

        results.append(("Health Endpoint", test_health_endpoint()))
        results.append(("Layouts Endpoint", test_layouts_endpoint()))
        results.append(("Gradient Generation (Fixed)", test_gradient_endpoint()))
        results.append(("headline_promo Minimal", test_headline_promo_minimal()))
        results.append(("headline_promo Full", test_headline_promo_full()))
        results.append(("Farsi Text (Fixed)", test_headline_promo_farsi()))
        results.append(("Invalid Layout Error", test_invalid_layout_type()))
        results.append(("Missing Content Validation", test_missing_required_content()))

        # Print summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)

        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name:.<45} {status}")

        total = len(results)
        passed_count = sum(1 for _, p in results if p)

        print(f"\nTotal: {passed_count}/{total} tests passed")

        if passed_count == total:
            print("\n🎉 All integration tests passed!")
            print("\n✅ Complete System Verification Successful!")
            print("\nVerified:")
            print("  ✅ Server starts and responds")
            print("  ✅ Layout registry working")
            print("  ✅ Gradient generation (with fixes)")
            print("  ✅ Farsi text rendering (with fixes)")
            print("  ✅ headline_promo layout working")
            print("  ✅ Error handling functional")
            print("  ✅ Validation working")
            return 0
        else:
            print(f"\n⚠️  {total - passed_count} test(s) failed")
            return 1

    finally:
        stop_server()


if __name__ == "__main__":
    sys.exit(main())
