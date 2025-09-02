# 🚀 Complete cURL Reference for Social Image Generator API

## 📍 Base URLs
- **Local Development**: `http://localhost:5000`
- **Docker Container**: `http://localhost:5000`
- **Production**: Configure your server URL

---

## 🔧 Configuration & System

### 1. Get API Documentation
```bash
curl http://localhost:5000/
```

### 2. Health Check
```bash
curl http://localhost:5000/health
```

### 3. Get Current Configuration
```bash
curl http://localhost:5000/config
```

### 4. Update URL Configuration
```bash
# Set to return relative paths (default)
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": false}'

# Set to return full URLs
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": true}'
```

---

## 📤 File Upload Endpoints

### 5. Upload Main Image
```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@/path/to/your/image.png"
```

### 6. Upload Watermark/Logo
```bash
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@/path/to/your/logo.png"
```

### 7. Upload Background Image
```bash
curl -X POST http://localhost:5000/upload/background \
  -F "file=@/path/to/your/background.png"
```

---

## 🖼️ Image Generation Endpoints

### 8. Generate Social Media Image
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Your Amazing Headline",
    "subheadline": "Supporting text goes here",
    "brand": "Your Brand Name",
    "background_color": [255, 255, 255],
    "main_image_url": "/uploads/main/filename.png",
    "watermark_image_url": "/uploads/watermark/filename.png",
    "background_image_url": "/uploads/background/filename.png",
    "watermark_position": "bottom-right"
  }'
```

**Watermark Positions Available:**
- `bottom-right` (default)
- `top-right`
- `bottom-center`
- `top-left`
- `bottom-left`

### 9. Generate Text-Based Layout
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "quote",
    "content": {
      "quote": "Success is not final, failure is not fatal.",
      "author": "Winston Churchill",
      "brand": "Inspiration Daily"
    }
  }'
```

**Supported Layout Types:**
- `quote` - Large quote with attribution
- `article` - Article excerpt with title and body
- `announcement` - Announcement with call-to-action
- `list` - List layout with bulleted items
- `testimonial` - Testimonial with quote and person info

### 10. Generate All Text Layouts
```bash
curl -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "Success is not final, failure is not fatal.",
      "author": "Winston Churchill",
      "brand": "Inspiration Daily"
    },
    "output_prefix": "inspirational_quote"
  }'
```

---

## 🎨 Gradient Generation

### 11. Generate Gradient Image
```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02,
    "apply_dither": false,
    "generate_harmony": false,
    "quality": 95
  }'
```

**Advanced Gradient Options:**
```bash
# With Auto Color Harmony
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B"],
    "gradient_type": "linear",
    "direction": "horizontal",
    "generate_harmony": true,
    "harmony_type": "triadic",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02
  }'

# Radial Gradient
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080,
    "colors": ["#FFFFFF", "#FF6B6B"],
    "gradient_type": "radial",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.025
  }'
```

**Gradient Types:**
- `linear` - Linear gradient with smooth transitions
- `radial` - Radial gradient emanating from center
- `diagonal` - Diagonal linear gradient

**Directions:**
- `vertical` - Top to bottom
- `horizontal` - Left to right
- `diagonal` - Corner to corner

**Harmony Types:**
- `triadic` - 3 colors, 120° apart
- `complementary` - Opposite colors
- `analogous` - Similar colors

### 12. Get Gradient Information
```bash
curl http://localhost:5000/gradient_info
```

---

## 📋 Information & Utility Endpoints

### 13. List All Files
```bash
curl http://localhost:5000/files
```

### 14. Get Text Layout Information
```bash
curl http://localhost:5000/text_layout_info
```

---

## 📁 File Access Endpoints

### 15. Access Uploaded Files
```bash
# Main images
curl http://localhost:5000/uploads/main/filename.png

# Watermark images
curl http://localhost:5000/uploads/watermark/filename.png

# Background images
curl http://localhost:5000/uploads/background/filename.png
```

### 16. Access Generated Files
```bash
curl http://localhost:5000/generated/filename.png
```

---

## 🔄 Complete Workflow Examples

### Example 1: Full Image Generation Workflow
```bash
#!/bin/bash

# 1. Upload main image
MAIN_RESPONSE=$(curl -s -X POST -F "file=@product.png" http://localhost:5000/upload/main)
MAIN_URL=$(echo $MAIN_RESPONSE | jq -r '.url')
echo "Main image uploaded: $MAIN_URL"

# 2. Upload logo
LOGO_RESPONSE=$(curl -s -X POST -F "file=@logo.png" http://localhost:5000/upload/watermark)
LOGO_URL=$(echo $LOGO_RESPONSE | jq -r '.url')
echo "Logo uploaded: $LOGO_URL"

# 3. Generate final image
GENERATE_RESPONSE=$(curl -s -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"headline\": \"New Product Launch\",
    \"subheadline\": \"Revolutionary Innovation\",
    \"brand\": \"Tech Corp\",
    \"main_image_url\": \"$MAIN_URL\",
    \"watermark_image_url\": \"$LOGO_URL\",
    \"watermark_position\": \"bottom-right\"
  }")

# 4. Get download URL
DOWNLOAD_URL=$(echo $GENERATE_RESPONSE | jq -r '.download_url')
echo "Download your image: $DOWNLOAD_URL"
```

### Example 2: Gradient Generation Workflow
```bash
#!/bin/bash

# Generate multiple gradients
GRADIENT_RESPONSE=$(curl -s -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "gradient_type": "linear",
    "direction": "horizontal",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02,
    "quality": 95
  }')

DOWNLOAD_URL=$(echo $GRADIENT_RESPONSE | jq -r '.download_url')
echo "Gradient generated: $DOWNLOAD_URL"
```

### Example 3: Text Layout Generation
```bash
#!/bin/bash

# Generate all text layouts
TEXT_RESPONSE=$(curl -s -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "The only way to do great work is to love what you do.",
      "author": "Steve Jobs",
      "brand": "Innovation Daily"
    },
    "output_prefix": "steve_jobs_quote"
  }')

echo "Text layouts generated:"
echo $TEXT_RESPONSE | jq -r '.generated_files[].download_url'
```

---

## ⚙️ Configuration Examples

### Set Relative Paths (Default)
```bash
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": false}'
```

**Response URLs will be:**
- `/uploads/main/filename.png`
- `/generated/filename.png`

### Set Full URLs
```bash
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": true}'
```

**Response URLs will be:**
- `http://localhost:5000/uploads/main/filename.png`
- `http://localhost:5000/generated/filename.png`

---

## 🔍 Response Examples

### Successful Upload Response
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "20240115_103000_abc12345.png",
  "url": "/uploads/main/20240115_103000_abc12345.png",
  "size": 524288,
  "upload_time": "2024-01-15T10:30:05.123456"
}
```

### Successful Generation Response
```json
{
  "success": true,
  "message": "Image generated successfully",
  "download_url": "/generated/generated_abc123def456.png",
  "filename": "generated_abc123def456.png",
  "size": 524288,
  "generated_at": "2024-01-15T10:30:05.123456"
}
```

---

## 🚨 Error Handling

### Common Error Responses
```bash
# Missing file
curl -X POST http://localhost:5000/upload/main
# Response: {"error": "No file provided"}

# Invalid JSON
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d 'invalid json'
# Response: {"error": "No JSON data provided"}

# Missing required field
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"subheadline": "Only subheadline"}'
# Response: {"error": "Headline is required"}
```

---

## 📝 Notes

1. **File Formats Supported**: PNG, JPG, JPEG, GIF, WebP
2. **Max File Size**: 16MB per file
3. **Image Dimensions**: Configurable, default 1080x1350
4. **URL Configuration**: Can switch between relative paths and full URLs
5. **CORS Enabled**: All endpoints support cross-origin requests
6. **Error Handling**: Comprehensive error messages with HTTP status codes

---

## 🐳 Docker Usage

If running in Docker, replace `localhost:5000` with your container's IP or mapped port:

```bash
# Check if running in Docker
curl http://your-docker-ip:5000/health

# Or if port mapped
curl http://localhost:9009/health
```
