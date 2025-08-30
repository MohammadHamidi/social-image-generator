#!/usr/bin/env python3
"""
Download required fonts for Docker deployment
"""

import os
import requests
import sys
from pathlib import Path

def download_file(url: str, destination: str, description: str):
    """Download a file with progress indication"""
    try:
        print(f"📥 Downloading {description}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r   Progress: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ Downloaded: {os.path.basename(destination)}")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download {description}: {e}")
        return False

def download_google_font(family: str, filename: str, description: str):
    """Download a font from Google Fonts"""
    # Google Fonts API endpoint
    base_url = "https://fonts.googleapis.com/css2"
    params = {
        'family': family,
        'display': 'swap'
    }
    
    try:
        # Get the CSS with font URLs
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Extract the font URL (this is a simplified approach)
        css_content = response.text
        
        # For simplicity, we'll use direct GitHub links to Noto fonts
        github_base = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf"
        
        font_urls = {
            'NotoSans-Regular.ttf': f"{github_base}/NotoSans/NotoSans-Regular.ttf",
            'NotoSans-Bold.ttf': f"{github_base}/NotoSans/NotoSans-Bold.ttf",
            'NotoSansArabic-Regular.ttf': f"{github_base}/NotoSansArabic/NotoSansArabic-Regular.ttf",
            'NotoSansArabic-Bold.ttf': f"{github_base}/NotoSansArabic/NotoSansArabic-Bold.ttf"
        }
        
        if filename in font_urls:
            return download_file(font_urls[filename], f"assets/fonts/{filename}", description)
        else:
            print(f"❌ Font {filename} not found in predefined URLs")
            return False
            
    except Exception as e:
        print(f"❌ Failed to download {description}: {e}")
        return False

def download_noto_fonts():
    """Download Noto fonts for the project"""
    print("🔤 DOWNLOADING FONTS FOR DOCKER DEPLOYMENT")
    print("=" * 50)
    
    # Ensure fonts directory exists
    fonts_dir = Path("assets/fonts")
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    # List of fonts to download
    fonts_to_download = [
        ('NotoSans-Regular.ttf', 'Noto Sans Regular (Latin)'),
        ('NotoSans-Bold.ttf', 'Noto Sans Bold (Latin)'),
        ('NotoSansArabic-Regular.ttf', 'Noto Sans Arabic Regular'),
        ('NotoSansArabic-Bold.ttf', 'Noto Sans Arabic Bold')
    ]
    
    successful_downloads = 0
    
    for filename, description in fonts_to_download:
        file_path = fonts_dir / filename
        
        # Skip if file already exists
        if file_path.exists():
            print(f"✅ {filename} already exists, skipping")
            successful_downloads += 1
            continue
        
        # Try to download
        if download_google_font('', filename, description):
            successful_downloads += 1
    
    print(f"\n📊 DOWNLOAD SUMMARY")
    print(f"✅ Successfully downloaded: {successful_downloads}/{len(fonts_to_download)} fonts")
    
    if successful_downloads == len(fonts_to_download):
        print("🎉 All fonts downloaded successfully!")
        print("📦 Ready for Docker deployment")
    else:
        print("⚠️  Some fonts failed to download")
        print("💡 You can manually download fonts from:")
        print("   - https://fonts.google.com/noto/specimen/Noto+Sans")
        print("   - https://fonts.google.com/noto/specimen/Noto+Sans+Arabic")
    
    return successful_downloads == len(fonts_to_download)

def alternative_download_methods():
    """Provide alternative ways to get fonts"""
    print("\n📋 ALTERNATIVE FONT DOWNLOAD METHODS")
    print("=" * 40)
    
    print("🔗 Option 1: Direct Download Links")
    print("   Copy these URLs to your browser:")
    
    direct_links = [
        ("Noto Sans Regular", "https://fonts.gstatic.com/s/notosans/v27/o-0IIpQlx3QUlC5A4PNr5TRASf6M7Q.woff2"),
        ("Noto Sans Bold", "https://fonts.gstatic.com/s/notosans/v27/o-0NIpQlx3QUlC5A4PNjXhFlYdfWm.woff2"),
        ("Noto Sans Arabic Regular", "https://fonts.gstatic.com/s/notosansarabic/v18/nwpxtLGrOAZMl5nJ_wfgRg3DrWFZWsnVBJ_sS6tlqHHFlhQ5l3g.woff2"),
        ("Noto Sans Arabic Bold", "https://fonts.gstatic.com/s/notosansarabic/v18/nwpxtLGrOAZMl5nJ_wfgRg3DrWFZWsnVBJ_sS6tlqHHFlnEql3g.woff2")
    ]
    
    for name, url in direct_links:
        print(f"   {name}: {url}")
    
    print("\n🔗 Option 2: Google Fonts Zip Download")
    print("   Visit: https://fonts.google.com/download?family=Noto%20Sans")
    print("   Visit: https://fonts.google.com/download?family=Noto%20Sans%20Arabic")
    
    print("\n🔗 Option 3: Use System Fonts (Development Only)")
    print("   The system will fall back to system fonts if bundled fonts aren't available")
    
    print("\n📁 Font File Placement")
    print("   Place downloaded .ttf files in: assets/fonts/")
    print("   Expected filenames:")
    print("   - NotoSans-Regular.ttf")
    print("   - NotoSans-Bold.ttf")
    print("   - NotoSansArabic-Regular.ttf")
    print("   - NotoSansArabic-Bold.ttf")

if __name__ == "__main__":
    # Install requests if not available
    try:
        import requests
    except ImportError:
        print("📦 Installing requests library...")
        os.system(f"{sys.executable} -m pip install requests")
        import requests
    
    # Download fonts
    success = download_noto_fonts()
    
    if not success:
        alternative_download_methods()
    
    print("\n🚀 Next Steps:")
    print("1. Verify fonts in assets/fonts/ directory")
    print("2. Test with: python3 test_docker_fonts.py")
    print("3. Build Docker image with fonts included")
