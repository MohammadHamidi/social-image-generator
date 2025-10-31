# Yuan Payment Carousel Layout - Implementation Complete

## Overview

The `yuan_payment_carousel` layout has been successfully implemented and is ready to use. This layout creates Instagram carousel posts in the Yuan Payment style with support for both custom uploaded images and random placeholder images.

## Features Implemented

✅ **Base Layout Structure**
- Square format (1080×1080 px)
- Red background (#C20000) with customization options
- Support for solid colors, gradients, and image backgrounds

✅ **Dual Image Support**
- **Custom Images**: Via `hero_image_url` in assets (local files, URLs, uploaded files)
- **Random Images**: Via `use_random_image: true` using picsum.photos API
- Automatic fallback when images fail to load

✅ **Layout Variations** (5 styles)
1. **centered_portrait** - Person/portrait centered with supporting icons
2. **symbol_focus** - Large yuan symbol with text box
3. **product_layout** - Product showcase on white background
4. **split_screen** - Split comparison view with text columns
5. **gradient_background** - Soft gradient with bullet list

✅ **Text Rendering**
- Persian/Farsi RTL support with proper text wrapping
- Multiple text sections (title, subtitle, body, bullets)
- Customizable colors (yellow/white on red background)
- Dynamic font sizing

✅ **UI Elements**
- Logo area (top) with optional logo image
- Slide number indicator (top-right, e.g., "1/5")
- Brand footer (bottom) with decorative separator
- Social handles text (@yuanpayment)

✅ **Supporting Icons**
- FAKE badges
- Checkmarks
- Yuan symbols
- Custom icons via `icon_urls` in assets

✅ **Integration**
- Registered with layout system
- Works with existing carousel API
- Example configurations provided

## Quick Start

### Basic Usage

```json
{
  "layout_type": "yuan_payment_carousel",
  "content": {
    "title": "عنوان اصلی",
    "subtitle": "زیرعنوان"
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
```

### With Random Images

```json
{
  "layout_type": "yuan_payment_carousel",
  "content": {
    "title": "پرداخت با یوان چینی",
    "body_text": "متن توضیحات..."
  },
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [[194, 0, 0], [168, 0, 0]],
      "direction": "vertical"
    }
  },
  "options": {
    "layout_style": "symbol_focus",
    "use_random_image": true,
    "random_image_seed": 1234,
    "slide_number": 2,
    "total_slides": 5
  }
}
```

## Layout Styles

### 1. centered_portrait
- **Use Case**: Person/portrait photos with supporting icons
- **Features**: Large centered image, title at top, subtitle at bottom, FAKE/checkmark icons

### 2. symbol_focus
- **Use Case**: Educational content with yuan symbol emphasis
- **Features**: Large symbol in center, title at top, text box at bottom

### 3. product_layout
- **Use Case**: Product showcases
- **Features**: Products on white background, title above, bullet points below

### 4. split_screen
- **Use Case**: Comparison views
- **Features**: Image on left, text columns on right, bullet lists

### 5. gradient_background
- **Use Case**: Soft, elegant layouts
- **Features**: Soft gradient background, title at top, bullet list in middle

## Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `layout_style` | string | `centered_portrait` | Layout variation to use |
| `use_random_image` | bool | `false` | Use random placeholder if no hero_image_url |
| `random_image_seed` | int | random | Seed for consistent random images |
| `show_slide_number` | bool | `true` | Show slide counter (top-right) |
| `slide_number` | int | 1 | Current slide number (1-based) |
| `total_slides` | int | 1 | Total slides in carousel |
| `show_logo` | bool | `true` | Show logo in top area |
| `show_brand_footer` | bool | `true` | Show brand footer at bottom |
| `title_color` | [R,G,B] | `[255,215,0]` | Yellow |
| `subtitle_color` | [R,G,B] | `[255,255,255]` | White |
| `body_text_color` | [R,G,B] | `[255,255,255]` | White |
| `supporting_icons` | array | `[]` | List of icons: `['fake_badge', 'checkmark']` |

## Example Files

All examples are in `examples/yuan_payment_carousel/`:

- `example_1_centered_portrait.json` - Centered portrait layout
- `example_2_symbol_focus.json` - Symbol focus with random image
- `example_3_product_layout.json` - Product showcase
- `example_4_split_screen.json` - Split screen comparison
- `example_5_gradient_background.json` - Gradient background
- `example_full_carousel.json` - Complete 5-slide carousel

## Testing

Test the layout via API:

```bash
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/yuan_payment_carousel/example_1_centered_portrait.json
```

Or generate a full carousel:

```bash
python generate_instagram_carousel.py examples/yuan_payment_carousel/example_full_carousel.json
```

## File Structure

```
src/layouts/
  └── yuan_payment_carousel.py       # Main layout implementation

examples/
  └── yuan_payment_carousel/
      ├── example_1_centered_portrait.json
      ├── example_2_symbol_focus.json
      ├── example_3_product_layout.json
      ├── example_4_split_screen.json
      ├── example_5_gradient_background.json
      └── example_full_carousel.json

assets/
  └── yuan_payment/                  # Optional icon assets
      ├── fake-badge.png
      ├── checkmark.png
      ├── yuan-symbol.png
      └── pagoda-icon.png
```

## Notes

1. **Random Images**: Uses `picsum.photos` API. Set `random_image_seed` for consistency across slides.

2. **Icons**: Icons are optional. The layout will work without them. Place icon files in `assets/yuan_payment/` or provide URLs via `icon_urls` in assets.

3. **Persian/Farsi Text**: Fully supported with RTL rendering. Uses IRANYekan fonts when available.

4. **Error Handling**: Gracefully handles missing images, failed loads, and invalid URLs.

5. **Customization**: All colors, fonts, and positions can be customized via options.

## Next Steps

1. Test with your own images and content
2. Customize colors and styles to match your brand
3. Add custom icons to `assets/yuan_payment/` folder
4. Generate full carousels using the carousel API

## Support

For issues or questions:
- Check example configurations
- Review error logs for image loading issues
- Ensure Persian fonts are available in `assets/fonts/`

