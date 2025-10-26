# Production Testing Guide

This guide explains how to test the deployed Instagram image generator at **https://imageeditor.flowiran.ir/**

## 📋 Test Scripts Available

### 1. Quick Test (Recommended for first check)
**File:** `quick_test_production.py`

Fast test that checks:
- ✅ System health
- ✅ Available layouts
- ✅ Basic image generation

**Run:**
```bash
python quick_test_production.py
```

**Output:**
- Saves one test image: `test_output.png`
- Takes ~10 seconds

---

### 2. Comprehensive Test (Full validation)
**File:** `test_production_deployment.py`

Complete test suite that:
- ✅ Tests all 7 layout types
- ✅ Tests English and Farsi text
- ✅ Tests with external images
- ✅ Validates all features

**Run:**
```bash
python test_production_deployment.py
```

**Output:**
- Saves multiple test images to `production_test_outputs/` directory
- Provides detailed test report
- Takes ~2-3 minutes

---

## 🚀 Quick Start

### Prerequisites

Install required Python package:
```bash
pip install requests
```

### Run Tests

**Option 1: Quick Check (10 seconds)**
```bash
python quick_test_production.py
```

**Option 2: Full Test Suite (2-3 minutes)**
```bash
python test_production_deployment.py
```

---

## 📊 What Gets Tested

### Layouts Tested

1. **headline_promo** - Marketing headlines with CTAs
2. **split_image_text** - Half photo, half text layouts
3. **product_showcase** - E-commerce product displays
4. **checklist** - Educational tips and guides
5. **testimonial** - Customer reviews with ratings
6. **overlay_text** - Text overlaid on images
7. **caption_box** - Images with caption boxes

### Features Tested

- ✅ Health endpoint
- ✅ Layouts listing
- ✅ Image generation
- ✅ Gradient backgrounds
- ✅ External image loading
- ✅ Farsi/RTL text rendering
- ✅ All layout options

---

## 🎯 Expected Results

### Successful Test Output

```
🚀 Production Deployment Test Suite
======================================================================
  Testing: https://imageeditor.flowiran.ir
======================================================================

TEST 1: System Health Check
======================================================================
✅ System is healthy!
ℹ️  Status: healthy
ℹ️  Version: 2.0

TEST 2: Available Layouts
======================================================================
✅ Found 7 available layouts
ℹ️  • headline_promo: Big headline focus with optional CTA
ℹ️  • split_image_text: Half photo, half text layout
...

TEST 3: Layout Generation Tests
======================================================================
📋 Testing headline_promo layout...
✅ basic: Image saved to production_test_outputs/...
...

TEST SUMMARY
======================================================================
✅ headline_promo: 2/2 passed
✅ split_image_text: 1/1 passed
...

TOTAL: 9/9 tests passed
✅ 🎉 All tests passed! Production system is working perfectly!
```

---

## 🐛 Troubleshooting

### Connection Errors

If you see:
```
❌ Health check error: Connection refused
```

**Solutions:**
1. Check if the URL is correct: `https://imageeditor.flowiran.ir/`
2. Check your internet connection
3. Verify the server is running

### 404 Errors

If you see:
```
❌ Health check failed: 404
```

**Solutions:**
1. The endpoint might not exist
2. Check if the server is properly deployed
3. Verify the API version

### Timeout Errors

If you see:
```
❌ Health check error: Timeout
```

**Solutions:**
1. Increase timeout in the script (change `timeout=10` to `timeout=30`)
2. Check network speed
3. Server might be overloaded

### Image Generation Fails

If generation works but specific layouts fail:

1. Check the error message for details
2. Some layouts require external images (may fail if image URLs are blocked)
3. Try with different image URLs

---

## 📝 Manual Testing (Alternative)

### Using cURL

**Test Health:**
```bash
curl https://imageeditor.flowiran.ir/health
```

**List Layouts:**
```bash
curl https://imageeditor.flowiran.ir/layouts
```

**Generate Image:**
```bash
curl -X POST https://imageeditor.flowiran.ir/generate_post \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "headline_promo",
    "content": {
      "headline": "Test Post"
    },
    "background": {
      "mode": "gradient",
      "gradient": {
        "colors": [[255, 200, 150], [255, 150, 200]],
        "direction": "vertical"
      }
    }
  }' \
  --output test.png
```

### Using Postman

1. Create a POST request to `https://imageeditor.flowiran.ir/generate_post`
2. Set header: `Content-Type: application/json`
3. Body (raw JSON):
```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Test Post",
    "subheadline": "Production test"
  },
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [[255, 200, 150], [255, 150, 200]],
      "direction": "vertical"
    }
  }
}
```
4. Send request
5. Save response as PNG image

---

## 📚 Example Requests

### Farsi Text Example

```python
import requests

config = {
    "layout_type": "headline_promo",
    "content": {
        "headline": "فروش ویژه تابستان",
        "subheadline": "تخفیف تا ۵۰ درصد"
    },
    "background": {
        "mode": "gradient",
        "gradient": {
            "colors": [[230, 240, 255], [255, 230, 240]],
            "direction": "vertical"
        }
    }
}

response = requests.post(
    "https://imageeditor.flowiran.ir/generate_post",
    json=config
)

with open("farsi_test.png", "wb") as f:
    f.write(response.content)
```

### Product Showcase Example

```python
import requests

config = {
    "layout_type": "product_showcase",
    "content": {
        "product_name": "Smart Watch Pro",
        "price": "$299",
        "description": "Advanced fitness tracking",
        "cta_text": "Buy Now"
    },
    "assets": {
        "hero_image_url": "https://picsum.photos/600/600"
    }
}

response = requests.post(
    "https://imageeditor.flowiran.ir/generate_post",
    json=config
)

with open("product_test.png", "wb") as f:
    f.write(response.content)
```

---

## 🎨 More Examples

All example JSON files are in the `examples/` directory:
- `examples/headline_promo/`
- `examples/split_image_text/`
- `examples/product_showcase/`
- `examples/checklist/`
- `examples/testimonial/`
- `examples/overlay_text/`
- `examples/caption_box/`

Each directory contains 2-3 example configurations you can use for testing.

---

## ✅ Success Criteria

A successful test should show:
- ✅ Health endpoint returns 200 OK
- ✅ Layouts endpoint lists all 7 layouts
- ✅ Image generation returns PNG images
- ✅ Farsi text renders correctly
- ✅ External images load successfully
- ✅ All layout types work

---

## 📞 Support

If tests fail or you encounter issues:
1. Check the error messages in the test output
2. Review server logs (if you have access)
3. Verify all dependencies are installed
4. Check that external image URLs are accessible

---

**Happy Testing! 🎉**
