#!/usr/bin/env python3
"""
Social Media Gradient Generator
Generates all 10 gradient palettes using the existing API system
"""

import requests
import json
import os
from datetime import datetime
import time

# Social Media Gradient Palettes
GRADIENT_PALETTES = {
    "sunset_glow": {
        "name": "Sunset Glow",
        "description": "Warm, inviting, tropical vibe",
        "colors": ["#FF6B6B", "#FFD93D", "#6BCB77"]
    },
    "ocean_breeze": {
        "name": "Ocean Breeze",
        "description": "Fresh aqua to green, calming & modern",
        "colors": ["#00C9FF", "#92FE9D"]
    },
    "cotton_candy": {
        "name": "Cotton Candy",
        "description": "Playful pastel mix, Instagram-friendly",
        "colors": ["#FF9A9E", "#FAD0C4", "#FBC2EB", "#A6C1EE"]
    },
    "neon_vibes": {
        "name": "Neon Vibes",
        "description": "Trendy neon pink to deep purple, bold look",
        "colors": ["#FF6FD8", "#3813C2"]
    },
    "sunrise_horizon": {
        "name": "Sunrise Horizon",
        "description": "Golden yellow into pink, perfect for motivational posts",
        "colors": ["#FEE140", "#FA709A"]
    },
    "minimal_mint": {
        "name": "Minimal Mint",
        "description": "Soft pastel mint blending into lavender, very clean",
        "colors": ["#D9F3E5", "#E0C3FC"]
    },
    "electric_blue": {
        "name": "Electric Blue",
        "description": "Bright, futuristic gradient, tech/startup feel",
        "colors": ["#1FA2FF", "#12D8FA", "#A6FFCB"]
    },
    "rose_gold": {
        "name": "Rose Gold",
        "description": "Feminine, elegant, luxury vibe",
        "colors": ["#FBD3E9", "#BB377D"]
    },
    "dark_mode_luxe": {
        "name": "Dark Mode Luxe",
        "description": "Moody gradient, professional & modern",
        "colors": ["#434343", "#000000", "#2C5364"]
    },
    "vivid_coral": {
        "name": "Vivid Coral",
        "description": "Energetic coral to pink, very eye-catching",
        "colors": ["#FF512F", "#DD2476"]
    }
}

class SocialGradientGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()

    def generate_gradient(self, palette_name, palette_data, gradient_type="linear",
                         direction="vertical", width=1080, height=1350):
        """
        Generate a gradient using the API endpoint
        """
        url = f"{self.base_url}/generate_gradient"

        payload = {
            "width": width,
            "height": height,
            "colors": palette_data["colors"],
            "gradient_type": gradient_type,
            "direction": direction,
            "use_hsl_interpolation": True,
            "add_noise": True,
            "noise_intensity": 0.02,
            "apply_dither": False,
            "generate_harmony": False,
            "quality": 95
        }

        try:
            print(f"🎨 Generating {palette_name} - {palette_data['name']} ({gradient_type} {direction})")

            response = self.session.post(url, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"✅ Successfully generated {palette_name}")
                    print(f"   Download URL: {result['download_url']}")
                    print(f"   Filename: {result['filename']}")
                    return result
                else:
                    print(f"❌ API returned error: {result.get('error')}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")

        return None

    def generate_all_palettes(self):
        """
        Generate all gradient palettes in multiple orientations
        """
        print("🚀 Starting Social Media Gradient Generation")
        print("=" * 60)

        # Different gradient configurations to generate
        configurations = [
            {"gradient_type": "linear", "direction": "vertical"},
            {"gradient_type": "linear", "direction": "horizontal"},
            {"gradient_type": "radial", "direction": "vertical"},
            {"gradient_type": "diagonal", "direction": "diagonal"}
        ]

        results = []

        for palette_key, palette_data in GRADIENT_PALETTES.items():
            print(f"\n🎨 Processing {palette_data['name']}")
            print(f"   {palette_data['description']}")
            print(f"   Colors: {', '.join(palette_data['colors'])}")

            palette_results = []

            for config in configurations:
                result = self.generate_gradient(
                    palette_key, palette_data,
                    gradient_type=config["gradient_type"],
                    direction=config["direction"]
                )

                if result:
                    result["config"] = config
                    palette_results.append(result)

                # Small delay to avoid overwhelming the server
                time.sleep(0.5)

            results.append({
                "palette": palette_key,
                "data": palette_data,
                "results": palette_results
            })

        return results

    def save_results_summary(self, results, output_file="gradient_generation_results.json"):
        """
        Save generation results to a JSON file
        """
        summary = {
            "generation_timestamp": datetime.now().isoformat(),
            "total_palettes": len(results),
            "palettes": []
        }

        for result in results:
            palette_summary = {
                "name": result["data"]["name"],
                "key": result["palette"],
                "description": result["data"]["description"],
                "colors": result["data"]["colors"],
                "generated_files": len(result["results"]),
                "files": []
            }

            for file_result in result["results"]:
                palette_summary["files"].append({
                    "filename": file_result["filename"],
                    "download_url": file_result["download_url"],
                    "config": file_result["config"],
                    "size": file_result["size"],
                    "dimensions": file_result["dimensions"]
                })

            summary["palettes"].append(palette_summary)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Results saved to {output_file}")
        return summary

def main():
    """Main execution function"""
    generator = SocialGradientGenerator()

    # Test server connection first
    try:
        health_response = requests.get("http://localhost:5000/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Server is not responding. Please make sure the API server is running.")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please make sure the API server is running on http://localhost:5000")
        return

    # Generate all gradients
    results = generator.generate_all_palettes()

    # Save results summary
    summary = generator.save_results_summary(results)

    # Print final summary
    print("\n" + "=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)

    total_files = 0
    for palette in summary["palettes"]:
        print(f"🎨 {palette['name']}")
        print(f"   Generated: {palette['generated_files']} files")
        for file_info in palette["files"]:
            print(f"   📁 {file_info['filename']} ({file_info['config']['gradient_type']} {file_info['config']['direction']})")
        total_files += palette["generated_files"]
        print()

    print(f"🎉 Total generated: {total_files} gradient images")
    print("📂 All gradients saved to the 'generated' folder"
    print("🌐 Download URLs available in gradient_generation_results.json")

if __name__ == "__main__":
    main()
