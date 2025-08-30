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
    print("✅ rembg AI background removal available!")
except ImportError:
    REMBG_AVAILABLE = False
    print("⚠️  rembg not available, using basic edge detection for background removal")

# Also try to import onnxruntime for better rembg performance
try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
    print("✅ ONNX Runtime available for optimized rembg performance")
except ImportError:
    ONNX_AVAILABLE = False
    print("ℹ️  ONNX Runtime not available, using standard rembg performance")

import numpy as np
from PIL import ImageOps

# Try to import scipy for advanced image processing
try:
    from scipy import ndimage
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available. Using simplified background removal.")

class EnhancedSocialImageGenerator:
    """
    Enhanced Social Media Image Generator with AI-powered background removal
    and dynamic layout positioning for professional social media content.

    This class provides a comprehensive solution for generating high-quality social media
    images with features including:
    - AI-powered background removal using rembg
    - Dynamic layout positioning based on content size
    - Multi-language text support (English, Arabic, Farsi)
    - Professional typography with custom fonts
    - Aspect ratio preservation for images
    - Collision avoidance for optimal element placement
    - Platform-specific configurations (Instagram, Facebook, etc.)

    Attributes:
        config (dict): Configuration dictionary loaded from JSON file
        main_image (PIL.Image): Main product/service image with background removed
        blueprint_image (PIL.Image): Brand logo/watermark image
        background_image (PIL.Image): Background image for the canvas
        fonts (dict): Dictionary of loaded fonts for different text types

    Example:
        >>> generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
        >>> img = generator.generate_improved_hero_layout(
        ...     "Premium Collection",
        ...     "Exceptional Quality & Design",
        ...     "Fashion Store"
        ... )
        >>> img.save('output/social_post.png', 'PNG')
    """

    def __init__(self, config_path: str = None):
        """
        Initialize the Enhanced Social Media Image Generator.

        Args:
            config_path (str, optional): Path to JSON configuration file.
                If None, uses default configuration. Defaults to None.

        Raises:
            FileNotFoundError: If config_path is provided but file doesn't exist.
            json.JSONDecodeError: If config file contains invalid JSON.

        Example:
            >>> # Using default config
            >>> generator = EnhancedSocialImageGenerator()
            >>>
            >>> # Using custom config
            >>> generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
        """
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

    def _resolve_image_path(self, path: str) -> str:
        """Resolve image path - handle both absolute and relative paths"""
        if not path:
            return ""
        
        # If it's already an absolute path and exists, use it directly
        if os.path.isabs(path) and os.path.exists(path):
            return path
        
        # Try relative to base directory
        relative_path = os.path.join(self.base_dir, path)
        if os.path.exists(relative_path):
            return relative_path
        
        # Try the path as-is
        if os.path.exists(path):
            return path
        
        # Return empty string if not found
        return ""

    def _load_fonts(self):
        """Load fonts with Docker-compatible bundled font system"""
        font_dir = os.path.join(self.assets_dir, 'fonts')

        # Font loading priority: bundled fonts -> system fonts -> default
        font_sets = {
            'arabic': {
                'bundled': [
                    os.path.join(font_dir, 'NotoSansArabic-Bold.ttf'),
                    os.path.join(font_dir, 'NotoSansArabic-Regular.ttf'),
                    os.path.join(font_dir, 'NotoSans-Bold.ttf'),  # Fallback to Latin
                    os.path.join(font_dir, 'NotoSans-Regular.ttf')
                ],
                'system': [
                    '/System/Library/Fonts/SFArabic.ttf',  # macOS
                    '/System/Library/Fonts/SFArabicRounded.ttf',  # macOS
                    '/System/Library/Fonts/ArialHB.ttc',  # macOS
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
                    '/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'  # Linux
                ]
            },
            'latin': {
                'bundled': [
                    os.path.join(font_dir, 'NotoSans-Bold.ttf'),
                    os.path.join(font_dir, 'NotoSans-Regular.ttf'),
                    os.path.join(font_dir, 'Inter-Bold.ttf'),
                    os.path.join(font_dir, 'Inter-Regular.ttf')
                ],
                'system': [
                    '/System/Library/Fonts/Helvetica.ttc',  # macOS
                    '/System/Library/Fonts/Arial.ttf',  # macOS
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
                    '/usr/share/fonts/TTF/arial.ttf'  # Linux
                ]
            }
        }

        self.fonts = {}

        # Load fonts with priority system
        self._load_font_category('headline', font_sets['arabic'], self.config['fonts']['headline_size'])
        self._load_font_category('subheadline', font_sets['arabic'], self.config['fonts']['subheadline_size'])
        self._load_font_category('brand', font_sets['latin'], self.config['fonts']['brand_size'])

        # Ensure all fonts are loaded (fallback to default if needed)
        for font_name in ['headline', 'subheadline', 'brand']:
            if font_name not in self.fonts:
                print(f"⚠️  Using default font for {font_name}")
                self.fonts[font_name] = ImageFont.load_default()

        print(f"✅ Fonts loaded: {list(self.fonts.keys())}")

    def _load_font_category(self, font_name: str, font_set: dict, size: int):
        """Load a specific font category with fallback system"""
        # Try bundled fonts first
        for font_path in font_set['bundled']:
            if os.path.exists(font_path):
                try:
                    self.fonts[font_name] = ImageFont.truetype(font_path, size)
                    print(f"✅ Loaded bundled font for {font_name}: {os.path.basename(font_path)}")
                    return
                except Exception as e:
                    print(f"⚠️  Failed to load bundled font {font_path}: {e}")
                    continue

        # Try system fonts as fallback
        for font_path in font_set['system']:
            if os.path.exists(font_path):
                try:
                    self.fonts[font_name] = ImageFont.truetype(font_path, size)
                    print(f"✅ Loaded system font for {font_name}: {os.path.basename(font_path)}")
                    return
                except Exception as e:
                    print(f"⚠️  Failed to load system font {font_path}: {e}")
                    continue

        # If no fonts loaded, will use default (handled in main function)

    def _remove_background_auto(self, image: Image.Image) -> Image.Image:
        """Remove background using rembg (AI-based) with fallback to enhanced edge detection"""
        if not REMBG_AVAILABLE:
            print("⚠️  rembg not available, using enhanced edge detection")
            return self._remove_background_edge_detection(image)

        try:
            print("🤖 Using rembg AI for professional background removal...")

            # Convert to bytes
            import io
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Use rembg with optimized settings
            # rembg automatically handles different image types and provides excellent results
            result_bytes = rembg_remove(
                img_byte_arr,
                # Use the best available model
                session=None,  # Auto-select best model
                # Additional options for quality
                alpha_matting=True,  # Better edge quality
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )

            result_image = Image.open(io.BytesIO(result_bytes)).convert('RGBA')

            # Verify the result is valid
            if result_image.size[0] > 0 and result_image.size[1] > 0:
                # Check if we have meaningful transparency
                alpha = result_image.split()[-1]
                alpha_stats = alpha.getextrema()
                has_transparency = alpha_stats[0] < 255

                if has_transparency:
                    print("✅ rembg AI background removal successful!")
                    print(f"   Alpha range: {alpha_stats}")

                    # Calculate foreground percentage
                    import numpy as np
                    alpha_array = np.array(alpha)
                    total_pixels = alpha_array.size
                    transparent_pixels = np.sum(alpha_array == 0)
                    opaque_pixels = total_pixels - transparent_pixels
                    opaque_ratio = opaque_pixels / total_pixels
                    print(f"   Opaque ratio: {opaque_ratio:.1%}")
                    return result_image
                else:
                    print("⚠️  rembg completed but no transparency detected, using enhanced edge detection")
                    return self._remove_background_edge_detection(image)
            else:
                print("⚠️  rembg returned invalid image, using enhanced edge detection")
                return self._remove_background_edge_detection(image)

        except Exception as e:
            print(f"❌ rembg failed ({e}), using enhanced edge detection")
            return self._remove_background_edge_detection(image)

    def _remove_background_edge_detection(self, image: Image.Image) -> Image.Image:
        """Remove background using enhanced edge detection with multiple strategies"""
        # Convert to RGBA
        img = image.convert('RGBA')
        data = np.array(img)

        # Get background removal mode from config
        removal_mode = self.config['custom_images'].get('background_removal_mode', 'enhanced')

        print(f"🎨 Using enhanced background removal mode: {removal_mode}")

        # Strategy 1: Multi-sample background detection
        corners = [
            data[0, 0][:3],      # Top-left
            data[0, -1][:3],     # Top-right
            data[-1, 0][:3],     # Bottom-left
            data[-1, -1][:3],    # Bottom-right
            data[10, 10][:3],    # Near top-left (avoid borders)
            data[10, -11][:3],   # Near top-right
            data[-11, 10][:3],   # Near bottom-left
            data[-11, -11][:3]   # Near bottom-right
        ]

        # Remove outliers and get robust background color
        corner_colors = np.array(corners)
        mean_color = np.mean(corner_colors, axis=0)
        std_color = np.std(corner_colors, axis=0)

        # Use robust background color (exclude outliers)
        valid_corners = []
        for corner in corners:
            if np.all(np.abs(corner - mean_color) < 2 * std_color):
                valid_corners.append(corner)

        if valid_corners:
            bg_color = np.mean(valid_corners, axis=0).astype(int)
        else:
            bg_color = mean_color.astype(int)

        print(f"   Detected background color: {bg_color}")

        # Strategy 2: Adaptive thresholding based on image characteristics
        color_variance = np.var(data[:, :, :3])
        brightness = np.mean(data[:, :, :3])

        # Adjust threshold based on image properties
        base_threshold = max(25, min(80, color_variance / 200))

        if removal_mode == 'aggressive':
            threshold = base_threshold * 0.6  # More aggressive
            min_foreground_ratio = 0.08
        elif removal_mode == 'conservative':
            threshold = base_threshold * 1.4  # More conservative
            min_foreground_ratio = 0.25
        else:  # 'enhanced' or 'smart'
            threshold = base_threshold
            min_foreground_ratio = 0.12

        print(f"   Adaptive threshold: {threshold:.1f}")
        print(f"   Minimum foreground ratio: {min_foreground_ratio}")

        # Strategy 3: Enhanced color difference calculation
        diff = np.sqrt(np.sum((data[:, :, :3] - bg_color) ** 2, axis=2))

        # Apply Gaussian blur to reduce noise
        if SCIPY_AVAILABLE:
            from scipy import ndimage
            diff = ndimage.gaussian_filter(diff, sigma=0.5)

        # Strategy 4: Multi-level masking
        # Primary mask
        primary_mask = diff > threshold

        # Secondary mask with lower threshold for edge refinement
        secondary_mask = diff > (threshold * 0.7)

        # Combine masks intelligently
        mask = primary_mask.copy()

        # Refine edges using secondary mask
        edge_pixels = primary_mask & ~secondary_mask
        if np.any(edge_pixels):
            # Soften edges
            mask = secondary_mask

        # Strategy 5: Morphological cleanup
        if SCIPY_AVAILABLE:
            # Close small holes
            mask = ndimage.binary_closing(mask, structure=np.ones((2,2)))
            # Remove small noise
            mask = ndimage.binary_opening(mask, structure=np.ones((2,2)))
            # Fill larger holes
            mask = ndimage.binary_fill_holes(mask)
        else:
            print("   Using simplified cleanup (scipy not available)")

        # Strategy 6: Quality assessment and fallback
        foreground_pixels = np.sum(mask)
        total_pixels = mask.size
        foreground_ratio = foreground_pixels / total_pixels

        print(f"   Final foreground ratio: {foreground_ratio:.2f} ({foreground_pixels}/{total_pixels} pixels)")

        # Quality checks
        if foreground_ratio < min_foreground_ratio:
            print(f"⚠️  Insufficient foreground detected ({foreground_ratio:.2f})")

            # Try progressive relaxation
            for relax_factor in [0.8, 0.6, 0.4]:
                relaxed_threshold = threshold * relax_factor
                relaxed_mask = diff > relaxed_threshold

                if SCIPY_AVAILABLE:
                    relaxed_mask = ndimage.binary_closing(relaxed_mask, structure=np.ones((2,2)))
                    relaxed_mask = ndimage.binary_fill_holes(relaxed_mask)

                relaxed_foreground = np.sum(relaxed_mask)
                relaxed_ratio = relaxed_foreground / total_pixels

                if relaxed_ratio >= min_foreground_ratio:
                    print(f"   Using relaxed threshold: {relaxed_threshold:.1f} (ratio: {relaxed_ratio:.2f})")
                    mask = relaxed_mask
                    foreground_ratio = relaxed_ratio
                    break

            # Final fallback
            if foreground_ratio < min_foreground_ratio:
                print("   ⚠️  Unable to achieve good background removal, keeping original image")
                return img

        # Apply final mask
        data[:, :, 3] = mask.astype(np.uint8) * 255

        print(f"✅ Enhanced background removal completed - {foreground_ratio:.2f} foreground retained")
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

    def _remove_background(self, image: Image.Image, is_watermark: bool = False) -> Image.Image:
        """Remove background from image using specified method"""
        # For watermarks that are already transparent, preserve transparency
        if is_watermark and image.mode == 'RGBA':
            # Check if image already has transparency
            alpha_channel = image.split()[-1]
            if alpha_channel.getextrema()[0] < 255:  # Has some transparency
                print("✅ Watermark already has transparency, preserving it")
                return image

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
        self.background_image = None

        # Check both possible locations for use_custom_images
        use_custom_images = (
            self.config.get('use_custom_images', False) or 
            self.config.get('custom_images', {}).get('use_custom_images', False)
        )
        
        if use_custom_images:
            print("🖼️ Loading custom images...")
            
            # Load main image
            main_image_path = self.config['custom_images'].get('main_image_path')
            if main_image_path:
                resolved_main_path = self._resolve_image_path(main_image_path)
                if resolved_main_path and os.path.exists(resolved_main_path):
                    try:
                        print(f"📂 Loading main image from: {resolved_main_path}")
                        raw_image = Image.open(resolved_main_path).convert('RGBA')
                        self.main_image = self._remove_background(raw_image)
                        print(f"✅ Main image loaded and processed successfully")
                        print(f"   Size: {self.main_image.size}, Mode: {self.main_image.mode}")
                    except Exception as e:
                        print(f"❌ Failed to load main image: {e}")
                        self.main_image = None
                else:
                    print(f"❌ Main image not found: {main_image_path}")
                    print(f"   Resolved path: {resolved_main_path}")

            # Load blueprint/watermark image
            blueprint_image_path = self.config['custom_images'].get('blueprint_image_path')
            if blueprint_image_path:
                resolved_blueprint_path = self._resolve_image_path(blueprint_image_path)
                if resolved_blueprint_path and os.path.exists(resolved_blueprint_path):
                    try:
                        print(f"📂 Loading blueprint image from: {resolved_blueprint_path}")
                        raw_image = Image.open(resolved_blueprint_path).convert('RGBA')
                        self.blueprint_image = self._remove_background(raw_image, is_watermark=True)
                        print(f"✅ Blueprint image loaded and processed successfully")
                        print(f"   Size: {self.blueprint_image.size}, Mode: {self.blueprint_image.mode}")
                    except Exception as e:
                        print(f"❌ Failed to load blueprint image: {e}")
                        self.blueprint_image = None
                else:
                    print(f"❌ Blueprint image not found: {blueprint_image_path}")
                    print(f"   Resolved path: {resolved_blueprint_path}")

            # Load background image if specified
            background_image_path = self.config['custom_images'].get('background_image_path')
            if background_image_path:
                resolved_background_path = self._resolve_image_path(background_image_path)
                if resolved_background_path and os.path.exists(resolved_background_path):
                    try:
                        print(f"📂 Loading background image from: {resolved_background_path}")
                        raw_image = Image.open(resolved_background_path).convert('RGB')
                        # Resize to canvas size
                        self.background_image = raw_image.resize(
                            (self.config['canvas_width'], self.config['canvas_height']), 
                            Image.Resampling.LANCZOS
                        )
                        print(f"✅ Background image loaded and processed successfully")
                        print(f"   Size: {self.background_image.size}, Mode: {self.background_image.mode}")
                    except Exception as e:
                        print(f"❌ Failed to load background image: {e}")
                        self.background_image = None
                else:
                    print(f"❌ Background image not found: {background_image_path}")

            # Summary
            images_loaded = sum([bool(self.main_image), bool(self.blueprint_image), bool(self.background_image)])
            print(f"📊 Custom images summary: {images_loaded} images loaded successfully")

        else:
            print("📝 Custom images disabled in config")

    def _create_enhanced_background(self) -> Image.Image:
        """Create enhanced background with gradient/pattern support"""
        # Use custom background image if available
        if self.background_image:
            print("🖼️ Using custom background image")
            return self.background_image.copy()

        bg_config = self.config.get('background', {})
        width, height = self.config['canvas_width'], self.config['canvas_height']

        bg_type = bg_config.get('type', 'gradient')

        if bg_type == 'solid':
            color = tuple(bg_config.get('primary_color', [255, 100, 100]))
            return Image.new('RGB', (width, height), color)

        elif bg_type == 'gradient':
            return self._create_gradient_background()

        elif bg_type == 'pattern':
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

    def _get_font_for_text(self, text: str, font_type: str) -> ImageFont.ImageFont:
        """Get the appropriate font for text content"""
        is_arabic = self._is_arabic_text(text)

        font_dir = os.path.join(self.assets_dir, 'fonts')

        if font_type in ['headline', 'subheadline']:
            if is_arabic:
                # Use Arabic font for Arabic text
                arabic_font_path = os.path.join(font_dir, 'NotoSansArabic-Bold.ttf')
                if os.path.exists(arabic_font_path):
                    try:
                        font_size = self.config['fonts'][f'{font_type}_size']
                        return ImageFont.truetype(arabic_font_path, font_size)
                    except:
                        pass

            # Use Latin font for Latin text or as fallback
            latin_font_path = os.path.join(font_dir, 'NotoSans-Bold.ttf')
            if os.path.exists(latin_font_path):
                try:
                    font_size = self.config['fonts'][f'{font_type}_size']
                    return ImageFont.truetype(latin_font_path, font_size)
                except:
                    pass

        # For brand or other font types, use existing logic
        if font_type in self.fonts:
            return self.fonts[font_type]

        # Fallback to default
        return ImageFont.load_default()

    def _resize_image_with_aspect_ratio(self, image: Image.Image, max_width: int,
                                       max_height: int, preserve_aspect_ratio: bool = True) -> Image.Image:
        """Resize image while optionally preserving aspect ratio"""
        if not preserve_aspect_ratio:
            return image.resize((max_width, max_height), Image.Resampling.LANCZOS)

        # Calculate aspect ratios
        original_width, original_height = image.size
        original_aspect = original_width / original_height
        target_aspect = max_width / max_height

        if original_aspect > target_aspect:
            # Image is wider than target - fit to width
            new_width = max_width
            new_height = int(max_width / original_aspect)
        else:
            # Image is taller than target - fit to height
            new_height = max_height
            new_width = int(max_height * original_aspect)

        # Ensure we don't exceed the maximum dimensions
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width / original_aspect)

        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * original_aspect)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _calculate_image_position_with_aspect_ratio(self, image_size: tuple,
                                                   canvas_size: tuple,
                                                   original_position: tuple,
                                                   alignment: str = 'center') -> tuple:
        """Calculate optimal position for image with preserved aspect ratio"""
        image_width, image_height = image_size
        canvas_width, canvas_height = canvas_size

        # Default to center positioning if no specific position given
        if original_position == (0, 0):
            x = (canvas_width - image_width) // 2
            y = (canvas_height - image_height) // 2
            return (x, y)

        # Use original position but adjust if image would go off-canvas
        x, y = original_position

        # Ensure image stays within canvas bounds
        if x + image_width > canvas_width:
            x = canvas_width - image_width
        if y + image_height > canvas_height:
            y = canvas_height - image_height

        # Ensure minimum margins
        x = max(20, x)  # Minimum 20px from left
        y = max(20, y)  # Minimum 20px from top

        return (x, y)
    
    def _is_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic/Persian characters"""
        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        import re
        return bool(re.search(arabic_pattern, text))
    
    def _format_quote_text(self, quote: str, is_arabic: bool = None) -> str:
        """Format quote with proper quotation marks based on language"""
        if is_arabic is None:
            is_arabic = self._is_arabic_text(quote)
        
        if is_arabic:
            # For Arabic, apply quotes to the ORIGINAL text, then process
            rtl_settings = self.config.get('rtl_settings', {})
            open_quote = rtl_settings.get('quote_marks', {}).get('open', '«')
            close_quote = rtl_settings.get('quote_marks', {}).get('close', '»')
            quoted_text = f"{open_quote}{quote}{close_quote}"
            # Process the quoted text for proper display
            return self._prepare_arabic_text(quoted_text)
        else:
            # Use proper typographic quotes for Latin text
            return f'"{quote}"'
    
    def _format_attribution(self, author: str, is_arabic: bool = None) -> str:
        """Format author attribution with proper punctuation"""
        if is_arabic is None:
            is_arabic = self._is_arabic_text(author)
        
        rtl_settings = self.config.get('rtl_settings', {})
        prefix = rtl_settings.get('attribution_prefix', '—')
        
        if is_arabic:
            # For Arabic: prefix + space + author
            return f"{prefix} {author}"
        else:
            # For Latin: em-dash + space + author
            return f"— {author}"
    
    def _get_max_text_width(self) -> int:
        """Get maximum text width based on design system"""
        design_system = self.config.get('design_system', {})
        grid = design_system.get('grid', {})
        return grid.get('max_text_width', 780)
    
    def _get_safe_margins(self) -> dict:
        """Get safe area margins"""
        design_system = self.config.get('design_system', {})
        grid = design_system.get('grid', {})
        return {
            'bottom': grid.get('safe_area_bottom', 64),
            'sides': grid.get('safe_area_sides', 60)
        }
    
    def _get_spacing(self, type: str) -> int:
        """Get spacing value from design system"""
        design_system = self.config.get('design_system', {})
        typography = design_system.get('typography', {})
        spacing = typography.get('spacing', {})
        
        defaults = {
            'paragraph': 24,
            'section': 40,
            'cta_margin': 32
        }
        
        return spacing.get(type, defaults.get(type, 24))
    
    def _get_font_size(self, type: str) -> int:
        """Get font size from design system"""
        design_system = self.config.get('design_system', {})
        typography = design_system.get('typography', {})
        scale = typography.get('scale', {})
        
        defaults = {
            'h1': 72,
            'h2': 48,
            'body': 32,
            'caption': 24,
            'brand': 28
        }
        
        return scale.get(type, defaults.get(type, 32))
    
    def _get_line_height_multiplier(self, text: str) -> float:
        """Get line height multiplier based on text language"""
        design_system = self.config.get('design_system', {})
        typography = design_system.get('typography', {})
        line_heights = typography.get('line_heights', {})
        
        if self._is_arabic_text(text):
            return line_heights.get('arabic', 1.45)
        else:
            return line_heights.get('latin', 1.4)

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Test current line + new word
            test_line = ' '.join(current_line + [word])
            display_test = self._prepare_arabic_text(test_line)
            
            # Get text width
            bbox = font.getbbox(display_test)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, force it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def _add_gradient_noise(self, img: Image.Image) -> Image.Image:
        """Add subtle noise to gradients to prevent banding"""
        import numpy as np
        
        # Get noise opacity from config
        noise_opacity = self.config.get('background', {}).get('noise_opacity', 0.02)
        
        if noise_opacity <= 0:
            return img
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Generate noise
        noise = np.random.normal(0, 8, img_array.shape).astype(np.int16)
        
        # Apply noise with opacity
        noisy_array = img_array.astype(np.int16) + (noise * noise_opacity).astype(np.int16)
        
        # Clip values to valid range
        noisy_array = np.clip(noisy_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(noisy_array)
    
    def _draw_scrim_overlay(self, img: Image.Image, scrim_type: str = 'medium') -> Image.Image:
        """Add a scrim overlay to improve text contrast"""
        design_system = self.config.get('design_system', {})
        overlays = design_system.get('overlays', {})
        
        scrim_colors = {
            'light': overlays.get('light_scrim', [0, 0, 0, 77]),  # 30% opacity
            'medium': overlays.get('medium_scrim', [0, 0, 0, 128]),  # 50% opacity
            'dark': overlays.get('dark_scrim', [0, 0, 0, 179])  # 70% opacity
        }
        
        scrim_color = scrim_colors.get(scrim_type, scrim_colors['medium'])
        
        # Ensure all color values are integers
        scrim_color = [int(c) for c in scrim_color]
        
        # Create overlay
        overlay = Image.new('RGBA', img.size, tuple(scrim_color))
        
        # Blend with original image
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        result = Image.alpha_composite(img, overlay)
        return result.convert('RGB')
    
    def _draw_multiline_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                            position: Tuple[int, int], color: Tuple[int, int, int],
                            max_width: int = None, line_spacing: int = None,
                            alignment: str = 'center', justify: bool = False, 
                            add_shadow: bool = True, is_rtl: bool = None) -> Tuple[int, int]:
        """Draw multi-line text with design system spacing and typography"""
        draw = ImageDraw.Draw(img)
        
        # Use design system defaults if not specified
        if max_width is None:
            max_width = self._get_max_text_width()
        
        if line_spacing is None:
            # Calculate line spacing based on font size and language
            line_height_multiplier = self._get_line_height_multiplier(text)
            font_size = getattr(font, 'size', 32)
            if isinstance(font_size, (list, tuple)):
                font_size = font_size[0] if font_size else 32
            line_spacing = max(8, int(float(font_size) * (line_height_multiplier - 1)))
        
        # Detect RTL if not specified
        if is_rtl is None:
            is_rtl = self._is_arabic_text(text)
        
        # Wrap text into lines
        lines = self._wrap_text(text, font, max_width)
        
        x, y = position
        total_height = 0
        max_line_width = 0
        
        # Enhanced shadow settings from design system
        design_system = self.config.get('design_system', {})
        shadow_config = design_system.get('shadows', {}).get('text', {})
        shadow_offset = int(shadow_config.get('offset', 2)) if add_shadow else 0
        shadow_blur = int(shadow_config.get('blur', 4))
        shadow_color_raw = shadow_config.get('color', [0, 0, 0, 153])
        shadow_color = tuple(int(c) for c in shadow_color_raw)  # Ensure integers
        
        for i, line in enumerate(lines):
            display_line = self._prepare_arabic_text(line)
            
            # Get line dimensions
            bbox = draw.textbbox((0, 0), display_line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            
            # Calculate position based on alignment and RTL
            line_x = x
            if alignment == 'center':
                line_x = x - line_width // 2
            elif alignment == 'right' or (is_rtl and alignment == 'left'):
                line_x = x - line_width
            # 'left' uses x as-is
            
            # Justify text (except last line)
            if justify and i < len(lines) - 1 and len(line.split()) > 1:
                line_x = self._draw_justified_line(draw, display_line, font, line_x, y + total_height, max_width, color, shadow_offset, shadow_color)
            else:
                # Regular text drawing with enhanced shadow
                text_color = tuple(color) if isinstance(color, list) else color
                current_y = y + total_height
                
                if add_shadow:
                    # Draw multiple shadow layers for better effect
                    for offset in range(1, shadow_offset + 1):
                        alpha = int(shadow_color[3] * (offset / shadow_offset) * 0.7)
                        shadow_rgba = (*shadow_color[:3], alpha)
                        draw.text((line_x + offset, current_y + offset), 
                                 display_line, font=font, fill=shadow_rgba)
                
                # Draw main text
                draw.text((line_x, current_y), display_line, font=font, fill=text_color)
            
            max_line_width = max(max_line_width, line_width)
            total_height += line_height + line_spacing
        
        return max_line_width, total_height

    def _draw_justified_line(self, draw: ImageDraw.Draw, line: str, font: ImageFont.ImageFont,
                            x: int, y: int, max_width: int, color: Tuple[int, int, int], 
                            shadow_offset: int = 0, shadow_color: Tuple[int, int, int, int] = None) -> int:
        """Draw a justified line of text with enhanced shadows"""
        if shadow_color is None:
            shadow_color = (0, 0, 0, 153)
            
        words = line.split()
        if len(words) <= 1:
            if shadow_offset:
                for offset in range(1, shadow_offset + 1):
                    alpha = int(shadow_color[3] * (offset / shadow_offset) * 0.7)
                    shadow_rgba = (*shadow_color[:3], alpha)
                    draw.text((x + offset, y + offset), line, font=font, fill=shadow_rgba)
            draw.text((x, y), line, font=font, fill=color)
            return x
        
        # Calculate total word width
        total_word_width = 0
        for word in words:
            bbox = draw.textbbox((0, 0), word, font=font)
            total_word_width += bbox[2] - bbox[0]
        
        # Calculate space width needed
        available_space = max_width - total_word_width
        space_between_words = available_space / (len(words) - 1)
        
        # Draw words with calculated spacing and enhanced shadows
        current_x = x
        for i, word in enumerate(words):
            if shadow_offset:
                for offset in range(1, shadow_offset + 1):
                    alpha = int(shadow_color[3] * (offset / shadow_offset) * 0.7)
                    shadow_rgba = (*shadow_color[:3], alpha)
                    draw.text((current_x + offset, y + offset), word, font=font, fill=shadow_rgba)
            
            draw.text((current_x, y), word, font=font, fill=color)
            bbox = draw.textbbox((0, 0), word, font=font)
            word_width = bbox[2] - bbox[0]
            current_x += word_width
            if i < len(words) - 1:  # Don't add space after last word
                current_x += space_between_words
        
        return x

    def _calculate_dynamic_layout(self, headline: str, subheadline: str, brand: str = None) -> dict:
        """
        Calculate dynamic layout based on element sizes and available space
        Returns positioning information for all elements
        """
        canvas_width = self.config['canvas_width']
        canvas_height = self.config['canvas_height']

        # Define layout zones as percentages of canvas height
        zones = {
            'header': (0.05, 0.25),    # 5% - 25% of height
            'content': (0.25, 0.75),   # 25% - 75% of height
            'footer': (0.75, 0.95)     # 75% - 95% of height
        }

        # Calculate available space considering custom images
        available_space = {
            'top': zones['header'][0] * canvas_height,
            'bottom': (1 - zones['footer'][1]) * canvas_height,
            'left': 50,  # Margin from left
            'right': 50  # Margin from right
        }

        # Account for image positions if custom images are used
        use_custom_images = (
            self.config.get('use_custom_images', False) or
            self.config.get('custom_images', {}).get('use_custom_images', False)
        )

        if use_custom_images:
            if self.main_image:
                # Get main image dimensions and position
                preserve_aspect = self.config['custom_images'].get('preserve_aspect_ratio', False)
                if preserve_aspect:
                    max_width = self.config['custom_images'].get('max_image_width', 500)
                    max_height = self.config['custom_images'].get('max_image_height', 500)
                    resized_main = self._resize_image_with_aspect_ratio(
                        self.main_image, max_width, max_height, preserve_aspect
                    )
                    canvas_size = (canvas_width, canvas_height)
                    original_pos = tuple(self.config['custom_images']['main_image_position'])
                    main_pos = self._calculate_image_position_with_aspect_ratio(
                        resized_main.size, canvas_size, original_pos
                    )
                else:
                    resized_main = self.main_image.resize(
                        tuple(self.config['custom_images']['main_image_size']), Image.Resampling.LANCZOS
                    )
                    main_pos = tuple(self.config['custom_images']['main_image_position'])

                # Adjust available space based on main image position
                img_width, img_height = resized_main.size
                img_x, img_y = main_pos

                # Reserve space around the main image
                available_space['image_reserved'] = {
                    'x': img_x,
                    'y': img_y,
                    'width': img_width,
                    'height': img_height
                }

        # Calculate text dimensions for dynamic positioning
        temp_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)

        # Get fonts
        headline_font = self._get_font_for_text(headline, 'headline')
        subheadline_font = self._get_font_for_text(subheadline, 'subheadline')
        brand_font = self._get_font_for_text(brand or '', 'brand')

        # Calculate text dimensions
        headline_text = self._prepare_arabic_text(headline)
        subheadline_text = self._prepare_arabic_text(subheadline)
        brand_text = self._prepare_arabic_text(brand or '')

        headline_bbox = draw.textbbox((0, 0), headline_text, font=headline_font)
        subheadline_bbox = draw.textbbox((0, 0), subheadline_text, font=subheadline_font)
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)

        text_dimensions = {
            'headline': {
                'width': headline_bbox[2] - headline_bbox[0],
                'height': headline_bbox[3] - headline_bbox[1]
            },
            'subheadline': {
                'width': subheadline_bbox[2] - subheadline_bbox[0],
                'height': subheadline_bbox[3] - subheadline_bbox[1]
            },
            'brand': {
                'width': brand_bbox[2] - brand_bbox[0],
                'height': brand_bbox[3] - brand_bbox[1]
            }
        }

        # Calculate dynamic positions based on available space and text dimensions

        # Header zone positioning
        header_start = int(zones['header'][0] * canvas_height)
        header_end = int(zones['header'][1] * canvas_height)

        # Distribute headline and subheadline in header zone
        total_text_height = text_dimensions['headline']['height'] + text_dimensions['subheadline']['height']
        spacing = max(20, (header_end - header_start - total_text_height) // 3)  # Dynamic spacing

        headline_y = header_start + spacing + text_dimensions['headline']['height'] // 2
        subheadline_y = headline_y + text_dimensions['headline']['height'] // 2 + spacing + text_dimensions['subheadline']['height'] // 2

        # Footer zone positioning
        footer_start = int(zones['footer'][0] * canvas_height)
        footer_end = int(zones['footer'][1] * canvas_height)

        brand_y = footer_end - text_dimensions['brand']['height'] // 2 - spacing

        # Ensure brand text doesn't overlap with reserved image space
        if 'image_reserved' in available_space:
            img_bottom = available_space['image_reserved']['y'] + available_space['image_reserved']['height']
            if brand_y - text_dimensions['brand']['height'] // 2 < img_bottom + 50:
                brand_y = img_bottom + 50 + text_dimensions['brand']['height'] // 2

        # Create brand position for logo calculation
        brand_pos = {
            'x': canvas_width // 2,
            'y': brand_y,
            'width': text_dimensions['brand']['width'],
            'height': text_dimensions['brand']['height']
        }

        # Calculate brand logo positioning (bottom-left corner near brand text)
        brand_logo_y = canvas_height - 150  # Above bottom edge
        brand_logo_x = 60  # Left margin

        # Adjust if brand text would overlap with logo
        logo_width = 120  # Assuming logo width from config
        if brand_pos['x'] - text_dimensions['brand']['width'] // 2 < brand_logo_x + logo_width + 50:
            # Move logo to the right if it would overlap with brand text
            brand_logo_x = brand_pos['x'] + text_dimensions['brand']['width'] // 2 + 50

        return {
            'headline': {
                'x': canvas_width // 2,
                'y': headline_y,
                'width': text_dimensions['headline']['width'],
                'height': text_dimensions['headline']['height']
            },
            'subheadline': {
                'x': canvas_width // 2,
                'y': subheadline_y,
                'width': text_dimensions['subheadline']['width'],
                'height': text_dimensions['subheadline']['height']
            },
            'brand': {
                'x': canvas_width // 2,
                'y': brand_y,
                'width': text_dimensions['brand']['width'],
                'height': text_dimensions['brand']['height']
            },
            'brand_logo': {
                'x': brand_logo_x,
                'y': brand_logo_y,
                'width': 120,  # From config
                'height': 120   # From config
            },
            'available_space': available_space,
            'zones': zones,
            'canvas_size': (canvas_width, canvas_height)
        }

    def _draw_text_with_panel(self, img: Image.Image, text: str, font_type: str,
                             position: tuple, text_color: tuple, panel_color: tuple = None,
                             padding: int = 20, corner_radius: int = 10) -> tuple:
        """Draw text with a background panel for better visibility"""
        draw = ImageDraw.Draw(img)

        # Prepare text for Arabic/Farsi
        display_text = self._prepare_arabic_text(text)

        # Get appropriate font based on text content
        font = self._get_font_for_text(text, font_type)

        # Get text dimensions
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = position

        # Default to dark semi-transparent panel
        if panel_color is None:
            panel_color = tuple(self.config.get('design_system', {})
                              .get('overlays', {})
                              .get('text_background', [0, 0, 0, 180]))

        # Calculate panel dimensions
        panel_width = text_width + (2 * padding)
        panel_height = text_height + (2 * padding)

        # Center the panel horizontally
        panel_x = x - panel_width // 2
        panel_y = y - padding

        # Create panel with rounded corners
        panel_img = Image.new('RGBA', (panel_width, panel_height), panel_color)

        # Create mask for rounded corners
        mask = Image.new('L', (panel_width, panel_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, panel_width, panel_height],
                                   radius=corner_radius, fill=255)

        # Apply mask to panel
        panel_with_corners = Image.new('RGBA', (panel_width, panel_height), (0, 0, 0, 0))
        panel_with_corners.paste(panel_img, (0, 0), mask)

        # Paste panel onto main image
        img.paste(panel_with_corners, (panel_x, panel_y), panel_with_corners)

        # Draw text on top of panel
        text_x = panel_x + padding
        text_y = panel_y + padding

        draw.text((text_x, text_y), display_text, font=font, fill=text_color)

        return text_width, text_height

    def _draw_enhanced_text(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                           position: Tuple[int, int], color: Tuple[int, int, int],
                           bg_color: Optional[Tuple[int, int, int, int]] = None,
                           centered: bool = True, add_shadow: bool = True) -> Tuple[int, int]:
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

        # Draw text with shadow for better visibility
        text_color = tuple(color) if isinstance(color, list) else color
        shadow_offset = 2 if add_shadow else 0
        
        if add_shadow:
            # Draw shadow
            draw.text((x + shadow_offset, y + shadow_offset), display_text, font=font, fill=(0, 0, 0))
        
        # Draw main text
        draw.text((x, y), display_text, font=font, fill=text_color)

        return text_width, text_height
    
    def _draw_cta_button(self, img: Image.Image, text: str, position: Tuple[int, int], 
                        font: ImageFont.ImageFont = None) -> Tuple[int, int]:
        """Draw a properly styled CTA button based on design system"""
        design_system = self.config.get('design_system', {})
        cta_config = design_system.get('cta', {})
        colors = design_system.get('colors', {})
        
        # CTA styling from design system
        padding_v = cta_config.get('padding_vertical', 18)
        padding_h = cta_config.get('padding_horizontal', 32)
        border_radius = cta_config.get('border_radius', 26)
        text_transform = cta_config.get('text_transform', 'uppercase')
        
        # Colors
        primary_color = tuple(colors.get('primary', [45, 123, 251]))
        text_color = tuple(colors.get('neutral', {}).get('white', [255, 255, 255]))
        
        # Transform text
        if text_transform == 'uppercase':
            text = text.upper()
        
        # Use brand font if no font specified
        if font is None:
            font_size = self._get_font_size('brand')
            try:
                font = ImageFont.truetype(self.fonts['brand'].path, font_size)
            except:
                font = self.fonts['brand']
        
        draw = ImageDraw.Draw(img)
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate button dimensions
        button_width = text_width + (2 * padding_h)
        button_height = text_height + (2 * padding_v)
        
        x, y = position
        button_x = x - button_width // 2  # Center the button
        button_y = y
        
        # Draw button background with rounded corners
        button_rect = [button_x, button_y, button_x + button_width, button_y + button_height]
        
        # Create a mask for rounded corners
        mask = Image.new('L', (button_width, button_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, button_width, button_height], 
                                   radius=border_radius, fill=255)
        
        # Create button background
        button_bg = Image.new('RGB', (button_width, button_height), primary_color)
        
        # Paste button onto main image using mask
        img.paste(button_bg, (button_x, button_y), mask)
        
        # Draw text on button
        text_x = button_x + padding_h
        text_y = button_y + padding_v
        
        draw.text((text_x, text_y), text, font=font, fill=text_color)
        
        return button_width, button_height

    def generate_enhanced_hero_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate enhanced hero layout with advanced color control"""
        img = self._create_enhanced_background()

        # FIXED: Add stronger scrim overlay for better text contrast
        img = self._draw_scrim_overlay(img, 'medium')  # 50% dark overlay

        colors = self.config['layout_colors']['hero']

        # Use custom images if available and enabled
        use_custom_images = (
            self.config.get('use_custom_images', False) or 
            self.config.get('custom_images', {}).get('use_custom_images', False)
        )
        
        if use_custom_images:
            # Draw main image using CONFIG values with aspect ratio preservation
            if self.main_image:
                # Check if aspect ratio preservation is enabled
                preserve_aspect = self.config['custom_images'].get('preserve_aspect_ratio', False)
                max_width = self.config['custom_images'].get('max_image_width', 500)
                max_height = self.config['custom_images'].get('max_image_height', 500)

                if preserve_aspect:
                    # Resize while preserving aspect ratio
                    resized_main = self._resize_image_with_aspect_ratio(
                        self.main_image, max_width, max_height, preserve_aspect
                    )
                    # Calculate optimal position
                    canvas_size = (self.config['canvas_width'], self.config['canvas_height'])
                    original_pos = tuple(self.config['custom_images']['main_image_position'])
                    main_pos = self._calculate_image_position_with_aspect_ratio(
                        resized_main.size, canvas_size, original_pos
                    )
                else:
                    # Use traditional fixed size approach
                    main_size = tuple(self.config['custom_images']['main_image_size'])
                    resized_main = self.main_image.resize(main_size, Image.Resampling.LANCZOS)
                    main_pos = tuple(self.config['custom_images']['main_image_position'])

                img.paste(resized_main, main_pos, resized_main)

            # Draw blueprint/watermark image using CONFIG values with aspect ratio preservation
            if self.blueprint_image:
                # Blueprint typically doesn't need aspect ratio preservation (logos/watermarks)
                blueprint_size = tuple(self.config['custom_images']['blueprint_image_size'])
                blueprint_pos = tuple(self.config['custom_images']['blueprint_image_position'])
                resized_blueprint = self.blueprint_image.resize(blueprint_size, Image.Resampling.LANCZOS)
                img.paste(resized_blueprint, blueprint_pos, resized_blueprint)
        else:
            # Draw programmatic coats
            self._draw_enhanced_coats(img, 150, 450, img.width - 300, 200)

        # FIXED TEXT POSITIONING WITH BACKGROUND PANELS FOR BETTER VISIBILITY

        # Get colors from design system
        text_colors = self.config.get('design_system', {}).get('colors', {}).get('text', {})
        primary_color = tuple(text_colors.get('primary', [255, 255, 255]))
        secondary_color = tuple(text_colors.get('secondary', [230, 230, 230]))
        muted_color = tuple(text_colors.get('muted', [200, 200, 200]))

        # Panel color for text backgrounds
        panel_color = tuple(self.config.get('design_system', {})
                           .get('overlays', {})
                           .get('text_background', [0, 0, 0, 180]))

        # 1. Headline - positioned at top without background panel
        headline_y = 150
        self._draw_enhanced_text(
            img, headline, self.fonts['headline'],
            (self.config['canvas_width'] // 2, headline_y),
            primary_color, centered=True, add_shadow=True
        )

        # 2. Subheadline - positioned below headline without background panel
        subheadline_y = 220
        self._draw_enhanced_text(
            img, subheadline, self.fonts['subheadline'],
            (self.config['canvas_width'] // 2, subheadline_y),
            secondary_color, centered=True, add_shadow=True
        )

        # 3. Brand - positioned at bottom with safe area without background panel
        if brand:
            brand_y = self.config['canvas_height'] - 100  # Safe area from bottom
            self._draw_enhanced_text(
                img, brand, self.fonts['brand'],
                (self.config['canvas_width'] // 2, brand_y),
                muted_color, centered=True, add_shadow=True
            )

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

    # ===== TEXT-FOCUSED LAYOUT METHODS =====

    def generate_quote_layout(self, quote: str, author: str = None, brand: str = None) -> Image.Image:
        """Generate a quote layout with proper design system implementation"""
        img = self._create_enhanced_background()
        
        # Apply noise to gradients to prevent banding
        img = self._add_gradient_noise(img)
        
        # Add scrim overlay for better text contrast
        img = self._draw_scrim_overlay(img, 'medium')
        
        # Get design system values
        safe_margins = self._get_safe_margins()
        max_text_width = self._get_max_text_width()
        
        # Use design system font sizes
        quote_font_size = self._get_font_size('h1')
        try:
            quote_font = ImageFont.truetype(self.fonts['headline'].path, quote_font_size)
        except:
            quote_font = self.fonts['headline']
        
        # Format quote with proper quotation marks
        is_arabic = self._is_arabic_text(quote)
        formatted_quote = self._format_quote_text(quote, is_arabic)
        
        # Calculate vertical centering
        canvas_center_y = self.config['canvas_height'] // 2
        quote_start_y = canvas_center_y - 100  # Offset upward for better balance
        
        # Draw quote with design system multiline text
        quote_width, quote_height = self._draw_multiline_text(
            img, formatted_quote, quote_font,
            (self.config['canvas_width'] // 2, quote_start_y),
            tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('primary', [255, 255, 255])),
            max_width=max_text_width,
            alignment='center' if not is_arabic else 'right',
            justify=False,
            is_rtl=is_arabic
        )
        
        # Author attribution with proper formatting
        if author:
            author_spacing = self._get_spacing('paragraph')
            author_y = quote_start_y + quote_height + author_spacing
            
            # Format attribution with proper punctuation
            formatted_author = self._format_attribution(author, is_arabic)
            
            # Use smaller font for attribution
            author_font_size = self._get_font_size('caption')
            try:
                author_font = ImageFont.truetype(self.fonts['subheadline'].path, author_font_size)
            except:
                author_font = self.fonts['subheadline']
            
            # Draw attribution with proper alignment
            text_color = tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('secondary', [203, 213, 225]))
            
            self._draw_enhanced_text(img, formatted_author, author_font,
                                   (self.config['canvas_width'] // 2, author_y),
                                   text_color, 
                                   centered=True if not is_arabic else False,
                                   add_shadow=True)

        # Brand at bottom with safe area - only show if no logo present
        use_custom_images = (
            self.config.get('use_custom_images', False) or
            self.config.get('custom_images', {}).get('use_custom_images', False)
        )
        brand_text_present = not self.blueprint_image if use_custom_images else True

        if brand and brand_text_present:
            brand_font_size = self._get_font_size('brand')
            try:
                brand_font = ImageFont.truetype(self.fonts['brand'].path, brand_font_size)
            except:
                brand_font = self.fonts['brand']

            brand_y = self.config['canvas_height'] - safe_margins['bottom']
            brand_color = tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('muted', [148, 163, 184]))

            self._draw_enhanced_text(img, brand, brand_font,
                                   (self.config['canvas_width'] // 2, brand_y),
                                   brand_color, centered=True, add_shadow=True)

        return img

    def generate_article_layout(self, title: str, body: str, brand: str = None) -> Image.Image:
        """Generate an article excerpt layout with title and body text"""
        img = self._create_enhanced_background()
        
        # Configure text area
        margin = 60
        content_width = self.config['canvas_width'] - (2 * margin)
        
        # Title - large and bold at top
        title_y = 150
        title_width, title_height = self._draw_multiline_text(
            img, title, self.fonts['headline'],
            (self.config['canvas_width'] // 2, title_y),
            (255, 255, 255), content_width, line_spacing=12,
            alignment='center', justify=False
        )
        
        # Body text - smaller, justified
        body_y = title_y + title_height + 80
        body_font_size = 28
        body_font = ImageFont.truetype(self.fonts['subheadline'].path, body_font_size)
        
        body_width, body_height = self._draw_multiline_text(
            img, body, body_font,
            (margin, body_y),
            (230, 230, 230), content_width, line_spacing=18,
            alignment='left', justify=True
        )
        
        # Brand at bottom
        if brand:
            self._draw_enhanced_text(img, brand, self.fonts['brand'],
                                   (self.config['canvas_width'] // 2, self.config['canvas_height'] - 100),
                                   (255, 255, 255), centered=True)
        
        return img

    def generate_announcement_layout(self, title: str, description: str, 
                                   cta: str = None, brand: str = None) -> Image.Image:
        """Generate an announcement layout with proper design system implementation"""
        img = self._create_enhanced_background()
        
        # Apply improvements
        img = self._add_gradient_noise(img)
        img = self._draw_scrim_overlay(img, 'medium')
        
        # Get design system values
        safe_margins = self._get_safe_margins()
        max_text_width = self._get_max_text_width()
        
        # Title - use H1 from design system
        title_font_size = self._get_font_size('h1')
        try:
            title_font = ImageFont.truetype(self.fonts['headline'].path, title_font_size)
        except:
            title_font = self.fonts['headline']
        
        # Start content higher for better balance
        title_y = 200
        
        # Check if title is Arabic for proper alignment
        is_title_arabic = self._is_arabic_text(title)
        
        title_width, title_height = self._draw_multiline_text(
            img, title, title_font,
            (self.config['canvas_width'] // 2, title_y),
            tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('primary', [255, 255, 255])),
            max_width=max_text_width,
            alignment='center' if not is_title_arabic else 'right',
            justify=False,
            is_rtl=is_title_arabic
        )
        
        # Description - proper spacing and typography
        section_spacing = self._get_spacing('section')
        desc_y = title_y + title_height + section_spacing
        
        # Use design system font size for body text
        desc_font_size = self._get_font_size('body')
        try:
            desc_font = ImageFont.truetype(self.fonts['subheadline'].path, desc_font_size)
        except:
            desc_font = self.fonts['subheadline']
        
        is_desc_arabic = self._is_arabic_text(description)
        text_secondary_color = tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('secondary', [203, 213, 225]))
        
        desc_width, desc_height = self._draw_multiline_text(
            img, description, desc_font,
            (self.config['canvas_width'] // 2, desc_y),
            text_secondary_color,
            max_width=max_text_width,
            alignment='center' if not is_desc_arabic else 'right',
            justify=False,
            is_rtl=is_desc_arabic
        )
        
        # Call-to-action - use design system CTA button
        if cta:
            cta_spacing = self._get_spacing('cta_margin')
            cta_y = desc_y + desc_height + cta_spacing
            
            # Use the new CTA button system
            self._draw_cta_button(img, cta, (self.config['canvas_width'] // 2, cta_y))
        
        # Brand at bottom with safe area
        if brand:
            brand_font_size = self._get_font_size('brand')
            try:
                brand_font = ImageFont.truetype(self.fonts['brand'].path, brand_font_size)
            except:
                brand_font = self.fonts['brand']
            
            brand_y = self.config['canvas_height'] - safe_margins['bottom']
            brand_color = tuple(self.config.get('design_system', {}).get('colors', {}).get('text', {}).get('muted', [148, 163, 184]))
            
            self._draw_enhanced_text(img, brand, brand_font,
                                   (self.config['canvas_width'] // 2, brand_y),
                                   brand_color, centered=True, add_shadow=True)
        
        return img

    def generate_list_layout(self, title: str, items: List[str], brand: str = None) -> Image.Image:
        """Generate a list layout with title and bulleted items"""
        img = self._create_enhanced_background()
        
        # Configure text area
        margin = 80
        content_width = self.config['canvas_width'] - (2 * margin)
        
        # Title
        title_y = 140
        title_width, title_height = self._draw_multiline_text(
            img, title, self.fonts['headline'],
            (self.config['canvas_width'] // 2, title_y),
            (255, 255, 255), content_width, line_spacing=12,
            alignment='center', justify=False
        )
        
        # List items
        item_font_size = 30
        item_font = ImageFont.truetype(self.fonts['subheadline'].path, item_font_size)
        item_y = title_y + title_height + 60
        
        for i, item in enumerate(items):
            # Bullet point
            bullet = "•"
            bullet_x = margin + 20
            
            # Draw bullet
            self._draw_enhanced_text(img, bullet, item_font,
                                   (bullet_x, item_y),
                                   (255, 255, 255), centered=False)
            
            # Draw item text
            item_x = bullet_x + 40
            item_max_width = content_width - 60
            
            item_width, item_height = self._draw_multiline_text(
                img, item, item_font,
                (item_x, item_y),
                (230, 230, 230), item_max_width, line_spacing=12,
                alignment='left', justify=False
            )
            
            item_y += item_height + 25
        
        # Brand at bottom
        if brand:
            self._draw_enhanced_text(img, brand, self.fonts['brand'],
                                   (self.config['canvas_width'] // 2, self.config['canvas_height'] - 100),
                                   (255, 255, 255), centered=True)
        
        return img

    def generate_testimonial_layout(self, quote: str, person_name: str, 
                                  person_title: str = None, brand: str = None) -> Image.Image:
        """Generate a testimonial layout with quote and person information"""
        img = self._create_enhanced_background()
        
        # Configure text area
        margin = 70
        content_width = self.config['canvas_width'] - (2 * margin)
        
        # Quote - with quotation marks
        quote_font_size = 36
        quote_font = ImageFont.truetype(self.fonts['subheadline'].path, quote_font_size)
        quote_y = 200
        
        formatted_quote = f'"{quote}"'
        
        quote_width, quote_height = self._draw_multiline_text(
            img, formatted_quote, quote_font,
            (self.config['canvas_width'] // 2, quote_y),
            (255, 255, 255), content_width, line_spacing=18,
            alignment='center', justify=False
        )
        
        # Person name
        name_y = quote_y + quote_height + 50
        name_font_size = 32
        name_font = ImageFont.truetype(self.fonts['brand'].path, name_font_size)
        
        self._draw_enhanced_text(img, person_name, name_font,
                               (self.config['canvas_width'] // 2, name_y),
                               (255, 255, 255), centered=True)
        
        # Person title/company
        if person_title:
            title_y = name_y + 45
            title_font_size = 24
            title_font = ImageFont.truetype(self.fonts['brand'].path, title_font_size)
            
            self._draw_enhanced_text(img, person_title, title_font,
                                   (self.config['canvas_width'] // 2, title_y),
                                   (200, 200, 200), centered=True)
        
        # Brand at bottom
        if brand:
            self._draw_enhanced_text(img, brand, self.fonts['brand'],
                                   (self.config['canvas_width'] // 2, self.config['canvas_height'] - 100),
                                   (255, 255, 255), centered=True)
        
        return img

    def generate_text_layout(self, layout_type: str, content: Dict[str, any]) -> Image.Image:
        """Generate text-based layout based on type and content"""
        if layout_type == 'quote':
            return self.generate_quote_layout(
                content.get('quote', ''),
                content.get('author'),
                content.get('brand')
            )
        elif layout_type == 'article':
            return self.generate_article_layout(
                content.get('title', ''),
                content.get('body', ''),
                content.get('brand')
            )
        elif layout_type == 'announcement':
            return self.generate_announcement_layout(
                content.get('title', ''),
                content.get('description', ''),
                content.get('cta'),
                content.get('brand')
            )
        elif layout_type == 'list':
            return self.generate_list_layout(
                content.get('title', ''),
                content.get('items', []),
                content.get('brand')
            )
        elif layout_type == 'testimonial':
            return self.generate_testimonial_layout(
                content.get('quote', ''),
                content.get('person_name', ''),
                content.get('person_title'),
                content.get('brand')
            )
        else:
            raise ValueError(f"Unknown text layout type: {layout_type}")

    def generate_all_text_layouts(self, content: Dict[str, any], output_prefix: str = "text_post"):
        """Generate all text layout variations"""
        text_layouts = ['quote', 'article', 'announcement', 'list', 'testimonial']
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        for layout_type in text_layouts:
            try:
                img = self.generate_text_layout(layout_type, content)
                output_path = os.path.join(self.output_dir, f"{output_prefix}_{layout_type}.png")
                img.save(output_path, 'PNG', quality=95)
                print(f"Generated: {output_path}")
            except Exception as e:
                print(f"Failed to generate {layout_type} layout: {e}")

    def generate_improved_hero_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """
        Generate a professional hero layout with dynamic positioning and AI-powered features.

        This method creates a complete social media image with:
        - Dynamic layout that adapts to text and image sizes
        - AI-powered background removal for main image
        - Multi-language text support (English, Arabic, Farsi)
        - Professional typography with background panels
        - Brand logo integration (replaces brand text when present)
        - Collision avoidance for optimal element placement

        Args:
            headline (str): Main headline text. Supports English, Arabic, and Farsi.
            subheadline (str): Secondary text below headline. Supports all languages.
            brand (str, optional): Brand/company name. Only displayed if no brand logo
                is configured. Supports all languages. Defaults to None.

        Returns:
            PIL.Image.Image: Generated social media image with RGBA mode for transparency.

        Raises:
            FileNotFoundError: If configured image files don't exist.
            ValueError: If text is too long for the canvas or invalid parameters.

        Example:
            >>> generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
            >>> img = generator.generate_improved_hero_layout(
            ...     headline="Premium Collection",
            ...     subheadline="Exceptional Quality & Design",
            ...     brand="Fashion Store"
            ... )
            >>> img.save('output/social_post.png', 'PNG')

        Note:
            - If a brand logo (blueprint_image) is configured, the brand text parameter
              is ignored and the logo is displayed instead.
            - Text is automatically reshaped for Arabic/Farsi languages.
            - Images are processed with AI background removal if rembg is available.
        """
        img = self._create_enhanced_background()

        # Add stronger scrim overlay for better contrast
        img = self._draw_scrim_overlay(img, 'medium')  # 50% dark overlay

        # Calculate dynamic layout based on content and available space
        layout_info = self._calculate_dynamic_layout(headline, subheadline, brand)

        # Position custom images with collision avoidance
        use_custom_images = (
            self.config.get('use_custom_images', False) or
            self.config.get('custom_images', {}).get('use_custom_images', False)
        )

        # Initialize brand text presence
        brand_text_present = not self.blueprint_image if use_custom_images else True

        if use_custom_images:
            # Draw main image using CONFIG values with aspect ratio preservation
            if self.main_image:
                # Check if aspect ratio preservation is enabled
                preserve_aspect = self.config['custom_images'].get('preserve_aspect_ratio', False)
                max_width = self.config['custom_images'].get('max_image_width', 500)
                max_height = self.config['custom_images'].get('max_image_height', 500)

                if preserve_aspect:
                    # Resize while preserving aspect ratio
                    resized_main = self._resize_image_with_aspect_ratio(
                        self.main_image, max_width, max_height, preserve_aspect
                    )
                    # Calculate optimal position
                    canvas_size = (self.config['canvas_width'], self.config['canvas_height'])
                    original_pos = tuple(self.config['custom_images']['main_image_position'])
                    main_pos = self._calculate_image_position_with_aspect_ratio(
                        resized_main.size, canvas_size, original_pos
                    )
                else:
                    # Use traditional fixed size approach
                    main_size = tuple(self.config['custom_images']['main_image_size'])
                    resized_main = self.main_image.resize(main_size, Image.Resampling.LANCZOS)
                    main_pos = tuple(self.config['custom_images']['main_image_position'])

                img.paste(resized_main, main_pos, resized_main)

            # Draw brand logo using DYNAMIC positioning (replaces brand text)
            if self.blueprint_image:
                # PRESERVE ORIGINAL ASPECT RATIO - Don't resize to fit config dimensions
                original_size = self.blueprint_image.size
                blueprint_size = original_size  # Keep original dimensions

                # Use dynamic brand logo position from layout calculations
                brand_logo_pos = layout_info.get('brand_logo', {})
                if brand_logo_pos:
                    blueprint_pos = (brand_logo_pos['x'], brand_logo_pos['y'])
                else:
                    # Fallback to config position
                    blueprint_pos = tuple(self.config['custom_images']['blueprint_image_position'])

                # No resizing - preserve aspect ratio
                img.paste(self.blueprint_image, blueprint_pos, self.blueprint_image)

        # DYNAMIC TEXT POSITIONING WITH COLLISION AVOIDANCE

        # 1. Headline - Dynamic position in header zone without panel
        headline_pos = layout_info['headline']
        headline_color = (255, 255, 255)  # White text

        self._draw_enhanced_text(
            img, headline, self.fonts['headline'],
            (headline_pos['x'], headline_pos['y']),
            headline_color, centered=True, add_shadow=True
        )

        # 2. Subheadline - Dynamic position below headline without panel
        subheadline_pos = layout_info['subheadline']
        subheadline_color = (230, 230, 230)  # Light gray

        self._draw_enhanced_text(
            img, subheadline, self.fonts['subheadline'],
            (subheadline_pos['x'], subheadline_pos['y']),
            subheadline_color, centered=True, add_shadow=True
        )

        # 3. Brand - Dynamic position in footer zone with collision avoidance
        # Only draw brand text if logo is not present and brand text is provided
        if brand and brand_text_present:
            brand_pos = layout_info['brand']
            brand_color = (200, 200, 200)  # Muted color

            self._draw_enhanced_text(
                img, brand, self.fonts['brand'],
                (brand_pos['x'], brand_pos['y']),
                brand_color, centered=True, add_shadow=True
            )

        return img
