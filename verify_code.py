#!/usr/bin/env python3
"""
Code Verification Script - Check if code has all required components
WITHOUT running the server

This verifies your code is complete before even starting the server.
"""

import os
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}")
        print(f"   Missing: {filepath}")
        return False


def check_code_contains(filepath, search_string, description):
    """Check if a file contains a specific string"""
    if not os.path.exists(filepath):
        print(f"❌ {description}")
        print(f"   File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if search_string in content:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            print(f"   Not found in: {filepath}")
            return False


def main():
    """Verify code completeness"""
    print("="*70)
    print("  🔍 CODE VERIFICATION")
    print("  Checking if code has all required components")
    print("="*70)

    all_checks = []

    # Check main API file
    print("\n📋 Checking Main API File:")
    all_checks.append(check_file_exists("social_image_api.py", "Main API file exists"))
    all_checks.append(check_code_contains("social_image_api.py", "@app.route('/layouts'", "Has /layouts endpoint"))
    all_checks.append(check_code_contains("social_image_api.py", "@app.route('/generate_post'", "Has /generate_post endpoint"))
    all_checks.append(check_code_contains("social_image_api.py", "from src.layouts import", "Imports layout engine"))

    # Check layouts directory
    print("\n📋 Checking Layout Engine:")
    all_checks.append(check_file_exists("src/layouts/__init__.py", "Layout engine module"))
    all_checks.append(check_file_exists("src/layouts/base.py", "Layout base classes"))
    all_checks.append(check_file_exists("src/asset_manager.py", "Asset manager"))

    # Check layout implementations
    print("\n📋 Checking Layout Implementations:")
    layouts = [
        "headline_promo",
        "split_image_text",
        "product_showcase",
        "checklist",
        "testimonial",
        "overlay_text",
        "caption_box"
    ]

    for layout in layouts:
        filepath = f"src/layouts/{layout}.py"
        all_checks.append(check_file_exists(filepath, f"Layout: {layout}"))

    # Check examples
    print("\n📋 Checking Examples:")
    all_checks.append(check_file_exists("examples/headline_promo/example_1_minimal.json", "Example: headline_promo"))
    all_checks.append(check_file_exists("examples/split_image_text/example_1_basic.json", "Example: split_image_text"))

    # Check test files
    print("\n📋 Checking Test Files:")
    all_checks.append(check_file_exists("test_integration.py", "Integration tests"))
    all_checks.append(check_file_exists("test_all_group_a.py", "Group A tests"))

    # Summary
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)

    passed = sum(all_checks)
    total = len(all_checks)

    print(f"\n{passed}/{total} checks passed")

    if passed == total:
        print("\n✅ CODE VERIFICATION PASSED!")
        print("\nYour code has all required components:")
        print("  ✅ Both new endpoints (/layouts and /generate_post)")
        print("  ✅ Layout engine architecture")
        print("  ✅ All 7 layout implementations")
        print("  ✅ Asset manager")
        print("  ✅ Example configurations")
        print("  ✅ Test files")
        print("\n📋 Next Step:")
        print("  Test the local server to verify it runs correctly:")
        print("  1. python social_image_api.py")
        print("  2. python test_local_server.py")
        return 0
    else:
        print("\n❌ CODE VERIFICATION FAILED!")
        print(f"\n{total - passed} component(s) missing or incorrect.")
        print("\n📋 Possible Issues:")
        print("  1. You might be on the wrong git branch")
        print("     Check: git status")
        print("     Should show: claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
        print("")
        print("  2. You might need to pull latest changes")
        print("     git pull origin claude/general-fixes-011CUVebGZwwfvQRfYEcbR7u")
        print("")
        print("  3. Files might not be committed yet")
        print("     Check: git status")
        return 1


if __name__ == "__main__":
    exit(main())
