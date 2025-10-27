"""
Product Showcase Layout - E-commerce product display

This layout is optimized for showcasing products with:
- Hero product image (center or side)
- Product name (prominent)
- Price display
- Optional description
- Optional CTA button
- Optional logo/brand

Perfect for: E-commerce, product launches, sales, promotions
"""

from .base import PhotoLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


@register_layout
class ProductShowcaseLayout(PhotoLayoutEngine):
    """
    Product Showcase Layout - E-commerce product display

    Content Fields:
        - product_name (required): Name of the product
        - price (required): Product price (string for formatting flexibility)
        - description (optional): Product description
        - cta (optional): Call-to-action button text
        - brand (optional): Brand name

    Assets:
        - hero_image_url (required): Product image
        - logo_image_url (optional): Brand logo

    Options:
        - layout_style: 'center' (default) or 'side'
        - price_style: 'prominent' (default) or 'subtle'
        - show_currency: true/false (default: true)
        - currency_symbol: string (default: '$')

    Example:
        {
            "layout_type": "product_showcase",
            "content": {
                "product_name": "Premium Headphones",
                "price": "299",
                "description": "Studio-quality sound",
                "cta": "Buy Now",
                "brand": "AudioPro"
            },
            "assets": {
                "hero_image_url": "https://example.com/headphones.jpg",
                "logo_image_url": "https://example.com/logo.png"
            },
            "background": {
                "mode": "gradient",
                "gradient": {
                    "colors": [[240, 240, 245], [255, 255, 255]],
                    "direction": "vertical"
                }
            }
        }
    """

    LAYOUT_TYPE = "product_showcase"
    LAYOUT_CATEGORY = "marketing"
    DESCRIPTION = "Product-centric display with pricing and CTA"
    SUPPORTS_CAROUSEL = False

    REQUIRED_ASSETS = ["hero_image_url"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'product_name' not in self.content:
            raise ValueError("product_name is required for product_showcase layout")

        if 'price' not in self.content:
            raise ValueError("price is required for product_showcase layout")

        if not self.content['product_name'].strip():
            raise ValueError("product_name cannot be empty")

        # Validate hero image is provided
        if 'hero_image_url' not in self.assets or not self.assets['hero_image_url']:
            raise ValueError("hero_image_url is required for product_showcase layout")

    def render(self) -> List[Image.Image]:
        """
        Render the product showcase layout.

        Returns:
            List containing single Image object
        """
        # Create base canvas
        canvas = self._create_background()

        # Get layout style
        layout_style = self.options.get('layout_style', 'center')

        # Add product image
        canvas = self._add_product_image(canvas, layout_style)

        # Add logo if provided
        if 'logo_image_url' in self.assets and self.assets['logo_image_url']:
            canvas = self._add_logo(canvas)

        # Add product information
        canvas = self._add_product_info(canvas, layout_style)
        
        # Add watermark if provided
        canvas = self._add_watermark(canvas)

        return [canvas]

    def _create_background(self) -> Image.Image:
        """Create background based on configuration."""
        # Use the base class method which supports gradient, solid_color, and image modes
        return self._create_background_from_config()

    def _add_product_image(self, canvas: Image.Image, layout_style: str) -> Image.Image:
        """Add product image to canvas."""
        from ..asset_manager import get_asset_manager

        product_url = self.assets.get('hero_image_url')
        print(f"🛍️  Adding product image from: {product_url}")

        try:
            asset_manager = get_asset_manager()
            print(f"📂 Loading product image asset: {product_url}")
            product_image = asset_manager.load_asset(
                self.assets['hero_image_url'],
                role='hero_image',
                remove_bg=self.remove_hero_bg,
                bg_removal_method=self.bg_removal_method,
                alpha_matting=self.bg_alpha_matting,
                color_tolerance=self.bg_color_tolerance
            )
            print(f"✅ Product image loaded successfully! Size: {product_image.size}")
            print(f"   Layout style: {layout_style}")

            if layout_style == 'center':
                # Center layout - product image in upper-middle area
                image_size = min(800, int(self.canvas_width * 0.7))
                fitted_image = asset_manager.resize_to_fit(
                    product_image,
                    image_size,
                    image_size,
                    maintain_aspect=True
                )
                print(f"   Product fitted to size: {fitted_image.size}")

                # Center horizontally, position in upper third
                x_pos = (self.canvas_width - fitted_image.width) // 2
                y_pos = 150

                canvas.paste(fitted_image, (x_pos, y_pos))
                print(f"   Placed at position: ({x_pos}, {y_pos})")

            else:  # side layout
                # Side layout - product on left, info on right
                image_width = int(self.canvas_width * 0.5)
                fitted_image = asset_manager.resize_to_fit(
                    product_image,
                    image_width,
                    self.canvas_height - 200,
                    maintain_aspect=True
                )
                print(f"   Product fitted to size: {fitted_image.size}")

                # Center in left half
                x_pos = (image_width - fitted_image.width) // 2
                y_pos = (self.canvas_height - fitted_image.height) // 2

                canvas.paste(fitted_image, (x_pos, y_pos))
                print(f"   Placed at position: ({x_pos}, {y_pos})")

            print(f"✅ Product image added successfully!")
            return canvas

        except Exception as e:
            print(f"❌ ERROR: Could not load product image: {e}")
            import traceback
            traceback.print_exc()
            return canvas

    def _add_logo(self, canvas: Image.Image) -> Image.Image:
        """Add brand logo to canvas (top-right corner)."""
        from ..asset_manager import get_asset_manager

        try:
            asset_manager = get_asset_manager()
            logo = asset_manager.load_asset(
                self.assets['logo_image_url'],
                role='logo_image'
            )

            # Resize logo to reasonable size
            logo_size = 100
            logo_fitted = asset_manager.resize_to_fit(logo, logo_size, logo_size)

            # Position in top-right with padding
            x_pos = self.canvas_width - logo_fitted.width - 40
            y_pos = 40

            # Convert to RGBA if needed
            if logo_fitted.mode != 'RGBA':
                logo_fitted = logo_fitted.convert('RGBA')

            # Paste with alpha
            canvas.paste(logo_fitted, (x_pos, y_pos), logo_fitted if logo_fitted.mode == 'RGBA' else None)

            return canvas

        except Exception as e:
            print(f"Warning: Could not load logo: {e}")
            return canvas

    def _add_product_info(self, canvas: Image.Image, layout_style: str) -> Image.Image:
        """Add product name, price, description, and CTA."""
        draw = ImageDraw.Draw(canvas)

        # Get content
        product_name = self.content['product_name']
        price = self.content['price']
        description = self.content.get('description', '')
        cta = self.content.get('cta', '')
        brand = self.content.get('brand', '')

        # Detect RTL
        is_rtl = self._is_rtl_text(product_name)

        # Get fonts
        name_font = self._get_product_name_font(is_rtl)
        price_font = self._get_price_font()
        desc_font = self._get_description_font(is_rtl)
        cta_font = self._get_cta_font()

        if layout_style == 'center':
            # Center layout - info below product image
            info_y_start = 1000  # Below product image

            # Product name
            current_y = info_y_start
            name_color = self.options.get('product_name_color', [52, 73, 94])
            current_y = self._draw_centered_text(
                canvas, product_name, name_font,
                current_y, tuple(name_color), is_rtl
            )

            # Price
            current_y += 20
            price_color = self.options.get('price_color', [220, 53, 69])
            current_y = self._draw_price(canvas, price, price_font, current_y, tuple(price_color))

            # Description
            if description:
                current_y += 30
                desc_color = self.options.get('description_color', [100, 100, 100])
                current_y = self._draw_centered_text(
                    canvas, description, desc_font,
                    current_y, tuple(desc_color), is_rtl
                )

            # CTA
            if cta:
                current_y += 50
                self._draw_cta_button(canvas, cta, cta_font, self.canvas_width // 2, current_y)

        else:  # side layout
            # Side layout - info on right side
            info_x = int(self.canvas_width * 0.55)
            max_width = int(self.canvas_width * 0.4)

            current_y = 300

            # Product name
            name_color = self.options.get('product_name_color', [52, 73, 94])
            current_y = self._draw_left_aligned_text(
                canvas, product_name, name_font,
                info_x, current_y, max_width,
                tuple(name_color), is_rtl
            )

            # Price
            current_y += 30
            price_color = self.options.get('price_color', [220, 53, 69])
            current_y = self._draw_price_left(canvas, price, price_font, info_x, current_y, tuple(price_color))

            # Description
            if description:
                current_y += 40
                desc_color = self.options.get('description_color', [100, 100, 100])
                current_y = self._draw_left_aligned_text(
                    canvas, description, desc_font,
                    info_x, current_y, max_width,
                    tuple(desc_color), is_rtl
                )

            # CTA
            if cta:
                current_y += 50
                self._draw_cta_button(canvas, cta, cta_font, info_x + 120, current_y)

        return canvas

    def _get_product_name_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for product name."""
        font_size = self.options.get('product_name_size', 64)
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

    def _get_price_font(self) -> ImageFont.ImageFont:
        """Get font for price."""
        font_size = self.options.get('price_size', 72)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')
        font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _get_description_font(self, is_rtl: bool) -> ImageFont.ImageFont:
        """Get font for description."""
        font_size = self.options.get('description_size', 28)
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

    def _get_cta_font(self) -> ImageFont.ImageFont:
        """Get font for CTA."""
        font_size = self.options.get('cta_size', 32)

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'assets', 'fonts')
        font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')

        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            return ImageFont.load_default()

    def _draw_centered_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                           y: int, color: Tuple[int, int, int], is_rtl: bool) -> int:
        """Draw centered text. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        if is_rtl:
            text = self._prepare_arabic_text(text)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.canvas_width - text_width) // 2

        draw.text((x, y), text, font=font, fill=color)

        return y + text_height

    def _draw_left_aligned_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                               x: int, y: int, max_width: int, color: Tuple[int, int, int],
                               is_rtl: bool) -> int:
        """Draw left-aligned text with wrapping. Returns new Y position."""
        draw = ImageDraw.Draw(img)

        if is_rtl:
            text = self._prepare_arabic_text(text)

        lines = self._wrap_text(text, font, max_width)

        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            line_height = bbox[3] - bbox[1]

            draw.text((x, current_y), line, font=font, fill=color)

            current_y += line_height + 10

        return current_y

    def _draw_price(self, img: Image.Image, price: str, font: ImageFont.ImageFont,
                   y: int, color: Tuple[int, int, int]) -> int:
        """Draw price (centered). Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Format price
        show_currency = self.options.get('show_currency', True)
        currency_symbol = self.options.get('currency_symbol', '$')

        if show_currency:
            price_text = f"{currency_symbol}{price}"
        else:
            price_text = price

        bbox = font.getbbox(price_text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.canvas_width - text_width) // 2

        draw.text((x, y), price_text, font=font, fill=color)

        return y + text_height

    def _draw_price_left(self, img: Image.Image, price: str, font: ImageFont.ImageFont,
                        x: int, y: int, color: Tuple[int, int, int]) -> int:
        """Draw price (left-aligned). Returns new Y position."""
        draw = ImageDraw.Draw(img)

        # Format price
        show_currency = self.options.get('show_currency', True)
        currency_symbol = self.options.get('currency_symbol', '$')

        if show_currency:
            price_text = f"{currency_symbol}{price}"
        else:
            price_text = price

        bbox = font.getbbox(price_text)
        text_height = bbox[3] - bbox[1]

        draw.text((x, y), price_text, font=font, fill=color)

        return y + text_height

    def _draw_cta_button(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                        x: int, y: int):
        """Draw CTA button."""
        draw = ImageDraw.Draw(img)

        # Measure text
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Button dimensions
        padding_x = 50
        padding_y = 20
        button_width = text_width + (padding_x * 2)
        button_height = text_height + (padding_y * 2)
        border_radius = 12

        # Button position (centered around x)
        button_x = x - button_width // 2
        button_y = y

        # Button colors
        button_color = tuple(self.options.get('cta_bg_color', [52, 73, 94]))
        text_color = tuple(self.options.get('cta_text_color', [255, 255, 255]))

        # Draw rounded rectangle button
        draw.rounded_rectangle(
            [(button_x, button_y), (button_x + button_width, button_y + button_height)],
            radius=border_radius,
            fill=button_color
        )

        # Draw text
        text_x = button_x + padding_x
        text_y = button_y + padding_y

        draw.text((text_x, text_y), text, font=font, fill=text_color)

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["product_name", "price"],
            "optional_content": ["description", "cta", "brand"],
            "required_assets": ["hero_image_url"],
            "optional_assets": ["logo_image_url"],
            "options": {
                "layout_style": "'center' (default) or 'side'",
                "price_style": "'prominent' (default) or 'subtle'",
                "show_currency": "true/false (default: true)",
                "currency_symbol": "string (default: '$')",
                "product_name_size": "Font size for product name (default: 64)",
                "price_size": "Font size for price (default: 72)",
                "description_size": "Font size for description (default: 28)",
                "cta_size": "Font size for CTA (default: 32)",
                "product_name_color": "RGB color for product name (default: [52,73,94])",
                "price_color": "RGB color for price (default: [220,53,69])",
                "description_color": "RGB color for description (default: [100,100,100])",
                "cta_bg_color": "RGB color for CTA button (default: [52,73,94])",
                "cta_text_color": "RGB color for CTA text (default: [255,255,255])"
            }
        })
        return base_schema
