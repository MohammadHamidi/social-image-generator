# Hero Text Replacement and Rich Text Support

## Overview

The `yuan_payment_carousel` layout now supports:
1. **Hero text replacement** - Display text in the hero image area instead of an image
2. **Rich text formatting** - Apply formatting to all text elements (bold, italic, colors, sizes)
3. **Text alignment** - Control text alignment for all text elements (left, center, right, justify)

## Hero Text Feature

### Usage

Instead of providing a hero image, you can provide `hero_text` in the `content` object:

```json
{
  "content": {
    "title": "Welcome",
    "hero_text": "重要通知\nPayment System",
    "description": "Description here"
  },
  "options": {
    "hero_mode": "text"
  }
}
```

### Hero Mode Options

- `"auto"` (default) - Automatically choose: use image if `hero_image_url` is provided, otherwise use `hero_text`
- `"image"` - Force use of image (if `hero_image_url` is provided)
- `"text"` - Force use of text (requires `hero_text` in content)

### Hero Text Options

- `hero_text_align`: `'center'` (default), `'left'`, `'right'`, `'justify'`
- `hero_text_color`: RGB array `[255, 215, 0]` or color string `'yellow'`
- `hero_text_size`: Integer (default: 48)

## Rich Text Formatting

All text fields now support rich text formatting using simple markdown-like syntax:

### Supported Formats

1. **Bold**: `**text**` or `__text__`
   - Example: `"Hello **world**"`
   
2. **Italic**: `*text*` or `_text_`
   - Example: `"This is *italic*"`
   
3. **Bold Italic**: `***text***`
   - Example: `"***Bold and italic***"`
   
4. **Color**: `#color:red#text#` or `#color:255,0,0#text#`
   - Example: `"#color:yellow#Important# message"`
   - Supported color names: `red`, `yellow`, `white`, `black`, `blue`, `green`
   - Or use RGB: `#color:255,215,0#text#`
   
5. **Size**: `#size:48#text#`
   - Example: `"Normal #size:56#Large# text"`

### Enable/Disable Rich Text

```json
{
  "options": {
    "enable_rich_text": true  // default: true
  }
}
```

## Text Alignment

All text elements now support alignment options:

### Title Alignment
```json
{
  "options": {
    "title_align": "center"  // 'center' (default), 'left', 'right'
  }
}
```

### Description Alignment
```json
{
  "options": {
    "description_align": "justify"  // 'center' (default), 'left', 'right', 'justify'
  }
}
```

### Subtitle Alignment
```json
{
  "options": {
    "subtitle_align": "center"  // 'center' (default), 'left', 'right'
  }
}
```

### Hero Text Alignment
```json
{
  "options": {
    "hero_text_align": "center"  // 'center' (default), 'left', 'right', 'justify'
  }
}
```

## Complete Example

```json
{
  "layout_type": "yuan_payment_carousel",
  "content": {
    "title": "**Welcome** to Yuan Payment",
    "hero_text": "#color:yellow#重要通知#\n**Payment System**\n*Now Available*",
    "description": "This is a **bold** description with *italic* text and #color:yellow#colored text#. You can mix formatting easily.",
    "subtitle": "*Learn more* about our services"
  },
  "assets": {
    "hero_image_url": "",
    "logo_url": ""
  },
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [
        [194, 0, 0],
        [150, 0, 0]
      ],
      "direction": "vertical"
    }
  },
  "options": {
    "layout_style": "centered_portrait",
    "hero_mode": "text",
    "hero_text_align": "center",
    "hero_text_color": [255, 215, 0],
    "hero_text_size": 56,
    "title_align": "center",
    "description_align": "justify",
    "subtitle_align": "center",
    "enable_rich_text": true,
    "show_slide_number": false,
    "show_brand_footer": true,
    "text_color": "white"
  }
}
```

## Features Summary

### ✅ Hero Text
- [x] Text can replace hero image
- [x] Supports rich text formatting
- [x] Supports alignment (center, left, right, justify)
- [x] Configurable color and size
- [x] Auto-mode selects image or text automatically

### ✅ Rich Text
- [x] Bold (`**text**`, `__text__`)
- [x] Italic (`*text*`, `_text_`)
- [x] Bold Italic (`***text***`)
- [x] Colors (`#color:red#text#`, `#color:255,0,0#text#`)
- [x] Sizes (`#size:48#text#`)
- [x] Works with RTL/Persian text
- [x] Can be disabled with `enable_rich_text: false`

### ✅ Text Alignment
- [x] Title: center, left, right
- [x] Description: center, left, right, justify
- [x] Subtitle: center, left, right
- [x] Hero text: center, left, right, justify
- [x] Justification distributes space evenly

## Notes

- Rich text parsing is enabled by default (`enable_rich_text: true`)
- If rich text is disabled, all tags are treated as plain text
- Hero text fills the same area as hero images (350x350px by default)
- Alignment options are independent for each text element
- Rich text works with both LTR and RTL text
- Colors can be specified by name or RGB tuple

## See Also

- See `examples/yuan_payment_carousel/hero_text_example.json` for a complete example
- Rich text formatting is applied to: title, hero_text, description, subtitle

