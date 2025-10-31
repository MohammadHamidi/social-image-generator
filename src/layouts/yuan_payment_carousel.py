"""
Yuan Payment Carousel Layout - Educational carousel with Persian/Farsi support

This layout creates Instagram carousel posts in the Yuan Payment style:
- 1:1 aspect ratio (1080×1080 px)
- Red background (#C20000 to #A80000)
- Yellow/white Persian text
- Multiple layout variations
- Support for custom uploaded images and random placeholder images
- Brand elements (logo, footer with pagoda + yuan symbol)
- Supporting icons (FAKE badges, checkmarks, etc.)

Perfect for: Educational carousels, marketing campaigns, brand content
"""

from .base import CarouselLayoutEngine, register_layout
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import List, Tuple, Optional, Dict, Any
import os
import random
import requests
from io import BytesIO


@register_layout
class YuanPaymentCarouselLayout(CarouselLayoutEngine):
    """
    Yuan Payment Carousel Layout - Educational carousel style

    Content Fields:
        - title (required): Main title text (Persian/Farsi)
        - subtitle (optional): Subtitle text
        - body_text (optional): Body content text
        - bullets (optional): List of bullet points

    Assets:
        - hero_image_url (optional): Custom main image
        - logo_url (optional): Brand logo image
        - icon_urls (optional): Dict of icon URLs (fake_badge, checkmark, etc.)

    Options:
        - layout_style: 'centered_portrait', 'symbol_focus', 'product_layout', 
                        'split_screen', 'gradient_background' (default: 'centered_portrait')
        - use_random_image: bool (default: false) - Use random placeholder if no hero_image_url
        - random_image_seed: int - Seed for consistent random images
        - show_slide_number: bool (default: true) - Show slide counter
        - slide_number: int - Current slide number (1-based)
        - total_slides: int - Total slides in carousel
        - show_logo: bool (default: true) - Show logo in top area
        - show_brand_footer: bool (default: true) - Show brand footer
        - title_color: [R, G, B] (default: [255, 215, 0]) - Yellow
        - subtitle_color: [R, G, B] (default: [255, 255, 255]) - White
        - body_text_color: [R, G, B] (default: [255, 255, 255]) - White
        - supporting_icons: List[str] - Icons to display (e.g., ['fake_badge', 'checkmark'])

    Example:
        {
            "layout_type": "yuan_payment_carousel",
            "content": {
                "title": "عنوان اصلی",
                "subtitle": "زیرعنوان",
                "body_text": "متن توضیحات...",
                "bullets": ["نکته اول", "نکته دوم"]
            },
            "assets": {
                "hero_image_url": "https://imageeditor.flowiran.ir/uploads/main/image.png"
            },
            "background": {
                "mode": "solid_color",
                "color": [194, 0, 0]
            },
            "options": {
                "layout_style": "centered_portrait",
                "slide_number": 1,
                "total_slides": 5
            }
        }
    """

    LAYOUT_TYPE = "yuan_payment_carousel"
    LAYOUT_CATEGORY = "carousel_multi_slide"
    DESCRIPTION = "Yuan Payment educational carousel with Persian support"
    SUPPORTS_CAROUSEL = True

    # Square format for carousel
    DEFAULT_WIDTH = 1080
    DEFAULT_HEIGHT = 1080

    REQUIRED_ASSETS = []  # hero_image_url is optional
    OPTIONAL_ASSETS = ["hero_image_url", "logo_url", "icon_urls"]

    def _validate(self):
        """Validate that required content fields are present."""
        if 'title' not in self.content:
            raise ValueError("title is required for yuan_payment_carousel layout")

        if not self.content['title'].strip():
            raise ValueError("title cannot be empty")

    def render(self) -> List[Image.Image]:
        """
        Render the Yuan Payment carousel layout.

        Returns:
            List containing single Image object
        """
        # Force square canvas
        self.canvas_width = 1080
        self.canvas_height = 1080

        # Create base background
        canvas = self._create_background()

        # Get layout style
        layout_style = self.options.get('layout_style', 'centered_portrait')

        # Add logo area (top)
        canvas = self._add_logo_area(canvas)

        # Render based on layout style
        if layout_style == 'centered_portrait':
            canvas = self._render_centered_portrait(canvas)
        elif layout_style == 'symbol_focus':
            canvas = self._render_symbol_focus(canvas)
        elif layout_style == 'product_layout':
            canvas = self._render_product_layout(canvas)
        elif layout_style == 'split_screen':
            canvas = self._render_split_screen(canvas)
        elif layout_style == 'gradient_background':
            canvas = self._render_gradient_background(canvas)
        else:
            # Default to centered portrait
            canvas = self._render_centered_portrait(canvas)

        # Add brand footer (bottom)
        if self.options.get('show_brand_footer', True):
            canvas = self._add_brand_footer(canvas)

        return [canvas]

    def _create_background(self) -> Image.Image:
        """Create red background with optional customization."""
        bg_mode = self.background.get('mode', 'solid_color')
        
        if bg_mode == 'gradient':
            return self._create_gradient_background()
        elif bg_mode == 'image':
            return self._create_image_background()
        else:
            # Default: solid red color
            color = tuple(self.background.get('color', [194, 0, 0]))  # #C20000
            return Image.new('RGB', (self.canvas_width, self.canvas_height), color)

    def _create_gradient_background(self) -> Image.Image:
        """Create gradient background."""
        gradient_config = self.background.get('gradient', {})
        colors = gradient_config.get('colors', [[194, 0, 0], [168, 0, 0]])  # Red gradient
        direction = gradient_config.get('direction', 'vertical')
        
        color1 = tuple(int(c) for c in colors[0])
        color2 = tuple(int(c) for c in colors[1]) if len(colors) > 1 else tuple([168, 0, 0])
        
        img = Image.new('RGB', (self.canvas_width, self.canvas_height))
        draw = ImageDraw.Draw(img)
        
        if direction == 'vertical':
            for y in range(self.canvas_height):
                ratio = y / self.canvas_height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(0, y), (self.canvas_width, y)], fill=(r, g, b))
        else:  # horizontal
            for x in range(self.canvas_width):
                ratio = x / self.canvas_width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(x, 0), (x, self.canvas_height)], fill=(r, g, b))
        
        return img

    def _create_image_background(self) -> Image.Image:
        """Create background from image with optional overlay."""
        image_url = self.background.get('image_url')
        if not image_url:
            return self._create_background()  # Fallback to solid color
        
        try:
            from src.asset_manager import get_asset_manager
            asset_manager = get_asset_manager()
            bg_image = asset_manager.load_asset(image_url, role='background', use_cache=True)
            
            # Fit to canvas (cover mode)
            bg_image = self._fit_image(bg_image, self.canvas_width, self.canvas_height, mode='cover')
            
            # Apply overlay if specified
            overlay_opacity = self.background.get('overlay_opacity', 0.0)
            if overlay_opacity > 0:
                overlay_color = tuple(self.background.get('overlay_color', [194, 0, 0]))
                overlay = Image.new('RGBA', (self.canvas_width, self.canvas_height), 
                                  (*overlay_color, int(overlay_opacity * 255)))
                bg_image = bg_image.convert('RGBA')
                bg_image = Image.alpha_composite(bg_image, overlay)
                return bg_image.convert('RGB')
            
            return bg_image.convert('RGB')
        except Exception as e:
            print(f"⚠️ Warning: Could not load background image: {e}")
            return self._create_background()

    def _add_logo_area(self, canvas: Image.Image) -> Image.Image:
        """Add logo area at top with optional slide number."""
        # Add logo if available
        logo_url = self.assets.get('logo_url', '')
        if self.options.get('show_logo', True) and logo_url and logo_url.strip():
            try:
                from src.asset_manager import get_asset_manager
                asset_manager = get_asset_manager()
                # Add background removal support for logos
                remove_logo_bg = self.options.get('remove_logo_background', False)
                logo_bg_method = self.options.get('logo_bg_removal_method', 'auto')
                logo = asset_manager.load_asset(
                    logo_url.strip(), 
                    role='logo', 
                    use_cache=True,
                    remove_bg=remove_logo_bg,
                    bg_removal_method=logo_bg_method
                )
                
                # Get logo size from options, default to 120
                logo_size = self.options.get('logo_size', 120)
                logo_width = min(logo_size, logo.width)
                logo_aspect = logo.height / logo.width
                logo_height = int(logo_width * logo_aspect)
                logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                
                # Position based on options, default to top-left
                logo_position = self.options.get('logo_position', 'top-left')
                padding = 60
                
                if logo_position == 'top-center':
                    x_pos = (self.canvas_width - logo_width) // 2
                    y_pos = padding
                elif logo_position == 'top-right':
                    x_pos = self.canvas_width - logo_width - padding
                    y_pos = padding
                else:  # top-left (default)
                    x_pos = padding
                    y_pos = padding
                
                if logo.mode == 'RGBA':
                    canvas.paste(logo, (x_pos, y_pos), logo)
                else:
                    canvas.paste(logo, (x_pos, y_pos))
            except Exception as e:
                print(f"⚠️ Warning: Could not load logo: {e}")

        # Add slide number (top-right) - default to False
        if self.options.get('show_slide_number', False):
            slide_num = self.options.get('slide_number', 1)
            total_slides = self.options.get('total_slides', 1)
            canvas = self._add_slide_number(canvas, slide_num, total_slides, position='top-right')

        return canvas

    def _add_slide_number(self, canvas: Image.Image, slide_num: int, 
                         total_slides: int, position: str = 'top-right') -> Image.Image:
        """Add slide number indicator."""
        draw = ImageDraw.Draw(canvas)
        
        # Create slide number text
        text = f"{slide_num}/{total_slides}"
        
        # Get font
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')
            font = ImageFont.truetype(font_path, 32)
        except:
            font = ImageFont.load_default()
        
        # Calculate position
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if position == 'top-right':
            x_pos = self.canvas_width - text_width - 60
            y_pos = 60
        else:
            x_pos = (self.canvas_width - text_width) // 2
            y_pos = 60
        
        # Draw background circle/rectangle for contrast
        padding = 10
        bg_rect = [
            x_pos - padding,
            y_pos - padding,
            x_pos + text_width + padding,
            y_pos + text_height + padding
        ]
        # Create semi-transparent background
        overlay = Image.new('RGBA', (self.canvas_width, self.canvas_height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle(bg_rect, fill=(0, 0, 0, 180), radius=8)
        canvas = Image.alpha_composite(canvas.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(canvas)
        
        # Draw text (white)
        draw.text((x_pos, y_pos), text, font=font, fill=(255, 255, 255))
        
        return canvas

    def _load_main_image(self) -> Optional[Image.Image]:
        """Load main image - either custom or random."""
        hero_url = self.assets.get('hero_image_url')
        use_random = self.options.get('use_random_image', False)
        
        if hero_url and not use_random:
            return self._load_custom_image(hero_url)
        else:
            return self._load_random_image()

    def _load_custom_image(self, url: str) -> Optional[Image.Image]:
        """Load custom uploaded image with background removal support."""
        try:
            from src.asset_manager import get_asset_manager
            asset_manager = get_asset_manager()
            # Read background removal options with proper defaults
            remove_bg = self.options.get('remove_hero_background', False)
            bg_method = self.options.get('bg_removal_method', 'auto')
            
            image = asset_manager.load_asset(
                url,
                role='hero_image',
                remove_bg=remove_bg,
                bg_removal_method=bg_method,
                alpha_matting=self.options.get('alpha_matting', True),
                color_tolerance=self.options.get('color_tolerance', 30)
            )
            if remove_bg:
                print(f"✅ Loaded custom image with background removal: {url} (method: {bg_method})")
            else:
                print(f"✅ Loaded custom image: {url}")
            return image
        except Exception as e:
            print(f"⚠️ Warning: Could not load custom image {url}: {e}")
            return None

    def _load_random_image(self) -> Optional[Image.Image]:
        """Load random placeholder image from picsum.photos."""
        try:
            # Get seed for consistency
            seed = self.options.get('random_image_seed', random.randint(1, 10000))
            
            # Use picsum.photos API
            width = 800
            height = 800
            url = f"https://picsum.photos/{width}/{height}?random={seed}"
            
            print(f"🖼️  Loading random image from picsum.photos (seed: {seed})")
            
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGB')
            
            print(f"✅ Loaded random image successfully")
            return image
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load random image: {e}")
            return None

    def _fit_image(self, image: Image.Image, target_width: int, 
                   target_height: int, mode: str = 'cover') -> Image.Image:
        """Fit image to target dimensions."""
        img_width, img_height = image.size
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height
        
        if mode == 'cover':
            # Fill the space and crop if needed
            if img_ratio > target_ratio:
                # Image is wider - fit to height
                new_height = target_height
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller - fit to width
                new_width = target_width
                new_height = int(new_width / img_ratio)
            
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to target size (center)
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            
            return resized.crop((left, top, right, bottom))
        else:
            # Contain mode - fit inside
            width_ratio = target_width / img_width
            height_ratio = target_height / img_height
            ratio = min(width_ratio, height_ratio)
            
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _render_centered_portrait(self, canvas: Image.Image) -> Image.Image:
        """Render centered portrait layout."""
        # Add title at top with proper spacing
        canvas = self._add_title_section(canvas, y_offset=80)
        
        # Initialize variables - reduced image size to 70%
        img_size = 350  # Reduced from 500 to 70%
        # Calculate y_pos: 80px top padding + ~60px title height + 50px spacing = ~190px
        y_pos = 180
        x_pos = (self.canvas_width - img_size) // 2
        
        # Load and add main image (centered)
        main_image = self._load_main_image()
        if main_image:
            # Adjust image size based on content - make room for text below
            fitted_img = self._fit_image(main_image, img_size, img_size, mode='cover')
            
            if fitted_img.mode == 'RGBA':
                canvas.paste(fitted_img, (x_pos, y_pos), fitted_img)
            else:
                canvas.paste(fitted_img, (x_pos, y_pos))
            
            # Add supporting icons
            supporting_icons = self.options.get('supporting_icons', [])
            if 'fake_badge' in supporting_icons:
                canvas = self._add_icon(canvas, 'fake_badge', x_pos - 80, y_pos + 150)
            if 'checkmark' in supporting_icons:
                canvas = self._add_icon(canvas, 'checkmark', x_pos + img_size + 20, y_pos + 150)
        
        # Add description if provided (below image with 50px spacing)
        description = self.content.get('description', '')
        description_y = None
        if description and main_image:
            description_y = y_pos + img_size + 50  # 50px spacing from image bottom
            canvas = self._add_text_block(canvas, description, 
                                        x=(self.canvas_width - 800) // 2, 
                                        y=description_y, 
                                        max_width=800)
        elif description:
            # If no image, show description in center
            description_y = 300
            canvas = self._add_text_block(canvas, description, 
                                        x=(self.canvas_width - 800) // 2, 
                                        y=description_y, 
                                        max_width=800)
        
        # Add subtitle at bottom with 40px gap from description
        subtitle = self.content.get('subtitle', '')
        if subtitle:
            if description and description_y:
                # Calculate subtitle position: description bottom + 40px gap
                # Estimate description height: ~3-4 lines = ~120-160px
                subtitle_y = description_y + 140 + 40  # Description height estimate + 40px gap
            else:
                subtitle_y = 850
            canvas = self._add_subtitle(canvas, subtitle, y_pos=subtitle_y)
        
        return canvas

    def _render_symbol_focus(self, canvas: Image.Image) -> Image.Image:
        """Render symbol focus layout."""
        # Add title at top
        canvas = self._add_title_section(canvas, y_offset=100)
        
        # Draw large yuan symbol in center (or use icon if available)
        yuan_symbol = self._get_yuan_symbol_image()
        if yuan_symbol:
            symbol_size = 400
            yuan_symbol = yuan_symbol.resize((symbol_size, symbol_size), Image.Resampling.LANCZOS)
            x_pos = (self.canvas_width - symbol_size) // 2
            y_pos = 350
            if yuan_symbol.mode == 'RGBA':
                canvas.paste(yuan_symbol, (x_pos, y_pos), yuan_symbol)
            else:
                canvas.paste(yuan_symbol, (x_pos, y_pos))
        
        # Add text box at bottom
        body_text = self.content.get('body_text', '')
        if body_text:
            canvas = self._add_content_box(canvas, body_text, y_pos=750)
        
        return canvas

    def _render_product_layout(self, canvas: Image.Image) -> Image.Image:
        """Render product layout."""
        # Add title above products
        canvas = self._add_title_section(canvas, y_offset=100)
        
        # Load and add product image
        main_image = self._load_main_image()
        if main_image:
            # Products on white/light background
            product_width = 700
            product_height = 400
            fitted_img = self._fit_image(main_image, product_width, product_height, mode='cover')
            
            x_pos = (self.canvas_width - product_width) // 2
            y_pos = 280
            
            # Create white background box for products
            white_bg = Image.new('RGB', (product_width + 40, product_height + 40), (255, 255, 255))
            canvas.paste(white_bg, (x_pos - 20, y_pos - 20))
            
            if fitted_img.mode == 'RGBA':
                canvas.paste(fitted_img, (x_pos, y_pos), fitted_img)
            else:
                canvas.paste(fitted_img, (x_pos, y_pos))
        
        # Add bullet points below
        bullets = self.content.get('bullets', [])
        if bullets:
            canvas = self._add_bullet_list(canvas, bullets, y_pos=y_pos + 420)
        
        return canvas

    def _render_split_screen(self, canvas: Image.Image) -> Image.Image:
        """Render split screen layout."""
        # Add title at top
        canvas = self._add_title_section(canvas, y_offset=100)
        
        # Split into two columns
        left_width = self.canvas_width // 2
        right_width = self.canvas_width // 2
        
        # Load main image for left side
        main_image = self._load_main_image()
        if main_image:
            left_img = self._fit_image(main_image, left_width - 40, self.canvas_height - 250, mode='cover')
            x_pos = 20
            y_pos = 200
            if left_img.mode == 'RGBA':
                canvas.paste(left_img, (x_pos, y_pos), left_img)
            else:
                canvas.paste(left_img, (x_pos, y_pos))
        
        # Add text on right side
        body_text = self.content.get('body_text', '')
        bullets = self.content.get('bullets', [])
        
        text_x = left_width + 40
        text_y = 200
        max_width = right_width - 80
        
        if body_text:
            canvas = self._add_text_block(canvas, body_text, text_x, text_y, max_width)
            text_y += 150
        
        if bullets:
            canvas = self._add_bullet_list(canvas, bullets, x=text_x, y=text_y, max_width=max_width)
        
        return canvas

    def _render_gradient_background(self, canvas: Image.Image) -> Image.Image:
        """Render gradient background layout."""
        # Create soft gradient background (already done in _create_background if mode is gradient)
        # Add title at top
        canvas = self._add_title_section(canvas, y_offset=100)
        
        # Add bullet list in middle
        bullets = self.content.get('bullets', [])
        if bullets:
            canvas = self._add_bullet_list(canvas, bullets, y_pos=400, max_width=800)
        
        # Optional: Add light image in background
        main_image = self._load_main_image()
        if main_image:
            # Use as subtle background
            bg_img = self._fit_image(main_image, self.canvas_width, self.canvas_height, mode='cover')
            # Make it very subtle
            bg_img = bg_img.convert('RGBA')
            alpha = bg_img.split()[3]
            alpha = alpha.point(lambda p: int(p * 0.2))  # 20% opacity
            bg_img.putalpha(alpha)
            
            # Composite under everything
            canvas_rgba = canvas.convert('RGBA')
            canvas_rgba = Image.alpha_composite(bg_img, canvas_rgba)
            canvas = canvas_rgba.convert('RGB')
        
        return canvas

    def _get_text_color(self, default_color: Tuple[int, int, int], color_type: str = 'title') -> Tuple[int, int, int]:
        """Get text color with support for generic text_color option."""
        # Check for generic text_color option first
        generic_color = self.options.get('text_color')
        if generic_color:
            # Handle string colors
            if isinstance(generic_color, str):
                color_map = {
                    'white': (255, 255, 255),
                    'black': (0, 0, 0),
                    'yellow': (255, 215, 0),
                    'red': (194, 0, 0)
                }
                if generic_color.lower() in color_map:
                    return color_map[generic_color.lower()]
            # Handle RGB array
            elif isinstance(generic_color, (list, tuple)) and len(generic_color) == 3:
                return tuple(int(c) for c in generic_color)
        
        # Fall back to specific color option
        specific_color = self.options.get(f'{color_type}_color', default_color)
        if isinstance(specific_color, (list, tuple)) and len(specific_color) == 3:
            return tuple(int(c) for c in specific_color)
        
        return default_color

    def _add_title_section(self, canvas: Image.Image, y_offset: int = 80) -> Image.Image:
        """Add title text at top."""
        title = self.content.get('title', '')
        if not title:
            return canvas
        
        draw = ImageDraw.Draw(canvas)
        
        # Get font
        is_rtl = self._is_rtl_text(title)
        font_size = 44  # Reduced from 56 for better hierarchy
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            if is_rtl:
                font_path = os.path.join(font_dir, 'IRANYekanBoldFaNum.ttf')
            else:
                font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Prepare text
        if is_rtl:
            title = self._prepare_arabic_text(title)
        
        # Get color - support generic text_color option
        title_color = self._get_text_color([255, 215, 0], 'title')
        
        # Wrap text
        lines = self._wrap_text(title, font, self.canvas_width - 120)
        
        # Draw lines (center-aligned)
        y_pos = y_offset
        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_x = (self.canvas_width - line_width) // 2
            
            draw.text((line_x, y_pos), line, font=font, fill=title_color)
            y_pos += bbox[3] - bbox[1] + 15
        
        return canvas

    def _add_subtitle(self, canvas: Image.Image, subtitle: str, y_pos: int = 850) -> Image.Image:
        """Add subtitle text."""
        draw = ImageDraw.Draw(canvas)
        
        is_rtl = self._is_rtl_text(subtitle)
        font_size = 24  # Reduced from 32 for better hierarchy
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            if is_rtl:
                font_path = os.path.join(font_dir, 'IRANYekanMediumFaNum.ttf')
            else:
                font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        if is_rtl:
            subtitle = self._prepare_arabic_text(subtitle)
        
        subtitle_color = self._get_text_color([255, 255, 255], 'subtitle')
        
        lines = self._wrap_text(subtitle, font, self.canvas_width - 120)
        
        current_y = y_pos
        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_x = (self.canvas_width - line_width) // 2
            
            draw.text((line_x, current_y), line, font=font, fill=subtitle_color)
            current_y += bbox[3] - bbox[1] + 10
        
        return canvas

    def _add_content_box(self, canvas: Image.Image, text: str, y_pos: int = 750) -> Image.Image:
        """Add content box with rounded rectangle."""
        draw = ImageDraw.Draw(canvas)
        
        # Box dimensions
        box_width = self.canvas_width - 120
        box_height = 150
        box_x = 60
        box_y = y_pos
        
        # Draw rounded rectangle background (white/light)
        bg_color = (245, 245, 250)
        draw.rounded_rectangle(
            [(box_x, box_y), (box_x + box_width, box_y + box_height)],
            fill=bg_color,
            radius=15
        )
        
        # Add text inside box
        is_rtl = self._is_rtl_text(text)
        font_size = 28
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            if is_rtl:
                font_path = os.path.join(font_dir, 'IRANYekanRegularFaNum.ttf')
            else:
                font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        if is_rtl:
            text = self._prepare_arabic_text(text)
        
        text_color = self._get_text_color([73, 80, 87], 'body_text')
        
        # Wrap text for box
        lines = self._wrap_text(text, font, box_width - 40)
        
        text_x = box_x + 20
        text_y = box_y + 20
        
        for line in lines:
            draw.text((text_x, text_y), line, font=font, fill=text_color)
            bbox = font.getbbox(line)
            text_y += bbox[3] - bbox[1] + 10
        
        return canvas

    def _add_text_block(self, canvas: Image.Image, text: str, x: int, y: int, max_width: int) -> Image.Image:
        """Add text block at specific position."""
        draw = ImageDraw.Draw(canvas)
        
        is_rtl = self._is_rtl_text(text)
        font_size = 32
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            if is_rtl:
                font_path = os.path.join(font_dir, 'IRANYekanRegularFaNum.ttf')
            else:
                font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        if is_rtl:
            text = self._prepare_arabic_text(text)
        
        text_color = self._get_text_color([255, 255, 255], 'body_text')
        
        lines = self._wrap_text(text, font, max_width)
        
        current_y = y
        for line in lines:
            draw.text((x, current_y), line, font=font, fill=text_color)
            bbox = font.getbbox(line)
            current_y += bbox[3] - bbox[1] + 12
        
        return canvas

    def _add_bullet_list(self, canvas: Image.Image, bullets: List[str], 
                        x: int = None, y: int = None, max_width: int = None, 
                        y_pos: int = None) -> Image.Image:
        """Add bullet point list."""
        if x is None:
            x = 100
        if y is None:
            y = y_pos if y_pos else 400
        if max_width is None:
            max_width = self.canvas_width - 200
        
        draw = ImageDraw.Draw(canvas)
        
        is_rtl = any(self._is_rtl_text(bullet) for bullet in bullets)
        font_size = 28
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            if is_rtl:
                font_path = os.path.join(font_dir, 'IRANYekanRegularFaNum.ttf')
            else:
                font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        bullet_color = self._get_text_color([255, 255, 255], 'body_text')
        bullet_size = 12
        bullet_spacing = 20
        
        current_y = y
        for bullet_text in bullets:
            if is_rtl and self._is_rtl_text(bullet_text):
                display_text = self._prepare_arabic_text(bullet_text)
            else:
                display_text = bullet_text
            
            bbox = font.getbbox(display_text)
            text_height = bbox[3] - bbox[1]
            bullet_center_y = current_y + text_height // 2
            
            # Draw bullet circle
            if is_rtl:
                bullet_x = x + max_width - bullet_size
                text_x = x
            else:
                bullet_x = x
                text_x = x + bullet_size + bullet_spacing
            
            draw.ellipse(
                [bullet_x, bullet_center_y - bullet_size//2, 
                 bullet_x + bullet_size, bullet_center_y + bullet_size//2],
                fill=bullet_color
            )
            
            # Draw text
            draw.text((text_x, current_y), display_text, font=font, fill=bullet_color)
            
            current_y += text_height + 25
        
        return canvas

    def _add_brand_footer(self, canvas: Image.Image) -> Image.Image:
        """Add brand footer at bottom with pagoda + yuan symbol."""
        draw = ImageDraw.Draw(canvas)
        
        footer_height = 100
        footer_y = self.canvas_height - footer_height
        
        # Draw decorative separator line - moved up 40px
        line_y = footer_y - 45  # Moved up from footer_y - 5 to footer_y - 45
        draw.line([(60, line_y), (self.canvas_width - 60, line_y)], fill=(255, 215, 0), width=2)
        
        # Add brand icon if available (pagoda + yuan symbol)
        icon_urls = self.assets.get('icon_urls', {})
        brand_icon_url = icon_urls.get('pagoda_yuan', None) or icon_urls.get('brand_icon', None)
        
        if brand_icon_url:
            try:
                from src.asset_manager import get_asset_manager
                asset_manager = get_asset_manager()
                brand_icon = asset_manager.load_asset(brand_icon_url, role='icon', use_cache=True)
                
                icon_size = 60
                brand_icon = brand_icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                icon_x = (self.canvas_width - icon_size) // 2
                icon_y = footer_y + 20
                
                if brand_icon.mode == 'RGBA':
                    canvas.paste(brand_icon, (icon_x, icon_y), brand_icon)
                else:
                    canvas.paste(brand_icon, (icon_x, icon_y))
            except Exception as e:
                print(f"⚠️ Warning: Could not load brand icon: {e}")
        
        # Add social handles text - make it dynamic and configurable
        social_text = self.options.get('footer_text', "@yuanpayment  |  @yuan-payment")
        if not social_text:
            social_text = "@yuanpayment  |  @yuan-payment"  # Default fallback
        
        try:
            font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'assets', 'fonts')
            font_path = os.path.join(font_dir, 'NotoSans-Regular.ttf')
            font_size = self.options.get('footer_font_size', 24)
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Get footer text color from options
        footer_text_color = self.options.get('footer_text_color', (255, 255, 255))
        if isinstance(footer_text_color, (list, tuple)) and len(footer_text_color) == 3:
            footer_text_color = tuple(int(c) for c in footer_text_color)
        elif isinstance(footer_text_color, str):
            color_map = {
                'white': (255, 255, 255),
                'black': (0, 0, 0),
                'yellow': (255, 215, 0),
                'red': (194, 0, 0)
            }
            footer_text_color = color_map.get(footer_text_color.lower(), (255, 255, 255))
        
        bbox = font.getbbox(social_text)
        text_width = bbox[2] - bbox[0]
        text_x = (self.canvas_width - text_width) // 2
        text_y = footer_y + 10  # Moved up 30px from footer_y + 30 to footer_y + 10
        
        draw.text((text_x, text_y), social_text, font=font, fill=footer_text_color)
        
        return canvas

    def _add_icon(self, canvas: Image.Image, icon_type: str, x: int, y: int) -> Image.Image:
        """Add supporting icon (FAKE badge, checkmark, etc.)."""
        icon_urls = self.assets.get('icon_urls', {})
        icon_url = icon_urls.get(icon_type, None)
        
        if not icon_url:
            # Try to find in assets folder
            icon_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'assets', 'yuan_payment', f'{icon_type}.png'
            )
            if os.path.exists(icon_path):
                icon_url = icon_path
            else:
                return canvas  # No icon available
        
        try:
            from src.asset_manager import get_asset_manager
            asset_manager = get_asset_manager()
            icon = asset_manager.load_asset(icon_url, role='icon', use_cache=True)
            
            icon_size = 80
            icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            
            if icon.mode == 'RGBA':
                canvas.paste(icon, (x, y), icon)
            else:
                canvas.paste(icon, (x, y))
        except Exception as e:
            print(f"⚠️ Warning: Could not load icon {icon_type}: {e}")
        
        return canvas

    def _get_yuan_symbol_image(self) -> Optional[Image.Image]:
        """Get yuan symbol image for symbol focus layout."""
        icon_urls = self.assets.get('icon_urls', {})
        yuan_symbol_url = icon_urls.get('yuan_symbol', None)
        
        if yuan_symbol_url:
            try:
                from src.asset_manager import get_asset_manager
                asset_manager = get_asset_manager()
                return asset_manager.load_asset(yuan_symbol_url, role='icon', use_cache=True)
            except:
                pass
        
        # Try assets folder
        yuan_symbol_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'assets', 'yuan_payment', 'yuan-symbol.png'
        )
        if os.path.exists(yuan_symbol_path):
            try:
                return Image.open(yuan_symbol_path)
            except:
                pass
        
        return None

    def get_schema(self) -> dict:
        """Get JSON schema for this layout."""
        base_schema = super().get_schema()
        base_schema.update({
            "required_content": ["title"],
            "optional_content": ["subtitle", "body_text", "bullets"],
            "optional_assets": ["hero_image_url", "logo_url", "icon_urls"],
            "options": {
                "layout_style": "'centered_portrait' (default), 'symbol_focus', 'product_layout', 'split_screen', 'gradient_background'",
                "use_random_image": "bool (default: false) - Use random placeholder if no hero_image_url",
                "random_image_seed": "int - Seed for consistent random images",
                "show_slide_number": "bool (default: false)",
                "slide_number": "int - Current slide number (1-based)",
                "total_slides": "int - Total slides in carousel",
                "show_logo": "bool (default: true)",
                "show_brand_footer": "bool (default: true)",
                "title_color": "RGB color array (default: [255, 215, 0])",
                "subtitle_color": "RGB color array (default: [255, 255, 255])",
                "body_text_color": "RGB color array (default: [255, 255, 255])",
                "text_color": "string or RGB array - Generic text color override ('white', 'black', 'yellow', 'red', or [R,G,B])",
                "supporting_icons": "List of icon types (e.g., ['fake_badge', 'checkmark'])",
                "footer_text": "string (default: '@yuanpayment  |  @yuan-payment') - Footer social handles text",
                "footer_text_color": "string or RGB array (default: white) - Footer text color",
                "footer_font_size": "int (default: 24) - Footer text font size",
                "remove_hero_background": "bool (default: false) - Remove background from main/hero image",
                "bg_removal_method": "str (default: 'auto') - Background removal method: 'auto', 'edge', 'color'",
                "alpha_matting": "bool (default: true) - Enable alpha matting for better edges",
                "color_tolerance": "int (default: 30) - Color tolerance for color-based removal",
                "remove_logo_background": "bool (default: false) - Remove background from logo",
                "logo_bg_removal_method": "str (default: 'auto') - Logo background removal method"
            }
        })
        return base_schema

