#!/usr/bin/env python3
"""
Simple Social Media Gradient Generator
Uses requests library to generate gradients via the API
"""

import requests
import json
import time
import os

# Social Media Gradient Palettes
PALETTES = {
    "sunset_glow": {
        "name": "Sunset Glow",
        "colors": ["#FF6B6B", "#FFD93D", "#6BCB77"]
    },
    "ocean_breeze": {
        "name": "Ocean Breeze",
        "colors": ["#00C9FF", "#92FE9D"]
    },
    "cotton_candy": {
        "name": "Cotton Candy",
        "colors": ["#FF9A9E", "#FAD0C4", "#FBC2EB", "#A6C1EE"]
    },
    "neon_vibes": {
        "name": "Neon Vibes",
        "colors": ["#FF6FD8", "#3813C2"]
    },
    "sunrise_horizon": {
        "name": "Sunrise Horizon",
        "colors": ["#FEE140", "#FA709A"]
    },
    "minimal_mint": {
        "name": "Minimal Mint",
        "colors": ["#D9F3E5", "#E0C3FC"]
    },
    "electric_blue": {
        "name": "Electric Blue",
        "colors": ["#1FA2FF", "#12D8FA", "#A6FFCB"]
    },
    "rose_gold": {
        "name": "Rose Gold",
        "colors": ["#FBD3E9", "#BB377D"]
    },
    "dark_mode_luxe": {
        "name": "Dark Mode Luxe",
        "colors": ["#434343", "#000000", "#2C5364"]
    },
    "vivid_coral": {
        "name": "Vivid Coral",
        "colors": ["#FF512F", "#DD2476"]
    }
}

def test_server():
    """Test if the server is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the Flask server is running on http://localhost:5000")
        return False

def generate_gradient(palette_name, palette_data, gradient_type="linear", direction="vertical"):
    """Generate a single gradient"""
    url = "http://localhost:5000/generate_gradient"

    payload = {
        "width": 1080,
        "height": 1350,
        "colors": palette_data["colors"],
        "gradient_type": gradient_type,
        "direction": direction,
        "use_hsl_interpolation": True,
        "add_noise": True,
        "noise_intensity": 0.02,
        "quality": 95
    }

    try:
        print(f"🎨 Generating {palette_name} - {gradient_type} {direction}")

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ Success: {result['filename']}")
                print(f"   Size: {result['size']} bytes")
                print(f"   URL: {result['download_url']}")
                return result
            else:
                print(f"❌ API Error: {result.get('error')}")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return None

def main():
    """Main function to generate all gradients"""
    print("🚀 Social Media Gradient Generator")
    print("=" * 50)

    # Test server connection
    if not test_server():
        return

    # Generate gradients for each palette
    results = []

    for palette_key, palette_data in PALETTES.items():
        print(f"\n🎨 Processing {palette_data['name']}")
        print(f"   Colors: {', '.join(palette_data['colors'])}")

        palette_results = []

        # Generate different types
        configs = [
            ("linear", "vertical"),
            ("linear", "horizontal"),
            ("radial", "vertical"),
            ("diagonal", "diagonal")
        ]

        for gradient_type, direction in configs:
            result = generate_gradient(palette_key, palette_data, gradient_type, direction)
            if result:
                result["config"] = {"type": gradient_type, "direction": direction}
                palette_results.append(result)

            time.sleep(0.5)  # Small delay between requests

        results.append({
            "palette": palette_key,
            "name": palette_data["name"],
            "results": palette_results
        })

    # Print summary
    print("\n" + "=" * 50)
    print("📊 GENERATION SUMMARY")
    print("=" * 50)

    total_generated = 0
    for result in results:
        generated = len(result["results"])
        total_generated += generated
        print(f"🎨 {result['name']}: {generated} gradients")

    print(f"\n🎉 Total generated: {total_generated} gradient images")
    print("📂 All gradients saved to the 'generated' folder")

    # Save summary to file
    summary = {
        "total_generated": total_generated,
        "palettes": results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("gradient_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("📄 Summary saved to gradient_summary.json")

if __name__ == "__main__":
    main()
