"""
Caption Box Layout - Image with prominent caption box

This layout displays:
- Hero image (top or side portion)
- Caption box with text content (bottom or side)
- Clean separation between image and caption

Perfect for: Instagram posts, blog feature images, portfolio pieces
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class CaptionBoxLayout(PhotoLayoutEngine):
    """
    Caption Box Layout - Image with prominent caption box

    Content Fields:
        - caption (required): Main caption text
        - title (optional): Optional title above caption
        - brand (optional): Brand name in caption box

    Assets:
        - hero_image_url (required): Main image

    Options:
        - layout_style: 'bottom_box' (default) or 'side_box'
        - image_ratio: 0.0-1.0 (default: 0.6 for 60% image, 40% caption)
        - caption_bg_color: Background color for caption box
        - box_padding: Padding inside caption box (default: 40)

    Example:
        {
            "layout_type": "caption_box",
            "content": {
                "title": "New Collection",
                "caption": "Discover our latest summer collection featuring bold colors and modern designs",
                "brand": "Fashion Studio"
            },
            "assets": {
                "hero_image_url": "https://picsum.photos/1080/800"
            },
            "options": {
                "layout_style": "bottom_box",
                "image_ratio": 0.65,
                "caption_bg_color": [245, 245, 250]
            }
        }
    """

    LAYOUT_TYPE = "caption_box"
    LAYOUT_CATEGORY = "photo_text_mixed"
    DESCRIPTION = "Image with prominent caption box"
    SUPPORTS_CAROUSEL = False

    REQUIRED_ASSETS = ["hero_image_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'caption' not in self.content:
            raise ValueError("caption is required for caption_box layout")

        if not self.content['caption'].strip():
            raise ValueError("caption cannot be empty")

        # Validate hero image is provided
        if 'hero_image_url' not in self.assets or not self.assets['hero_image_url']:
            raise ValueError("hero_image_url is required for caption_box layout")

    def render(self) -> List[Image.Image]:
        """
        Render the caption box layout.

        Returns:
            List containing single Image object
        """
        # Get layout configuration
        layout_style = self.options.get('layout_style', 'bottom_box')
        image_ratio = self.options.get('image_ratio', 0.6)

        # Clamp ratio
        image_ratio = max(0.3, min(0.8, image_ratio))

        # Create canvas
        canvas = self._create_canvas((255, 255, 255))

        # Add image and caption based on layout style
        if layout_style == 'side_box':
            canvas = self._render_side_layout(canvas, image_ratio)
        else:  # bottom_box (default)
            canvas = self._render_bottom_layout(canvas, image_ratio)

        return [canvas]

    def _render_bottom_layout(self, canvas: Image.Image, image_ratio: float) -> Image.Image:
        """Render layout with image on top, caption box on bottom."""
        # Calculate dimensions
        image_height = int(self.canvas_height * image_ratio)
        caption_height = self.canvas_height - image_height

        # Load and fit image
        hero_image = self._load_hero_image()
        hero_image = self._fit_image(hero_image, self.canvas_width, image_height, mode='cover')

        # Paste image
        canvas.paste(hero_image, (0, 0))

        # Draw caption box
        canvas = self._draw_caption_box(
            canvas,
            x=0,
            y=image_height,
            width=self.canvas_width,
            height=caption_height
        )

        return canvas

    def _render_side_layout(self, canvas: Image.Image, image_ratio: float) -> Image.Image:
        """Render layout with image on left, caption box on right."""
        # Calculate dimensions
        image_width = int(self.canvas_width * image_ratio)
        caption_width = self.canvas_width - image_width

        # Load and fit image
        hero_image = self._load_hero_image()
        hero_image = self._fit_image(hero_image, image_width, self.canvas_height, mode='cover')

        # Paste image
        canvas.paste(hero_image, (0, 0))

        # Draw caption box
        canvas = self._draw_caption_box(
            canvas,
            x=image_width,
            y=0,
            width=caption_width,
            height=self.canvas_height
        )

        return canvas

    def _load_hero_image(self) -> Image.Image:
        """Load hero image from assets."""
        try:
            from src.asset_manager import AssetManager

            asset_manager = AssetManager()
            hero_image = asset_manager.load_asset(
                self.assets['hero_image_url'],
                role='hero',
                use_cache=True
            )

            return hero_image

        except Exception as e:
            # Fallback to gray placeholder
            fallback = Image.new('RGB', (800, 800), (180, 180, 180))
            return fallback

    def _draw_caption_box(self, canvas: Image.Image, x: int, y: int,
                          width: int, height: int) -> Image.Image:
        """Draw caption box with text content."""
        draw = ImageDraw.Draw(canvas)

        # Get caption box background color
        caption_bg_color = tuple(self.options.get('caption_bg_color', [245, 245, 250]))

        # Draw background
        draw.rectangle(
            [(x, y), (x + width, y + height)],
            fill=caption_bg_color
        )

        # Get content
        title = self.content.get('title', '')
        caption = self.content['caption']
        brand = self.content.get('brand', '')

        # Get options
        box_padding = self.options.get('box_padding', 40)

        # Detect RTL
        is_rtl = self._is_rtl_text(caption)

        # Get fonts
        title_font = self._get_title_font(is_rtl)
        caption_font = self._get_caption_font(is_rtl)
        brand_font = self._get_brand_font(is_rtl)

        # Get colors
        title_color = tuple(self.options.get('title_color', [33, 37, 41]))
        caption_color = tuple(self.options.get('caption_color', [73, 80, 87]))
        brand_color = tuple(self.options.get('brand_color', [108, 117, 125]))

        # Calculate available text area
        text_x = x + box_padding
        text_width = width - (box_padding * 2)
        current_y = y + box_padding

        # Draw title if present
        if title:
            if is_rtl and self._is_rtl_text(title):
                display_title = self._prepare_arabic_text(title)
            else:
                display_title = title

            title_lines = self._wrap_text(display_title, title_font, text_width)

            for line in title_lines:
                bbox = title_font.getbbox(line)
                line_height = bbox[3] - bbox[1]

                draw.text((text_x, current_y), line, font=title_font, fill=title_color)
                current_y += line_height + 10

            current_y += 20

        # Draw caption
        if is_rtl:
            display_caption = self._prepare_arabic_text(caption)
        else:
            display_caption = caption

        caption_lines = self._wrap_text(display_caption, caption_font, text_width)

        for line in caption_lines:
            bbox = caption_font.getbbox(line)
            line_height = bbox[3] - bbox[1]

            draw.text((text_x, current_y), line, font=caption_font, fill=caption_color)
            current_y += line_height + 12

        # Draw brand at bottom if present
        if brand:
            if is_rtl and self._is_rtl_text(brand):
                display_brand = self._prepare_arabic_text(brand)
            else:
                display_brand = brand

            brand_y = y + height - box_padding - 30

            draw.text((text_x, brand_y), display_brand, font=brand_font, fill=brand_color)

        return canvas

    def _get_title_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for title."""
        font_size = self.options.get('title_size', 40)
        if is_rtl:
            font_size = int(font_size * 1.1)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanBoldFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _get_caption_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for caption."""
        font_size = self.options.get('caption_size', 28)
        if is_rtl:
            font_size = int(font_size * 1.1)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanRegularFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _get_brand_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for brand."""
        font_size = self.options.get('brand_size', 22)
        if is_rtl:
            font_size = int(font_size * 1.1)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanRegularFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["caption"],
            "optional_content": ["title", "brand"],
            "options": {
                "layout_style": "'bottom_box' (default) or 'side_box'",
                "image_ratio": "0.0-1.0, portion for image (default: 0.6)",
                "box_padding": "Padding inside caption box (default: 40)",
                "caption_bg_color": "RGB background for caption box (default: [245,245,250])",
                "title_size": "Font size for title (default: 40)",
                "caption_size": "Font size for caption (default: 28)",
                "brand_size": "Font size for brand (default: 22)",
                "title_color": "RGB color for title (default: [33,37,41])",
                "caption_color": "RGB color for caption (default: [73,80,87])",
                "brand_color": "RGB color for brand (default: [108,117,125])"
            }
        })
        return base_schema
