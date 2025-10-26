"""
Base Layout Engine - Foundation for all Instagram layout types

This module provides the base class and infrastructure for implementing
all 20+ layout types in the Social Image Generator system.

Design Principles:
- Layout as Code: Each layout type is a subclass of LayoutEngine
- Declarative Configuration: Layouts declare their requirements via schema
- Smart Defaults: Minimal required parameters from users
- Fail Gracefully: Validation with helpful error messages
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image, ImageDraw, ImageFont
import os


class LayoutEngine(ABC):
    """
    Base class for all Instagram layout types.

    Each layout implementation must:
    1. Define its schema (required/optional fields)
    2. Implement the render() method
    3. Handle asset placement logic
    4. Support both single and multi-slide output
    """

    # Layout metadata (override in subclasses)
    LAYOUT_TYPE: str = "base"
    LAYOUT_CATEGORY: str = "unknown"
    DESCRIPTION: str = "Base layout engine"
    SUPPORTS_CAROUSEL: bool = False

    # Asset requirements (override in subclasses)
    REQUIRED_ASSETS: List[str] = []
    OPTIONAL_ASSETS: List[str] = []

    # Default dimensions (Instagram Post)
    DEFAULT_WIDTH: int = 1080
    DEFAULT_HEIGHT: int = 1350

    def __init__(self,
                 content: Dict[str, Any],
                 assets: Optional[Dict[str, Any]] = None,
                 background: Optional[Dict[str, Any]] = None,
                 options: Optional[Dict[str, Any]] = None):
        """
        Initialize layout engine with content and assets.

        Args:
            content: Layout-specific content (text, data, etc.)
            assets: Asset URLs/paths (hero_image, logo, etc.)
            background: Background configuration (gradient/image/solid)
            options: Layout-specific options (alignment, colors, etc.)
        """
        self.content = content or {}
        self.assets = assets or {}
        self.background = background or {}
        self.options = options or {}

        # Canvas settings
        self.canvas_width = self.options.get('width', self.DEFAULT_WIDTH)
        self.canvas_height = self.options.get('height', self.DEFAULT_HEIGHT)

        # Validate inputs
        self._validate()

    def _validate(self):
        """
        Validate content and assets against layout requirements.

        Raises:
            ValueError: If required fields are missing
        """
        # Subclasses can override this to add custom validation
        pass

    @abstractmethod
    def render(self) -> List[Image.Image]:
        """
        Render the layout and return list of generated images.

        Returns:
            List of PIL Image objects (single item for non-carousel layouts)

        Raises:
            ValueError: If rendering fails due to invalid content/assets
        """
        pass

    def _get_safe_margins(self) -> Dict[str, int]:
        """
        Get safe area margins for Instagram platform.

        Returns:
            Dictionary with margin values (top, bottom, left, right, sides)
        """
        return {
            'top': 80,
            'bottom': 100,
            'left': 60,
            'right': 60,
            'sides': 60  # Horizontal margin
        }

    def _get_max_text_width(self) -> int:
        """
        Get maximum width for text content.

        Returns:
            Maximum text width in pixels
        """
        margins = self._get_safe_margins()
        return self.canvas_width - (margins['left'] + margins['right'])

    def _create_canvas(self, background_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """
        Create a new blank canvas.

        Args:
            background_color: RGB tuple for background

        Returns:
            New PIL Image object
        """
        return Image.new('RGB', (self.canvas_width, self.canvas_height), background_color)

    def _is_rtl_text(self, text: str) -> bool:
        """
        Detect if text contains RTL characters (Arabic/Farsi).

        Args:
            text: Text to analyze

        Returns:
            True if text contains RTL characters
        """
        import re
        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        return bool(re.search(arabic_pattern, text))

    def _prepare_arabic_text(self, text: str) -> str:
        """
        Prepare Arabic/Farsi text for proper display.

        Args:
            text: Original text

        Returns:
            Reshaped text ready for rendering
        """
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display

            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        except Exception:
            return text

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """
        Wrap text to fit within specified width.

        Args:
            text: Text to wrap
            font: Font to use for measurement
            max_width: Maximum line width in pixels

        Returns:
            List of text lines
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def get_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for this layout type.

        Returns:
            JSON schema dictionary defining required/optional fields
        """
        return {
            "layout_type": self.LAYOUT_TYPE,
            "category": self.LAYOUT_CATEGORY,
            "description": self.DESCRIPTION,
            "supports_carousel": self.SUPPORTS_CAROUSEL,
            "required_content": [],
            "optional_content": [],
            "required_assets": self.REQUIRED_ASSETS,
            "optional_assets": self.OPTIONAL_ASSETS
        }


class TextLayoutEngine(LayoutEngine):
    """
    Base class for text-focused layouts (quote, announcement, etc.).

    Inherits all text rendering utilities from LayoutEngine base class.
    """

    LAYOUT_CATEGORY = "text_focused"


class PhotoLayoutEngine(LayoutEngine):
    """
    Base class for photo-heavy layouts (product_showcase, split_image_text, etc.).

    Provides common image manipulation utilities.
    """

    LAYOUT_CATEGORY = "photo_text_mixed"

    def _fit_image(self, image: Image.Image,
                   target_width: int,
                   target_height: int,
                   mode: str = 'cover') -> Image.Image:
        """
        Fit image to target dimensions.

        Args:
            image: Source image
            target_width: Target width
            target_height: Target height
            mode: 'cover' (fill and crop) or 'contain' (fit inside)

        Returns:
            Fitted image
        """
        img_width, img_height = image.size
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height

        if mode == 'cover':
            # Fill the space and crop if needed
            if img_ratio > target_ratio:
                # Image is wider, fit to height
                new_height = target_height
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller, fit to width
                new_width = target_width
                new_height = int(new_width / img_ratio)

            # Resize
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Crop to exact size (center crop)
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            return resized.crop((left, top, right, bottom))

        else:  # contain
            # Fit inside the space
            if img_ratio > target_ratio:
                # Image is wider, fit to width
                new_width = target_width
                new_height = int(new_width / img_ratio)
            else:
                # Image is taller, fit to height
                new_height = target_height
                new_width = int(new_height * img_ratio)

            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _apply_rounded_corners(self, image: Image.Image, radius: int) -> Image.Image:
        """
        Apply rounded corners to image.

        Args:
            image: Source image
            radius: Corner radius in pixels

        Returns:
            Image with rounded corners
        """
        # Create a mask
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

        # Apply mask
        output = Image.new('RGBA', image.size, (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)

        return output


class CarouselLayoutEngine(LayoutEngine):
    """
    Base class for carousel layouts (carousel_text, carousel_photos, etc.).

    Provides slide generation and numbering utilities.
    """

    LAYOUT_CATEGORY = "carousel_multi_slide"
    SUPPORTS_CAROUSEL = True

    def _add_slide_number(self, image: Image.Image,
                         slide_num: int,
                         total_slides: int,
                         position: str = 'top-right') -> Image.Image:
        """
        Add slide number indicator to image.

        Args:
            image: Source image
            slide_num: Current slide number (1-based)
            total_slides: Total number of slides
            position: Where to place indicator ('top-right', 'bottom-center', etc.)

        Returns:
            Image with slide number overlay
        """
        # Create a copy to avoid modifying original
        img = image.copy()
        draw = ImageDraw.Draw(img)

        # Create slide number text
        text = f"{slide_num}/{total_slides}"

        # TODO: Implement slide number rendering
        # This is a placeholder - proper implementation needed

        return img


# Layout Registry - Maps layout_type to class
LAYOUT_REGISTRY: Dict[str, type] = {}


def register_layout(layout_class: type):
    """
    Decorator to register a layout class.

    Usage:
        @register_layout
        class QuoteLayout(TextLayoutEngine):
            LAYOUT_TYPE = "quote"
            ...
    """
    LAYOUT_REGISTRY[layout_class.LAYOUT_TYPE] = layout_class
    return layout_class


def get_layout_engine(layout_type: str) -> type:
    """
    Get layout engine class by type.

    Args:
        layout_type: Layout type identifier

    Returns:
        Layout engine class

    Raises:
        ValueError: If layout type is not registered
    """
    if layout_type not in LAYOUT_REGISTRY:
        raise ValueError(f"Unknown layout type: {layout_type}")

    return LAYOUT_REGISTRY[layout_type]


def list_available_layouts() -> Dict[str, Dict[str, Any]]:
    """
    Get list of all available layout types.

    Returns:
        Dictionary mapping layout_type to schema info
    """
    layouts = {}
    for layout_type, layout_class in LAYOUT_REGISTRY.items():
        try:
            # Try to get schema directly from class if possible
            if hasattr(layout_class, 'get_schema') and callable(getattr(layout_class, 'get_schema')):
                # Create instance with minimal data just to get schema
                # Some layouts may have validation, so we catch errors
                try:
                    instance = layout_class({}, {}, {}, {})
                    layouts[layout_type] = instance.get_schema()
                except:
                    # If instance creation fails, create a basic schema
                    layouts[layout_type] = {
                        'layout_type': layout_type,
                        'description': getattr(layout_class, 'DESCRIPTION', 'No description'),
                        'category': getattr(layout_class, 'LAYOUT_CATEGORY', 'unknown'),
                        'supports_carousel': getattr(layout_class, 'SUPPORTS_CAROUSEL', False)
                    }
            else:
                layouts[layout_type] = {
                    'layout_type': layout_type,
                    'description': getattr(layout_class, 'DESCRIPTION', 'No description')
                }
        except Exception as e:
            # Fallback for layouts that can't be instantiated
            layouts[layout_type] = {
                'layout_type': layout_type,
                'description': getattr(layout_class, 'DESCRIPTION', 'No description'),
                'error': str(e)
            }

    return layouts
