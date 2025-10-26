"""
Overlay Text Layout - Text overlaid on full-background image

This layout displays:
- Full-screen hero image background
- Text content overlaid on top
- Optional gradient overlay for better text readability
- Optional darkening/lightening effect

Perfect for: Quotes over photos, motivational posts, announcements with imagery
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from typing import List, Tuple, Optional
import os


@register_layout
class OverlayTextLayout(PhotoLayoutEngine):
    """
    Overlay Text Layout - Text overlaid on full-background image

    Content Fields:
        - text (required): Main text to overlay
        - subtitle (optional): Secondary text

    Assets:
        - background_image_url (required): Full-screen background image

    Options:
        - text_position: 'center' (default), 'top', 'bottom', 'left', 'right'
        - overlay_opacity: 0.0-1.0 darkness overlay (default: 0.4)
        - text_alignment: 'center' (default), 'left', 'right'
        - text_box_style: 'none' (default), 'rounded', 'pill'

    Example:
        {
            "layout_type": "overlay_text",
            "content": {
                "text": "Every day is a new beginning",
                "subtitle": "Make it count"
            },
            "assets": {
                "background_image_url": "https://picsum.photos/1080/1350"
            },
            "options": {
                "text_position": "center",
                "overlay_opacity": 0.5
            }
        }
    """

    LAYOUT_TYPE = "overlay_text"
    LAYOUT_CATEGORY = "photo_text_mixed"
    DESCRIPTION = "Text overlaid on full-background image"
    SUPPORTS_CAROUSEL = False

    REQUIRED_ASSETS = ["background_image_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'text' not in self.content:
            raise ValueError("text is required for overlay_text layout")

        if not self.content['text'].strip():
            raise ValueError("text cannot be empty")

        # Validate background image is provided
        if 'background_image_url' not in self.assets or not self.assets['background_image_url']:
            raise ValueError("background_image_url is required for overlay_text layout")

    def render(self) -> List[Image.Image]:
        """
        Render the overlay text layout.

        Returns:
            List containing single Image object
        """
        # Load and prepare background image
        canvas = self._create_background_image()

        # Apply overlay for better text readability
        canvas = self._apply_overlay(canvas)

        # Add text content
        canvas = self._add_overlay_text(canvas)

        return [canvas]

    def _create_background_image(self) -> Image.Image:
        """Load and fit background image to canvas."""
        try:
            from src.asset_manager import AssetManager

            # Load background image
            asset_manager = AssetManager()
            bg_image = asset_manager.load_asset(
                self.assets['background_image_url'],
                role='background',
                use_cache=True
            )

            # Fit to canvas size (cover mode - fill and crop)
            bg_image = self._fit_image(
                bg_image,
                self.canvas_width,
                self.canvas_height,
                mode='cover'
            )

            return bg_image

        except Exception as e:
            # Fallback to solid color if image loading fails
            fallback_color = self.options.get('fallback_color', [100, 100, 100])
            return Image.new('RGB', (self.canvas_width, self.canvas_height), tuple(fallback_color))

    def _apply_overlay(self, img: Image.Image) -> Image.Image:
        """Apply dark/light overlay for better text readability."""
        overlay_opacity = self.options.get('overlay_opacity', 0.4)

        if overlay_opacity <= 0:
            return img

        # Create overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        overlay_color = self.options.get('overlay_color', [0, 0, 0])
        alpha = int(overlay_opacity * 255)

        draw.rectangle(
            [(0, 0), img.size],
            fill=(*overlay_color, alpha)
        )

        # Convert img to RGBA and composite
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, overlay)

        return img_rgba.convert('RGB')

    def _add_overlay_text(self, canvas: Image.Image) -> Image.Image:
        """Add text overlay on the image."""
        draw = ImageDraw.Draw(canvas)

        # Get content
        text = self.content['text']
        subtitle = self.content.get('subtitle', '')

        # Get options
        text_position = self.options.get('text_position', 'center')
        text_alignment = self.options.get('text_alignment', 'center')
        text_box_style = self.options.get('text_box_style', 'none')

        # Detect RTL
        is_rtl = self._is_rtl_text(text)

        # Get fonts
        text_font = self._get_text_font(is_rtl)
        subtitle_font = self._get_subtitle_font(is_rtl)

        # Get colors
        text_color = tuple(self.options.get('text_color', [255, 255, 255]))
        subtitle_color = tuple(self.options.get('subtitle_color', [230, 230, 230]))

        # Calculate text dimensions and position
        margins = self._get_safe_margins()
        max_width = self.canvas_width - (margins['sides'] * 2)

        # Prepare text
        if is_rtl:
            display_text = self._prepare_arabic_text(text)
        else:
            display_text = text

        # Wrap text
        lines = self._wrap_text(display_text, text_font, max_width)

        # Calculate total height
        line_heights = []
        for line in lines:
            bbox = text_font.getbbox(line)
            line_heights.append(bbox[3] - bbox[1])

        total_text_height = sum(line_heights) + (len(lines) - 1) * 15

        # Add subtitle height if present
        subtitle_lines = []
        if subtitle:
            if is_rtl and self._is_rtl_text(subtitle):
                display_subtitle = self._prepare_arabic_text(subtitle)
            else:
                display_subtitle = subtitle

            subtitle_lines = self._wrap_text(display_subtitle, subtitle_font, max_width)
            subtitle_bbox = subtitle_font.getbbox(subtitle_lines[0] if subtitle_lines else subtitle)
            subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]
            total_text_height += subtitle_height * len(subtitle_lines) + 40

        # Calculate starting Y position based on text_position
        if text_position == 'top':
            current_y = margins['top'] + 100
        elif text_position == 'bottom':
            current_y = self.canvas_height - margins['bottom'] - total_text_height - 100
        elif text_position == 'center':
            current_y = (self.canvas_height - total_text_height) // 2
        else:
            current_y = (self.canvas_height - total_text_height) // 2

        # Draw text box background if requested
        if text_box_style != 'none':
            self._draw_text_box_background(canvas, current_y, total_text_height, text_box_style)

        # Draw main text
        for i, line in enumerate(lines):
            bbox = text_font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Calculate X position based on alignment
            if text_alignment == 'center' or text_position in ['center']:
                line_x = margins['sides'] + (max_width - line_width) // 2
            elif text_alignment == 'right':
                line_x = self.canvas_width - margins['right'] - line_width
            else:  # left
                line_x = margins['left']

            draw.text((line_x, current_y), line, font=text_font, fill=text_color)
            current_y += line_height + 15

        # Draw subtitle if present
        if subtitle_lines:
            current_y += 25

            for line in subtitle_lines:
                bbox = subtitle_font.getbbox(line)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]

                # Calculate X position based on alignment
                if text_alignment == 'center' or text_position in ['center']:
                    line_x = margins['sides'] + (max_width - line_width) // 2
                elif text_alignment == 'right':
                    line_x = self.canvas_width - margins['right'] - line_width
                else:  # left
                    line_x = margins['left']

                draw.text((line_x, current_y), line, font=subtitle_font, fill=subtitle_color)
                current_y += line_height + 12

        return canvas

    def _draw_text_box_background(self, img: Image.Image, y: int, height: int, style: str):
        """Draw background box for text."""
        draw = ImageDraw.Draw(img)

        margins = self._get_safe_margins()
        padding = 40

        x1 = margins['left'] - padding
        y1 = y - padding
        x2 = self.canvas_width - margins['right'] + padding
        y2 = y + height + padding

        box_color = tuple(self.options.get('text_box_color', [0, 0, 0]))
        box_opacity = self.options.get('text_box_opacity', 0.6)

        # Create semi-transparent overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        alpha = int(box_opacity * 255)

        if style == 'rounded':
            overlay_draw.rounded_rectangle(
                [(x1, y1), (x2, y2)],
                radius=20,
                fill=(*box_color, alpha)
            )
        elif style == 'pill':
            overlay_draw.rounded_rectangle(
                [(x1, y1), (x2, y2)],
                radius=(y2 - y1) // 2,
                fill=(*box_color, alpha)
            )

        # Composite
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, overlay)
        img.paste(img_rgba.convert('RGB'), (0, 0))

    def _get_text_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for main text."""
        font_size = self.options.get('text_size', 56)
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

    def _get_subtitle_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for subtitle."""
        font_size = self.options.get('subtitle_size', 32)
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
            "required_content": ["text"],
            "optional_content": ["subtitle"],
            "options": {
                "text_position": "'center' (default), 'top', 'bottom'",
                "overlay_opacity": "Darkness overlay 0.0-1.0 (default: 0.4)",
                "text_alignment": "'center' (default), 'left', 'right'",
                "text_box_style": "'none' (default), 'rounded', 'pill'",
                "text_size": "Font size for main text (default: 56)",
                "subtitle_size": "Font size for subtitle (default: 32)",
                "text_color": "RGB color for text (default: [255,255,255])",
                "subtitle_color": "RGB color for subtitle (default: [230,230,230])",
                "overlay_color": "RGB color for overlay (default: [0,0,0])",
                "text_box_color": "RGB color for text box (default: [0,0,0])",
                "text_box_opacity": "Text box opacity 0.0-1.0 (default: 0.6)",
                "fallback_color": "RGB color if image fails to load (default: [100,100,100])"
            }
        })
        return base_schema
