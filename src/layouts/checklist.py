"""
Checklist Layout - Steps and bullet lists

This layout displays:
- Title
- List of items with checkmarks or bullets
- Optional brand/author

Perfect for: Tips, how-to guides, feature lists, task lists
"""

from .base import TextLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class ChecklistLayout(TextLayoutEngine):
    """
    Checklist Layout - Steps and bullet lists

    Content Fields:
        - title (required): Checklist title
        - items (required): List of checklist items (strings)
        - brand (optional): Brand name for footer

    Options:
        - check_style: 'checkmark' (default) or 'bullet' or 'number'
        - items_checked: List of indices (0-based) of checked items
        - max_items: Maximum items to display (default: 10)

    Example:
        {
            "layout_type": "checklist",
            "content": {
                "title": "5 Tips for Better Design",
                "items": [
                    "Keep it simple and clean",
                    "Use consistent typography",
                    "Test with real users",
                    "Focus on user needs",
                    "Iterate based on feedback"
                ],
                "brand": "Design Studio"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 247, 230], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        }
    """

    LAYOUT_TYPE = "checklist"
    LAYOUT_CATEGORY = "educational"
    DESCRIPTION = "Title with bulleted/numbered list"
    SUPPORTS_CAROUSEL = False

    def _validate(self):
        """Validate that required content fields are present."""
        if 'title' not in self.content:
            raise ValueError("title is required for checklist layout")

        if 'items' not in self.content:
            raise ValueError("items is required for checklist layout")

        if not self.content['title'].strip():
            raise ValueError("title cannot be empty")

        if not isinstance(self.content['items'], list) or len(self.content['items']) == 0:
            raise ValueError("items must be a non-empty list")

    def render(self) -> List[Image.Image]:
        """
        Render the checklist layout.

        Returns:
            List containing single Image object
        """
        # Create base canvas
        canvas = self._create_background()

        # Add content
        canvas = self._add_checklist_content(canvas)

        return [canvas]

    def _create_background(self) -> Image.Image:
        """Create background based on configuration."""
        # Use the base class method which supports gradient, solid_color, and image modes
        return self._create_background_from_config()

    def _add_checklist_content(self, canvas: Image.Image) -> Image.Image:
        """Add title and checklist items."""
        draw = ImageDraw.Draw(canvas)

        # Get content
        title = self.content['title']
        items = self.content['items']
        brand = self.content.get('brand', '')

        # Get options
        check_style = self.options.get('check_style', 'checkmark')
        items_checked = self.options.get('items_checked', [])
        max_items = self.options.get('max_items', 10)

        # Limit items
        items = items[:max_items]

        # Detect RTL
        is_rtl = self._is_rtl_text(title)

        # Get fonts
        title_font = self._get_title_font(is_rtl)
        item_font = self._get_item_font(is_rtl)

        # Get colors
        title_color = tuple(self.options.get('title_color', [52, 73, 94]))
        item_color = tuple(self.options.get('item_color', [73, 80, 87]))
        check_color = tuple(self.options.get('check_color', [40, 167, 69]))

        # Calculate layout
        margins = self._get_safe_margins()
        max_width = self.canvas_width - (margins['sides'] * 2)

        # Starting position
        current_y = 200

        # Draw title
        current_y = self._draw_title(
            canvas, title, title_font,
            margins['sides'], current_y, max_width,
            title_color, is_rtl
        )

        # Add spacing
        current_y += 100

        # Draw checklist items
        for idx, item in enumerate(items):
            is_checked = idx in items_checked

            current_y = self._draw_checklist_item(
                canvas, item, item_font,
                margins['sides'], current_y, max_width,
                item_color, check_color,
                check_style, is_checked, idx + 1, is_rtl
            )

            current_y += 35  # Spacing between items for better readability

        # Draw brand if provided
        if brand:
            brand_font = self._get_brand_font()
            brand_color = tuple(self.options.get('brand_color', [108, 117, 125]))
            brand_y = self.canvas_height - margins['bottom']

            self._draw_centered_text(canvas, brand, brand_font, brand_y, brand_color)

        return canvas

    def _get_title_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for title using font manager."""
        font_size = self.options.get('title_size', 64)
        if is_rtl:
            font_size = int(font_size * 1.1)
        
        title_text = self.content.get('title', '')
        return self._get_font(title_text, font_size, 'bold')

    def _get_item_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for items using font manager."""
        font_size = self.options.get('item_size', 36)
        if is_rtl:
            font_size = int(font_size * 1.1)
        
        # Use first item to detect language
        items = self.content.get('items', [])
        sample_text = items[0] if items else ''
        return self._get_font(sample_text, font_size, 'regular')

    def _get_brand_font(self) -> ImageFont.ImageFont:
        """Get font for brand using font manager."""
        font_size = 24
        brand_text = self.content.get('brand', '')
        return self._get_font(brand_text, font_size, 'regular')

    def _draw_title(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                   x: int, y: int, max_width: int, color: Tuple[int, int, int],
                   is_rtl: bool) -> int:
        """Draw title text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        if is_rtl:
            text = self._prepare_arabic_text(text)

        # Wrap text
        lines = self._wrap_text(text, font, max_width)

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Center align title
            line_x = x + (max_width - line_width) // 2

            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 15

        return current_y

    def _draw_checklist_item(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                            x: int, y: int, max_width: int,
                            text_color: Tuple[int, int, int],
                            check_color: Tuple[int, int, int],
                            check_style: str, is_checked: bool, number: int,
                            is_rtl: bool) -> int:
        """Draw a single checklist item with drawn shapes. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Prepare text
        if is_rtl and self._is_rtl_text(text):
            display_text = self._prepare_arabic_text(text)
        else:
            display_text = text

        # Measure text for proper alignment
        bbox = font.getbbox(display_text)
        text_height = bbox[3] - bbox[1]
        
        # Shape configuration
        box_size = 32
        checkbox_margin = 15
        
        # Calculate positions
        if check_style == 'number':
            # For numbers, use text rendering
            symbol = f"{number}."
            symbol_bbox = font.getbbox(symbol)
            symbol_width = symbol_bbox[2] - symbol_bbox[0]
            draw.text((x, y), symbol, font=font, fill=check_color)
            text_x = x + symbol_width + 20
        else:
            # Draw shapes for checkboxes and bullets
            if check_style == 'checkmark':
                # Draw checkbox
                checkbox_y = y + (text_height - box_size) // 2
                
                if is_checked:
                    # Filled checkbox with checkmark
                    draw.rectangle([x, checkbox_y, x + box_size, checkbox_y + box_size],
                                 fill=check_color, outline=check_color, width=2)
                    # Draw checkmark
                    self._draw_checkmark(draw, x, checkbox_y, box_size, (255, 255, 255))
                else:
                    # Empty checkbox
                    draw.rectangle([x, checkbox_y, x + box_size, checkbox_y + box_size],
                                 fill=None, outline=text_color, width=2)
            else:
                # Draw bullet
                bullet_size = 10
                bullet_y = y + text_height // 2
                draw.ellipse([x, bullet_y - bullet_size//2,
                            x + bullet_size, bullet_y + bullet_size//2],
                           fill=check_color)
                box_size = bullet_size  # Adjust spacing for bullets
            
            text_x = x + box_size + 25

        # Draw text
        text_max_width = max_width - (text_x - x)
        draw.text((text_x, y), display_text, font=font, fill=text_color)

        return y + text_height
    
    def _draw_checkmark(self, draw: ImageDraw.ImageDraw, x: int, y: int, size: int,
                       color: Tuple[int, int, int]):
        """Draw a checkmark inside a checkbox."""
        # Checkmark as a polyline
        padding = size * 0.2
        check_points = [
            (x + padding + size * 0.2, y + size * 0.5),
            (x + padding + size * 0.4, y + size * 0.7),
            (x + size - padding, y + padding)
        ]
        draw.line(check_points, fill=color, width=3, joint='curve')

    def _draw_centered_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                           y: int, color: Tuple[int, int, int]):
        """Draw centered text."""
        draw = ImageDraw.Draw(img)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]

        x = (self.canvas_width - text_width) // 2

        draw.text((x, y), text, font=font, fill=color)

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["title", "items"],
            "optional_content": ["brand"],
            "options": {
                "check_style": "'checkmark' (default), 'bullet', or 'number'",
                "items_checked": "List of checked item indices (0-based)",
                "max_items": "Maximum items to display (default: 10)",
                "title_size": "Font size for title (default: 64)",
                "item_size": "Font size for items (default: 36)",
                "title_color": "RGB color for title (default: [52,73,94])",
                "item_color": "RGB color for items (default: [73,80,87])",
                "check_color": "RGB color for checkmarks/bullets (default: [40,167,69])",
                "brand_color": "RGB color for brand (default: [108,117,125])"
            }
        })
        return base_schema
