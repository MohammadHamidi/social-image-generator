# Text Visibility Guide for Enhanced Social Image Generator

## 🎯 Problem Solved

**Issue**: Text was not displaying correctly on custom images due to transparency and positioning conflicts.

**Solution**: Enhanced text rendering with automatic background panels for visibility.

## 📋 Key Improvements

### ✅ Automatic Text Backgrounds
- **Custom Images**: White semi-transparent backgrounds for black text
- **Programmatic Generation**: Dark semi-transparent backgrounds for white text
- **Smart Positioning**: Text positioned to avoid image overlap

### ✅ Enhanced Color Management
- **Dynamic Colors**: Text colors adapt based on background type
- **Contrast Optimization**: Automatic contrast adjustment for readability
- **Brand Consistency**: Maintains your brand colors while ensuring visibility

## 🚀 Quick Usage

### Basic Usage with Custom Images
```python
from src.enhanced_social_generator import EnhancedSocialImageGenerator

# Load enhanced configuration
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

img.save('output/visible_text_image.png', 'PNG')
```

### Programmatic Generation (No Custom Images)
```python
# Uses default programmatic generation
generator = EnhancedSocialImageGenerator()

img = generator.generate_enhanced_hero_layout(
    "Your Headline",
    "Your Subheadline",
    "Your Brand"
)
```

## 🎨 Text Positioning & Styling

### Layout Structure:
```
┌─────────────────────────────────────┐
│           Headline Text             │ ← Top with white/black background
│         Subheadline Text            │ ← Below headline
│                                     │
│         [Custom Main Image]         │ ← Your main content
│                                     │
│        [Blueprint/Watermark]        │ ← Your secondary image
│                                     │
│           Brand Name                │ ← Bottom with white background
└─────────────────────────────────────┘
```

### Text Properties:
- **Headline**: Large, prominent, top positioning
- **Subheadline**: Medium size, below headline
- **Brand**: Small, bottom positioning
- **Backgrounds**: Semi-transparent for visibility
- **Colors**: Automatic contrast optimization

## ⚙️ Configuration Options

### Custom Images Mode:
```json
{
    "custom_images": {
        "use_custom_images": true
    },
    "layout_colors": {
        "hero": {
            "headline_color": [0, 0, 0],
            "subheadline_color": [0, 0, 0],
            "brand_color": [0, 0, 0]
        }
    }
}
```

### Programmatic Mode:
```json
{
    "custom_images": {
        "use_custom_images": false
    },
    "layout_colors": {
        "hero": {
            "headline_color": [255, 255, 255],
            "subheadline_color": [220, 220, 220],
            "brand_color": [200, 200, 200]
        }
    }
}
```

## 🔧 Troubleshooting

### Text Still Not Visible?
1. **Check Image Transparency**: Ensure your custom images aren't interfering
2. **Verify Colors**: Black text on white backgrounds should always be visible
3. **Background Opacity**: Adjust the alpha values in configuration

### Arabic Text Issues?
1. **Font Loading**: SF Arabic font should load automatically
2. **Text Processing**: Arabic reshaping is handled automatically
3. **RTL Support**: Right-to-left text rendering is built-in

### Custom Positioning?
```python
# Modify text positions in the configuration
"custom_images": {
    "main_image_position": [240, 450],
    "blueprint_image_position": [850, 200]
}
```

## 📁 Generated Files

After running the enhanced generator, you'll get:

- `output/enhanced_visible_text.png` - Your main result
- `output/comparison_original.png` - Original approach
- `output/comparison_enhanced.png` - Enhanced approach
- Various demo files from `demo_enhanced_features.py`

## 🎉 Result

**Before**: Text was hidden behind custom images
**After**: Text has white/black backgrounds ensuring perfect visibility

The enhanced generator now automatically handles text visibility while maintaining the beautiful design of your custom images! ✨
