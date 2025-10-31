# Complete Usage Guide: Social Image Generator API

## 📖 Overview

This guide combines API documentation and practical examples to help you get started quickly with the Social Image Generator API.

**You need both**:
- **API Documentation** (`docs/`) - Understanding endpoints, parameters, and schemas
- **Examples** (`examples/`) - Working code samples and JSON configurations

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd social-image-generator

# Install dependencies
pip install -r requirements.txt

# Start the server
python social_image_api.py
```

The API will be available at: `http://localhost:5000`

### Health Check

```bash
curl http://localhost:5000/health
```

---

## 📚 Understanding the API Structure

### Core Concepts

1. **Layout Types** - Different visual designs for your social media posts
2. **Content** - Text, headlines, descriptions (layout-specific)
3. **Assets** - Images (hero, logo, background)
4. **Background** - Gradients, solid colors, or images
5. **Options** - Customization settings (colors, sizes, positions)

### API Endpoints Overview

#### System Endpoints
- `GET /` - API documentation
- `GET /health` - Health check
- `GET /config` - Get configuration
- `POST /config` - Update configuration

#### Upload Endpoints
- `POST /upload/main` - Upload main/hero images
- `POST /upload/watermark` - Upload logos/watermarks
- `POST /upload/background` - Upload background images

#### Generation Endpoints
- `POST /generate_post` - **Main endpoint** for creating social media posts
- `POST /generate_gradient` - Generate gradient backgrounds only

#### Information Endpoints
- `GET /layouts` - List available layouts
- `GET /gradient_info` - Gradient documentation
- `GET /text_layout_info` - Text layout documentation

#### Utility Endpoints
- `GET /files` - List uploaded files
- `GET /uploads/{folder}/{filename}` - Serve uploaded files
- `GET /generated/{filename}` - Serve generated images

---

## 🎨 Available Layout Types

### 1. **headline_promo**
Marketing headlines with optional CTA button.

**Example from `examples/headline_promo/example_3_with_cta.json`:**

```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Summer Sale",
    "subheadline": "Up to 50% Off Everything",
    "cta": "Shop Now"
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

### 2. **split_image_text**
Text on one side, image on the other.

**Example from `examples/split_image_text/example_1_basic.json`:**

```json
{
  "layout_type": "split_image_text",
  "content": {
    "title": "Premium Features",
    "description": "Everything you need in one powerful platform"
  },
  "assets": {
    "hero_image_url": "https://picsum.photos/540/1350"
  },
  "options": {
    "split_direction": "vertical",
    "image_position": "left"
  }
}
```

### 3. **overlay_text**
Text overlaid on background image.

**Example from `examples/overlay_text/example_1_basic.json`:**

```json
{
  "layout_type": "overlay_text",
  "content": {
    "text": "Every day is a new beginning",
    "subtitle": "Make it count"
  },
  "assets": {
    "background_image_url": "https://picsum.photos/1080/1350?random=10"
  },
  "options": {
    "text_position": "center",
    "overlay_opacity": 0.5
  }
}
```

### 4. **caption_box**
Image with caption overlay.

**Example from `examples/caption_box/example_1_bottom.json`:**

```json
{
  "layout_type": "caption_box",
  "content": {
    "title": "New Collection",
    "caption": "Discover our latest summer collection",
    "brand": "Fashion Studio"
  },
  "assets": {
    "hero_image_url": "https://picsum.photos/1080/800?random=40"
  }
}
```

### 5. **product_showcase**
Centered product display.

**Example from `examples/product_showcase/example_1_basic.json`:**

```json
{
  "layout_type": "product_showcase",
  "content": {
    "product_name": "Premium Headphones",
    "price": "299",
    "description": "Studio-quality sound"
  },
  "assets": {
    "hero_image_url": "https://picsum.photos/800/800"
  }
}
```

### 6. **checklist**
List with checkmarks.

**Example from `examples/checklist/example_1_basic.json`:**

```json
{
  "layout_type": "checklist",
  "content": {
    "title": "5 Tips for Better Design",
    "items": [
      "Keep it simple and clean",
      "Use consistent typography",
      "Test with real users"
    ]
  }
}
```

### 7. **testimonial**
Testimonial with attribution.

**Example from `examples/testimonial/example_1_basic.json`:**

```json
{
  "layout_type": "testimonial",
  "content": {
    "quote": "This product changed my life!",
    "name": "Sarah Johnson",
    "title": "Marketing Director"
  }
}
```

---

## 🔧 How to Use Examples

### Method 1: Using curl

```bash
# Use example file directly
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_1_minimal.json

# Save response
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_3_with_cta.json \
  -o response.json

# Download generated image
curl http://localhost:5000/generated/headline_promo_abc123_slide1.png \
  -o output.png
```

### Method 2: Using Python

```python
import requests
import json

# Load example
with open('examples/headline_promo/example_3_with_cta.json') as f:
    data = json.load(f)

# Send request
response = requests.post(
    'http://localhost:5000/generate_post',
    json=data
)

# Get result
result = response.json()
print(f"Success: {result['success']}")
print(f"Files: {len(result['generated_files'])}")
for file in result['generated_files']:
    print(f"Download: http://localhost:5000{file['download_url']}")
```

### Method 3: Using JavaScript/Fetch

```javascript
// Load example
const example = await fetch('examples/headline_promo/example_3_with_cta.json')
  .then(r => r.json());

// Send request
const response = await fetch('http://localhost:5000/generate_post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(example)
});

// Get result
const result = await response.json();
console.log('Generated:', result.generated_files[0].download_url);
```

---

## 🎨 Creating Custom Images

### Step 1: Upload Your Assets

```bash
# Upload logo
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@logo.png"

# Upload product image
curl -X POST http://localhost:5000/upload/main \
  -F "file=@product.jpg"

# Upload background
curl -X POST http://localhost:5000/upload/background \
  -F "file=@bg.jpg"
```

**Response:**
```json
{
  "success": true,
  "filename": "logo-123456.png",
  "url": "/uploads/watermark/logo-123456.png",
  "path": "uploads/watermark/logo-123456.png"
}
```

### Step 2: Create Your Request JSON

```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Your Headline",
    "subheadline": "Your Subheadline",
    "cta": "Call to Action"
  },
  "assets": {
    "logo_url": "uploads/watermark/logo-123456.png"
  },
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [[200, 16, 46], [255, 215, 0]],
      "direction": "diagonal"
    }
  },
  "options": {
    "logo_position": "top-center",
    "logo_size": 120
  }
}
```

### Step 3: Generate the Image

```bash
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @my_request.json
```

---

## 🎨 Background Options

### 1. Gradient Backgrounds

```json
{
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [[255, 107, 107], [78, 205, 196]],
      "direction": "vertical"  // or "horizontal" or "diagonal"
    }
  }
}
```

### 2. Solid Color Backgrounds

```json
{
  "background": {
    "mode": "solid_color",
    "color": [52, 73, 94]  // RGB array
  }
}
```

### 3. Image Backgrounds

```json
{
  "background": {
    "mode": "image",
    "image_url": "uploads/background/my-bg.jpg"
  }
}
```

### 4. Image with Overlay

```json
{
  "background": {
    "mode": "image_overlay",
    "overlay_opacity": 0.3,
    "overlay_color": [200, 16, 46]
  }
}
```

---

## 🎯 Advanced Features

### Background Removal

Remove backgrounds from product images:

```json
{
  "options": {
    "remove_hero_background": true,
    "bg_removal_method": "auto",  // "auto", "edge", or "color"
    "bg_removal_alpha_matting": false
  }
}
```

**Methods:**
- `auto` - AI-powered (best quality, uses rembg)
- `edge` - Enhanced edge detection
- `color` - Color threshold-based

### Farsi/RTL Support

For Persian/Farsi text (right-to-left):

```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "فروش تابستانی",
    "subheadline": "تا ۵۰٪ تخفیف",
    "cta": "خرید کنید"
  }
}
```

### Custom Colors

All color specifications support RGB arrays:

```json
{
  "options": {
    "headline_color": [255, 255, 255],
    "text_color": [50, 50, 50],
    "cta_bg_color": [255, 215, 0],
    "cta_text_color": [200, 16, 46]
  }
}
```

---

## 🎠 Creating Instagram Carousels

The API supports multi-slide carousels. See full examples in `examples/carousel/`:

**Example Structure:**

```json
{
  "carousel_posts": [
    {
      "slide": 1,
      "layout_type": "headline_promo",
      "content": { "headline": "Slide 1" },
      "assets": { "logo_url": "uploads/watermark/logo.png" },
      "background": { "mode": "gradient", "gradient": { "colors": [[200, 16, 46], [255, 215, 0]], "direction": "diagonal" }}
    },
    {
      "slide": 2,
      "layout_type": "checklist",
      "content": { "title": "Checklist", "items": ["Item 1", "Item 2"] }
    }
  ],
  "metadata": {
    "campaign_name": "My Campaign",
    "post_caption": "#mycampaign\n\nCheck out this post!"
  }
}
```

**Usage:**

```bash
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/carousel/yuan_payment_carousel.json
```

---

## 📝 Common Request Patterns

### Pattern 1: Simple Headline with Gradient

```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Your Message"
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

### Pattern 2: Product with Logo

```json
{
  "layout_type": "product_showcase",
  "content": {
    "product_name": "Product Name",
    "price": "$99",
    "description": "Product description"
  },
  "assets": {
    "hero_image_url": "uploads/main/product.jpg",
    "logo_url": "uploads/watermark/logo.png"
  },
  "options": {
    "remove_hero_background": true,
    "logo_position": "top-left"
  }
}
```

### Pattern 3: Text-Only Checklist

```json
{
  "layout_type": "checklist",
  "content": {
    "title": "Checklist Title",
    "items": ["Item 1", "Item 2", "Item 3"]
  },
  "background": {
    "mode": "solid_color",
    "color": [255, 255, 255]
  }
}
```

---

## 🔍 Understanding Responses

### Success Response

```json
{
  "success": true,
  "layout_type": "headline_promo",
  "generated_files": [
    {
      "slide": 1,
      "download_url": "/generated/headline_promo_abc123_slide1.png",
      "filename": "headline_promo_abc123_slide1.png",
      "width": 1080,
      "height": 1350,
      "size_bytes": 32768
    }
  ],
  "total_slides": 1,
  "generated_at": "2025-10-28T12:00:00"
}
```

### Error Response

```json
{
  "error": "InvalidRequest",
  "message": "Layout type 'invalid' is not supported",
  "timestamp": "2025-10-28T12:00:00"
}
```

### Accessing Generated Files

```bash
# Full URL
curl http://localhost:5000/generated/headline_promo_abc123_slide1.png

# In browser
http://localhost:5000/generated/headline_promo_abc123_slide1.png
```

---

## 🧪 Testing Workflow

### 1. Test Each Layout Type

```bash
# Test headline_promo
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_1_minimal.json

# Test checklist
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/checklist/example_1_basic.json

# Test product_showcase
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/product_showcase/example_1_basic.json
```

### 2. Check Available Layouts

```bash
curl http://localhost:5000/layouts | jq .
```

### 3. Test Background Removal

```bash
# First upload a product image
curl -X POST http://localhost:5000/upload/main \
  -F "file=@product.png"

# Then generate with background removal
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "product_showcase",
    "content": {"product_name": "Product", "price": "$99"},
    "assets": {"hero_image_url": "uploads/main/product.png"},
    "background": {"mode": "solid_color", "color": [255, 255, 255]},
    "options": {"remove_hero_background": true}
  }'
```

---

## 📚 Reference Documentation

### API Documentation
- OpenAPI Spec: `docs/openapi.yaml`
- API README: `docs/README.md`
- Available layouts: `GET /layouts`
- Gradient info: `GET /gradient_info`
- Text layout info: `GET /text_layout_info`

### Examples
- Headline Promo: `examples/headline_promo/`
- Checklist: `examples/checklist/`
- Product Showcase: `examples/product_showcase/`
- Carousel: `examples/carousel/`
- Caption Box: `examples/caption_box/`
- Overlay Text: `examples/overlay_text/`
- Split Image Text: `examples/split_image_text/`
- Testimonial: `examples/testimonial/`

### Example README
- `examples/README.md` - Complete examples guide

---

## 🎓 Learning Path

### Beginner
1. Start with `examples/headline_promo/example_1_minimal.json`
2. Try different layouts from examples
3. Test gradient colors
4. Add logos and images

### Intermediate
1. Create carousels with multiple slides
2. Use background removal
3. Customize colors and fonts
4. Mix different layout types

### Advanced
1. Build complex multi-slide campaigns
2. Optimize for different platforms
3. Create your own layouts
4. Integrate into your applications

---

## 🐛 Troubleshooting

### Common Issues

**1. "Layout type not found"**
- Check `GET /layouts` for available layouts
- Ensure `layout_type` matches exactly

**2. "File not found"**
- Verify file path in `assets`
- Upload files first using `/upload` endpoints
- Check `GET /files` to see uploaded files

**3. "Background removal failed"**
- Try different `bg_removal_method`
- Ensure image has clear subject
- Check image format (PNG recommended)

**4. "Font rendering issues with Farsi"**
- Ensure using supported fonts
- Check text direction
- Verify UTF-8 encoding

### Debug Mode

```bash
# Enable verbose logging
export FLASK_DEBUG=1

# Check server logs
tail -f server.log

# Test with curl verbose
curl -v -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_1_minimal.json
```

---

## 💡 Best Practices

### 1. Start Simple
Begin with minimal examples, then add complexity.

### 2. Use Examples as Templates
Copy example JSON files and modify for your needs.

### 3. Organize Your Assets
```bash
uploads/
  watermark/
    brand-logo.png
  main/
    product-1.jpg
    product-2.jpg
  background/
    bg-1.png
```

### 4. Use Consistent Colors
Define brand colors in your project and reuse them.

### 5. Test Locally First
Run API locally before deploying to production.

### 6. Monitor File Sizes
Large images can slow generation. Optimize before upload.

### 7. Cache Results
Reuse generated images when possible to save processing time.

---

## 🚀 Next Steps

1. **Explore Examples** - Try all examples in each layout folder
2. **Read API Docs** - Deep dive into `docs/openapi.yaml`
3. **Build a Campaign** - Create a complete Instagram carousel
4. **Integrate API** - Add to your application or workflow
5. **Customize** - Adapt to your brand and use cases

---

## 📞 Getting Help

- **API Documentation**: See `docs/README.md`
- **OpenAPI Spec**: View `docs/openapi.yaml`
- **Examples**: Browse `examples/` directory
- **Health Check**: `GET /health`
- **Layout Info**: `GET /layouts`

---

## 📝 Quick Reference

### Essential Endpoints
```bash
GET  /                                # API docs
GET  /health                          # Health check
GET  /layouts                         # List layouts
POST /generate_post                   # Generate image (main)
POST /upload/main                     # Upload image
POST /upload/watermark                # Upload logo
GET  /uploads/{folder}/{filename}     # Get uploaded file
GET  /generated/{filename}            # Get generated image
```

### Essential Example Files
```bash
examples/headline_promo/example_3_with_cta.json
examples/checklist/example_1_basic.json
examples/product_showcase/example_1_basic.json
examples/carousel/yuan_payment_simple.json
```

### Essential Background Colors
```json
"colors": [[255, 107, 107], [253, 187, 45]]  // Red-orange gradient
"colors": [[78, 205, 196], [255, 107, 107]]  // Teal-red gradient
"colors": [[200, 16, 46], [255, 215, 0]]     // Red-gold gradient
```

---

**Remember**: You need both API docs (how it works) and examples (how to use it) to be successful!

This combined guide gives you both. Happy image generating! 🎨

