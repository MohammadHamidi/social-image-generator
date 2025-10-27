"""
Text Utilities - Language detection and text processing

This module provides utilities for:
- Detecting text language (Arabic/Farsi vs Latin)
- Safe Arabic text reshaping
- Numeral detection
- Smart font selection based on content
"""

import re
from typing import Dict, Tuple, Optional


def detect_text_language(text: str) -> Dict[str, any]:
    """
    Detect language characteristics of text.

    Analyzes text to determine script types, presence of numbers,
    and primary language for proper font selection.

    Args:
        text: Input text to analyze

    Returns:
        dict with keys:
            - has_arabic: bool - Contains Arabic/Farsi characters
            - has_latin: bool - Contains Latin characters (A-Z, a-z)
            - has_numbers: bool - Contains Western numerals (0-9)
            - has_persian_numbers: bool - Contains Persian numerals (۰-۹)
            - primary_script: str - 'arabic', 'latin', or 'mixed'
            - should_use_arabic_font: bool - Recommendation for font selection

    Example:
        >>> detect_text_language("Hello World 123")
        {'has_arabic': False, 'has_latin': True, 'has_numbers': True,
         'primary_script': 'latin', 'should_use_arabic_font': False}

        >>> detect_text_language("سلام دنیا ۱۲۳")
        {'has_arabic': True, 'has_latin': False, 'has_numbers': False,
         'primary_script': 'arabic', 'should_use_arabic_font': True}
    """
    if not text:
        return {
            'has_arabic': False,
            'has_latin': False,
            'has_numbers': False,
            'has_persian_numbers': False,
            'primary_script': 'unknown',
            'should_use_arabic_font': False
        }

    # Detect character types
    has_arabic = bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
    has_latin = bool(re.search(r'[A-Za-z]', text))
    has_numbers = bool(re.search(r'[0-9]', text))
    has_persian_numbers = bool(re.search(r'[۰-۹]', text))

    # Determine primary script
    if has_arabic and not has_latin:
        primary_script = 'arabic'
        should_use_arabic_font = True
    elif has_latin and not has_arabic:
        primary_script = 'latin'
        should_use_arabic_font = False
    elif has_arabic and has_latin:
        # Mixed content - decide based on which is dominant
        arabic_count = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))
        latin_count = len(re.findall(r'[A-Za-z]', text))
        primary_script = 'mixed'
        should_use_arabic_font = arabic_count > latin_count
    else:
        # No letters, just numbers/symbols
        primary_script = 'neutral'
        should_use_arabic_font = has_persian_numbers

    return {
        'has_arabic': has_arabic,
        'has_latin': has_latin,
        'has_numbers': has_numbers,
        'has_persian_numbers': has_persian_numbers,
        'primary_script': primary_script,
        'should_use_arabic_font': should_use_arabic_font
    }


def is_arabic_text(text: str) -> bool:
    """
    Simple check if text contains Arabic/Farsi characters.

    Args:
        text: Input text

    Returns:
        bool: True if text contains Arabic/Farsi characters
    """
    if not text:
        return False
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))


def prepare_arabic_text_safe(text: str) -> str:
    """
    Safely prepare Arabic/Farsi text for rendering with validation.

    This function:
    1. Detects if text is Arabic/Farsi
    2. Applies BiDi algorithm and reshaping
    3. Validates output to detect corruption
    4. Returns original text if processing fails

    Args:
        text: Input text (may be Arabic/Farsi or Latin)

    Returns:
        str: Properly shaped text ready for rendering
    """
    if not text or not is_arabic_text(text):
        return text

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display

        # Reshape Arabic characters
        reshaped = arabic_reshaper.reshape(text)

        # Apply BiDi algorithm
        bidi_text = get_display(reshaped)

        # Validation: reshaped text should not be suspiciously longer
        # (some corruption causes massive expansion)
        if len(bidi_text) > len(text) * 2:
            print(f"⚠️  Warning: Text reshaping produced suspicious output")
            print(f"   Original length: {len(text)}")
            print(f"   Reshaped length: {len(bidi_text)}")
            print(f"   Returning original text")
            return text

        return bidi_text

    except ImportError:
        print("⚠️  Arabic reshaping libraries not available")
        print("   Install: pip install arabic-reshaper python-bidi")
        return text
    except Exception as e:
        print(f"❌ Error reshaping Arabic text: {e}")
        return text


def should_use_latin_font(text: str) -> bool:
    """
    Determine if text should use Latin fonts (NotoSans).

    Rules:
    - Pure English text → Latin font
    - English with Western numerals → Latin font
    - Pure Arabic/Farsi → Arabic font
    - Mixed content → depends on dominant script

    Args:
        text: Input text

    Returns:
        bool: True if Latin font should be used
    """
    lang_info = detect_text_language(text)

    # English text with numbers should use Latin fonts
    # (to avoid IRANYekan converting 0-9 to ۰-۹)
    if lang_info['has_latin'] and lang_info['has_numbers'] and not lang_info['has_arabic']:
        return True

    # Pure Latin text
    if lang_info['primary_script'] == 'latin':
        return True

    # Arabic/Farsi text
    if lang_info['should_use_arabic_font']:
        return False

    # Default to Latin for neutral/unknown
    return True


def convert_persian_to_western_numerals(text: str) -> str:
    """
    Convert Persian numerals (۰-۹) to Western numerals (0-9).

    Args:
        text: Input text

    Returns:
        str: Text with Western numerals
    """
    persian_to_western = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }

    result = text
    for persian, western in persian_to_western.items():
        result = result.replace(persian, western)

    return result


def convert_western_to_persian_numerals(text: str) -> str:
    """
    Convert Western numerals (0-9) to Persian numerals (۰-۹).

    Args:
        text: Input text

    Returns:
        str: Text with Persian numerals
    """
    western_to_persian = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }

    result = text
    for western, persian in western_to_persian.items():
        result = result.replace(western, persian)

    return result


def get_text_direction(text: str) -> str:
    """
    Determine text direction (RTL or LTR).

    Args:
        text: Input text

    Returns:
        str: 'rtl' for right-to-left, 'ltr' for left-to-right
    """
    return 'rtl' if is_arabic_text(text) else 'ltr'


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text for safe rendering.

    Args:
        text: Input text
        max_length: Optional maximum length (will truncate with ellipsis)

    Returns:
        str: Sanitized text
    """
    if not text:
        return ""

    # Remove control characters
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

    # Normalize whitespace
    text = ' '.join(text.split())

    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length - 3] + '...'

    return text


def wrap_text(text: str, max_width: int, font, draw) -> list:
    """
    Wrap text to fit within a maximum width.

    Args:
        text: Text to wrap
        max_width: Maximum width in pixels
        font: PIL ImageFont object
        draw: PIL ImageDraw object

    Returns:
        list: List of wrapped text lines
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines
