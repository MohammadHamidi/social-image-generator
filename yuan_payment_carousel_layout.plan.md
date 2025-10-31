# Yuan Payment Carousel Layout - Implementation Plan

## Overview

Create a new `yuan_payment_carousel` layout that replicates the Yuan Payment Instagram carousel style with support for both custom uploaded images and random placeholder images.

## Requirements Summary

### Design Specifications
- **Aspect Ratio**: 1:1 (1080×1080 px) - square format
- **Background**: Solid red (#C20000 to #A80000) with optional gradient/overlay
- **Text Colors**: Yellow (#FFD700) and White (#FFFFFF) for Persian/Farsi text
- **Layout Variations**: 5+ sub-layout types (centered portrait, symbol focus, product layout, split-screen, gradient)
- **Brand Elements**: Logo area (top), brand footer (bottom) with pagoda + yuan symbol
- **Supporting Icons**: FAKE badges, checkmarks, yuan icons, decorative elements
- **Slide Numbering**: Display slide number (e.g., "1/5") in top-right corner

### Functional Requirements
1. **Dual Image Support**: 
   - Custom uploaded images (via `hero_image_url` in assets)
   - Random placeholder images (via `use_random_image: true` or fallback logic)
2. **Persian/Farsi Text**: Full RTL support with proper text rendering
3. **Multiple Layout Variations**: Support different visual arrangements per slide
4. **Carousel Integration**: Works with existing carousel generation infrastructure
5. **Error Handling**: Graceful fallback when images fail to load

## Implementation Plan

### Phase 1: Create Base Layout Class

**File**: `src/layouts/yuan_payment_carousel.py`

**Class Structure**:
```python
@register_layout
class YuanPaymentCarouselLayout(CarouselLayoutEngine):
    LAYOUT_TYPE = "yuan_payment_carousel"
    LAYOUT_CATEGORY = "carousel_multi_slide"
    SUPPORTS_CAROUSEL = True
    
    # Default square dimensions
    DEFAULT_WIDTH = 1080
    DEFAULT_HEIGHT = 1080
```

**Key Methods to Implement**:
1. `render()` - Main rendering method
2. `_create_background()` - Red background with optional gradient
3. `_add_logo_area()` - Top logo section with slide number
4. `_add_main_visual()` - Main image/symbol area (supports custom or random)
5. `_add_text_sections()` - Title and content text blocks
6. `_add_brand_footer()` - Bottom brand area with pagoda + yuan symbol
7. `_add_supporting_icons()` - FAKE badges, checkmarks, etc.

### Phase 2: Image Loading Strategy

**Custom Images**:
- Use existing `asset_manager.load_asset()` with `hero_image_url` from assets
- Support local paths, URLs, and uploaded files
- Apply background removal if needed

**Random/Placeholder Images**:
- Add option `use_random_image: true` in options
- When enabled or when `hero_image_url` is missing, generate/load random image
- Options:
  - **Option A**: Use `picsum.photos` API with random seed (`https://picsum.photos/800/800?random={seed}`)
  - **Option B**: Generate gradient/pattern placeholder programmatically
  - **Option C**: Use predefined set of placeholder images from assets folder
- Store random seed in options for consistency across slides

**Implementation**:
```python
def _load_main_image(self) -> Image.Image:
    """Load main image - either custom or random."""
    hero_url = self.assets.get('hero_image_url')
    use_random = self.options.get('use_random_image', False)
    
    if hero_url and not use_random:
        # Load custom image
        return self._load_custom_image(hero_url)
    else:
        # Generate/load random image
        return self._load_random_image()
```

### Phase 3: Layout Variations

**Sub-layout Types** (via `options.layout_style`):

1. **`centered_portrait`**: 
   - Person/portrait in center
   - Title at top
   - Small caption at bottom
   - Icons on sides (FAKE left, checkmark right)

2. **`symbol_focus`**:
   - Large yuan currency symbol in center
   - Title at top
   - Text box at bottom
   - Gradient fade background

3. **`product_layout`**:
   - Products displayed on white/light background
   - Title above products
   - Bullet points below
   - Clean, minimalist

4. **`split_screen`**:
   - Two hands/figures exchanging yuan
   - Text columns left/right
   - Comparison checklist (SWIFT vs CNY)

5. **`gradient_background`**:
   - Soft gradient background
   - Title at top
   - Bullet list in middle
   - Brand footer at bottom
   - Light feminine color scheme

**Implementation**:
```python
def render(self) -> List[Image.Image]:
    canvas = self._create_background()
    
    layout_style = self.options.get('layout_style', 'centered_portrait')
    
    # Apply layout-specific rendering
    if layout_style == 'centered_portrait':
        canvas = self._render_centered_portrait(canvas)
    elif layout_style == 'symbol_focus':
        canvas = self._render_symbol_focus(canvas)
    # ... etc
```

### Phase 4: Text Rendering

**Text Areas**:
1. **Title Block**: Large bold Persian text, center-aligned, yellow/white
2. **Subtitle/Subheading**: Medium weight, below title
3. **Content Box**: Rounded rectangle with body text, left-aligned
4. **Bullet Points**: List items with custom bullet shapes

**Features**:
- RTL support for Persian/Farsi text (use existing `_is_rtl_text()`, `_prepare_arabic_text()`)
- Text wrapping with proper line breaks
- Dynamic font sizing based on canvas size
- Color contrast checking (yellow/white on red background)

**Implementation**:
- Reuse existing base class text rendering methods
- Add Yuan Payment specific fonts (IRANYekan for Persian)
- Support text highlighting (key phrases in different colors)

### Phase 5: Design Elements

**Logo Area** (Top Section):
- "Yuan Payment" logo (optional, from assets)
- Slide counter: "1/5", "2/5", etc. (top-right corner)
- Position: Top center or top-left with 60px padding

**Brand Footer** (Bottom Section):
- Decorative wave/curved separator (black/yellow/red)
- Brand icon: Pagoda + yuan symbol (optional, from assets)
- Social handles: `@yuanpayment`, `@yuan-payment` with Instagram icons
- Navigation arrows: `>>` or `next` indicator

**Supporting Icons**:
- **FAKE badge**: Red warning icon, positioned relative to main image
- **Checkmarks**: Green check icons for validation
- **Yuan symbols**: Currency symbols as decorative elements
- **Icons**: PNG files from assets folder, positioned dynamically

**Implementation**:
```python
def _add_supporting_icons(self, canvas: Image.Image, icon_type: str, position: str) -> Image.Image:
    """Add supporting icons (FAKE, checkmarks, etc.)"""
    icon_path = self._get_icon_path(icon_type)
    if icon_path:
        icon = Image.open(icon_path)
        # Resize and position
        canvas.paste(icon, position, icon if icon.mode == 'RGBA' else None)
    return canvas
```

### Phase 6: Integration

**Register Layout**:
- Add import in `src/layouts/__init__.py`
- Layout auto-discovery will pick it up
- Add to API endpoint layout list

**Schema Definition**:
- Define required/optional content fields
- Document all options
- Provide example JSON configurations

**Testing**:
- Test with custom images
- Test with random images
- Test with various layout styles
- Test Persian/Farsi text rendering
- Test error handling (missing images, invalid URLs)

## File Structure

```
src/layouts/
  └── yuan_payment_carousel.py       # Main layout implementation

examples/
  └── yuan_payment_carousel/
      ├── example_1_centered.json     # Example: centered portrait
      ├── example_2_symbol.json      # Example: symbol focus
      ├── example_3_product.json      # Example: product layout
      ├── example_4_split.json       # Example: split screen
      ├── example_5_gradient.json    # Example: gradient background
      └── example_full_carousel.json  # Complete 5-slide carousel

assets/
  └── yuan_payment/
      ├── logo.png                    # Yuan Payment logo (optional)
      ├── pagoda-icon.png            # Brand footer icon (optional)
      ├── fake-badge.png             # FAKE warning icon
      ├── checkmark.png              # Checkmark icon
      └── yuan-symbol.png            # Yuan currency symbol
```

## JSON Schema Example

```json
{
  "layout_type": "yuan_payment_carousel",
  "content": {
    "title": "عنوان اصلی",
    "subtitle": "زیرعنوان (اختیاری)",
    "body_text": "متن توضیحات در اینجا قرار می‌گیرد...",
    "bullets": ["نکته اول", "نکته دوم", "نکته سوم"]
  },
  "assets": {
    "hero_image_url": "https://imageeditor.flowiran.ir/uploads/main/image.png",
    "logo_url": "uploads/yuan_payment/logo.png"
  },
  "background": {
    "mode": "solid_color",
    "color": [194, 0, 0]
  },
  "options": {
    "layout_style": "centered_portrait",
    "use_random_image": false,
    "random_image_seed": 123,
    "show_slide_number": true,
    "slide_number": 1,
    "total_slides": 5,
    "show_logo": true,
    "show_brand_footer": true,
    "title_color": [255, 215, 0],
    "subtitle_color": [255, 255, 255],
    "body_text_color": [255, 255, 255],
    "supporting_icons": ["fake_badge", "checkmark"]
  }
}
```

## Implementation Checklist

### Phase 1: Base Structure
- [ ] Create `yuan_payment_carousel.py` file
- [ ] Define layout class extending `CarouselLayoutEngine`
- [ ] Set up default dimensions (1080x1080)
- [ ] Register layout with `@register_layout` decorator
- [ ] Implement basic `render()` method
- [ ] Add layout to `__init__.py` imports

### Phase 2: Background & Canvas
- [ ] Implement `_create_background()` with red color
- [ ] Support gradient backgrounds
- [ ] Support image backgrounds with overlay
- [ ] Add background color customization options

### Phase 3: Image Loading
- [ ] Implement `_load_custom_image()` for uploaded images
- [ ] Implement `_load_random_image()` using picsum.photos
- [ ] Add fallback logic when images fail
- [ ] Support background removal for hero images
- [ ] Add random seed support for consistent random images

### Phase 4: Layout Variations
- [ ] Implement `centered_portrait` layout
- [ ] Implement `symbol_focus` layout
- [ ] Implement `product_layout` layout
- [ ] Implement `split_screen` layout
- [ ] Implement `gradient_background` layout
- [ ] Add layout style routing in `render()`

### Phase 5: Text Elements
- [ ] Implement title rendering (top section)
- [ ] Implement subtitle rendering
- [ ] Implement content box with rounded rectangle
- [ ] Implement bullet list rendering
- [ ] Add Persian/Farsi RTL support
- [ ] Add text color customization

### Phase 6: UI Elements
- [ ] Implement logo area (top)
- [ ] Implement slide number display (top-right)
- [ ] Implement brand footer (bottom)
- [ ] Implement decorative separator/wave
- [ ] Add social handle text rendering
- [ ] Add navigation arrows

### Phase 7: Icons & Graphics
- [ ] Create/obtain icon assets (FAKE, checkmark, yuan symbol)
- [ ] Implement icon loading from assets folder
- [ ] Implement icon positioning logic
- [ ] Add icon scaling and styling
- [ ] Support custom icon URLs

### Phase 8: Integration & Testing
- [ ] Register layout in layout registry
- [ ] Add layout to API endpoints
- [ ] Create example JSON configurations
- [ ] Test with custom images
- [ ] Test with random images
- [ ] Test all layout variations
- [ ] Test Persian/Farsi text rendering
- [ ] Test error handling
- [ ] Update documentation

## Dependencies

- Existing infrastructure:
  - `CarouselLayoutEngine` base class
  - `asset_manager` for image loading
  - Persian/Farsi text rendering utilities
  - Color utilities
  - Font manager

- New dependencies:
  - `requests` library (already used) for picsum.photos API
  - Icon assets (PNG files)

## Notes

1. **Random Images**: Use `picsum.photos` API which is already used in examples. Format: `https://picsum.photos/{width}/{height}?random={seed}`

2. **Aspect Ratio**: Force 1:1 (1080x1080) even if canvas dimensions suggest otherwise

3. **Brand Elements**: Make logo and footer icons optional - layout should work without them

4. **Backward Compatibility**: Ensure layout works with existing carousel generation infrastructure

5. **Performance**: Cache random images or use consistent seeds for faster generation

## Success Criteria

- [ ] Layout generates valid 1080x1080 images
- [ ] Supports both custom and random images
- [ ] All 5 layout variations work correctly
- [ ] Persian/Farsi text renders properly (RTL)
- [ ] All design elements (logo, footer, icons) display correctly
- [ ] Error handling works (missing images, invalid URLs)
- [ ] Integrates with existing carousel API
- [ ] Example configurations provided
- [ ] Documentation updated

