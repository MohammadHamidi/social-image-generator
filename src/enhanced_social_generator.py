from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import json
from typing import Dict, List, Tuple, Optional
import arabic_reshaper
from bidi.algorithm import get_display

# Background removal imports
try:
    from rembg import remove as rembg_remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not installed. Background removal will use basic edge detection.")

import numpy as np
from PIL import ImageOps

class EnhancedSocialImageGenerator:
    def __init__(self, config_path: str = None):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        self.output_dir = os.path.join(self.base_dir, 'output')

        # Enhanced default configuration with advanced color control
        self.config = {
            'canvas_width': 1080,
            'canvas_height': 1350,

            # Background settings
            'background': {
                'type': 'gradient',  # 'solid', 'gradient', 'pattern'
                'primary_color': [255, 100, 100],
                'secondary_color': [255, 150, 150],
                'gradient_direction': 'diagonal',  # 'horizontal', 'vertical', 'diagonal', 'radial'
                'pattern_opacity': 0.3
            },

            # Layout-specific color schemes
            'layout_colors': {
                'hero': {
                    'background_overlay': [0, 0, 0, 180],
                    'text_panel_bg': [0, 0, 0, 200],
                    'headline_color': [255, 255, 255],
                    'subheadline_color': [220, 220, 220],
                    'brand_color': [200, 200, 200]
                },
                'split': {
                    'left_panel_bg': [255, 255, 255, 150],
                    'right_panel_bg': [0, 0, 0, 100],
                    'headline_color': [50, 50, 50],
                    'subheadline_color': [80, 80, 80],
                    'brand_color': [255, 255, 255]
                },
                'top_heavy': {
                    'top_panel_bg': [255, 255, 255, 180],
                    'bottom_panel_bg': [0, 0, 0, 50],
                    'headline_color': [50, 50, 50],
                    'subheadline_color': [80, 80, 80],
                    'brand_color': [255, 255, 255]
                },
                'bottom_heavy': {
                    'top_panel_bg': [0, 0, 0, 150],
                    'bottom_panel_bg': [255, 255, 255, 200],
                    'headline_color': [255, 255, 255],
                    'subheadline_color': [220, 220, 220],
                    'brand_color': [100, 100, 100]
                }
            },

            # Coat/content colors
            'coat_colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'coat_count': 5,

            # Font settings
            'fonts': {
                'headline_size': 48,
                'subheadline_size': 32,
                'brand_size': 24
            },

            # Custom image settings with background removal
            'custom_images': {
                'use_custom_images': False,
                'main_image_path': 'assets/custom/main_section.png',
                'blueprint_image_path': 'assets/custom/blueprint.png',
                'main_image_size': [500, 500],
                'blueprint_image_size': [178, 108],
                'main_image_position': [290, 450],
                'blueprint_image_position': [451, 300],
                'remove_background': True,
                'background_removal_method': 'auto',  # 'auto', 'edge_detection', 'color_threshold'
                'edge_threshold': 50,
                'color_tolerance': 30
            }
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self._deep_merge_config(self.config, user_config)

        self._load_fonts()
        self._load_custom_images()

    def _deep_merge_config(self, base: dict, update: dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge_config(base[key], value)
            else:
                base[key] = value

    def _load_fonts(self):
        """Load required fonts with improved font finding"""
        font_dir = os.path.join(self.assets_dir, 'fonts')

        # Arabic font paths
        arabic_font_paths = [
            '/System/Library/Fonts/SFArabic.ttf',
            '/System/Library/Fonts/SFArabicRounded.ttf',
            '/System/Library/Fonts/ArialHB.ttc',
            '/System/Library/Fonts/Arial.ttf',
            os.path.join(font_dir, 'NotoSansArabic-Bold.ttf'),
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        ]

        self.fonts = {}

        # Load Arabic font
        for path in arabic_font_paths:
            if os.path.exists(path):
                try:
                    self.fonts['headline'] = ImageFont.truetype(path, self.config['fonts']['headline_size'])
                    self.fonts['subheadline'] = ImageFont.truetype(path, self.config['fonts']['subheadline_size'])
                    break
                except Exception:
                    continue

        if 'headline' not in self.fonts:
            self.fonts['headline'] = ImageFont.load_default()
            self.fonts['subheadline'] = ImageFont.load_default()

        # Load brand font
        try:
            self.fonts['brand'] = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.config['fonts']['brand_size'])
        except:
            self.fonts['brand'] = ImageFont.load_default()

    def _remove_background_auto(self, image: Image.Image) -> Image.Image:
        """Remove background using rembg (AI-based)"""
        if not REMBG_AVAILABLE:
            return self._remove_background_edge_detection(image)

        try:
            # Convert to bytes
            import io
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Remove background
            result_bytes = rembg_remove(img_byte_arr)
            result_image = Image.open(io.BytesIO(result_bytes)).convert('RGBA')
            return result_image
        except Exception as e:
            print(f"rembg failed, falling back to edge detection: {e}")
            return self._remove_background_edge_detection(image)

    def _remove_background_edge_detection(self, image: Image.Image) -> Image.Image:
        """Remove background using edge detection"""
        # Convert to RGBA
        img = image.convert('RGBA')
        data = np.array(img)

        # Get the corner color as background color (most common approach)
        bg_color = data[0, 0][:3]  # Top-left corner

        # Create mask based on color similarity
        threshold = self.config['custom_images']['edge_threshold']
        diff = np.sqrt(np.sum((data[:, :, :3] - bg_color) ** 2, axis=2))
        mask = diff > threshold

        # Apply mask to alpha channel
        data[:, :, 3] = mask * 255

        return Image.fromarray(data, 'RGBA')

    def _remove_background_color_threshold(self, image: Image.Image) -> Image.Image:
        """Remove background using color threshold"""
        img = image.convert('RGBA')
        data = np.array(img)

        # Assume white background (most common)
        white_bg = np.array([255, 255, 255])
        tolerance = self.config['custom_images']['color_tolerance']

        # Create mask
        diff = np.sqrt(np.sum((data[:, :, :3] - white_bg) ** 2, axis=2))
        mask = diff > tolerance

        # Apply mask
        data[:, :, 3] = mask * 255

        return Image.fromarray(data, 'RGBA')

    def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background from image using specified method"""
        if not self.config['custom_images']['remove_background']:
            return image.convert('RGBA')

        method = self.config['custom_images']['background_removal_method']

        if method == 'auto':
            return self._remove_background_auto(image)
        elif method == 'edge_detection':
            return self._remove_background_edge_detection(image)
        elif method == 'color_threshold':
            return self._remove_background_color_threshold(image)
        else:
            return self._remove_background_auto(image)

    def _load_custom_images(self):
        """Load and process custom images with background removal"""
        self.main_image = None
        self.blueprint_image = None

        if self.config.get('use_custom_images', False):
            # Load main image
            main_image_path = self.config['custom_images'].get('main_image_path')
            if main_image_path and os.path.exists(main_image_path):
                try:
                    raw_image = Image.open(main_image_path).convert('RGBA')
                    self.main_image = self._remove_background(raw_image)
                    print(f"✅ Loaded and processed main image: {main_image_path}")
                except Exception as e:
                    print(f"❌ Failed to load main image: {e}")
            else:
                print(f"❌ Main image path not found: {main_image_path}")

            # Load blueprint/watermark image
            blueprint_image_path = self.config['custom_images'].get('blueprint_image_path')
            if blueprint_image_path and os.path.exists(blueprint_image_path):
                try:
                    raw_image = Image.open(blueprint_image_path).convert('RGBA')
                    self.blueprint_image = self._remove_background(raw_image)
                    print(f"✅ Loaded and processed blueprint image: {blueprint_image_path}")
                except Exception as e:
                    print(f"❌ Failed to load blueprint image: {e}")
            else:
                print(f"❌ Blueprint image path not found: {blueprint_image_path}")

    def _create_enhanced_background(self) -> Image.Image:
        """Create enhanced background with gradient/pattern support"""
        bg_config = self.config['background']
        width, height = self.config['canvas_width'], self.config['canvas_height']

        if bg_config['type'] == 'solid':
            color = tuple(bg_config['primary_color'])
            return Image.new('RGB', (width, height), color)

        elif bg_config['type'] == 'gradient':
            return self._create_gradient_background()

        elif bg_config['type'] == 'pattern':
            return self._create_pattern_background()

        else:
            # Default to gradient
            return self._create_gradient_background()

    def _create_gradient_background(self) -> Image.Image:
        """Create gradient background"""
        bg_config = self.config['background']
        width, height = self.config['canvas_width'], self.config['canvas_height']

        color1 = tuple(bg_config['primary_color'])
        color2 = tuple(bg_config['secondary_color'])
        direction = bg_config['gradient_direction']

        # Create base image
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        if direction == 'horizontal':
            for x in range(width):
                ratio = x / width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        elif direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        elif direction == 'diagonal':
            for y in range(height):
                for x in range(width):
                    ratio = (x + y) / (width + height)
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    draw.point((x, y), fill=(r, g, b))

        elif direction == 'radial':
            center_x, center_y = width // 2, height // 2
            max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5

            for y in range(height):
                for x in range(width):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    ratio = min(distance / max_distance, 1.0)
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    draw.point((x, y), fill=(r, g, b))

        return img

    def _create_pattern_background(self) -> Image.Image:
        """Create pattern-based background"""
        # First create gradient base
        img = self._create_gradient_background()

        # Add pattern overlay
        pattern_path = os.path.join(self.assets_dir, 'backgrounds', 'swirly_pattern.png')

        if os.path.exists(pattern_path):
            pattern = Image.open(pattern_path)
            pattern = pattern.resize((self.config['canvas_width'], self.config['canvas_height']))
            pattern = pattern.convert('L').convert('RGB')

            # Blend with base
            opacity = self.config['background']['pattern_opacity']
            img = Image.blend(img, pattern, opacity)

        return img

    def _prepare_arabic_text(self, text: str) -> str:
        """Prepare Arabic/Farsi text for proper display"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        except:
            return text

    def _draw_enhanced_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                           position: Tuple[int, int], color: Tuple[int, int, int],
                           bg_color: Optional[Tuple[int, int, int, int]] = None,
                           centered: bool = True) -> Tuple[int, int]:
        """Draw text with enhanced styling options"""
        draw = ImageDraw.Draw(img)

        # Prepare text for Arabic/Farsi
        display_text = self._prepare_arabic_text(text)

        # Get text dimensions
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = position

        # Center text if requested
        if centered:
            x = x - text_width // 2

        # NO BACKGROUND PANELS - Draw text directly on background
        # Background panels removed for clean, minimal design

        # Draw text
        text_color = tuple(color) if isinstance(color, list) else color
        draw.text((x, y), display_text, font=font, fill=text_color)

        return text_width, text_height

    def generate_enhanced_hero_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate enhanced hero layout with advanced color control"""
        img = self._create_enhanced_background()
        colors = self.config['layout_colors']['hero']

        # Use custom images if available and enabled
        if self.config['custom_images']['use_custom_images']:
            # Draw main image (with background removed)
            if self.main_image:
                main_size = tuple(self.config['custom_images']['main_image_size'])
                main_pos = tuple(self.config['custom_images']['main_image_position'])
                resized_main = self.main_image.resize(main_size, Image.Resampling.LANCZOS)
                img.paste(resized_main, main_pos, resized_main)

            # Draw blueprint/watermark image (with background removed)
            if self.blueprint_image:
                blueprint_size = tuple(self.config['custom_images']['blueprint_image_size'])
                blueprint_pos = tuple(self.config['custom_images']['blueprint_image_position'])
                resized_blueprint = self.blueprint_image.resize(blueprint_size, Image.Resampling.LANCZOS)
                img.paste(resized_blueprint, blueprint_pos, resized_blueprint)
        else:
            # Draw programmatic coats
            self._draw_enhanced_coats(img, 150, 450, img.width - 300, 200)

        # Draw text elements WITHOUT background panels for clean, minimal design
        # Headline - positioned at top, white text on background
        headline_y = 120
        headline_color = (255, 255, 255)  # White text for clean look
        self._draw_enhanced_text(img, headline, self.fonts['headline'],
                                (img.width // 2, headline_y),
                                headline_color,
                                None,  # No background
                                centered=True)

        # Subheadline - below headline
        subheadline_y = headline_y + 80
        subheadline_color = (255, 255, 255)  # White text for consistency
        self._draw_enhanced_text(img, subheadline, self.fonts['subheadline'],
                                (img.width // 2, subheadline_y),
                                subheadline_color,
                                None,  # No background
                                centered=True)

        # Brand - at bottom
        if brand:
            brand_color = (255, 255, 255)  # White text for brand
            self._draw_enhanced_text(img, brand, self.fonts['brand'],
                                    (img.width // 2, img.height - 100),
                                    brand_color,
                                    None,  # No background
                                    centered=True)

        return img

    def _draw_enhanced_coats(self, img: Image.Image, x: int, y: int, width: int, height: int):
        """Draw enhanced coats with better styling"""
        draw = ImageDraw.Draw(img)
        coat_width = width // self.config['coat_count']
        coat_height = height

        for i in range(self.config['coat_count']):
            color = self.config['coat_colors'][i % len(self.config['coat_colors'])]

            coat_x = x + i * coat_width + 5
            coat_y = y

            # Draw coat with shadow effect
            shadow_offset = 3
            # Shadow
            draw.rectangle([coat_x + shadow_offset, coat_y + shadow_offset,
                           coat_x + coat_width - 10 + shadow_offset, coat_y + coat_height + shadow_offset],
                          fill=(0, 0, 0, 50))
            # Main coat
            draw.rectangle([coat_x, coat_y, coat_x + coat_width - 10, coat_y + coat_height],
                          fill=color, outline='white', width=2)
