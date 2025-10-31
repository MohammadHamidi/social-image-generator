# Hero Text Replacement and Rich Text Support Plan

## Overview

Enhance the `yuan_payment_carousel` layout to:
1. Support text in the hero image area (alternative to image)
2. Add rich text formatting support for all text elements
3. Support text justification (left, center, right, justify)

## Requirements

### 1. Hero Area Text Replacement
- When `hero_image_url` is not provided, use `hero_text` instead
- Hero text should fill the same area as hero image (350x350px area)
- Support text justification options (centered, left, right, justify)
- Support multiple lines with proper wrapping

### 2. Rich Text Formatting
- Parse text with markdown-like syntax or simple tags
- Support formats: **bold**, *italic*, colored text, different sizes
- Syntax options:
  - Option A: Markdown-style (`**bold**`, `*italic*`, `#color:red#text#`)
  - Option B: HTML-like tags (`<b>bold</b>`, `<i>italic</i>`, `<color="red">text</color>`)
  - Option C: Simple tags (`{b}bold{/b}`, `{i}italic{/i}`, `{color:red}text{/color}`)
- Apply to: title, hero_text, description, subtitle, footer_text

## Implementation Plan

### Phase 1: Rich Text Parser

**Create `_parse_rich_text()` method:**
- Parse text with formatting tags
- Return list of (text, style) tuples
- Styles: bold, italic, color, size
- Example: `"Hello **bold** world"` → `[("Hello ", {}), ("bold", {"bold": True}), (" world", {})]`

**Create `_draw_rich_text()` method:**
- Draw text with multiple styles
- Handle font changes (bold/italic)
- Handle color changes
- Handle size changes
- Support RTL text with formatting

### Phase 2: Hero Text Area

**Update `_render_centered_portrait()` method:**
- Check if `hero_image_url` exists OR `hero_text` exists
- If `hero_text` provided and no image:
  - Render text in hero area (350x350px equivalent space)
  - Support justification options
  - Use rich text formatting
- If both provided, prioritize image (or allow option to choose)

**Create `_add_hero_text()` method:**
- Render text in hero image area
- Support justification (center, left, right, justify)
- Support rich text formatting
- Calculate proper sizing to fill area

### Phase 3: Text Justification Support

**Update all text rendering methods:**
- Add `text_align` option support to:
  - `_add_title_section()` - support left/center/right
  - `_add_text_block()` - support left/center/right/justify
  - `_add_subtitle()` - support left/center/right
  - `_add_hero_text()` - support left/center/right/justify

**Implement justification logic:**
- Center: Calculate center position for each line
- Left: Use x position directly
- Right: Calculate right-aligned position
- Justify: Distribute spaces evenly (for multi-line text)

### Phase 4: Content Field Updates

**Add new content fields:**
- `hero_text` - Text to display in hero area instead of image
- Keep `hero_image_url` optional

**Add new options:**
- `hero_mode` - 'image' (default) or 'text'
- `hero_text_align` - 'center' (default), 'left', 'right', 'justify'
- `hero_text_color` - RGB array or string
- `hero_text_size` - int (default: calculated based on area)
- `title_align` - 'center' (default), 'left', 'right'
- `description_align` - 'center' (default), 'left', 'right', 'justify'
- `subtitle_align` - 'center' (default), 'left', 'right'
- `enable_rich_text` - bool (default: true) - Enable rich text parsing

## Rich Text Syntax Design

Recommended: Simple markdown-style with color support

```
**bold text**
*italic text*
***bold and italic***
#color:red#colored text#
#size:36#larger text#
```

Example:
```
"Hello **world**, this is *italic* and #color:yellow#yellow text#"
```

## Implementation Details

### File: `src/layouts/yuan_payment_carousel.py`

1. **Add `_parse_rich_text()` method:**
   - Parse text for `**bold**`, `*italic*`, `#color:value#text#`, `#size:value#text#`
   - Return list of (text, styles) tuples
   - Handle nested formatting

2. **Add `_draw_rich_text()` method:**
   - Draw text segments with different styles
   - Handle font switching (regular/bold/italic)
   - Handle color switching
   - Support RTL text

3. **Add `_add_hero_text()` method:**
   - Render text in hero image area (350x350px space)
   - Support alignment options
   - Support rich text
   - Calculate font size to fill area appropriately

4. **Update `_render_centered_portrait()`:**
   - Check for hero_text when no image
   - Call `_add_hero_text()` if text provided
   - Maintain same spacing as with image

5. **Update all text rendering methods:**
   - Add alignment parameter support
   - Use `_draw_rich_text()` for rich text rendering
   - Fall back to simple text if rich text disabled

## Schema Updates

```json
{
  "content": {
    "title": "**Bold Title** with normal text",
    "hero_text": "#color:yellow#Hero Text# in hero area",
    "description": "*Italic* description text",
    "subtitle": "**Bold** subtitle"
  },
  "options": {
    "hero_mode": "text",
    "hero_text_align": "center",
    "hero_text_color": [255, 215, 0],
    "hero_text_size": 48,
    "title_align": "center",
    "description_align": "justify",
    "subtitle_align": "center",
    "enable_rich_text": true
  }
}
```

## Testing Checklist

- [ ] Hero text displays when hero_image_url is not provided
- [ ] Hero text fills hero image area properly
- [ ] Hero text supports all alignment options
- [ ] Rich text parsing works for bold/italic
- [ ] Rich text parsing works for colors
- [ ] Rich text parsing works for sizes
- [ ] Rich text works with RTL text
- [ ] All text elements support alignment options
- [ ] Justification works for multi-line text
- [ ] Rich text disabled mode falls back to plain text

