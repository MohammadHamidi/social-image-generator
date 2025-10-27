"""
Split Image Text Layout - Half photo, half text

This layout divides the canvas into two sections:
- One half displays the hero image
- Other half displays text content

Perfect for: Product features, services, educational content with visuals
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class SplitImageTextLayout(PhotoLayoutEngine):
    """
    Split Image Text Layout - Half photo, half text

    Content Fields:
        - title (required): Main heading
        - description (optional): Supporting text
        - bullets (optional): List of bullet points

    Assets:
        - hero_image_url (required): Image to display

    Options:
        - split_direction: 'vertical' (default) or 'horizontal'
        - image_position: 'left' or 'right' (for vertical), 'top' or 'bottom' (for horizontal)
        - image_ratio: 0.0-1.0 (default: 0.5 for 50/50 split)

    Example:
        {
            "layout_type": "split_image_text",
            "content": {
                "title": "Premium Features",
                "description": "Everything you need in one place",
                "bullets": ["Fast Performance", "Easy to Use", "Secure"]
            },
            "assets": {
                "hero_image_url": "https://example.com/product.jpg"
            },
            "options": {
                "split_direction": "vertical",
                "image_position": "left",
                "image_ratio": 0.5
            }
        }
    """

    LAYOUT_TYPE = "split_image_text"
    LAYOUT_CATEGORY = "photo_text_mixed"
    DESCRIPTION = "Half photo, half text layout"
    SUPPORTS_CAROUSEL = False

    REQUIRED_ASSETS = ["hero_image_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'title' not in self.content:
            raise ValueError("title is required for split_image_text layout")

        if not self.content['title'].strip():
            raise ValueError("title cannot be empty")

        # Validate hero image is provided
        if 'hero_image_url' not in self.assets or not self.assets['hero_image_url']:
            raise ValueError("hero_image_url is required for split_image_text layout")

    def render(self) -> List[Image.Image]:
        """
        Render the split image text layout.

        Returns:
            List containing single Image object
        """
        # Create base canvas
        canvas = self._create_background()

        # Get split configuration
        split_direction = self.options.get('split_direction', 'vertical')
        image_position = self.options.get('image_position', 'left')
        image_ratio = self.options.get('image_ratio', 0.5)

        # Validate ratio
        image_ratio = max(0.3, min(0.7, image_ratio))  # Clamp between 30%-70%

        # Load and place hero image
        canvas = self._add_split_image(canvas, split_direction, image_position, image_ratio)

        # Add text content
        canvas = self._add_split_text(canvas, split_direction, image_position, image_ratio)

        return [canvas]

    def _create_background(self) -> Image.Image:
        """Create background based on configuration."""
        # Use the base class method which supports gradient, solid_color, and image modes
        return self._create_background_from_config()

    def _add_split_image(self, canvas: Image.Image, split_direction: str,
                        image_position: str, image_ratio: float) -> Image.Image:
        """Add hero image to canvas in split configuration."""
        from ..asset_manager import get_asset_manager

        try:
            asset_manager = get_asset_manager()
            hero_image = asset_manager.load_asset(
                self.assets['hero_image_url'],
                role='hero_image',
                remove_bg=self.remove_hero_bg,
                bg_removal_method=self.bg_removal_method,
                alpha_matting=self.bg_alpha_matting,
                color_tolerance=self.bg_color_tolerance
            )

            if split_direction == 'vertical':
                # Vertical split (left/right)
                image_width = int(self.canvas_width * image_ratio)

                # Fit image to area
                fitted_image = asset_manager.smart_crop(
                    hero_image,
                    (image_width, self.canvas_height),
                    focus='center'
                )

                # Paste image
                if image_position == 'left':
                    canvas.paste(fitted_image, (0, 0))
                else:  # right
                    x_pos = self.canvas_width - image_width
                    canvas.paste(fitted_image, (x_pos, 0))

            else:  # horizontal
                # Horizontal split (top/bottom)
                image_height = int(self.canvas_height * image_ratio)

                # Fit image to area
                fitted_image = asset_manager.smart_crop(
                    hero_image,
                    (self.canvas_width, image_height),
                    focus='center'
                )

                # Paste image
                if image_position == 'top':
                    canvas.paste(fitted_image, (0, 0))
                else:  # bottom
                    y_pos = self.canvas_height - image_height
                    canvas.paste(fitted_image, (0, y_pos))

            return canvas

        except Exception as e:
            print(f"Warning: Could not load hero image: {e}")
            return canvas

    def _add_split_text(self, canvas: Image.Image, split_direction: str,
                       image_position: str, image_ratio: float) -> Image.Image:
        """Add text content to the text half of the split layout."""
        draw = ImageDraw.Draw(canvas)

        # Get content
        title = self.content['title']
        description = self.content.get('description', '')
        bullets = self.content.get('bullets', [])

        # Detect RTL
        is_rtl = self._is_rtl_text(title)

        # Calculate text area
        if split_direction == 'vertical':
            text_width = int(self.canvas_width * (1 - image_ratio))
            text_height = self.canvas_height

            if image_position == 'left':
                text_x = int(self.canvas_width * image_ratio)
                text_y = 0
            else:  # right
                text_x = 0
                text_y = 0
        else:  # horizontal
            text_width = self.canvas_width
            text_height = int(self.canvas_height * (1 - image_ratio))

            text_x = 0
            if image_position == 'top':
                text_y = int(self.canvas_height * image_ratio)
            else:  # bottom
                text_y = 0

        # Add padding
        padding = 60
        text_x += padding
        text_y += padding
        text_width -= (padding * 2)
        text_height -= (padding * 2)

        # Get fonts
        title_font = self._get_title_font(is_rtl)
        desc_font = self._get_description_font(is_rtl)
        bullet_font = self._get_bullet_font(is_rtl)

        # Calculate vertical centering
        current_y = text_y

        # Draw title
        title_color = self.options.get('title_color', [52, 73, 94])
        current_y = self._draw_title(
            canvas, title, title_font,
            text_x, current_y, text_width,
            tuple(title_color), is_rtl
        )

        # Draw description
        if description:
            current_y += 30  # Spacing
            desc_color = self.options.get('description_color', [100, 100, 100])
            current_y = self._draw_description(
                canvas, description, desc_font,
                text_x, current_y, text_width,
                tuple(desc_color), is_rtl
            )

        # Draw bullets
        if bullets:
            current_y += 40  # Spacing
            bullet_color = self.options.get('bullet_color', [52, 73, 94])
            self._draw_bullets(
                canvas, bullets, bullet_font,
                text_x, current_y, text_width,
                tuple(bullet_color), is_rtl
            )

        return canvas

    def _get_title_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for title."""
        font_size = self.options.get('title_size', 56)
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

    def _get_description_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for description."""
        font_size = self.options.get('description_size', 32)
        if is_rtl:
            font_size = int(font_size * 1.1)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanMediumFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _get_bullet_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for bullets."""
        font_size = self.options.get('bullet_size', 28)
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

    def _draw_title(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                   x: int, y: int, max_width: int, color: Tuple[int, int, int],
                   is_rtl: bool) -> int:
        """Draw title text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Prepare text
        if is_rtl:
            text = self._prepare_arabic_text(text)

        # Wrap text
        lines = self._wrap_text(text, font, max_width)

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Left align for split layout
            line_x = x

            # Draw text
            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 15

        return current_y

    def _draw_description(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                         x: int, y: int, max_width: int, color: Tuple[int, int, int],
                         is_rtl: bool) -> int:
        """Draw description text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Prepare text
        if is_rtl and self._is_rtl_text(text):
            text = self._prepare_arabic_text(text)

        # Wrap text
        lines = self._wrap_text(text, font, max_width)

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Left align
            line_x = x

            # Draw text
            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 10

        return current_y

    def _draw_bullets(self, img: Image.Image, bullets: List[str], font: ImageFont.ImageFont,
                     x: int, y: int, max_width: int, color: Tuple[int, int, int],
                     is_rtl: bool):
        """Draw bullet points."""
        draw = ImageDraw.Draw(img)

        current_y = y
        bullet_char = "•"

        for bullet_text in bullets:
            # Prepare text
            if is_rtl and self._is_rtl_text(bullet_text):
                display_text = self._prepare_arabic_text(bullet_text)
            else:
                display_text = bullet_text

            # Format with bullet
            line = f"{bullet_char} {display_text}"

            bbox = font.getbbox(line)
            line_height = bbox[3] - bbox[1]

            # Draw bullet point
            draw.text((x, current_y), line, font=font, fill=color)

            current_y += line_height + 20

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["title"],
            "optional_content": ["description", "bullets"],
            "required_assets": ["hero_image_url"],
            "options": {
                "split_direction": "'vertical' (default) or 'horizontal'",
                "image_position": "'left'/'right' (vertical) or 'top'/'bottom' (horizontal)",
                "image_ratio": "0.3-0.7 (default: 0.5 for 50/50 split)",
                "title_size": "Font size for title (default: 56)",
                "description_size": "Font size for description (default: 32)",
                "bullet_size": "Font size for bullets (default: 28)",
                "title_color": "RGB color for title (default: [52,73,94])",
                "description_color": "RGB color for description (default: [100,100,100])",
                "bullet_color": "RGB color for bullets (default: [52,73,94])"
            }
        })
        return base_schema
