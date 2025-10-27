# Current Issues Analysis - Post Gradient Fix

## Summary
After fixing the gradient background issue, tests pass but several critical issues remain based on image analysis:

## ✅ FIXED: Gradient Backgrounds
**Status**: Working correctly now
- All gradient versions show proper vertical gradients
- File sizes differ between solid and gradient versions (as expected)
- Gradients transition smoothly from lighter to darker shades

---

## ❌ CRITICAL: Number Format Issues

### Problem
English text is displaying Farsi/Eastern Arabic numerals (۰-۹) instead of Western Arabic numerals (0-9).

**Examples from images:**
- `announcement_gradient_english` shows "Summer Sale ۲۰۲۴" (should be "2024")
- Same image shows "۵۰%" (should be "50%")
- Testimonial images show "۳۰۰%" (should be "300%")

### Root Cause
The font selection logic in `_get_font_for_text()` is choosing IRANYekan fonts even for English text with numbers, and these fonts automatically convert Western numerals to Persian numerals.

### Fix Required
1. Detect when text is English with numbers
2. Force use of Latin fonts (NotoSans) to preserve Western numerals
3. Add explicit numeral conversion before rendering

---

## ❌ CRITICAL: Text Truncation

### Problem
Long Farsi text in article layouts is being cut off mid-word.

**Examples:**
- Article Farsi layouts show text ending abruptly (like "میدهد" cut to "میدهـ")
- Text doesn't fit in the designated space

### Root Cause
The `_wrap_arabic_text()` method only breaks on word boundaries. If a single word is too long for the available width, it gets cut off.

### Fix Required
1. Add character-level fallback for extremely long words
2. Dynamically adjust font size or width
3. Better line wrapping logic for Arabic/Farsi

---

## ❌ MEDIUM: Icon/Character Rendering

### Problem
Empty square characters appearing before author names in quote layouts.

**Example:**
- Quote images show an empty square before "Steve Jobs" or "Winston Churchill"

### Root Cause
Likely an encoding issue with special characters or quotation marks.

### Fix Required
1. Validate character encoding before rendering
2. Replace problematic characters with safe alternatives
3. Use proper Unicode quotation marks

---

## ❌ LOW: Color Contrast

### Problem
Some text elements have insufficient contrast against backgrounds.

**Examples:**
- Dark gray footer text on dark backgrounds
- Light text on light gradient backgrounds

### Fix Required
Dynamic text color selection based on background brightness.

---

## Observations

### Working Correctly
- ✅ Gradient backgrounds now functional
- ✅ Text wrapping works for most cases
- ✅ Font selection works for pure text
- ✅ All 20 tests pass (but with visual issues)

### Breaking
- ❌ Mixed-language content causing numeral conversion issues
- ❌ Farsi text wrapping incomplete words
- ❌ Special character rendering issues

---

## Priority Fix Order

1. **Number Format** (CRITICAL - breaks language consistency)
2. **Text Truncation** (CRITICAL - breaks readability)
3. **Icon Rendering** (MEDIUM - visual artifact)
4. **Color Contrast** (LOW - usability issue)

