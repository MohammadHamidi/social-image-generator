# Next Steps - Immediate Actions

> **Created:** 2025-10-26
> **Priority:** Start with Marketing-Oriented Layouts
> **Goal:** Get first production-ready layout types working

---

## 🎯 This Week's Focus

### Day 1-2: Complete Architecture Foundation

**Status: IN PROGRESS** ✅

**Completed:**
- [x] Created `src/layouts/base.py` - Base layout engine classes
- [x] Created `src/asset_manager.py` - Asset loading and caching
- [x] Documented implementation roadmap

**Remaining:**
- [ ] Create `/generate_post` universal endpoint
- [ ] Test base classes with existing quote layout
- [ ] Create schema template structure

**Files to Create Next:**
```
src/api/
├── __init__.py
├── generate_post.py      # Universal endpoint
└── validators.py         # Request validation

src/schemas/
├── base.schema.json      # Universal fields
├── quote.schema.json     # Quote layout
└── template.schema.json  # Template for new schemas
```

---

### Day 3-4: First Marketing Layout - `headline_promo`

**Priority:** HIGH - This is the most requested marketing layout

**Specification:**
```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Summer Sale",
    "subheadline": "Up to 50% Off",
    "cta": "Shop Now"
  },
  "assets": {
    "hero_image_url": "https://... (optional)"
  },
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [[255, 107, 107], [253, 187, 45]],
      "direction": "vertical"
    }
  }
}
```

**Implementation Tasks:**
- [ ] Create `src/layouts/headline_promo.py`
- [ ] Implement text hierarchy (large headline, smaller sub)
- [ ] Add CTA button renderer with rounded corners
- [ ] Support with/without hero image modes
- [ ] Test with Farsi and English content
- [ ] Create example JSON requests
- [ ] Generate sample images

**Design Rules:**
- Headline: 72-96px font size, bold
- Subheadline: 36-48px font size, medium weight
- CTA: Button with 20px padding, 12px border radius
- Hero image (if present): 40% of canvas, top or left side
- Text contrast: Auto overlay if using hero image

---

### Day 5: Testing & Documentation

- [ ] Write unit tests for `headline_promo`
- [ ] Create API documentation
- [ ] Generate example gallery
- [ ] Test performance benchmarks

---

## 🎨 Priority Layout Implementation Order

Based on user demand and complexity:

### Week 1 (Current)
1. ✅ Architecture foundation
2. 🔨 `headline_promo` - Marketing focus layout

### Week 2
3. `product_showcase` - E-commerce focus
4. `split_image_text` - Photo + text combination
5. `checklist` - Educational content

### Week 3
6. `carousel_text` - Multi-slide blog posts
7. `testimonial` (enhance existing)
8. `overlay_text` - Photo with smart contrast

### Week 4
9. `before_after` - Comparison layout
10. `step_guide` - Tutorial content

---

## 📝 Immediate Action Items

### TODAY:
1. **Create `/generate_post` endpoint skeleton**
   - Add to `social_image_api.py`
   - Wire up layout registry
   - Test with existing quote layout

2. **Migrate quote layout to new architecture**
   - Create `src/layouts/quote.py` using `LayoutEngine`
   - Register in layout registry
   - Test compatibility

3. **Create validation system**
   - Build schema validator
   - Add helpful error messages
   - Test with malformed requests

### TOMORROW:
1. **Start `headline_promo` implementation**
   - Create layout class
   - Implement render method
   - Test text hierarchy

2. **Create example generator**
   - Script to generate all examples
   - Save to `examples/` directory
   - Document usage

---

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_layouts/test_headline_promo.py
def test_headline_only():
    """Test with headline only (minimal content)"""

def test_headline_with_subheadline():
    """Test with headline and subheadline"""

def test_headline_with_cta():
    """Test with CTA button"""

def test_with_hero_image():
    """Test with hero image background"""

def test_farsi_text():
    """Test with Farsi headline"""

def test_mixed_language():
    """Test with English headline + Farsi subheadline"""
```

### Integration Tests
```python
# tests/test_api/test_generate_post.py
def test_generate_post_headline_promo():
    """Test full API request for headline_promo"""

def test_invalid_layout_type():
    """Test error handling for unknown layout"""

def test_missing_required_content():
    """Test validation error messages"""
```

---

## 📊 Success Metrics for This Week

- [ ] `/generate_post` endpoint working
- [ ] `headline_promo` layout complete and tested
- [ ] At least 5 example images generated
- [ ] API documentation updated
- [ ] All tests passing
- [ ] Performance: <1s per image

---

## 🔄 Migration Plan

### Existing Code to Preserve
- ✅ Gradient generation (working)
- ✅ Farsi text rendering (working)
- ✅ Font loading system (working)
- ✅ Existing `/generate_text` endpoint (keep for compatibility)

### New Code to Add
- Layout engine system
- Asset manager
- Universal endpoint
- Schema validation
- Layout registry

### Compatibility Strategy
- Keep old endpoints working
- Add deprecation warnings
- Provide migration guide for users
- Support both old and new formats during transition

---

## 📚 Documentation Priorities

### User Documentation
1. **API Reference** - All endpoints with examples
2. **Layout Guide** - Each layout type with visual examples
3. **Migration Guide** - How to upgrade from old API
4. **Asset Guide** - How to use different asset types

### Developer Documentation
1. **Architecture Overview** - System design
2. **Creating New Layouts** - How to add layout types
3. **Testing Guide** - How to write tests
4. **Deployment Guide** - Production setup

---

## 🚀 Quick Start Command

To begin implementing `headline_promo`:

```bash
# 1. Create the layout file
touch src/layouts/headline_promo.py

# 2. Copy template structure
cat > src/layouts/headline_promo.py << 'EOF'
from .base import TextLayoutEngine, register_layout
from PIL import Image, ImageDraw
from typing import List

@register_layout
class HeadlinePromoLayout(TextLayoutEngine):
    LAYOUT_TYPE = "headline_promo"
    DESCRIPTION = "Big headline focus with optional CTA"

    def render(self) -> List[Image.Image]:
        # Implementation here
        pass
EOF

# 3. Create test file
touch tests/test_layouts/test_headline_promo.py

# 4. Run tests
python -m pytest tests/test_layouts/test_headline_promo.py -v
```

---

## 💡 Tips for Implementation

### Text Hierarchy Best Practices
- Use `_get_font_with_size()` for dynamic sizing
- Test with long text (wrapping scenarios)
- Always handle RTL text properly
- Add text shadows for contrast

### Asset Handling Best Practices
- Use `AssetManager.load_asset()` for all images
- Cache assets for performance
- Handle missing assets gracefully
- Validate image formats

### Layout Design Best Practices
- Follow Instagram safe area margins
- Test on actual Instagram (1080x1350)
- Support both light and dark backgrounds
- Ensure text is always readable

---

**Status:** Ready to begin `headline_promo` implementation
**Blockers:** None
**Next Review:** End of this week
