"""
Color Utilities - WCAG-compliant contrast checking and color manipulation

This module provides functions for ensuring readable text colors against
backgrounds according to WCAG 2.1 accessibility guidelines.

WCAG Contrast Requirements:
- Normal text: 4.5:1 minimum
- Large text (18pt+ or 14pt+ bold): 3.0:1 minimum
- UI components: 3.0:1 minimum
"""

from typing import Tuple


def get_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Calculate relative luminance of an RGB color.

    Uses the WCAG 2.1 formula for relative luminance calculation.

    Args:
        rgb: RGB tuple (r, g, b) with values 0-255

    Returns:
        float: Relative luminance (0.0 to 1.0)

    Reference:
        https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    """
    r, g, b = [x / 255.0 for x in rgb]

    def adjust_channel(c):
        """Apply gamma correction to channel."""
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = adjust_channel(r), adjust_channel(g), adjust_channel(b)

    # Calculate luminance using WCAG coefficients
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(color1: Tuple[int, int, int],
                            color2: Tuple[int, int, int]) -> float:
    """
    Calculate WCAG contrast ratio between two colors.

    Args:
        color1: First RGB tuple (r, g, b)
        color2: Second RGB tuple (r, g, b)

    Returns:
        float: Contrast ratio (1.0 to 21.0)
        - 1.0 = no contrast (same color)
        - 21.0 = maximum contrast (black on white)

    Example:
        >>> calculate_contrast_ratio((0, 0, 0), (255, 255, 255))
        21.0
        >>> calculate_contrast_ratio((255, 255, 255), (255, 255, 255))
        1.0
    """
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def meets_contrast_requirement(text_color: Tuple[int, int, int],
                               bg_color: Tuple[int, int, int],
                               level: str = 'AA',
                               large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG contrast requirements.

    Args:
        text_color: Text RGB color
        bg_color: Background RGB color
        level: 'AA' (standard) or 'AAA' (enhanced)
        large_text: True if text is large (18pt+ or 14pt+ bold)

    Returns:
        bool: True if contrast requirement is met

    WCAG Requirements:
        - Level AA, normal text: 4.5:1
        - Level AA, large text: 3.0:1
        - Level AAA, normal text: 7.0:1
        - Level AAA, large text: 4.5:1
    """
    ratio = calculate_contrast_ratio(text_color, bg_color)

    if level == 'AAA':
        min_ratio = 4.5 if large_text else 7.0
    else:  # AA
        min_ratio = 3.0 if large_text else 4.5

    return ratio >= min_ratio


def ensure_readable_contrast(text_color: Tuple[int, int, int],
                            bg_color: Tuple[int, int, int],
                            min_ratio: float = 4.5) -> Tuple[int, int, int]:
    """
    Adjust text color to ensure minimum contrast ratio against background.

    If the current text color doesn't meet the minimum contrast ratio,
    this function returns an adjusted color that does.

    Args:
        text_color: Original text RGB color
        bg_color: Background RGB color
        min_ratio: Minimum contrast ratio (default 4.5 for WCAG AA normal text)

    Returns:
        tuple: Adjusted RGB color with sufficient contrast

    Strategy:
        1. Check if current color already meets requirement
        2. If not, determine if background is light or dark
        3. Return high-contrast color (dark gray on light, white on dark)
        4. Optionally try to preserve hue while adjusting luminance

    Example:
        >>> ensure_readable_contrast((100, 100, 100), (110, 110, 110), 4.5)
        (30, 30, 30)  # Dark gray for better contrast
    """
    current_ratio = calculate_contrast_ratio(text_color, bg_color)

    if current_ratio >= min_ratio:
        return text_color  # Already readable

    # Determine if background is light or dark
    bg_luminance = get_luminance(bg_color)

    if bg_luminance > 0.5:
        # Light background → use dark text
        # Try progressively darker shades
        for darkness in [30, 20, 10, 0]:
            dark_color = (darkness, darkness, darkness)
            if calculate_contrast_ratio(dark_color, bg_color) >= min_ratio:
                return dark_color
        return (0, 0, 0)  # Pure black as fallback
    else:
        # Dark background → use light text
        # Try progressively lighter shades
        for lightness in [255, 245, 235, 225]:
            light_color = (lightness, lightness, lightness)
            if calculate_contrast_ratio(light_color, bg_color) >= min_ratio:
                return light_color
        return (255, 255, 255)  # Pure white as fallback


def get_contrasting_color(bg_color: Tuple[int, int, int],
                         high_contrast: bool = True) -> Tuple[int, int, int]:
    """
    Get a contrasting color for text on a given background.

    Simple helper that returns black or white based on background luminance.

    Args:
        bg_color: Background RGB color
        high_contrast: If True, returns pure black/white. If False, returns softer shades.

    Returns:
        tuple: RGB color that contrasts well with background
    """
    bg_luminance = get_luminance(bg_color)

    if bg_luminance > 0.5:
        # Light background → dark text
        return (0, 0, 0) if high_contrast else (30, 30, 30)
    else:
        # Dark background → light text
        return (255, 255, 255) if high_contrast else (245, 245, 245)


def adjust_color_brightness(color: Tuple[int, int, int],
                           factor: float) -> Tuple[int, int, int]:
    """
    Adjust color brightness by a factor.

    Args:
        color: RGB tuple
        factor: Brightness factor (0.0 to 2.0)
                < 1.0 = darker, > 1.0 = lighter

    Returns:
        tuple: Adjusted RGB color
    """
    r, g, b = color
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
    return (r, g, b)


def blend_colors(color1: Tuple[int, int, int],
                color2: Tuple[int, int, int],
                ratio: float = 0.5) -> Tuple[int, int, int]:
    """
    Blend two colors together.

    Args:
        color1: First RGB tuple
        color2: Second RGB tuple
        ratio: Blend ratio (0.0 = all color1, 1.0 = all color2)

    Returns:
        tuple: Blended RGB color
    """
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)
