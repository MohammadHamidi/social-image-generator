# Enhanced Social Image Generator

This guide explains how to use the enhanced Social Image Generator with advanced background removal, custom images, and granular color control.

## ✨ New Features

### 🖼️ **Background Removal**
- **AI-powered removal** using rembg (automatic subject detection)
- **Edge detection fallback** for when AI isn't available
- **Color threshold removal** for solid backgrounds
- **Configurable sensitivity** and methods

### 🎨 **Advanced Color Control**
- **Layout-specific color schemes** (hero, split, top-heavy, bottom-heavy)
- **Multiple background types** (solid, gradient, pattern)
- **Gradient directions** (horizontal, vertical, diagonal, radial)
- **Individual text element colors** (headline, subheadline, brand)
- **Panel opacity and colors** for perfect text readability

### 🖼️ **Custom Images Integration**
- **Main Section Image**: Replaces the programmatically generated coat shapes
- **Blueprint/Watermark Image**: Adds a secondary image (like a logo, pattern, or watermark)
- **Automatic background removal** for seamless integration
- **Flexible positioning and sizing**

## Quick Start

### 1. Install Enhanced Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Demo

```bash
python demo_enhanced_features.py
```

### 3. Use Enhanced Generator

```python
from src.enhanced_social_generator import EnhancedSocialImageGenerator

# Load with custom theme
generator = EnhancedSocialImageGenerator("config/enhanced_modern_theme.json")

content = {
    'headline': 'کت‌های زمستانی جدید',
    'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
    'brand': 'Fashion Store'
}

img = generator.generate_enhanced_hero_layout(
    content['headline'],
    content['subheadline'],
    content['brand']
)

img.save('output/enhanced_social_post.png', 'PNG')
```

## Setup Instructions

### 1. Prepare Your Images

Create two PNG images (transparent or with white background):

```
assets/custom/
├── main_section.png    # Your main content image
└── blueprint.png       # Your watermark/blueprint image
```

### 2. Configure the Generator

Edit `config/default_config.json` to enable custom images:

```json
{
    "use_custom_images": true,
    "main_image_path": "assets/custom/main_section.png",
    "blueprint_image_path": "assets/custom/blueprint.png",
    "main_image_size": [600, 400],
    "blueprint_image_size": [200, 150],
    "main_image_position": [240, 450],
    "blueprint_image_position": [850, 200]
}
```

### 3. Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `use_custom_images` | Enable/disable custom images | `true` |
| `main_image_path` | Path to main content image | `"assets/custom/main_section.png"` |
| `blueprint_image_path` | Path to blueprint/watermark image | `"assets/custom/blueprint.png"` |
| `main_image_size` | Size of main image [width, height] | `[600, 400]` |
| `blueprint_image_size` | Size of blueprint image [width, height] | `[200, 150]` |
| `main_image_position` | Position of main image [x, y] | `[240, 450]` |
| `blueprint_image_position` | Position of blueprint image [x, y] | `[850, 200]` |

## Usage Examples

### Python API

```python
from src.social_image_generator import SocialImageGenerator

# With custom images
generator = SocialImageGenerator("config/custom_images_example.json")

content = {
    'headline': 'Your Headline',
    'subheadline': 'Your Subheadline',
    'brand': 'Your Brand'
}

img = generator.generate_hero_layout(
    content['headline'],
    content['subheadline'],
    content['brand']
)

img.save('output/custom_social_post.png', 'PNG')
```

### Command Line

```bash
# Generate with custom images
python generate_with_custom_images.py

# Or use the demo script
python -c "
import sys
sys.path.append('src')
from social_image_generator import SocialImageGenerator

generator = SocialImageGenerator('config/custom_images_example.json')
img = generator.generate_hero_layout('Test', 'Subtitle', 'Brand')
img.save('output/test.png', 'PNG')
"
```

## Image Requirements

### Main Section Image
- **Format**: PNG (transparent or white background)
- **Recommended Size**: 600x400 pixels (configurable)
- **Purpose**: Replaces the colored coat rectangles
- **Position**: Centered in the main content area

### Blueprint/Watermark Image
- **Format**: PNG (transparent or white background)
- **Recommended Size**: 200x150 pixels (configurable)
- **Purpose**: Logo, pattern, or secondary graphic element
- **Position**: Typically in corner or alongside main content

## Fallback Behavior

If custom images are not found or loading fails, the generator automatically falls back to programmatic generation using the default shapes and colors.

## Tips for Best Results

1. **Transparency**: Use transparent PNGs for seamless integration
2. **Resolution**: High-resolution images (300 DPI recommended)
3. **Aspect Ratio**: Plan your images to fit the configured sizes
4. **Testing**: Test different sizes and positions to get perfect placement
5. **Backup**: Keep programmatic generation as fallback option

## Example Layout

```
┌─────────────────────────────────────┐
│           Headline Text             │ ← White text on background
│         Subheadline Text            │ ← White text on background
│                                     │
│    ┌─────────────────────────┐      │
│    │                         │      │
│    │    Main Section Image    │      │ ← Your custom image
│    │    (600x400)            │      │
│    │                         │      │
│    └─────────────────────────┘      │
│                                     │
│                    Blueprint Image  │ ← Your watermark (200x150)
│                        (850,200)    │
│                                     │
│           Brand Name                │ ← White text
└─────────────────────────────────────┘
```

## Troubleshooting

- **Images not loading**: Check file paths and permissions
- **Wrong positioning**: Adjust position coordinates in config
- **Poor quality**: Ensure high-resolution source images
- **Transparency issues**: Verify PNG format and alpha channel
