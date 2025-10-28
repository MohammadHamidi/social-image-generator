"""
Font Manager - Automatically download and manage fonts for any language
"""
import os
import requests
from pathlib import Path
from PIL import ImageFont
import sys

class FontManager:
    """
    Manages font downloads and caching for multilingual support.
    
    Features:
    - Automatic font detection based on language/script
    - Download fonts from CDN if not available locally
    - Cache fonts to avoid repeated downloads
    - Fallback to system fonts or bundled fonts
    """
    
    def __init__(self, assets_dir=None):
        """Initialize FontManager with directory structure"""
        if assets_dir is None:
            # Get the assets directory (works from both local and Docker)
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            # Handle both local and Docker paths
            if os.path.exists('/app'):
                assets_dir = '/app/assets'
            else:
                assets_dir = os.path.join(script_dir, 'assets')
        
        self.assets_dir = assets_dir
        self.fonts_dir = os.path.join(assets_dir, 'fonts')
        self.downloads_dir = os.path.join(assets_dir, 'fonts', 'downloaded')
        
        # Try to ensure directories exist (may fail in Docker, that's OK)
        try:
            Path(self.fonts_dir).mkdir(parents=True, exist_ok=True)
            Path(self.downloads_dir).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # In Docker with volumes, directories might already exist with different ownership
            # This is OK, we can still use them
            print(f"⚠️  Could not create directories, but will try to use existing ones")
        
        # Font CDN sources
        self.font_sources = {
            'noto_sans': 'https://github.com/google/fonts/raw/main/ofl/notosans/NotoSans-Regular.ttf',
            'noto_sans_bold': 'https://github.com/google/fonts/raw/main/ofl/notosans/NotoSans-Bold.ttf',
            'noto_sans_arabic': 'https://github.com/google/fonts/raw/main/ofl/notosansarabic/NotoSansArabic-Regular.ttf',
            'noto_sans_arabic_bold': 'https://github.com/google/fonts/raw/main/ofl/notosansarabic/NotoSansArabic-Bold.ttf',
            'noto_sans_farsi': 'https://github.com/google/fonts/raw/main/ofl/notosansarabic/NotoSansArabic-Regular.ttf',  # Use Arabic for Farsi
            'noto_naskh': 'https://github.com/google/fonts/raw/main/ofl/notonaskharabic/NotoNaskhArabic-Regular.ttf',
            'amiri': 'https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf',
            'barlow': 'https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Regular.ttf',
            'barlow_bold': 'https://github.com/google/fonts/raw/main/ofl/barlow/Barlow-Bold.ttf',
            'inter': 'https://github.com/google/fonts/raw/main/ofl/inter/Inter-Regular.ttf',
            'inter_bold': 'https://github.com/google/fonts/raw/main/ofl/inter/Inter-Bold.ttf',
        }
        
        # Language to font mapping
        self.language_fonts = {
            'latin': ['noto_sans', 'barlow', 'inter'],
            'arabic': ['noto_sans_arabic', 'noto_naskh', 'amiri'],
            'farsi': ['noto_sans_farsi', 'noto_sans_arabic', 'amiri'],
            'urdu': ['noto_sans_arabic', 'noto_naskh'],
            'default': ['noto_sans', 'barlow']
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect language/script from text.
        
        Args:
            text: Input text string
            
        Returns:
            Language code (e.g., 'farsi', 'arabic', 'latin')
        """
        if not text:
            return 'latin'
        
        # Character range detection
        for char in text[:100]:  # Check first 100 characters
            code = ord(char)
            
            # Arabic/Farsi range (U+0600 to U+06FF, U+0750 to U+077F, etc.)
            if 0x0600 <= code <= 0x06FF or 0x0750 <= code <= 0x077F or \
               0x08A0 <= code <= 0x08FF or 0xFB50 <= code <= 0xFDFF:
                return 'farsi'  # Treat all Arabic script as Farsi initially
            
            # Chinese/Japanese/Korean
            if 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF:
                return 'cjk'
            
            # Hebrew
            if 0x0590 <= code <= 0x05FF:
                return 'hebrew'
            
            # Thai
            if 0x0E00 <= code <= 0x0E7F:
                return 'thai'
        
        return 'latin'
    
    def get_font_path(self, font_name: str, weight: str = 'regular') -> str:
        """
        Get font path, download if not available.
        
        Args:
            font_name: Font name (e.g., 'noto_sans')
            weight: Font weight ('regular' or 'bold')
            
        Returns:
            Path to font file
        """
        # Check bundled fonts first
        bundled_path = os.path.join(self.fonts_dir, f'{font_name}.ttf')
        if os.path.exists(bundled_path):
            return bundled_path
        
        # Check downloaded fonts
        downloaded_path = os.path.join(self.downloads_dir, f'{font_name}.ttf')
        if os.path.exists(downloaded_path):
            return downloaded_path
        
        # Download if available in sources
        if font_name in self.font_sources:
            downloaded = self.download_font(font_name)
            if downloaded:
                return downloaded_path
        
        # Fallback: try system fonts
        fallback_path = self._try_system_fonts(font_name)
        if fallback_path:
            return fallback_path
        
        return None
    
    def download_font(self, font_name: str) -> bool:
        """
        Download font from CDN.
        
        Args:
            font_name: Font identifier from self.font_sources
            
        Returns:
            True if download successful
        """
        if font_name not in self.font_sources:
            return False
        
        url = self.font_sources[font_name]
        output_path = os.path.join(self.downloads_dir, f'{font_name}.ttf')
        
        try:
            print(f"📥 Downloading font: {font_name}")
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Downloaded: {font_name}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to download {font_name}: {e}")
            return False
    
    def _try_system_fonts(self, font_name: str) -> str:
        """Try to find font in system font directories"""
        system_paths = [
            '/System/Library/Fonts',  # macOS
            '/Library/Fonts',  # macOS
            '/usr/share/fonts',  # Linux
            '/usr/share/fonts/truetype',
            '/usr/share/fonts/opentype',
            'C:/Windows/Fonts',  # Windows
        ]
        
        # Common font mappings
        font_mappings = {
            'noto_sans': ['NotoSans.ttf', 'noto.ttf'],
            'noto_sans_arabic': ['NotoSansArabic.ttf', 'Amiri-Regular.ttf'],
            'farsi': ['NotoSansArabic.ttf', 'Amiri-Regular.ttf'],
        }
        
        for path in system_paths:
            if not os.path.exists(path):
                continue
            
            if font_name in font_mappings:
                for font_file in font_mappings[font_name]:
                    full_path = os.path.join(path, font_file)
                    if os.path.exists(full_path):
                        return full_path
        
        return None
    
    def get_font(self, text: str, size: int, weight: str = 'regular') -> ImageFont.ImageFont:
        """
        Get appropriate font for text with automatic language detection.
        
        Args:
            text: Text to render
            size: Font size in pixels
            weight: Font weight ('regular' or 'bold')
            
        Returns:
            PIL ImageFont object
        """
        # Detect language
        lang = self.detect_language(text)
        
        # Get font candidates for this language
        if lang in self.language_fonts:
            font_candidates = self.language_fonts[lang]
        else:
            font_candidates = self.language_fonts['default']
        
        # Try each font candidate
        for font_name in font_candidates:
            # Append weight suffix for bold
            if weight == 'bold' and font_name.endswith('_bold'):
                search_name = font_name
            elif weight == 'bold':
                search_name = f'{font_name}_bold'
            else:
                search_name = font_name
            
            font_path = self.get_font_path(search_name)
            
            if font_path and os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        # Fallback to default
        print(f"⚠️ Using default font for language: {lang}")
        return ImageFont.load_default()
    
    def ensure_fonts_for_language(self, language: str) -> bool:
        """
        Ensure all fonts for a language are downloaded.
        
        Args:
            language: Language code (e.g., 'farsi', 'arabic')
            
        Returns:
            True if fonts are available
        """
        if language in self.language_fonts:
            font_candidates = self.language_fonts[language]
        else:
            font_candidates = self.language_fonts['default']
        
        available = 0
        for font_name in font_candidates:
            font_path = self.get_font_path(font_name)
            if font_path and os.path.exists(font_path):
                available += 1
        
        return available > 0


# Global font manager instance
_font_manager = None

def get_font_manager() -> FontManager:
    """Get or create global FontManager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager

