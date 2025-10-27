"""
Headline Promo Layout - Marketing-focused layout with big headline

This layout is designed for promotional content with:
- Large, eye-catching headline
- Optional subheadline
- Optional CTA (Call-to-Action) button
- Optional hero image background

Perfect for: Sales, announcements, launches, promotions
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class HeadlinePromoLayout(PhotoLayoutEngine):
    """
    Headline Promo Layout - Big headline with optional CTA

    Content Fields:
        - headline (required): Main promotional text
        - subheadline (optional): Supporting text
        - cta (optional): Call-to-action button text

    Assets:
        - hero_image_url (optional): Background or side image

    Example:
        {
            "layout_type": "headline_promo",
            "content": {
                "headline": "Summer Sale",
                "subheadline": "Up to 50% Off Everything",
                "cta": "Shop Now"
            },
            "assets": {
                "hero_image_url": "https://example.com/beach.jpg"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[255, 107, 107], [253, 187, 45]],
                    "direction": "vertical"
                }
            }
        }
    """

    LAYOUT_TYPE = "headline_promo"
    LAYOUT_CATEGORY = "marketing"
    DESCRIPTION = "Big headline focus with optional CTA and hero image"
    SUPPORTS_CAROUSEL = False

    OPTIONAL_ASSETS = ["hero_image_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'headline' not in self.content:
            raise ValueError("headline is required for headline_promo layout")

        # Validate headline is not empty
        if not self.content['headline'].strip():
            raise ValueError("headline cannot be empty")

    def render(self) -> List[Image.Image]:
        """
        Render the headline promo layout.

        Returns:
            List containing single Image object
        """
        # Create base canvas
        img = self._create_background()

        # Add hero image if provided
        has_hero = 'hero_image_url' in self.assets and self.assets['hero_image_url']

        if has_hero:
            img = self._add_hero_image(img)

        # Add text content
        img = self._add_text_content(img, has_hero)
        
        # Add watermark if provided
        img = self._add_watermark(img)

        return [img]

    def _create_background(self) -> Image.Image:
        """
        Create background based on configuration.

        Returns:
            Background image
        """
        # Use the base class method which supports gradient, solid_color, and image modes
        return self._create_background_from_config()

    def _create_product_shadow(self, product_img: Image.Image) -> Image.Image:
        """
        Create soft shadow for product image.
        
        Args:
            product_img: Product image to create shadow for
            
        Returns:
            RGBA image with shadow effect
        """
        from PIL import ImageFilter
        
        # Create shadow layer
        shadow = Image.new('RGBA', product_img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw semi-transparent black rectangle
        shadow_draw.rectangle([(0, 0), product_img.size], fill=(0, 0, 0, 100))
        
        # Apply blur for soft shadow effect
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        
        return shadow

    def _add_hero_image(self, canvas: Image.Image) -> Image.Image:
        """
        Add hero image to canvas.
        
        Args:
            canvas: Base canvas
        
        Returns:
            Canvas with hero image added
        """
        from ..asset_manager import get_asset_manager

        hero_url = self.assets.get('hero_image_url')
        print(f"🖼️  Adding hero image from: {hero_url}")

        try:
            asset_manager = get_asset_manager()
            print(f"📂 Loading hero image asset: {hero_url}")
            hero_image = asset_manager.load_asset(
                self.assets['hero_image_url'],
                role='hero_image',
                remove_bg=self.remove_hero_bg,
                bg_removal_method=self.bg_removal_method,
                alpha_matting=self.bg_alpha_matting,
                color_tolerance=self.bg_color_tolerance
            )
            print(f"✅ Hero image loaded successfully! Size: {hero_image.size}")

            # Determine layout mode
            layout_mode = self.options.get('hero_layout', 'background')
            print(f"   Layout mode: {layout_mode}")

            if layout_mode == 'background':
                # Use hero as full background with overlay
                hero_fitted = asset_manager.smart_crop(
                    hero_image,
                    (self.canvas_width, self.canvas_height),
                    focus='center'
                )
                print(f"   Hero fitted to canvas: {hero_fitted.size}")

                # Create overlay for text contrast
                overlay = Image.new('RGBA', (self.canvas_width, self.canvas_height),
                                   (0, 0, 0, 128))  # 50% black overlay

                # Composite
                canvas = hero_fitted.convert('RGB')
                canvas.paste(overlay, (0, 0), overlay)
                print(f"✅ Hero image applied as background with overlay")

            elif layout_mode == 'side':
                # Place hero on left side, text on right
                hero_width = self.canvas_width // 2
                hero_fitted = asset_manager.smart_crop(
                    hero_image,
                    (hero_width, self.canvas_height),
                    focus='center'
                )
                canvas.paste(hero_fitted, (0, 0))
                print(f"✅ Hero image placed on side")

            elif layout_mode == 'product':
                # New mode: product positioned in lower-center with shadow
                max_product_height = int(self.canvas_height * 0.5)  # 50% of canvas
                max_product_width = int(self.canvas_width * 0.6)
                
                # Fit product maintaining aspect ratio
                hero_fitted = asset_manager.fit_to_bounds(
                    hero_image,
                    (max_product_width, max_product_height),
                    maintain_aspect=True
                )
                print(f"✅ Product fitted to bounds: {hero_fitted.size}")
                
                # Position in lower-center
                x_pos = (self.canvas_width - hero_fitted.width) // 2
                y_pos = int(self.canvas_height * 0.45)  # Start at 45% down
                
                # Add shadow if enabled
                if self.options.get('product_shadow', True):
                    shadow = self._create_product_shadow(hero_fitted)
                    shadow_x = x_pos + 10
                    shadow_y = y_pos + 10
                    
                    # Create composite image for proper shadow rendering
                    shadow_canvas = Image.new('RGBA', (self.canvas_width, self.canvas_height), (0, 0, 0, 0))
                    shadow_canvas.paste(shadow, (shadow_x, shadow_y), shadow)
                    shadow_canvas = shadow_canvas.convert('RGB')
                    
                    # Composite shadow on main canvas
                    canvas = Image.alpha_composite(canvas.convert('RGBA'), shadow_canvas.convert('RGBA')).convert('RGB')
                    print(f"✅ Product shadow applied")
                
                # Paste product on top
                if hero_fitted.mode == 'RGBA':
                    canvas.paste(hero_fitted, (x_pos, y_pos), hero_fitted)
                else:
                    canvas.paste(hero_fitted, (x_pos, y_pos))
                print(f"✅ Product positioned at ({x_pos}, {y_pos})")

            return canvas

        except Exception as e:
            print(f"❌ ERROR: Could not load hero image: {e}")
            import traceback
            traceback.print_exc()
            return canvas

    def _add_text_content(self, img: Image.Image, has_hero: bool) -> Image.Image:
        """
        Add headline, subheadline, and CTA to image.

        Args:
            img: Base image
            has_hero: Whether hero image is present (affects text positioning)

        Returns:
            Image with text added
        """
        draw = ImageDraw.Draw(img)

        # Add text contrast overlay if enabled
        if self.options.get('text_overlay', True):
            overlay_height = int(self.canvas_height * 0.4)  # Top 40%
            overlay = Image.new('RGBA', (self.canvas_width, overlay_height), 
                               (0, 0, 0, int(255 * 0.3)))  # 30% black
            img.paste(overlay, (0, 0), overlay)
            print(f"✅ Text contrast overlay applied")

        # Get content
        headline = self.content['headline']
        subheadline = self.content.get('subheadline')
        cta = self.content.get('cta')

        # Detect RTL
        is_rtl = self._is_rtl_text(headline)

        # Get fonts
        headline_font = self._get_headline_font(is_rtl)
        subheadline_font = self._get_subheadline_font(is_rtl) if subheadline else None
        cta_font = self._get_cta_font() if cta else None

        # Calculate layout
        margins = self._get_safe_margins()
        max_text_width = self._get_max_text_width()

        # Determine text area (account for hero image position)
        hero_layout = self.options.get('hero_layout', 'background')
        if hero_layout == 'side' and has_hero:
            text_x_start = self.canvas_width // 2 + margins['left']
            max_text_width = (self.canvas_width // 2) - (margins['left'] + margins['right'])
        else:
            text_x_start = self.canvas_width // 2

        # Calculate vertical centering
        total_height = self._calculate_total_text_height(
            headline, subheadline, cta,
            headline_font, subheadline_font, cta_font,
            max_text_width, is_rtl
        )

        # Use rule-of-thirds positioning for background layout
        if hero_layout == 'background':
            start_y = int(self.canvas_height * 0.15)  # 15% from top for better hierarchy
        else:
            start_y = (self.canvas_height - total_height) // 2  # Keep centered for side layout

        current_y = start_y

        # Draw headline
        headline_color = self.options.get('headline_color', [255, 255, 255])
        current_y = self._draw_headline(
            img, headline, headline_font,
            text_x_start, current_y,
            max_text_width, tuple(headline_color), is_rtl
        )

        # Draw subheadline
        if subheadline:
            current_y += 30  # Spacing
            subheadline_color = self.options.get('subheadline_color', [240, 240, 240])
            current_y = self._draw_subheadline(
                img, subheadline, subheadline_font,
                text_x_start, current_y,
                max_text_width, tuple(subheadline_color), is_rtl
            )

        # Draw CTA button
        if cta:
            current_y += 50  # Spacing before CTA
            self._draw_cta_button(
                img, cta, cta_font,
                text_x_start, current_y,
                is_rtl
            )

        return img

    def _get_headline_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for headline."""
        font_size = self.options.get('headline_size', 84)
        if is_rtl:
            font_size = int(font_size * 1.1)  # Slightly larger for Farsi

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanBoldFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        try:
            if not os.path.exists(font_path):
                print(f"❌ Font not found: {font_path}")
                return ImageFont.load_default()
            
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ Loaded font: {os.path.basename(font_path)} at size {font_size}")
            return font
        except Exception as e:
            print(f"❌ Font loading error: {e}")
            return ImageFont.load_default()

    def _get_subheadline_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for subheadline."""
        font_size = self.options.get('subheadline_size', 42)
        if is_rtl:
            font_size = int(font_size * 1.1)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')

        if is_rtl:
            font_path = os.path.join(font_dir, 'IRANYekanMediumFaNum.ttf')
        else:
            font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')

        try:
            if not os.path.exists(font_path):
                print(f"❌ Font not found: {font_path}")
                return ImageFont.load_default()
            
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ Loaded font: {os.path.basename(font_path)} at size {font_size}")
            return font
        except Exception as e:
            print(f"❌ Font loading error: {e}")
            return ImageFont.load_default()

    def _get_cta_font(self) -> ImageFont.ImageFont:
        """Get font for CTA button."""
        font_size = self.options.get('cta_size', 32)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')
        font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _calculate_total_text_height(self, headline: str, subheadline: Optional[str],
                                    cta: Optional[str],
                                    headline_font: ImageFont.ImageFont,
                                    subheadline_font: Optional[ImageFont.ImageFont],
                                    cta_font: Optional[ImageFont.ImageFont],
                                    max_width: int, is_rtl: bool) -> int:
        """Calculate total height of all text elements."""
        total = 0

        # Headline
        headline_lines = self._wrap_text(headline, headline_font, max_width)
        if is_rtl:
            headline_lines = [self._prepare_arabic_text(line) for line in headline_lines]

        for line in headline_lines:
            bbox = headline_font.getbbox(line)
            total += (bbox[3] - bbox[1]) + 15  # Line height + spacing

        # Subheadline
        if subheadline and subheadline_font:
            total += 30  # Spacing before subheadline
            subheadline_lines = self._wrap_text(subheadline, subheadline_font, max_width)
            if is_rtl and self._is_rtl_text(subheadline):
                subheadline_lines = [self._prepare_arabic_text(line) for line in subheadline_lines]

            for line in subheadline_lines:
                bbox = subheadline_font.getbbox(line)
                total += (bbox[3] - bbox[1]) + 10

        # CTA
        if cta and cta_font:
            total += 50  # Spacing before CTA
            total += 60  # CTA button height

        return total

    def _draw_headline(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                      x: int, y: int, max_width: int, color: Tuple[int, int, int],
                      is_rtl: bool) -> int:
        """Draw headline text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        lines = self._wrap_text(text, font, max_width)
        if is_rtl:
            lines = [self._prepare_arabic_text(line) for line in lines]

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Center align
            line_x = x - line_width // 2

            # Draw shadow for depth
            shadow_offset = 3
            draw.text((line_x + shadow_offset, current_y + shadow_offset),
                     line, font=font, fill=(0, 0, 0, 100))

            # Draw main text
            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 15

        return current_y

    def _draw_subheadline(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                         x: int, y: int, max_width: int, color: Tuple[int, int, int],
                         is_rtl: bool) -> int:
        """Draw subheadline text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        lines = self._wrap_text(text, font, max_width)
        if is_rtl and self._is_rtl_text(text):
            lines = [self._prepare_arabic_text(line) for line in lines]

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            # Center align
            line_x = x - line_width // 2

            # Draw text
            draw.text((line_x, current_y), line, font=font, fill=color)

            current_y += line_height + 10

        return current_y

    def _draw_cta_button(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                        x: int, y: int, is_rtl: bool):
        """Draw CTA button."""
        draw = ImageDraw.Draw(img)

        # Prepare text
        display_text = self._prepare_arabic_text(text) if is_rtl and self._is_rtl_text(text) else text

        # Measure text
        bbox = font.getbbox(display_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Button dimensions
        padding_x = 40
        padding_y = 20
        button_width = text_width + (padding_x * 2)
        button_height = text_height + (padding_y * 2)
        border_radius = 12

        # Button position (centered)
        button_x = x - button_width // 2
        button_y = y

        # Button colors
        button_color = tuple(self.options.get('cta_bg_color', [255, 255, 255]))
        text_color = tuple(self.options.get('cta_text_color', [52, 73, 94]))

        # Draw rounded rectangle button
        draw.rounded_rectangle(
            [(button_x, button_y), (button_x + button_width, button_y + button_height)],
            radius=border_radius,
            fill=button_color
        )

        # Draw text
        text_x = button_x + padding_x
        text_y = button_y + padding_y

        draw.text((text_x, text_y), display_text, font=font, fill=text_color)

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["headline"],
            "optional_content": ["subheadline", "cta"],
            "optional_assets": ["hero_image_url"],
            "options": {
                "headline_size": "Font size for headline (default: 84)",
                "subheadline_size": "Font size for subheadline (default: 42)",
                "cta_size": "Font size for CTA (default: 32)",
                "headline_color": "RGB color for headline (default: [255,255,255])",
                "subheadline_color": "RGB color for subheadline (default: [240,240,240])",
                "cta_bg_color": "RGB color for CTA button background (default: [255,255,255])",
                "cta_text_color": "RGB color for CTA text (default: [52,73,94])",
                "hero_layout": "Hero image layout mode: 'background' or 'side' (default: 'background')"
            }
        })
        return base_schema
