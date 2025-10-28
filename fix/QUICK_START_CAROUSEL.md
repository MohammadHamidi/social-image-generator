# Yuan Payment Carousel - Quick Start Guide

Get your Instagram carousel generated in 5 minutes with this guide.

## Prerequisites

- Docker and Docker Compose installed
- Basic knowledge of JSON (or just copy/paste the examples!)

## Method 1: No Images (Fastest - 2 Minutes)

Perfect for getting started without worrying about images.

### Step 1: Clone or Navigate to Project

```bash
cd social-image-generator
```

### Step 2: Ensure Logo Exists

The Yuan Payment logo should already be in place:
```bash
ls uploads/watermark/yuan-payment-logo.png
```

If missing, regenerate it:
```bash
python3 generate_logo.py
```

### Step 3: Generate Carousel

```bash
# Using Docker
docker-compose run --rm app python src/main.py \
  --config examples/carousel/yuan_payment_no_images.json \
  --output output/yuan_payment

# Or without Docker (if you have Python environment)
python src/main.py \
  --config examples/carousel/yuan_payment_no_images.json \
  --output output/yuan_payment
```

### Step 4: Find Your Images

```bash
ls output/yuan_payment/
# You should see: slide_1.jpg, slide_2.jpg, ..., slide_7.jpg
```

**Done!** You now have 7 ready-to-post Instagram carousel images.

## Method 2: With Custom Images (5 Minutes)

Add your own AI-generated images for richer content.

### Step 1: Prepare Your Images

Generate 4 images using AI tools (Midjourney, DALL-E, etc.):

| Slide | Image Subject | Recommended Prompt |
|-------|--------------|-------------------|
| 2 | Payment Transfer | "digital payment, Chinese yuan, fintech, red and gold --ar 4:5" |
| 3 | Trusted Supplier | "business handshake, Chinese marketplace, professional --ar 4:5" |
| 4 | Hidden Costs | "transparent pricing, financial calculator, modern --ar 4:5" |
| 5 | Cosmetics | "luxury cosmetics, Chinese imports, elegant --ar 1:1" |

Save them as:
- `china-payment-transfer.jpg`
- `trusted-supplier.jpg`
- `hidden-costs.jpg`
- `cosmetics-products.jpg`

### Step 2: Upload Images

```bash
mkdir -p uploads/ai-generated
cp /path/to/your/images/*.jpg uploads/ai-generated/
```

### Step 3: Verify Image References

The config `yuan_payment_with_images.json` already references these files:

```bash
cat examples/carousel/yuan_payment_with_images.json | grep hero_image_url
```

### Step 4: Generate Carousel

```bash
docker-compose run --rm app python src/main.py \
  --config examples/carousel/yuan_payment_with_images.json \
  --output output/yuan_payment_custom
```

### Step 5: Review Output

```bash
ls output/yuan_payment_custom/
# Opens first slide in default viewer (Linux/Mac)
xdg-open output/yuan_payment_custom/slide_1.jpg
```

## Method 3: Customize Your Own

Create a custom carousel in 10 minutes.

### Step 1: Copy Example Config

```bash
cp examples/carousel/yuan_payment_no_images.json \
   examples/carousel/my_custom_carousel.json
```

### Step 2: Edit Content

Open `my_custom_carousel.json` and modify:

```json
{
  "carousel_posts": [
    {
      "slide": 1,
      "layout_type": "headline_promo",
      "content": {
        "headline": "Your Headline Here",
        "subheadline": "Your subheadline here",
        "cta": "Your CTA Button Text"
      },
      "background": {
        "mode": "gradient",
        "gradient": {
          "colors": [
            [200, 16, 46],   // Chinese Red
            [255, 215, 0]    // Gold
          ],
          "direction": "diagonal"
        }
      }
    }
  ]
}
```

### Step 3: Customize Colors

Use the Chinese theme colors or create your own:

```json
"metadata": {
  "brand_colors": {
    "primary_red": [200, 16, 46],    // #C8102E
    "gold": [255, 215, 0],           // #FFD700
    "black": [28, 28, 28],           // #1C1C1C
    "white": [255, 255, 255]         // #FFFFFF
  }
}
```

**Color Scheme Generator Tools:**
- Coolors.co - Generate color palettes
- Adobe Color - Create harmonious colors
- Paletton - Color scheme designer

### Step 4: Test Your Config

```bash
# Validate JSON syntax
python -m json.tool examples/carousel/my_custom_carousel.json

# Generate carousel
docker-compose run --rm app python src/main.py \
  --config examples/carousel/my_custom_carousel.json \
  --output output/my_carousel
```

## Common Customizations

### Change Text

```json
{
  "content": {
    "headline": "تخفیف ویژه",           // Special Offer
    "subheadline": "فقط امروز!",       // Only Today!
    "cta": "خرید کنید"                 // Buy Now
  }
}
```

### Adjust Font Sizes

```json
{
  "options": {
    "headline_size": 84,        // Larger headline
    "subheadline_size": 42,     // Smaller subheadline
    "cta_size": 32              // Button text size
  }
}
```

### Change Button Colors

```json
{
  "options": {
    "cta_bg_color": [255, 215, 0],      // Gold background
    "cta_text_color": [200, 16, 46]     // Red text
  }
}
```

### Modify Gradient

```json
{
  "background": {
    "mode": "gradient",
    "gradient": {
      "colors": [
        [255, 107, 107],    // Start color (Coral)
        [253, 187, 45]      // End color (Yellow)
      ],
      "direction": "vertical"  // or "horizontal", "diagonal"
    }
  }
}
```

### Solid Color Background

```json
{
  "background": {
    "mode": "solid_color",
    "color": [255, 255, 255]  // White
  }
}
```

### Logo Position

```json
{
  "options": {
    "logo_position": "top-center",    // or "bottom-center", "top-right", etc.
    "logo_size": 120                  // Size in pixels
  }
}
```

## Available Layout Types

### 1. Headline Promo
Big headline with optional CTA button
```json
{
  "layout_type": "headline_promo",
  "content": {
    "headline": "Big Announcement",
    "subheadline": "Supporting text",
    "cta": "Learn More"
  }
}
```

### 2. Split Image Text
Text on one side, image on the other
```json
{
  "layout_type": "split_image_text",
  "content": {
    "title": "Feature Title",
    "description": "Description text",
    "bullets": ["Point 1", "Point 2", "Point 3"]
  },
  "assets": {
    "hero_image_url": "uploads/ai-generated/image.jpg"
  }
}
```

### 3. Overlay Text
Text overlaid on background image
```json
{
  "layout_type": "overlay_text",
  "content": {
    "headline": "Main Message",
    "subheadline": "Supporting text"
  },
  "assets": {
    "hero_image_url": "uploads/ai-generated/background.jpg"
  },
  "background": {
    "mode": "image_overlay",
    "overlay_opacity": 0.3,
    "overlay_color": [200, 16, 46]
  }
}
```

### 4. Caption Box
Image with caption overlay
```json
{
  "layout_type": "caption_box",
  "content": {
    "title": "Title",
    "caption": "Main caption text",
    "details": "Additional details"
  },
  "assets": {
    "hero_image_url": "uploads/ai-generated/photo.jpg"
  }
}
```

### 5. Product Showcase
Centered product display
```json
{
  "layout_type": "product_showcase",
  "content": {
    "product_name": "Product Name",
    "description": "Product description",
    "price": "$99"
  },
  "assets": {
    "hero_image_url": "uploads/ai-generated/product.jpg"
  }
}
```

### 6. Checklist
List with checkmarks
```json
{
  "layout_type": "checklist",
  "content": {
    "title": "Complete Guide",
    "items": [
      "Step 1",
      "Step 2",
      "Step 3"
    ],
    "brand": "@yourbrand"
  }
}
```

## Workflow Examples

### Example 1: Product Launch (3 Slides)

```json
{
  "carousel_posts": [
    {
      "slide": 1,
      "layout_type": "headline_promo",
      "content": {
        "headline": "New Product",
        "subheadline": "Available Now",
        "cta": "Shop Now"
      }
    },
    {
      "slide": 2,
      "layout_type": "product_showcase",
      "content": {
        "product_name": "Amazing Product",
        "description": "Revolutionary features",
        "price": "$299"
      }
    },
    {
      "slide": 3,
      "layout_type": "headline_promo",
      "content": {
        "headline": "Limited Time Offer",
        "cta": "Order Today"
      }
    }
  ]
}
```

### Example 2: Educational (5 Slides)

```json
{
  "carousel_posts": [
    {
      "slide": 1,
      "layout_type": "headline_promo",
      "content": {
        "headline": "Complete Guide",
        "subheadline": "Everything You Need to Know",
        "cta": "Swipe to Learn →"
      }
    },
    {
      "slide": 2,
      "layout_type": "split_image_text",
      "content": {
        "title": "Step 1: Basics",
        "bullets": ["Point A", "Point B", "Point C"]
      }
    },
    {
      "slide": 3,
      "layout_type": "split_image_text",
      "content": {
        "title": "Step 2: Advanced",
        "bullets": ["Point D", "Point E", "Point F"]
      }
    },
    {
      "slide": 4,
      "layout_type": "checklist",
      "content": {
        "title": "Quick Reference",
        "items": ["Tip 1", "Tip 2", "Tip 3"]
      }
    },
    {
      "slide": 5,
      "layout_type": "headline_promo",
      "content": {
        "headline": "Ready to Start?",
        "cta": "Get Started"
      }
    }
  ]
}
```

## Troubleshooting

### "File not found" Error

```bash
# Check if file exists
ls examples/carousel/yuan_payment_no_images.json

# If missing, the file might be in a different location
find . -name "yuan_payment*.json"
```

### "Cannot connect to Docker daemon"

```bash
# Start Docker service
sudo systemctl start docker

# Or use Docker Desktop (Mac/Windows)
```

### "Permission denied" When Writing Output

```bash
# Fix permissions
chmod -R 755 output/

# Or run with sudo (not recommended)
sudo docker-compose run --rm app python src/main.py ...
```

### Text Shows as Squares (□□□□)

This means fonts aren't loaded properly. Rebuild the Docker container:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Wrong Colors

Check your RGB values are in 0-255 range:
```json
// ✓ Correct
"color": [200, 16, 46]

// ✗ Wrong (hex not supported directly)
"color": "#C8102E"

// ✗ Wrong (values too high)
"color": [300, 16, 46]
```

### Image Quality Poor

Use higher resolution source images:
- Minimum: 1080px width
- Recommended: 1080x1350px (portrait) or 1080x1080px (square)
- Format: JPG (90%+ quality) or PNG

## Next Steps

1. **Customize Content**: Edit the JSON configs to match your brand
2. **Add Images**: Follow the [Custom Images Guide](HOW_TO_USE_CUSTOM_IMAGES.md)
3. **Post on Instagram**: Upload your generated images to Instagram
4. **Iterate**: Generate new versions with different colors/text/layouts

## Performance Tips

### Batch Generation

Generate multiple carousels at once:

```bash
#!/bin/bash
# generate_all.sh

configs=(
  "yuan_payment_no_images"
  "yuan_payment_with_images"
  "my_custom_carousel"
)

for config in "${configs[@]}"; do
  echo "Generating $config..."
  docker-compose run --rm app python src/main.py \
    --config "examples/carousel/${config}.json" \
    --output "output/${config}"
done

echo "All carousels generated!"
```

### Faster Docker Builds

Keep Docker images up to date:
```bash
# Pull latest changes
git pull

# Rebuild only if Dockerfile changed
docker-compose build

# Start services
docker-compose up -d
```

## API Usage

Start the API server for programmatic access:

```bash
# Start server
docker-compose up -d

# Check status
curl http://localhost:8000/health

# Generate carousel via API
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d @examples/carousel/yuan_payment_no_images.json

# Download generated images
curl http://localhost:8000/api/download/latest
```

See [OpenAPI documentation](../docs/openapi.yaml) for full API reference.

## Getting Help

- **Documentation**: Check `fix/` directory for detailed guides
- **Examples**: Browse `examples/carousel/` for config templates
- **Logs**: Run `docker-compose logs` to see error messages
- **Issues**: Report bugs on GitHub

## Frequently Asked Questions

**Q: Can I use English text instead of Farsi?**
A: Yes! Just replace the content with English text. The system auto-detects RTL languages.

**Q: How many slides can I have?**
A: Instagram supports up to 10 slides per carousel. We recommend 5-7 for optimal engagement.

**Q: Can I change the canvas size?**
A: Yes, edit the canvas dimensions in your config or use the API parameters.

**Q: How do I add my own fonts?**
A: Place font files in `src/fonts/` directory and update font paths in the config.

**Q: Can I remove the logo?**
A: Yes, just omit the `logo_url` field from the assets section.

**Q: How do I schedule posts?**
A: Use Instagram's built-in scheduling feature or third-party tools like Later, Buffer, or Hootsuite.

## Resources

- [Instagram Best Practices](https://business.instagram.com/blog)
- [Color Palette Generator](https://coolors.co)
- [Midjourney Documentation](https://docs.midjourney.com)
- [DALL-E Guide](https://help.openai.com/en/articles/6654000-dall-e-guide)

## Success Checklist

- [ ] Generated first carousel using no-images config
- [ ] Reviewed all 7 slides
- [ ] Customized text content for my brand
- [ ] Adjusted colors to match brand palette
- [ ] Added custom logo
- [ ] Generated version with AI images (optional)
- [ ] Uploaded to Instagram
- [ ] Monitored engagement metrics

**Congratulations!** You're now ready to create stunning Instagram carousels with Yuan Payment generator.

---

**Need more help?** Check the detailed guide: [HOW_TO_USE_CUSTOM_IMAGES.md](HOW_TO_USE_CUSTOM_IMAGES.md)
