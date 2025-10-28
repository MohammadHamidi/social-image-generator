# How to Use AI-Generated Images with Yuan Payment Carousel

This guide shows you how to integrate custom AI-generated images into your Instagram carousel posts.

## Overview

The Yuan Payment carousel generator supports two workflows:

1. **No Images Mode**: Pure design using gradients and solid colors (works immediately)
2. **Custom Images Mode**: Add your own AI-generated images for richer visual content

## Image Specifications

### Recommended Dimensions

| Layout Type | Dimensions | Aspect Ratio | Use Case |
|------------|------------|--------------|----------|
| Portrait | 1080 x 1350px | 4:5 | Standard Instagram post |
| Square | 1080 x 1080px | 1:1 | Product showcases |
| Landscape | 1080 x 608px | 16:9 | Wide backgrounds |

### File Requirements

- **Format**: JPG or PNG
- **Max File Size**: 10MB recommended
- **Background**: Can be solid, gradient, or transparent (PNG)
- **Color Space**: RGB (not CMYK)

## Generating Images with AI Tools

### Midjourney

**Prompt Template:**
```
[subject], Chinese business theme, red and gold colors, modern minimalist,
professional, high quality, 4k --ar 4:5
```

**Example Prompts:**

1. **Money Transfer:**
```
digital payment transfer, Chinese yuan symbol, modern fintech,
red and gold gradient background, professional business style,
clean composition --ar 4:5
```

2. **Trusted Supplier:**
```
business handshake, Chinese marketplace, trustworthy seller,
professional setting, red accents, modern photography --ar 4:5
```

3. **Hidden Costs:**
```
transparent pricing concept, financial calculator, cost breakdown,
gold coins, professional business illustration, clean style --ar 4:5
```

4. **Cosmetics Import:**
```
luxury cosmetics products, Chinese imports, beauty products layout,
elegant presentation, soft lighting, red and gold theme --ar 1:1
```

**Midjourney Settings:**
- Use `--ar 4:5` for portrait images
- Use `--ar 1:1` for square images
- Add `--stylize 500` for more artistic results
- Add `--quality 2` for higher quality

### DALL-E 3

**Prompt Template:**
```
Create a professional business illustration of [subject] in a modern Chinese
theme with red (#C8102E) and gold (#FFD700) colors. The image should be
clean, minimalist, and suitable for Instagram marketing.
```

**Example Prompts:**

1. **Money Transfer:**
```
Create a professional illustration of digital money transfer between countries,
featuring Chinese yuan symbols and modern fintech elements. Use Chinese red
(#C8102E) and gold (#FFD700) as primary colors. Modern, clean, minimalist style.
Vertical composition for Instagram.
```

2. **Trusted Supplier:**
```
Professional business photograph of a trustworthy Chinese supplier in a modern
office setting. Include subtle red and gold accents. Clean, professional
composition. Suitable for business marketing on Instagram.
```

### Stable Diffusion

**Model Recommendations:**
- SDXL 1.0 or newer
- Realistic Vision v5.1
- DreamShaper XL

**Prompt Template:**
```
professional photograph of [subject], Chinese business theme, red and gold
color scheme, modern minimalist, studio lighting, high quality, 8k,
masterpiece, best quality
```

**Negative Prompt:**
```
low quality, blurry, distorted, watermark, text, logo, signature,
amateur, poor lighting, cluttered
```

### Leonardo AI

**Settings:**
- Model: Leonardo Diffusion XL or Phoenix
- Image Dimensions: 832 x 1216 (portrait) or 1024 x 1024 (square)
- Guidance Scale: 7-9
- Steps: 30-50

## Upload Directory Structure

Create the following directory structure for your images:

```
social-image-generator/
└── uploads/
    ├── ai-generated/          # Your custom AI images
    │   ├── china-payment-transfer.jpg
    │   ├── trusted-supplier.jpg
    │   ├── hidden-costs.jpg
    │   └── cosmetics-products.jpg
    └── watermark/             # Logo files
        └── yuan-payment-logo.png
```

## How to Upload Images

### Method 1: Direct Upload (Local Development)

```bash
# From your project directory
cd social-image-generator

# Create directory if it doesn't exist
mkdir -p uploads/ai-generated

# Copy your images
cp /path/to/your/images/*.jpg uploads/ai-generated/
```

### Method 2: Docker Volume Mount (Production)

The `uploads/` directory is automatically mounted as a Docker volume. Simply place your images in the directory and restart the container:

```bash
docker-compose restart
```

### Method 3: API Upload (Coming Soon)

Future versions will include an API endpoint for image uploads.

## Referencing Images in Configs

### Basic Reference

```json
{
  "slide": 2,
  "layout_type": "split_image_text",
  "assets": {
    "hero_image_url": "uploads/ai-generated/china-payment-transfer.jpg",
    "logo_url": "uploads/watermark/yuan-payment-logo.png"
  }
}
```

### Background Image

```json
{
  "slide": 3,
  "layout_type": "overlay_text",
  "assets": {
    "hero_image_url": "uploads/ai-generated/trusted-supplier.jpg"
  },
  "background": {
    "mode": "image_overlay",
    "overlay_opacity": 0.3,
    "overlay_color": [200, 16, 46]
  }
}
```

### Product Showcase

```json
{
  "slide": 5,
  "layout_type": "product_showcase",
  "assets": {
    "hero_image_url": "uploads/ai-generated/cosmetics-products.jpg"
  },
  "options": {
    "product_position": "center",
    "show_price": true
  }
}
```

## Fallback Behavior

If an image file is missing or cannot be loaded:

1. **Graceful Degradation**: The generator will continue without the image
2. **Console Warning**: A warning message will appear in the logs
3. **Background Fallback**: The slide will use the background color/gradient specified

**Example:**
```
⚠️  WARNING: Could not load image: uploads/ai-generated/missing.jpg
✓ Falling back to background gradient
```

## Testing Your Setup

### 1. Generate Without Images

First, test the no-images version to ensure everything works:

```bash
cd social-image-generator

# Generate using no-images config
python src/main.py \
  --config examples/carousel/yuan_payment_no_images.json \
  --output output/yuan_payment_no_images
```

### 2. Add One Image

Add a single test image and update the config:

```bash
# Copy test image
mkdir -p uploads/ai-generated
cp path/to/test-image.jpg uploads/ai-generated/

# Generate with images config
python src/main.py \
  --config examples/carousel/yuan_payment_with_images.json \
  --output output/yuan_payment_with_images
```

### 3. Add All Images

Once one image works, add the rest according to your config.

## Troubleshooting

### Image Not Appearing

**Problem**: Image doesn't show in generated carousel

**Solutions:**
1. Check file path is correct (case-sensitive on Linux)
2. Verify file exists in `uploads/` directory
3. Check file permissions: `chmod 644 uploads/ai-generated/*.jpg`
4. Review logs for error messages

### Image Quality Issues

**Problem**: Images look pixelated or low quality

**Solutions:**
1. Use higher resolution source images (minimum 1080px width)
2. Save as high-quality JPG (90-100% quality) or PNG
3. Avoid upscaling small images
4. Re-generate with better AI settings

### Wrong Aspect Ratio

**Problem**: Images are cropped incorrectly

**Solutions:**
1. Use recommended dimensions (1080x1350 or 1080x1080)
2. Check layout type requirements
3. Enable `smart_crop` option for automatic adjustment
4. Pre-crop images to exact dimensions before upload

### Permission Denied

**Problem**: Cannot write to uploads directory

**Solutions:**
```bash
# Fix permissions
chmod 755 uploads/
chmod 755 uploads/ai-generated/
chmod 644 uploads/ai-generated/*.jpg
```

### Large File Size

**Problem**: Upload takes too long or fails

**Solutions:**
1. Compress images to under 5MB
2. Use JPG instead of PNG for photos
3. Use online tools like TinyPNG to reduce size without quality loss

## Best Practices

### 1. Consistent Style

- Use the same AI model for all images in a carousel
- Keep the same lighting and style
- Maintain consistent color themes (red and gold)

### 2. Naming Convention

Use descriptive, lowercase names with hyphens:

```
✓ good-examples:
  china-payment-transfer.jpg
  trusted-supplier.jpg
  hidden-costs.jpg

✗ bad-examples:
  IMG_1234.jpg
  screenshot 2023.png
  pic.jpg
```

### 3. Backup Your Images

Always keep original AI-generated images in a separate backup folder:

```
my-project/
├── ai-images-backup/      # Keep originals here
│   └── originals/
└── social-image-generator/
    └── uploads/
        └── ai-generated/   # Copies for production
```

### 4. Version Control

For team projects, use `.gitignore` to exclude large image files:

```gitignore
# .gitignore
uploads/ai-generated/*.jpg
uploads/ai-generated/*.png

# Keep the directory structure
!uploads/ai-generated/.gitkeep
```

## Example Workflow

### Complete Example: Creating a 7-Slide Carousel

**Step 1**: Generate AI images

```bash
# Use Midjourney to generate 4 images
# Save them locally as:
# - payment-transfer.jpg (slide 2)
# - trusted-seller.jpg (slide 3)
# - transparency.jpg (slide 4)
# - cosmetics.jpg (slide 5)
```

**Step 2**: Upload images

```bash
cd social-image-generator
mkdir -p uploads/ai-generated
cp ~/Downloads/payment-*.jpg uploads/ai-generated/
```

**Step 3**: Update config

```json
{
  "carousel_posts": [
    {
      "slide": 2,
      "assets": {
        "hero_image_url": "uploads/ai-generated/payment-transfer.jpg"
      }
    }
    // ... more slides
  ]
}
```

**Step 4**: Generate carousel

```bash
python src/main.py \
  --config examples/carousel/yuan_payment_with_images.json \
  --output output/my_carousel
```

**Step 5**: Review and iterate

Check the output images and adjust:
- Image positions
- Overlay opacity
- Text placement
- Colors

## Need Help?

- Check the Quick Start Guide: `fix/QUICK_START_CAROUSEL.md`
- Review example configs: `examples/carousel/`
- Check logs for error messages: `docker-compose logs`
- Open an issue on GitHub for bug reports

## Coming Soon

- [ ] Web UI for image upload
- [ ] Automatic image optimization
- [ ] Background removal integration
- [ ] Batch image processing
- [ ] AI prompt suggestions based on carousel theme
