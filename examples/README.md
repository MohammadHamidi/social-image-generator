# Example Requests for Social Image Generator

This directory contains example JSON requests for each layout type supported by the Social Image Generator API.

## Directory Structure

```
examples/
├── headline_promo/          # Marketing-focused headlines with CTA
│   ├── example_1_minimal.json
│   ├── example_2_with_subheadline.json
│   ├── example_3_with_cta.json
│   ├── example_4_farsi.json
│   └── example_5_solid_background.json
├── quote/                   # Coming soon
├── product_showcase/        # Coming soon
└── ...                      # More layouts
```

## How to Use Examples

### Via curl (Command Line)

```bash
# Example 1: Minimal headline
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_1_minimal.json

# Example 2: With subheadline
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_2_with_subheadline.json

# Example 3: Full (headline + subheadline + CTA)
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_3_with_cta.json

# Example 4: Farsi text
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d @examples/headline_promo/example_4_farsi.json
```

### Via Python

```python
import requests
import json

# Load example
with open('examples/headline_promo/example_1_minimal.json') as f:
    data = json.load(f)

# Send request
response = requests.post(
    'http://localhost:5000/generate_post',
    json=data
)

# Get result
result = response.json()
print(f"Generated: {result['generated_files'][0]['download_url']}")
```

### Via JavaScript/Fetch

```javascript
// Load and send example
fetch('http://localhost:5000/generate_post', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: await fetch('./examples/headline_promo/example_1_minimal.json').then(r => r.text())
})
  .then(response => response.json())
  .then(data => {
    console.log('Generated:', data.generated_files[0].download_url);
  });
```

## Example Breakdown

### headline_promo

Marketing-focused layout with big headline, optional subheadline, and CTA button.

**example_1_minimal.json** - Simplest form (headline only)
- Headline: "Summer Sale"
- Background: Red-orange vertical gradient

**example_2_with_subheadline.json** - Headline + subheadline
- Headline: "Summer Sale"
- Subheadline: "Up to 50% Off Everything"
- Background: Red-orange vertical gradient

**example_3_with_cta.json** - Full content (headline + subheadline + CTA)
- Headline: "Summer Sale"
- Subheadline: "Up to 50% Off Everything"
- CTA: "Shop Now" (white button)
- Background: Red-orange vertical gradient

**example_4_farsi.json** - Farsi/Persian text with RTL support
- Headline: "فروش تابستانی" (Summer Sale)
- Subheadline: "تا ۵۰٪ تخفیف روی همه محصولات" (Up to 50% off all products)
- CTA: "خرید کنید" (Shop)
- Background: Teal-red vertical gradient

**example_5_solid_background.json** - Solid color background
- Headline: "New Product Launch"
- Subheadline: "Coming Soon This Fall"
- CTA: "Get Notified"
- Background: Solid dark blue (#34495E)

## Customization Options

All examples support these optional parameters:

### Background Options

```json
"background": {
  "mode": "gradient | solid_color | image",

  // If mode = "gradient"
  "gradient": {
    "colors": [[R1, G1, B1], [R2, G2, B2], ...],
    "direction": "vertical | horizontal"
  },

  // If mode = "solid_color"
  "color": [R, G, B],

  // If mode = "image" (coming soon)
  "image_url": "https://example.com/bg.jpg"
}
```

### Layout-Specific Options

```json
"options": {
  "width": 1080,           // Canvas width (default: 1080)
  "height": 1350,          // Canvas height (default: 1350)
  "headline_size": 84,     // Font size for headline
  "subheadline_size": 42,  // Font size for subheadline
  "cta_size": 32,          // Font size for CTA button
  "headline_color": [255, 255, 255],      // RGB color
  "subheadline_color": [240, 240, 240],   // RGB color
  "cta_bg_color": [255, 255, 255],        // Button background
  "cta_text_color": [52, 73, 94]          // Button text
}
```

### Asset Options (for photo-based layouts)

```json
"assets": {
  "hero_image_url": "https://example.com/product.jpg",
  "logo_image_url": "https://example.com/logo.png"
}
```

## Response Format

All requests return:

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
  "generated_at": "2025-10-26T12:00:00.000000"
}
```

## Testing Examples

Run all examples:

```bash
python test_headline_promo.py
```

This will generate all examples and save them to `test_output/`.

## Adding New Examples

1. Create a new JSON file in the appropriate layout directory
2. Follow the structure of existing examples
3. Test with `curl` or the Python test script
4. Commit the example to the repository

## Available Layouts

Currently implemented:
- ✅ **headline_promo** - Marketing headlines with CTA

Coming soon:
- 🔨 **quote** - Text quotes with author attribution
- 🔨 **product_showcase** - Product photos with pricing
- 🔨 **split_image_text** - Half photo, half text
- 🔨 **checklist** - Bulleted lists
- 🔨 **carousel_text** - Multi-slide text content

## Getting Layout Information

List all available layouts:

```bash
curl http://localhost:5000/layouts
```

Get schema for specific layout:

```bash
curl http://localhost:5000/layouts | jq '.layouts.headline_promo'
```

## Support

- API Documentation: See main README
- Issues: https://github.com/MohammadHamidi/social-image-generator/issues
- Examples: This directory
