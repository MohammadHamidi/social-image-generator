# Implementation Roadmap - Social Image Generator
## Master Requirements Implementation Plan

> **Based on:** Final Unified Specification (2025-10-26)
> **Goal:** Transform current system into full-featured Instagram Visual Composer

---

## 📋 Phase 1: Foundation & Architecture (Priority: CRITICAL)

### 1.1 Core System Restructuring

**Objective:** Create flexible architecture to support 20+ layout types

**Tasks:**
- [ ] Create `LayoutEngine` base class
- [ ] Implement layout registry system
- [ ] Create asset manager module
- [ ] Build smart placement calculator
- [ ] Design universal validation schema

**Files to Create:**
- `src/layout_engine.py` - Base layout engine
- `src/asset_manager.py` - Asset loading and caching
- `src/placement_calculator.py` - Smart positioning logic
- `src/schemas/` - JSON schemas for each layout type
- `src/layouts/` - Individual layout implementations

**Estimated Time:** 3-4 days

---

### 1.2 Universal API Endpoint

**Objective:** Create `/generate_post` endpoint

**Current State:**
- ✅ `/generate_text` - Text layouts only
- ✅ `/generate_gradient` - Backgrounds only
- ❌ No unified endpoint

**Target Structure:**
```python
POST /generate_post
{
  "layout_type": "product_showcase",
  "content": { ... },
  "assets": { ... },
  "background": { ... },
  "options": { ... }
}
```

**Tasks:**
- [ ] Design unified request schema
- [ ] Create layout type router
- [ ] Implement asset validation
- [ ] Build response formatter (multi-slide support)
- [ ] Add error handling with layout-specific messages

**Files to Modify:**
- `social_image_api.py` - Add new endpoint
- Create `src/api_schemas.py` - Request/response schemas

**Estimated Time:** 2 days

---

## 📋 Phase 2: Priority Layout Types (Marketing Focus)

### 2.1 Marketing-Oriented Layouts

**Priority Order:**

#### 1. `headline_promo` (HIGH PRIORITY)
**Description:** Big headline focus with optional CTA
**Content Fields:** `headline`, `subheadline?`, `cta?`
**Assets:** `hero_image` (optional)
**Complexity:** ⭐⭐ (Medium)

**Implementation:**
- [ ] Create `layouts/headline_promo.py`
- [ ] Design text hierarchy (large headline + smaller sub)
- [ ] Implement CTA button renderer
- [ ] Add hero image smart cropping
- [ ] Test with/without hero image

---

#### 2. `split_image_text` (HIGH PRIORITY)
**Description:** Half photo + half text
**Content Fields:** `title`, `description`
**Assets:** `hero_image` (required)
**Complexity:** ⭐⭐⭐ (Medium-High)

**Implementation:**
- [ ] Create `layouts/split_image_text.py`
- [ ] Implement 50/50 split layout
- [ ] Add vertical/horizontal split options
- [ ] Smart text wrapping for constrained space
- [ ] Hero image aspect ratio preservation

---

#### 3. `product_showcase` (HIGH PRIORITY)
**Description:** Hero photo focus + price/CTA
**Content Fields:** `product_name`, `price`, `description?`, `cta?`
**Assets:** `hero_image`, `logo_image` (optional)
**Complexity:** ⭐⭐⭐ (Medium-High)

**Implementation:**
- [ ] Create `layouts/product_showcase.py`
- [ ] Design product-centered composition
- [ ] Implement price badge renderer
- [ ] Add logo corner placement
- [ ] Smart background contrast overlay

---

#### 4. `testimonial` (ALREADY EXISTS - ENHANCE)
**Description:** Quote + person info
**Content Fields:** `quote`, `person_name`, `title?`, `rating?`
**Assets:** `hero_image` (optional profile photo)
**Complexity:** ⭐⭐ (Medium)

**Implementation:**
- [ ] Enhance existing testimonial layout
- [ ] Add profile photo circle mask
- [ ] Implement star rating renderer
- [ ] Add person title/role display
- [ ] Improve quote mark styling

---

#### 5. `overlay_text` (MEDIUM PRIORITY)
**Description:** Text overlaying photo with smart contrast
**Content Fields:** `title`, `subtitle?`
**Assets:** `background_image` or `hero_image` (required)
**Complexity:** ⭐⭐⭐ (Medium-High)

**Implementation:**
- [ ] Create `layouts/overlay_text.py`
- [ ] Implement automatic contrast detection
- [ ] Add gradient overlay for readability
- [ ] Support multiple text positions (top/center/bottom)
- [ ] Smart shadow/outline for light backgrounds

---

#### 6. `caption_box` (MEDIUM PRIORITY)
**Description:** Text block under photo
**Content Fields:** `caption`, `title?`
**Assets:** `hero_image` (required)
**Complexity:** ⭐⭐ (Medium)

**Implementation:**
- [ ] Create `layouts/caption_box.py`
- [ ] Design caption box styling
- [ ] Implement hero image top placement
- [ ] Add caption text wrapping
- [ ] Support icon/emoji in caption

**Estimated Time for Phase 2.1:** 5-7 days

---

### 2.2 Content/Educational Layouts

#### 7. `quote` (ALREADY EXISTS - WORKING ✅)
**Status:** Already implemented and tested
**Enhancement Tasks:**
- [ ] Add quote style variations
- [ ] Implement custom quote mark designs
- [ ] Add author photo option

---

#### 8. `checklist` (HIGH PRIORITY)
**Description:** Title + bulleted items
**Content Fields:** `title`, `items[]`
**Assets:** `icons[]` (optional)
**Complexity:** ⭐⭐⭐ (Medium-High)

**Implementation:**
- [ ] Create `layouts/checklist.py`
- [ ] Design checkbox/checkmark renderer
- [ ] Implement multi-line item wrapping
- [ ] Add custom icon support per item
- [ ] Support checked/unchecked states

---

#### 9. `carousel_text` (HIGH PRIORITY)
**Description:** Multiple text-only slides
**Content Fields:** `slides[]` (each with title + text)
**Assets:** None required
**Complexity:** ⭐⭐⭐⭐ (High)

**Implementation:**
- [ ] Create `layouts/carousel_text.py`
- [ ] Implement slide template system
- [ ] Add slide numbering (1/5, 2/5, etc.)
- [ ] Support consistent styling across slides
- [ ] Generate multiple output files
- [ ] Test with 3-10 slide carousels

---

#### 10. `step_guide` (MEDIUM PRIORITY)
**Description:** Sequential step instructions
**Content Fields:** `title`, `steps[]` (each with step_number, text)
**Assets:** `icons[]` (optional)
**Complexity:** ⭐⭐⭐ (Medium-High)

**Implementation:**
- [ ] Create `layouts/step_guide.py`
- [ ] Design numbered step renderer
- [ ] Add arrow/connector lines between steps
- [ ] Support icon per step
- [ ] Implement step highlight styling

---

#### 11. `infographic` (MEDIUM PRIORITY)
**Description:** Data visualization with stats/icons
**Content Fields:** `title`, `stats[]` (each with label, value, icon?)
**Assets:** `supporting_images[]` (icons/graphics)
**Complexity:** ⭐⭐⭐⭐ (High)

**Implementation:**
- [ ] Create `layouts/infographic.py`
- [ ] Design stat card renderer
- [ ] Implement icon placement system
- [ ] Add number formatting (1K, 1M, etc.)
- [ ] Support multiple layout grids (2x2, 3x1, etc.)

**Estimated Time for Phase 2.2:** 6-8 days

---

## 📋 Phase 3: Advanced Features & Asset Intelligence

### 3.1 Smart Asset Manager

**Objective:** Intelligent asset loading, caching, and placement

**Features:**
- [ ] URL asset fetching (HTTP/HTTPS)
- [ ] Local file asset loading
- [ ] Image caching system
- [ ] Automatic resizing/cropping
- [ ] Format conversion (JPEG→PNG, etc.)
- [ ] Asset preloading for carousels

**Implementation:**
```python
class AssetManager:
    def load_asset(url_or_path: str, role: str) -> Image.Image
    def get_cached(asset_id: str) -> Image.Image
    def smart_crop(image: Image, target_size: tuple, focus: str) -> Image.Image
    def apply_mask(image: Image, mask_type: str) -> Image.Image
```

**Files to Create:**
- `src/asset_manager.py`
- `src/cache_manager.py`
- `src/image_processor.py`

**Estimated Time:** 3-4 days

---

### 3.2 Smart Placement Calculator

**Objective:** Automatic element positioning based on layout rules

**Features:**
- [ ] Safe area calculation (avoid text cutoff)
- [ ] Element collision detection
- [ ] Dynamic spacing based on content
- [ ] RTL-aware positioning
- [ ] Multi-language text metrics

**Implementation:**
```python
class PlacementCalculator:
    def calculate_text_position(layout_type: str, content: dict) -> tuple
    def calculate_hero_bounds(canvas_size: tuple, layout_type: str) -> tuple
    def get_safe_margins(platform: str) -> dict
    def check_overlap(element1: dict, element2: dict) -> bool
```

**Files to Create:**
- `src/placement_calculator.py`
- `src/collision_detector.py`

**Estimated Time:** 3-4 days

---

### 3.3 Carousel Generation System

**Objective:** Multi-slide generation with consistent styling

**Features:**
- [ ] Slide template inheritance
- [ ] Consistent background across slides
- [ ] Auto-numbering (1/5, 2/5, etc.)
- [ ] Navigation hints (swipe arrows)
- [ ] Batch generation
- [ ] ZIP file output option

**Layouts Supporting Carousels:**
- `carousel_text`
- `carousel_photos`
- `carousel_promo_mixed`
- Any layout with `slides[]` array

**Implementation:**
- [ ] Create `src/carousel_generator.py`
- [ ] Implement slide numbering renderer
- [ ] Add consistent theming engine
- [ ] Support slide transitions preview

**Estimated Time:** 4-5 days

---

## 📋 Phase 4: Additional Layout Types

### 4.1 Comparison Layouts

#### `before_after`
**Complexity:** ⭐⭐⭐⭐ (High)
- [ ] Create `layouts/before_after.py`
- [ ] Implement side-by-side comparison
- [ ] Add slider/divider line
- [ ] Support top/bottom split
- [ ] Label positioning (Before/After)

#### `comparison_stats`
**Complexity:** ⭐⭐⭐ (Medium-High)
- [ ] Create `layouts/comparison_stats.py`
- [ ] Design table/grid renderer
- [ ] Implement feature checkmarks
- [ ] Add column headers

**Estimated Time:** 3-4 days

---

### 4.2 Special Purpose Layouts

#### `announcement`
**Status:** Already exists - Enhance
- [ ] Add urgency indicators (countdown, badges)
- [ ] Implement date/time formatting
- [ ] Add event location support

#### `meme`
**Complexity:** ⭐⭐ (Medium)
- [ ] Create `layouts/meme.py`
- [ ] Top/bottom text positioning
- [ ] Classic meme font styling
- [ ] Text stroke/outline

#### `story_highlight_cover`
**Complexity:** ⭐⭐ (Medium)
- [ ] Create `layouts/story_highlight_cover.py`
- [ ] Circular frame support
- [ ] Icon + label combination
- [ ] Minimalist design

**Estimated Time:** 2-3 days

---

## 📋 Phase 5: Polish & Production Readiness

### 5.1 Validation System

**Objective:** Comprehensive input validation per layout type

**Tasks:**
- [ ] Create JSON schemas for all layout types
- [ ] Implement schema validator
- [ ] Add helpful error messages
- [ ] Build schema documentation generator

**Files to Create:**
- `src/schemas/quote.schema.json`
- `src/schemas/product_showcase.schema.json`
- (... one per layout type)
- `src/validator.py`

**Estimated Time:** 3-4 days

---

### 5.2 Documentation & Examples

**Tasks:**
- [ ] Generate API documentation
- [ ] Create example gallery (one per layout)
- [ ] Write integration guide
- [ ] Build interactive demo page
- [ ] Document all asset roles

**Files to Create:**
- `docs/API_REFERENCE.md`
- `docs/LAYOUT_GUIDE.md`
- `docs/examples/` - Example JSON requests
- `gallery/` - Generated sample images

**Estimated Time:** 4-5 days

---

### 5.3 Testing & Quality Assurance

**Tasks:**
- [ ] Unit tests for each layout type
- [ ] Integration tests for API endpoints
- [ ] Asset loading stress tests
- [ ] Carousel generation tests
- [ ] Performance benchmarks
- [ ] Memory leak detection

**Files to Create:**
- `tests/test_layouts/`
- `tests/test_assets.py`
- `tests/test_carousel.py`
- `tests/performance/`

**Estimated Time:** 5-6 days

---

## 📊 Total Estimated Timeline

| Phase | Description                 | Duration  |
|-------|----------------------------|-----------|
| 1     | Foundation & Architecture  | 5-6 days  |
| 2     | Priority Layouts           | 11-15 days|
| 3     | Advanced Features          | 10-13 days|
| 4     | Additional Layouts         | 5-7 days  |
| 5     | Polish & Production        | 12-15 days|

**Total Estimated Time:** 43-56 days (8.5-11 weeks)

---

## 🎯 Immediate Next Steps (This Week)

### Priority 1: Architecture Foundation
1. Create `LayoutEngine` base class
2. Implement asset manager
3. Build `/generate_post` endpoint skeleton

### Priority 2: First Marketing Layout
4. Implement `headline_promo` layout (complete)
5. Test with various content

### Priority 3: Documentation
6. Create schema template
7. Document API structure

---

## 📝 Implementation Notes

### Design Principles
- **Layout as Code:** Each layout type is a Python class
- **Declarative Configuration:** JSON schemas define requirements
- **Smart Defaults:** Minimal required parameters
- **Fail Gracefully:** Helpful error messages
- **Test-Driven:** Every layout has tests

### Code Organization
```
src/
├── layouts/
│   ├── base.py              # LayoutEngine base class
│   ├── quote.py             # Quote layout (existing)
│   ├── headline_promo.py    # New layout
│   └── ...
├── asset_manager.py         # Asset loading & caching
├── placement_calculator.py  # Smart positioning
├── carousel_generator.py    # Multi-slide support
└── schemas/
    ├── base.schema.json     # Universal schema
    └── quote.schema.json    # Layout-specific schema
```

### API Structure
```
/generate_post       # Universal endpoint (new)
/generate_text       # Legacy (keep for compatibility)
/generate_gradient   # Background generation (existing)
/upload/background   # Asset upload (existing)
/files               # File listing (existing)
```

---

## ✅ Success Metrics

- [ ] All 20+ layout types implemented
- [ ] Carousel generation working
- [ ] Asset management system complete
- [ ] Full API documentation
- [ ] 100+ test cases passing
- [ ] Example gallery with all layouts
- [ ] Performance: <2s per single image, <10s per carousel

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Status:** Ready for Implementation
