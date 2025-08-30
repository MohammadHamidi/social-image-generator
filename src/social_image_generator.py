from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import json
from typing import Dict, List, Tuple, Optional
import arabic_reshaper
from bidi.algorithm import get_display

class SocialImageGenerator:
    def __init__(self, config_path: str = None):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        self.output_dir = os.path.join(self.base_dir, 'output')
        
        # Default configuration
        self.config = {
            'canvas_width': 1080,
            'canvas_height': 1350,
            'background_color': (255, 100, 100),
            'coat_colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'coat_count': 5,
            'font_size_headline': 48,
            'font_size_subheadline': 32,
            'brand_font_size': 24,
            'text_color': (255, 255, 255),
            'panel_opacity': 180
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        
        self._load_fonts()
        self._load_custom_images()

    def _load_fonts(self):
        """Load required fonts"""
        font_dir = os.path.join(self.assets_dir, 'fonts')
        
        # Try to find Arabic-supporting fonts (prioritize system fonts)
        arabic_font_paths = [
            '/System/Library/Fonts/SFArabic.ttf',  # macOS SF Arabic
            '/System/Library/Fonts/SFArabicRounded.ttf',  # macOS SF Arabic Rounded
            '/System/Library/Fonts/ArialHB.ttc',  # macOS Arial Hebrew (has Arabic support)
            '/System/Library/Fonts/Arial.ttf',  # macOS Arial fallback
            os.path.join(font_dir, 'NotoSansArabic-Bold.ttf'),  # Downloaded font (if available)
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # Linux fallback
        ]
        
        self.arabic_font = None
        for path in arabic_font_paths:
            if os.path.exists(path):
                try:
                    self.arabic_font = ImageFont.truetype(path, self.config['font_size_headline'])
                    break
                except Exception:
                    continue
        
        if not self.arabic_font:
            self.arabic_font = ImageFont.load_default()

        # Load brand font (Latin)
        try:
            self.brand_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.config['brand_font_size'])
        except:
            self.brand_font = ImageFont.load_default()

    def _load_custom_images(self):
        """Load custom images for main content and blueprint/watermark"""
        self.main_image = None
        self.blueprint_image = None

        if self.config.get('use_custom_images', False):
            # Load main image
            main_image_path = os.path.join(self.base_dir, self.config.get('main_image_path', ''))
            if os.path.exists(main_image_path):
                try:
                    self.main_image = Image.open(main_image_path).convert('RGBA')
                    print(f"Loaded main image: {main_image_path}")
                except Exception as e:
                    print(f"Failed to load main image: {e}")

            # Load blueprint/watermark image
            blueprint_image_path = os.path.join(self.base_dir, self.config.get('blueprint_image_path', ''))
            if os.path.exists(blueprint_image_path):
                try:
                    self.blueprint_image = Image.open(blueprint_image_path).convert('RGBA')
                    print(f"Loaded blueprint image: {blueprint_image_path}")
                except Exception as e:
                    print(f"Failed to load blueprint image: {e}")

    def _prepare_arabic_text(self, text: str) -> str:
        """Prepare Arabic/Farsi text for proper display"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        except:
            return text
    
    def _create_background(self) -> Image.Image:
        """Create the tinted background from pattern"""
        pattern_path = os.path.join(self.assets_dir, 'backgrounds', 'swirly_pattern.png')
        
        if os.path.exists(pattern_path):
            # Load and resize pattern
            pattern = Image.open(pattern_path)
            pattern = pattern.resize((self.config['canvas_width'], self.config['canvas_height']))
            
            # Convert to grayscale and apply tint
            pattern = pattern.convert('L')
            pattern = pattern.convert('RGB')
            
            # Apply background color
            tinted = Image.new('RGB', pattern.size)
            draw = ImageDraw.Draw(tinted)
            bg_color = tuple(self.config['background_color']) if isinstance(self.config['background_color'], list) else self.config['background_color']
            draw.rectangle([0, 0, pattern.width, pattern.height], fill=bg_color)
            
            # Blend pattern with tint
            result = Image.blend(tinted, pattern, 0.3)
            return result
        else:
            # Create solid colored background as fallback
            bg_color = tuple(self.config['background_color']) if isinstance(self.config['background_color'], list) else self.config['background_color']
            img = Image.new('RGB', (self.config['canvas_width'], self.config['canvas_height']),
                          bg_color)
            return img
    
    def _draw_coats(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int):
        """Draw a row of colorful coats"""
        coat_width = width // self.config['coat_count']
        coat_height = height - 40
        
        for i in range(self.config['coat_count']):
            color = self.config['coat_colors'][i % len(self.config['coat_colors'])]
            
            coat_x = x + i * coat_width + 10
            coat_y = y + 20
            
            # Draw coat body (rectangle)
            draw.rectangle([coat_x, coat_y, coat_x + coat_width - 20, coat_y + coat_height], 
                         fill=color, outline=(255, 255, 255), width=2)
            
            # Draw hanger (small arc at top)
            hanger_x = coat_x + (coat_width - 20) // 2
            draw.arc([hanger_x - 8, coat_y - 15, hanger_x + 8, coat_y + 5], 
                    start=0, end=180, fill=(100, 100, 100), width=3)
    
    def _draw_text_with_background(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                                 position: Tuple[int, int], color: Tuple[int, int, int],
                                 bg_color: Tuple[int, int, int, int] = None):
        """Draw text with optional background panel"""
        draw = ImageDraw.Draw(img)
        
        # Prepare text for Arabic/Farsi
        display_text = self._prepare_arabic_text(text)
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x, y = position
        
        # Draw background panel if specified
        if bg_color:
            panel_padding = 20
            panel_img = Image.new('RGBA', (text_width + 2*panel_padding, text_height + 2*panel_padding), bg_color)
            img.paste(panel_img, (x - panel_padding, y - panel_padding), panel_img)
        
        # Draw text
        draw.text((x, y), display_text, font=font, fill=color)
        
        return text_width, text_height

    def _draw_coats_minimal(self, draw: ImageDraw.Draw, x: int, y: int, width: int, height: int):
        """Draw a row of colorful coats - minimalist version (no hangers, no outlines)"""
        coat_width = width // self.config['coat_count']
        coat_height = height

        for i in range(self.config['coat_count']):
            color = self.config['coat_colors'][i % len(self.config['coat_colors'])]

            coat_x = x + i * coat_width + 5
            coat_y = y

            # Draw simple coat rectangle (no outline, no hanger)
            draw.rectangle([coat_x, coat_y, coat_x + coat_width - 10, coat_y + coat_height],
                         fill=color)

    def _draw_text_minimal(self, img: Image.Image, text: str, font: ImageFont.ImageFont,
                          position: Tuple[int, int], color: Tuple[int, int, int]):
        """Draw text directly on background - minimalist version (no background panel)"""
        draw = ImageDraw.Draw(img)

        # Prepare text for Arabic/Farsi
        display_text = self._prepare_arabic_text(text)

        # Get text dimensions for centering
        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = position
        # Center the text horizontally
        centered_x = x - text_width // 2

        # Draw text directly on background (no panel)
        draw.text((centered_x, y), display_text, font=font, fill=color)

        return text_width, text_height

    def generate_hero_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate hero layout with centered content - supports custom images or programmatic generation"""
        img = self._create_background()
        draw = ImageDraw.Draw(img)

        # Use custom images if available and enabled
        if self.config.get('use_custom_images', False):
            # Draw main image (replaces coats)
            if self.main_image:
                main_size = tuple(self.config.get('main_image_size', [500, 500]))
                main_pos = tuple(self.config.get('main_image_position', [290, 450]))
                resized_main = self.main_image.resize(main_size, Image.Resampling.LANCZOS)
                img.paste(resized_main, main_pos, resized_main)

            # Draw blueprint/watermark image (positioned where text used to be)
            if self.blueprint_image:
                blueprint_size = tuple(self.config.get('blueprint_image_size', [178, 108]))
                blueprint_pos = tuple(self.config.get('blueprint_image_position', [451, 300]))
                resized_blueprint = self.blueprint_image.resize(blueprint_size, Image.Resampling.LANCZOS)
                img.paste(resized_blueprint, blueprint_pos, resized_blueprint)

            # Skip text drawing when using custom images (watermark replaces text)
        else:
            # Fallback to programmatic generation
            coats_y = 450
            self._draw_coats_minimal(draw, 150, coats_y, img.width - 300, 200)

            # Draw headline above main content - directly on background (no dark panel)
            headline_y = 250
            self._draw_text_minimal(img, headline, self.arabic_font,
                                   (img.width // 2, headline_y),
                                   self.config['text_color'])

            # Draw subheadline below headline - directly on background
            subheadline_font = ImageFont.truetype(self.arabic_font.path, self.config['font_size_subheadline'])
            self._draw_text_minimal(img, subheadline, subheadline_font,
                                   (img.width // 2, headline_y + 100),
                                   self.config['text_color'])

        # Draw brand at bottom if provided (always show brand)
        if brand:
            draw.text((img.width // 2 - len(brand) * 6, img.height - 80), brand,
                     font=self.brand_font, fill=(0, 0, 0))

        return img
    
    def generate_split_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate split layout with text on left, coats on right"""
        img = self._create_background()
        draw = ImageDraw.Draw(img)
        
        # Draw left panel for text (light)
        draw.rectangle([0, 0, img.width // 2, img.height], 
                      fill=(255, 255, 255, 150))
        
        # Draw right panel for coats (dark)
        draw.rectangle([img.width // 2, 0, img.width, img.height], 
                      fill=(0, 0, 0, 100))
        
        # Draw text on left side
        text_x = 50
        headline_y = 300
        self._draw_text_with_background(img, headline, self.arabic_font,
                                      (text_x, headline_y), (50, 50, 50))
        
        subheadline_font = ImageFont.truetype(self.arabic_font.path, self.config['font_size_subheadline'])
        self._draw_text_with_background(img, subheadline, subheadline_font,
                                      (text_x, headline_y + 100), (80, 80, 80))
        
        # Draw coats on right side
        self._draw_coats(draw, img.width // 2 + 20, 400, img.width // 2 - 40, 400)
        
        # Draw brand at bottom if provided
        if brand:
            draw.text((img.width // 2 - 50, img.height - 60), brand, 
                     font=self.brand_font, fill=(255, 255, 255))
        
        return img
    
    def generate_top_heavy_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate top-heavy layout with large text area at top"""
        img = self._create_background()
        draw = ImageDraw.Draw(img)
        
        # Draw large top panel for text
        draw.rectangle([0, 0, img.width, img.height * 2 // 3], 
                      fill=(255, 255, 255, 180))
        
        # Draw text in top section
        headline_y = 150
        self._draw_text_with_background(img, headline, self.arabic_font,
                                      (img.width // 2 - 250, headline_y), (50, 50, 50))
        
        subheadline_font = ImageFont.truetype(self.arabic_font.path, self.config['font_size_subheadline'])
        self._draw_text_with_background(img, subheadline, subheadline_font,
                                      (img.width // 2 - 200, headline_y + 100), (80, 80, 80))
        
        # Draw coats in bottom section
        coats_y = img.height * 2 // 3 + 50
        self._draw_coats(draw, 100, coats_y, img.width - 200, 200)
        
        # Draw brand at bottom if provided
        if brand:
            draw.text((img.width // 2 - 50, img.height - 60), brand, 
                     font=self.brand_font, fill=(255, 255, 255))
        
        return img
    
    def generate_bottom_heavy_layout(self, headline: str, subheadline: str, brand: str = None) -> Image.Image:
        """Generate bottom-heavy layout with large content area at bottom"""
        img = self._create_background()
        draw = ImageDraw.Draw(img)
        
        # Draw small top panel for text
        draw.rectangle([0, 0, img.width, img.height // 3], 
                      fill=(0, 0, 0, 150))
        
        # Draw text in top section
        headline_y = 80
        self._draw_text_with_background(img, headline, self.arabic_font,
                                      (img.width // 2 - 200, headline_y), 
                                      self.config['text_color'])
        
        subheadline_font = ImageFont.truetype(self.arabic_font.path, self.config['font_size_subheadline'])
        self._draw_text_with_background(img, subheadline, subheadline_font,
                                      (img.width // 2 - 150, headline_y + 70), 
                                      self.config['text_color'])
        
        # Draw large bottom panel
        draw.rectangle([0, img.height // 3, img.width, img.height], 
                      fill=(255, 255, 255, 200))
        
        # Draw coats in bottom section
        coats_y = img.height // 3 + 100
        self._draw_coats(draw, 100, coats_y, img.width - 200, 300)
        
        # Draw brand at bottom if provided
        if brand:
            draw.text((img.width // 2 - 50, img.height - 60), brand, 
                     font=self.brand_font, fill=(100, 100, 100))
        
        return img
    
    def generate_all_layouts(self, content: Dict[str, str], output_prefix: str = "social_post"):
        """Generate all four layout variations"""
        layouts = {
            'hero': self.generate_hero_layout,
            'split': self.generate_split_layout,
            'top_heavy': self.generate_top_heavy_layout,
            'bottom_heavy': self.generate_bottom_heavy_layout
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        for layout_name, layout_func in layouts.items():
            img = layout_func(
                content.get('headline', ''),
                content.get('subheadline', ''),
                content.get('brand', None)
            )
            
            output_path = os.path.join(self.output_dir, f"{output_prefix}_{layout_name}.png")
            img.save(output_path, 'PNG', quality=95)
            print(f"Generated: {output_path}")

def main():
    # Sample content
    content = {
        'headline': 'کت‌های زمستانی جدید',  # "New Winter Coats" in Farsi
        'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',  # "Collection of the best designs" in Farsi
        'brand': 'Fashion Store'
    }
    
    generator = SocialImageGenerator()
    generator.generate_all_layouts(content, "farsi_coats_post")
    print("All layouts generated successfully!")

if __name__ == "__main__":
    main()
