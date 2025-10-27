"""
Testimonial Layout - Customer testimonials and reviews

This layout displays:
- Customer quote/testimonial
- Profile photo (circular)
- Customer name
- Optional title/role
- Optional rating stars

Perfect for: Social proof, reviews, customer feedback, case studies
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class TestimonialLayout(PhotoLayoutEngine):
    """
    Testimonial Layout - Customer testimonials and reviews

    Content Fields:
        - quote (required): The testimonial text
        - name (required): Customer name
        - title (optional): Customer title/role (e.g., "CEO at Company")
        - rating (optional): Star rating (1-5)

    Assets:
        - profile_photo_url (optional): Customer profile photo
        - logo_url (optional): Company/product logo

    Options:
        - quote_style: 'standard' (default) or 'large'
        - show_rating: true/false (default: true if rating provided)
        - photo_size: Size of profile photo in pixels (default: 120)

    Example:
        {
            "layout_type": "testimonial",
            "content": {
                "quote": "This product changed my life! Highly recommended.",
                "name": "Sarah Johnson",
                "title": "Marketing Director",
                "rating": 5
            },
            "assets": {
                "profile_photo_url": "https://example.com/sarah.jpg"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[250, 250, 255], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        }
    """

    LAYOUT_TYPE = "testimonial"
    LAYOUT_CATEGORY = "social_proof"
    DESCRIPTION = "Customer testimonial with photo and rating"
    SUPPORTS_CAROUSEL = True

    OPTIONAL_ASSETS = ["profile_photo_url", "logo_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'quote' not in self.content:
            raise ValueError("quote is required for testimonial layout")

        if 'name' not in self.content:
            raise ValueError("name is required for testimonial layout")

        if not self.content['quote'].strip():
            raise ValueError("quote cannot be empty")

        if not self.content['name'].strip():
            raise ValueError("name cannot be empty")

        # Validate rating if provided
        if 'rating' in self.content:
            rating = self.content['rating']
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                raise ValueError("rating must be a number between 1 and 5")

    def render(self) -> List[Image.Image]:
        """
        Render the testimonial layout.

        Returns:
            List containing single Image object
        """
        # Create base canvas
        canvas = self._create_background()

        # Add content
        canvas = self._add_testimonial_content(canvas)

        return [canvas]

    def _create_background(self) -> Image.Image:
        """Create background based on configuration."""
        # Use the base class method which supports gradient, solid_color, and image modes
        return self._create_background_from_config()

    def _add_testimonial_content(self, canvas: Image.Image) -> Image.Image:
        """Add testimonial content: quote, photo, name, title, rating."""
        draw = ImageDraw.Draw(canvas)

        # Get content
        quote = self.content['quote']
        name = self.content['name']
        title = self.content.get('title', '')
        rating = self.content.get('rating')

        # Get options
        quote_style = self.options.get('quote_style', 'standard')
        show_rating = self.options.get('show_rating', rating is not None)
        photo_size = self.options.get('photo_size', 120)

        # Detect RTL
        is_rtl = self._is_rtl_text(quote)

        # Get fonts
        quote_font = self._get_quote_font(is_rtl, quote_style)
        name_font = self._get_name_font(is_rtl)
        title_font = self._get_title_font(is_rtl)

        # Get colors
        quote_color = tuple(self.options.get('quote_color', [52, 58, 64]))
        name_color = tuple(self.options.get('name_color', [33, 37, 41]))
        title_color = tuple(self.options.get('title_color', [108, 117, 125]))
        star_color = tuple(self.options.get('star_color', [255, 193, 7]))

        # Calculate layout
        margins = self._get_safe_margins()
        max_width = self.canvas_width - (margins['sides'] * 2)

        # Starting position - leave room at top for photo
        current_y = 180

        # Draw profile photo if provided
        has_photo = 'profile_photo_url' in self.assets and self.assets['profile_photo_url']
        if has_photo:
            photo_y = current_y
            self._draw_profile_photo(canvas, photo_y, photo_size)
            current_y = photo_y + photo_size + 50
        else:
            current_y += 30

        # Draw quote
        current_y = self._draw_quote(
            canvas, quote, quote_font,
            margins['sides'], current_y, max_width,
            quote_color, is_rtl
        )

        # Add spacing
        current_y += 60

        # Draw rating if requested
        if show_rating and rating:
            current_y = self._draw_rating(canvas, rating, current_y, star_color)
            current_y += 40

        # Draw name
        current_y = self._draw_centered_text(
            canvas, name, name_font, current_y, name_color
        )

        # Draw title if provided
        if title:
            current_y += 15
            self._draw_centered_text(
                canvas, title, title_font, current_y, title_color
            )

        return canvas

    def _draw_profile_photo(self, img: Image.Image, y: int, size: int):
        """Draw circular profile photo at top center."""
        try:
            from src.asset_manager import AssetManager

            # Load photo
            asset_manager = AssetManager()
            photo = asset_manager.load_asset(
                self.assets['profile_photo_url'],
                role='profile',
                use_cache=True,
                remove_bg=self.remove_hero_bg,
                bg_removal_method=self.bg_removal_method,
                alpha_matting=self.bg_alpha_matting,
                color_tolerance=self.bg_color_tolerance
            )

            # Resize to square
            photo = photo.resize((size, size), Image.Resampling.LANCZOS)

            # Create circular mask
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), (size, size)], fill=255)

            # Apply mask
            output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            output.paste(photo, (0, 0))
            output.putalpha(mask)

            # Paste onto canvas (centered)
            x = (self.canvas_width - size) // 2

            # Convert canvas to RGBA for compositing
            if img.mode != 'RGBA':
                img_rgba = img.convert('RGBA')
            else:
                img_rgba = img

            img_rgba.paste(output, (x, y), output)

            # Convert back to RGB
            img.paste(img_rgba.convert('RGB'), (0, 0))

        except Exception as e:
            # If photo loading fails, draw a placeholder circle
            draw = ImageDraw.Draw(img)
            x = (self.canvas_width - size) // 2
            draw.ellipse(
                [(x, y), (x + size, y + size)],
                fill=(200, 200, 200),
                outline=(150, 150, 150),
                width=2
            )

    def _draw_quote(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                    x: int, y: int, max_width: int, color: Tuple[int, int, int],
                    is_rtl: bool) -> int:
        """Draw quote text with quotation marks. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Add quotation marks
        if is_rtl:
            text = self._prepare_arabic_text(text)
            quoted_text = f'«{text}»'
        else:
            quoted_text = f'"{text}"'

        # Wrap text
        lines = self._wrap_text(quoted_text, font, max_width)

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Center align
            line_x = x + (max_width - line_width) // 2

            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 12

        return current_y

    def _draw_rating(self, img: Image.Image, rating: float, y: int,
                     color: Tuple[int, int, int]) -> int:
        """Draw star rating centered. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Create rating text (★ for filled, ☆ for empty)
        full_stars = int(rating)
        has_half = (rating - full_stars) >= 0.5
        empty_stars = 5 - full_stars - (1 if has_half else 0)

        stars_text = "★" * full_stars
        if has_half:
            stars_text += "½"
        stars_text += "☆" * empty_stars

        # Use a medium font for stars
        font_size = self.options.get('rating_size', 40)
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')
        font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        bbox = font.getbbox(stars_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.canvas_width - text_width) // 2

        draw.text((x, y), stars_text, font=font, fill=color)

        return y + text_height

    def _draw_centered_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                           y: int, color: Tuple[int, int, int]) -> int:
        """Draw centered text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Handle RTL if needed
        if self._is_rtl_text(text):
            text = self._prepare_arabic_text(text)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.canvas_width - text_width) // 2

        draw.text((x, y), text, font=font, fill=color)

        return y + text_height

    def _get_quote_font(self, is_rtl: bool, style: str) -> ImageFont.ImageFont:
        """Get font for quote."""
        if style == 'large':
            font_size = self.options.get('quote_size', 48)
        else:
            font_size = self.options.get('quote_size', 36)

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

    def _get_name_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for customer name."""
        font_size = self.options.get('name_size', 32)
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

    def _get_title_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for customer title."""
        font_size = self.options.get('title_size', 24)
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
            "required_content": ["quote", "name"],
            "optional_content": ["title", "rating"],
            "options": {
                "quote_style": "'standard' (default) or 'large'",
                "show_rating": "Show rating stars (default: true if rating provided)",
                "photo_size": "Profile photo size in pixels (default: 120)",
                "quote_size": "Font size for quote (default: 36 for standard, 48 for large)",
                "name_size": "Font size for name (default: 32)",
                "title_size": "Font size for title (default: 24)",
                "rating_size": "Font size for stars (default: 40)",
                "quote_color": "RGB color for quote (default: [52,58,64])",
                "name_color": "RGB color for name (default: [33,37,41])",
                "title_color": "RGB color for title (default: [108,117,125])",
                "star_color": "RGB color for rating stars (default: [255,193,7])"
            }
        })
        return base_schema
