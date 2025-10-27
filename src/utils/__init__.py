"""
Utility modules for Social Image Generator

This package contains helper functions for:
- Color manipulation and contrast checking
- Text processing and language detection
- Font selection
"""

from .color_utils import (
    calculate_contrast_ratio,
    ensure_readable_contrast,
    get_luminance,
    get_contrasting_color,
    meets_contrast_requirement,
    adjust_color_brightness,
    blend_colors
)

from .text_utils import (
    detect_text_language,
    is_arabic_text,
    prepare_arabic_text_safe,
    should_use_latin_font,
    convert_persian_to_western_numerals,
    convert_western_to_persian_numerals,
    get_text_direction,
    sanitize_text,
    wrap_text
)

__all__ = [
    # Color utilities
    'calculate_contrast_ratio',
    'ensure_readable_contrast',
    'get_luminance',
    'get_contrasting_color',
    'meets_contrast_requirement',
    'adjust_color_brightness',
    'blend_colors',
    # Text utilities
    'detect_text_language',
    'is_arabic_text',
    'prepare_arabic_text_safe',
    'should_use_latin_font',
    'convert_persian_to_western_numerals',
    'convert_western_to_persian_numerals',
    'get_text_direction',
    'sanitize_text',
    'wrap_text'
]
