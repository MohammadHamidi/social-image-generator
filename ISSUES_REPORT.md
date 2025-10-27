# Image Generation Issues Report

## Summary of Issues Found in Generated Images

Based on analysis of the test-generated images, here are the key issues identified:

### 1. **Number Format Issues** 🔢
**Problem**: Farsi/Eastern Arabic numerals (۰-۹) are appearing in English text where Western numerals (0-9) should be used.

**Examples**:
- `announcement_english_20251027_022326.png`: Shows "۳۰۰%" instead of "300%" in English text
- `testimonial_english_20251027_022346.png`: Shows "۳۰۰%" instead of "300%"

**Root Cause**: The font selection logic is not properly detecting when English text contains numbers and needs to use Latin fonts (NotoSans) instead of Farsi fonts (IRANYekan) to preserve Western numeral format.

**Expected Fix Location**: `src/enhanced_social_generator.py` - `_get_font_for_text()` method

---

### 2. **Text Truncation/Clipping Issues** ✂️
**Problem**: Farsi text is being cut off mid-word at the end of lines.

**Examples**:
- `article_farsi_20251027_022333.png`: Text ends with "میدهد" cut to "میدهـ"
- `article_gradient_farsi_20251027_022335.png`: Similar truncation issues

**Root Cause**: The `_wrap_arabic_text()` method in `src/enhanced_social_generator.py` (lines 1007-1037) wraps by spaces but doesn't handle the case where reshaping breaks words or where words are too long.

**Expected Fix**: Need to either:
- Break long words at character level (not ideal for Farsi)
- Increase max_width tolerance for Arabic text
- Implement smarter wrapping that considers character-level measurement

---

### 3. **Icon/Character Rendering Issues** 📦
**Problem**: Empty square characters appearing before author names in some quote/testimonial layouts.

**Examples**:
- `quote_gradient_english_20251027_022344.png`: Shows empty square before "Steve Jobs"

**Root Cause**: Likely an encoding issue or missing character in the font being used for the attribution text.

---

### 4. **Color Contrast Issues** 🎨
**Problem**: Some text elements have low contrast against backgrounds.

**Examples**:
- Various images show dark gray footer text on dark backgrounds
- Light text on light backgrounds in gradient variants

**Root Cause**: The text color selection in layout methods doesn't always adapt to background colors.

---

## Proposed Solutions

### Fix 1: Number Format Issue
**File**: `src/enhanced_social_generator.py`
**Method**: `_get_font_for_text()` (around line 758)

**Current Logic Issue**: The method checks for Arabic text but doesn't properly handle the case where English text should use Western numerals.

**Fix**:
```python
def _get_font_for_text(self, text: str, font_type: str) -> ImageFont.ImageFont:
    """Get appropriate font with proper number handling"""
    
    # Detect if text contains Western numerals
    has_western_numbers = bool(re.search(r'[0-9]', text))
    is_arabic = self._is_arabic_text(text)
    
    # CRITICAL: If text is primarily English with Western numerals,
    # ALWAYS use Latin font to prevent numeral conversion
    if has_western_numbers and not is_arabic:
        # Force Latin font for English text with numbers
        return self._get_latin_font(font_type)
    
    # Rest of existing logic...
```

### Fix 2: Text Truncation
**File**: `src/enhanced_social_generator.py`
**Method**: `_wrap_arabic_text()` (lines 1007-1037)

**Issue**: The method doesn't handle cases where words are too long even after reshaping.

**Fix**:
```python
def _wrap_arabic_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    """Wrap Arabic/Farsi text with character-level fallback"""
    lines = []
    current_line = ""
    words = text.split()

    for word in words:
        test_line = current_line + " " + word if current_line else word
        processed_test = self._prepare_arabic_text(test_line)
        bbox = font.getbbox(processed_test)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
                current_line = word
            else:
                # Word is too long - wrap at character level
                char_lines = self._wrap_word_character_level(word, font, max_width)
                lines.extend(char_lines[:-1])  # All except last
                current_line = char_lines[-1] if char_lines else word
```

### Fix 3: Icon Rendering
**File**: `src/enhanced_social_generator.py`
**Method**: Layout render methods

**Fix**: Add encoding validation before drawing special characters:
```python
def _safe_draw_text(self, img, text, font, position, color):
    """Draw text with encoding safety"""
    try:
        # Ensure text is properly encoded
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        # Remove or replace problematic characters
        text = text.replace('\u25A1', '')  # Remove empty square
        # Draw text...
    except Exception as e:
        print(f"Text rendering error: {e}")
```

### Fix 4: Color Contrast
**File**: `src/enhanced_social_generator.py`
**Method**: Background and text color selection

**Fix**: Add background-aware text color selection:
```python
def _get_text_color_for_background(self, bg_color):
    """Select text color based on background brightness"""
    brightness = sum(bg_color) / 3
    if brightness > 128:  # Light background
        return (50, 50, 50)  # Dark text
    else:  # Dark background
        return (255, 255, 255)  # Light text
```

---

## Testing Plan

After fixes are implemented:

1. Re-run the test suite: `python test_production_deployment.py`
2. Verify all 20 images are generated without issues
3. Check each layout type for:
   - Proper number formatting
   - No text truncation
   - Proper character rendering
   - Good contrast

---

## Priority Levels

1. **HIGH**: Number format issues (breaks language consistency)
2. **HIGH**: Text truncation (breaks readability)
3. **MEDIUM**: Icon rendering (visual artifact)
4. **LOW**: Color contrast (usability but not breaking)

---

## Issue Found: Gradient Background Not Working (FIXED)

**Problem**: The `background_color` parameter was being completely ignored by the `/generate_text` API endpoint.

**Root Cause**: The API endpoint was not processing the `background_color` parameter from the request and passing it to the generator. The generator was using default configuration instead of the requested colors.

**Fix Applied**: Modified `social_image_api.py` to:
1. Extract `background_color` from the request
2. Create an appropriate gradient from the provided color
3. Update the generator's config with the new background settings
4. Support both 'gradient' and 'solid' background types

**Code Changes**: Added background handling logic in `/generate_text` endpoint (lines 807-848)

---

## Additional Notes

- The test suite passed all 20 tests but these are visual/generation issues
- These issues may not be caught by the current test framework
- Need to add visual regression tests or image comparison tests

