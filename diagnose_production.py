#!/usr/bin/env python3
"""
Production Deployment Diagnostic - Check what's actually deployed
"""

import requests
import json

BASE_URL = "https://imageeditor.flowiran.ir"

def check_endpoint(method, path, description):
    """Check if an endpoint exists"""
    print(f"\nChecking: {method} {path}")
    print(f"Purpose: {description}")

    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
        else:
            response = requests.head(f"{BASE_URL}{path}", timeout=10)

        if response.status_code == 404:
            print(f"  ❌ Not Found (404) - Endpoint doesn't exist")
            return False
        elif response.status_code < 400:
            print(f"  ✅ Available ({response.status_code})")
            return True
        else:
            print(f"  ⚠️  Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Check what endpoints are available"""
    print("="*70)
    print("  🔍 Production Deployment Diagnostic")
    print("="*70)
    print(f"\nTarget: {BASE_URL}")

    # Check health
    print("\n" + "="*70)
    print("  System Health")
    print("="*70)

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System is healthy")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Platform: {data.get('system', {}).get('platform', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # Check endpoints
    print("\n" + "="*70)
    print("  Available Endpoints")
    print("="*70)

    endpoints = {
        # New endpoints (from layout engine)
        ("GET", "/layouts", "List available layout types (NEW)"),
        ("POST", "/generate_post", "Universal layout generation endpoint (NEW)"),

        # Original endpoints
        ("GET", "/", "API documentation homepage"),
        ("GET", "/gradient_info", "Gradient generation info"),
        ("GET", "/text_layout_info", "Text layout info"),
        ("POST", "/generate", "Original image generation"),
        ("POST", "/generate_gradient", "Gradient generation"),
        ("POST", "/generate_text", "Text-based layouts"),
        ("POST", "/generate_all_text", "All text layouts"),
        ("GET", "/files", "List uploaded files"),
        ("POST", "/upload/main", "Upload main image"),
        ("POST", "/upload/watermark", "Upload watermark"),
        ("POST", "/upload/background", "Upload background"),
    }

    available = []
    missing = []

    for method, path, desc in endpoints:
        result = check_endpoint(method, path, desc)
        if result:
            available.append((method, path))
        else:
            missing.append((method, path))

    # Summary
    print("\n" + "="*70)
    print("  Summary")
    print("="*70)

    print(f"\n✅ Available endpoints: {len(available)}")
    for method, path in available:
        print(f"   • {method} {path}")

    print(f"\n❌ Missing endpoints: {len(missing)}")
    for method, path in missing:
        print(f"   • {method} {path}")

    # Diagnosis
    print("\n" + "="*70)
    print("  Diagnosis")
    print("="*70)

    if ("GET", "/layouts") in missing and ("POST", "/generate_post") in missing:
        print("\n⚠️  NEW LAYOUT ENGINE NOT DEPLOYED")
        print("\nThe production server is running an OLDER version without:")
        print("  • Layout engine architecture")
        print("  • /layouts endpoint")
        print("  • /generate_post endpoint")
        print("  • All 7 new layout types")

        print("\n📋 TO FIX:")
        print("  1. Deploy the latest code from branch:")
        print("     claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
        print("  2. Or merge the pull request to main and deploy")
        print("  3. Restart the production server")

        print("\n💡 CURRENT DEPLOYMENT:")
        print("  The server is healthy but running OLD code.")
        print("  You can still test the original endpoints with:")
        print("    • POST /generate")
        print("    • POST /generate_gradient")
        print("    • POST /generate_text")

    elif ("GET", "/layouts") in available and ("POST", "/generate_post") in available:
        print("\n✅ LATEST CODE DEPLOYED")
        print("\nThe production server has the new layout engine!")
        print("You can test all 7 layouts with:")
        print("  python test_production_deployment.py")

    else:
        print("\n⚠️  PARTIAL DEPLOYMENT")
        print("\nSome but not all new endpoints are available.")
        print("This might indicate an incomplete deployment.")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
