# 🚀 Comprehensive cURL Reference for Social Image Generator API

## 📍 Base URLs
- **Local Development**: `http://localhost:5000`
- **Docker Container**: `http://localhost:5000`
- **Production**: `http://87.236.166.7:9009`

---

## 🔧 Configuration & System Endpoints

### 1. Get API Documentation
```bash
curl http://87.236.166.7:9009/
```

**Response Example:**
```json
{
  "name": "Social Image Generator API",
  "version": "2.0",
  "description": "Generate custom social media images with uploaded content",
  "status": {
    "directories_initialized": true,
    "upload_ready": true,
    "generation_ready": true
  },
  "endpoints": {
    "POST /upload/main": "Upload main image",
    "POST /upload/watermark": "Upload watermark image",
    "POST /upload/background": "Upload background image",
    "POST /generate": "Generate social media image",
    "POST /generate_text": "Generate text-based layouts",
    "POST /generate_all_text": "Generate all text layouts",
    "POST /generate_gradient": "Generate gradient backgrounds",
    "GET /text_layout_info": "Text layout documentation",
    "GET /health": "Health check",
    "GET /files": "List uploaded files"
  }
}
```

### 2. Health Check
```bash
curl http://87.236.166.7:9009/health
```

**Response Example:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "version": "2.0",
  "system": {
    "python_version": "3.9.6",
    "platform": "darwin",
    "upload_ready": true,
    "generation_ready": true,
    "upload_limit_mb": 16
  },
  "storage": {
    "free_space_gb": 245.67,
    "total_space_gb": 500.0,
    "used_space_gb": 254.33
  }
}
```

### 3. Get Current Configuration
```bash
curl http://87.236.166.7:9009/config
```

**Response Example:**
```json
{
  "return_full_urls": false,
  "description": "When True, returns full URLs. When False, returns relative paths.",
  "example": {
    "full_urls": "http://87.236.166.7:9009/generated/filename.png",
    "relative_paths": "/generated/filename.png"
  }
}
```

### 4. Update URL Configuration
```bash
# Set to return relative paths (default)
curl -X POST http://87.236.166.7:9009/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": false}'
```

**Parameters:**
- `return_full_urls` (boolean): Whether to return full URLs or relative paths

**Response Example:**
```json
{
  "success": true,
  "message": "Configuration updated: return_full_urls = false",
  "return_full_urls": false
}
```

---

## 📤 File Upload Endpoints

### 5. Upload Main Image
```bash
curl -X POST http://87.236.166.7:9009/upload/main \
  -F "file=@/path/to/your/image.png"
```

**Parameters:**
- `file` (file): Image file (PNG, JPG, JPEG, GIF, WebP, max 16MB)

**Success Response (200):**
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

**Error Responses:**
- `400`: No file provided or invalid file type
- `500`: Upload failed

### 6. Upload Watermark/Logo
```bash
curl -X POST http://87.236.166.7:9009/upload/watermark \
  -F "file=@/path/to/your/logo.png"
```

**Parameters:**
- `file` (file): Image file (PNG, JPG, JPEG, GIF, WebP, max 16MB)

**Success Response (200):**
```json
{
  "success": true,
  "message": "Watermark image uploaded successfully",
  "filename": "20240115_103001_def67890.png",
  "url": "/uploads/watermark/20240115_103001_def67890.png",
  "size": 51200,
  "upload_time": "2024-01-15T10:30:06.234567"
}
```

### 7. Upload Background Image
```bash
curl -X POST http://87.236.166.7:9009/upload/background \
  -F "file=@/path/to/your/background.png"
```

**Parameters:**
- `file` (file): Image file (PNG, JPG, JPEG, GIF, WebP, max 16MB)

**Success Response (200):**
```json
{
  "success": true,
  "message": "Background image uploaded and processed successfully",
  "filename": "20240115_103002_ghi12345.png",
  "url": "/uploads/background/20240115_103002_ghi12345.png",
  "local_path": "/app/uploads/background/20240115_103002_ghi12345.png",
  "size": 1024000,
  "upload_time": "2024-01-15T10:30:07.345678"
}
```

---

## 🖼️ Image Generation Endpoints

### 8. Generate Social Media Image
```bash
curl -X POST http://87.236.166.7:9009/generate \
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

**Required Parameters:**
- `headline` (string): Main headline text

**Optional Parameters:**
- `subheadline` (string): Secondary text
- `brand` (string): Brand/company name (ignored if watermark provided)
- `background_color` (array): RGB color array, default: [255, 255, 255]
- `main_image_url` (string): URL to main image
- `watermark_image_url` (string): URL to watermark/logo
- `background_image_url` (string): URL to background image
- `watermark_position` (string): Position for watermark - "bottom-right", "top-right", "bottom-center", "top-left", "bottom-left"

**Success Response (200):**
```json
{
  "success": true,
  "message": "Image generated successfully",
  "download_url": "/generated/generated_abc123def456.png",
  "filename": "generated_abc123def456.png",
  "size": 524288,
  "generated_at": "2024-01-15T10:30:10.123456",
  "config": {
    "headline": "Your Amazing Headline",
    "subheadline": "Supporting text goes here",
    "brand": "Your Brand Name",
    "background_color": [255, 255, 255],
    "watermark_position": "bottom-right",
    "main_image_used": true,
    "watermark_image_used": true,
    "background_image_used": false
  }
}
```

### 9. Generate Text-Based Layout
```bash
curl -X POST http://87.236.166.7:9009/generate_text \
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

**Required Parameters:**
- `layout_type` (string): Type of text layout
- `content` (object): Content data for the layout

**Optional Parameters:**
- `config` (string): Path to config file (default: "config/text_layouts_config.json")

**Supported Layout Types:**
- `quote` - Large quote with attribution
- `article` - Article excerpt with title and body
- `announcement` - Announcement with call-to-action
- `list` - List layout with bulleted items
- `testimonial` - Testimonial with quote and person info

**Success Response (200):**
```json
{
  "success": true,
  "message": "Text layout quote generated successfully",
  "layout_type": "quote",
  "filename": "text_quote_abc123def456.png",
  "download_url": "/generated/text_quote_abc123def456.png",
  "size": 314572,
  "generated_at": "2024-01-15T10:30:12.123456",
  "content_used": {
    "quote": "Success is not final, failure is not fatal.",
    "author": "Winston Churchill",
    "brand": "Inspiration Daily"
  }
}
```

### 10. Generate All Text Layouts
```bash
curl -X POST http://87.236.166.7:9009/generate_all_text \
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

**Required Parameters:**
- `content` (object): Content data for layouts

**Optional Parameters:**
- `output_prefix` (string): Prefix for output files (default: "text_post")
- `config` (string): Path to config file

**Success Response (200):**
```json
{
  "success": true,
  "message": "Generated 5 text layouts",
  "generated_files": [
    {
      "layout_type": "quote",
      "filename": "inspirational_quote_quote.png",
      "download_url": "/generated/inspirational_quote_quote.png",
      "size": 314572,
      "generated_at": "2024-01-15T10:30:15.123456"
    },
    {
      "layout_type": "article",
      "filename": "inspirational_quote_article.png",
      "download_url": "/generated/inspirational_quote_article.png",
      "size": 298765,
      "generated_at": "2024-01-15T10:30:16.234567"
    }
  ],
  "content_used": {
    "quote": "Success is not final, failure is not fatal.",
    "author": "Winston Churchill",
    "brand": "Inspiration Daily"
  },
  "output_prefix": "inspirational_quote"
}
```

---

## 🎨 Gradient Generation

### 11. Generate Gradient Image
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
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

**Required Parameters:**
- `colors` (array): Array of color values (minimum 2 colors)

**Optional Parameters:**
- `width` (integer): Image width in pixels (default: 1080, min: 100, max: 4096)
- `height` (integer): Image height in pixels (default: 1350, min: 100, max: 4096)
- `gradient_type` (string): "linear", "radial", "diagonal" (default: "linear")
- `direction` (string): "vertical", "horizontal", "diagonal" (default: "vertical")
- `use_hsl_interpolation` (boolean): Use HSL color space for smoother transitions (default: true)
- `add_noise` (boolean): Add subtle texture noise (default: true)
- `noise_intensity` (number): Noise strength (0-1, default: 0.02)
- `apply_dither` (boolean): Apply Floyd-Steinberg dithering (default: false)
- `generate_harmony` (boolean): Auto-generate color harmony (default: false)
- `harmony_type` (string): "complementary", "triadic", "analogous", "split_complementary" (default: "complementary")
- `quality` (integer): PNG quality (1-100, default: 95)

**Success Response (200):**
```json
{
  "success": true,
  "message": "Gradient generated successfully",
  "download_url": "/generated/gradient_abc123def456.png",
  "filename": "gradient_abc123def456.png",
  "size": 786432,
  "dimensions": {
    "width": 1080,
    "height": 1350
  },
  "gradient_config": {
    "type": "linear",
    "direction": "vertical",
    "colors": ["#FF6B6B", "#4ECDC4"],
    "rgb_colors": [[255, 107, 107], [78, 205, 196]]
  },
  "enhancements": {
    "hsl_interpolation": true,
    "noise_added": true,
    "noise_intensity": 0.02,
    "dither_applied": false,
    "harmony_generated": false,
    "quality": 95
  },
  "generated_at": "2024-01-15T10:30:20.123456"
}
```

### 12. Get Gradient Information
```bash
curl http://87.236.166.7:9009/gradient_info
```

**Response Example:**
```json
{
  "gradient_types": {
    "linear": {
      "description": "Linear gradient with smooth color transitions",
      "directions": ["vertical", "horizontal", "diagonal"],
      "examples": [
        {
          "direction": "vertical",
          "description": "Top to bottom gradient"
        }
      ]
    },
    "radial": {
      "description": "Radial gradient emanating from center",
      "directions": ["vertical"],
      "examples": [
        {
          "direction": "vertical",
          "description": "Circular gradient from center"
        }
      ]
    }
  },
  "color_formats": [
    "Hex colors: #FF6B6B, #4ECDC4, #45B7D1",
    "RGB arrays: [255, 107, 107], [78, 205, 196], [69, 183, 209]"
  ],
  "parameters": {
    "width": {
      "type": "integer",
      "min": 100,
      "max": 4096,
      "default": 1080
    },
    "height": {
      "type": "integer",
      "min": 100,
      "max": 4096,
      "default": 1350
    }
  }
}
```

---

## 📋 Information & Utility Endpoints

### 13. List All Files
```bash
curl http://87.236.166.7:9009/files
```

**Response Example:**
```json
{
  "main_images": [
    "20240115_103000_abc12345.png",
    "20240115_103005_def67890.png"
  ],
  "watermark_images": [
    "20240115_103001_ghi12345.png"
  ],
  "background_images": [
    "20240115_103002_jkl67890.png"
  ],
  "generated_images": [
    "generated_xyz789abc.png",
    "gradient_abc123def.png"
  ],
  "total_main": 2,
  "total_watermark": 1,
  "total_background": 1,
  "total_generated": 2
}
```

### 14. Get Text Layout Information
```bash
curl http://87.236.166.7:9009/text_layout_info
```

**Response Example:**
```json
{
  "text_layouts": {
    "quote": {
      "description": "Large quote with attribution",
      "required_fields": ["quote"],
      "optional_fields": ["author", "brand"],
      "example": {
        "quote": "Success is not final, failure is not fatal.",
        "author": "Winston Churchill",
        "brand": "Inspiration Daily"
      }
    },
    "article": {
      "description": "Article excerpt with title and body text",
      "required_fields": ["title", "body"],
      "optional_fields": ["brand"],
      "example": {
        "title": "The Future of Technology",
        "body": "Artificial intelligence is transforming every industry...",
        "brand": "Tech Insights"
      }
    },
    "announcement": {
      "description": "Announcement with title, description, and call-to-action",
      "required_fields": ["title", "description"],
      "optional_fields": ["cta", "brand"],
      "example": {
        "title": "New Product Launch",
        "description": "Revolutionary innovation for your workflow",
        "cta": "Learn More",
        "brand": "Innovation Co."
      }
    },
    "list": {
      "description": "List layout with title and bulleted items",
      "required_fields": ["title", "items"],
      "optional_fields": ["brand"],
      "example": {
        "title": "5 Tips for Better Design",
        "items": [
          "Keep it simple and clean",
          "Use consistent typography",
          "Test with real users"
        ],
        "brand": "Design Studio"
      }
    },
    "testimonial": {
      "description": "Testimonial with quote and person information",
      "required_fields": ["quote", "person_name"],
      "optional_fields": ["person_title", "brand"],
      "example": {
        "quote": "This product completely transformed our business operations.",
        "person_name": "Sarah Johnson",
        "person_title": "CEO, Tech Startup",
        "brand": "Product Reviews"
      }
    }
  },
  "features": [
    "Multi-line text wrapping with intelligent line breaks",
    "Justified text alignment for professional appearance",
    "Full Arabic/Farsi text support with proper RTL handling",
    "Customizable fonts and colors based on design system",
    "Responsive layouts that adapt to content length",
    "Professional typography with proper spacing"
  ]
}
```

---

## 📁 File Access Endpoints

### 15. Access Uploaded Files
```bash
# Main images
curl http://87.236.166.7:9009/uploads/main/filename.png

# Watermark images
curl http://87.236.166.7:9009/uploads/watermark/filename.png

# Background images
curl http://87.236.166.7:9009/uploads/background/filename.png
```

### 16. Access Generated Files
```bash
curl http://87.236.166.7:9009/generated/filename.png
```

---

## 🔄 Complete Workflow Examples

### Example 1: Full Image Generation Workflow
```bash
#!/bin/bash

# 1. Upload main image
MAIN_RESPONSE=$(curl -s -X POST -F "file=@product.png" http://87.236.166.7:9009/upload/main)
MAIN_URL=$(echo $MAIN_RESPONSE | jq -r '.url')
echo "Main image uploaded: $MAIN_URL"

# 2. Upload logo
LOGO_RESPONSE=$(curl -s -X POST -F "file=@logo.png" http://87.236.166.7:9009/upload/watermark)
LOGO_URL=$(echo $LOGO_RESPONSE | jq -r '.url')
echo "Logo uploaded: $LOGO_URL"

# 3. Generate final image
GENERATE_RESPONSE=$(curl -s -X POST http://87.236.166.7:9009/generate \
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
GRADIENT_RESPONSE=$(curl -s -X POST http://87.236.166.7:9009/generate_gradient \
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
TEXT_RESPONSE=$(curl -s -X POST http://87.236.166.7:9009/generate_all_text \
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

### Example 4: Advanced Gradient with Color Harmony
```bash
#!/bin/bash

# Generate gradient with automatic color harmony
HARMONY_RESPONSE=$(curl -s -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080,
    "colors": ["#FF6B6B"],
    "gradient_type": "radial",
    "direction": "vertical",
    "generate_harmony": true,
    "harmony_type": "triadic",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.025
  }')

DOWNLOAD_URL=$(echo $HARMONY_RESPONSE | jq -r '.download_url')
echo "Harmony gradient generated: $DOWNLOAD_URL"
```

---

## ⚙️ Configuration Examples

### Set Relative Paths (Default)
```bash
curl -X POST http://87.236.166.7:9009/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": false}'
```

**Response URLs will be:**
- `/uploads/main/filename.png`
- `/generated/filename.png`

### Set Full URLs
```bash
curl -X POST http://87.236.166.7:9009/config \
  -H "Content-Type: application/json" \
  -d '{"return_full_urls": true}'
```

**Response URLs will be:**
- `http://87.236.166.7:9009/uploads/main/filename.png`
- `http://87.236.166.7:9009/generated/filename.png`

---

## 🚨 Error Handling Examples

### Common Error Responses

#### Missing File Upload
```bash
curl -X POST http://87.236.166.7:9009/upload/main
```

**Response:**
```json
{
  "error": "No file provided"
}
```

#### Invalid JSON
```bash
curl -X POST http://87.236.166.7:9009/generate \
  -H "Content-Type: application/json" \
  -d 'invalid json'
```

**Response:**
```json
{
  "error": "No JSON data provided"
}
```

#### Missing Required Field
```bash
curl -X POST http://87.236.166.7:9009/generate \
  -H "Content-Type: application/json" \
  -d '{"subheadline": "Only subheadline"}'
```

**Response:**
```json
{
  "error": "Headline is required"
}
```

#### Invalid File Type
```bash
curl -X POST http://87.236.166.7:9009/upload/main \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "error": "File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP"
}
```

#### File Too Large
```bash
curl -X POST http://87.236.166.7:9009/upload/main \
  -F "file=@large_image.png"
```

**Response:**
```json
{
  "error": "File too large",
  "message": "File size exceeds 16MB limit",
  "max_size_mb": 16
}
```

---

## 📝 Important Notes

1. **File Formats Supported**: PNG, JPG, JPEG, GIF, WebP
2. **Max File Size**: 16MB per file
3. **Image Dimensions**: Configurable, default 1080x1350
4. **URL Configuration**: Can switch between relative paths and full URLs
5. **CORS Enabled**: All endpoints support cross-origin requests
6. **Error Handling**: Comprehensive error messages with HTTP status codes
7. **Color Formats**: Support both hex (#FF6B6B) and RGB array ([255, 107, 107]) formats
8. **Text Support**: Full English, Arabic, and Farsi (Persian) support with RTL handling

---

## 🐳 Docker Usage

If running in Docker, replace `localhost:5000` with your container's IP or mapped port:

```bash
# Check if running in Docker
curl http://your-docker-ip:5000/health

# Or if port mapped
curl http://87.236.166.7:9009/health
```

---

## 📊 HTTP Status Codes

- **200 OK**: Successful request
- **400 Bad Request**: Invalid parameters or missing required fields
- **404 Not Found**: File or endpoint not found
- **413 Payload Too Large**: File exceeds 16MB limit
- **415 Unsupported Media Type**: Invalid file format
- **500 Internal Server Error**: Server-side processing error

---

## 🔧 Advanced Parameters Reference

### Watermark Positions
- `bottom-right` (default)
- `top-right`
- `bottom-center`
- `top-left`
- `bottom-left`

### Gradient Types
- `linear` - Linear gradient with smooth transitions
- `radial` - Radial gradient emanating from center
- `diagonal` - Diagonal linear gradient

### Directions
- `vertical` - Top to bottom
- `horizontal` - Left to right
- `diagonal` - Corner to corner

### Harmony Types
- `complementary` - Opposite colors (180° apart)
- `triadic` - 3 colors, 120° apart
- `analogous` - Similar colors (adjacent on color wheel)
- `split_complementary` - Base + two adjacent to complement

### Text Layout Types
- `quote` - Large quote with attribution
- `article` - Article excerpt with title and body
- `announcement` - Announcement with call-to-action
- `list` - List layout with bulleted items
- `testimonial` - Testimonial with quote and person info

---

## 🎯 Quick Reference Table

| Method | Endpoint | Description | Key Parameters |
|--------|----------|-------------|----------------|
| GET | `/` | API documentation | - |
| GET | `/health` | Health check | - |
| GET/POST | `/config` | URL configuration | `return_full_urls` |
| POST | `/upload/main` | Upload main image | `file` |
| POST | `/upload/watermark` | Upload logo | `file` |
| POST | `/upload/background` | Upload background | `file` |
| POST | `/generate` | Generate social image | `headline`, `main_image_url`, etc. |
| POST | `/generate_text` | Generate text layout | `layout_type`, `content` |
| POST | `/generate_all_text` | Generate all text layouts | `content`, `output_prefix` |
| POST | `/generate_gradient` | Generate gradient | `colors`, `gradient_type`, etc. |
| GET | `/gradient_info` | Gradient documentation | - |
| GET | `/text_layout_info` | Text layout documentation | - |
| GET | `/files` | List files | - |
| GET | `/uploads/<folder>/<filename>` | Serve uploaded files | - |
| GET | `/generated/<filename>` | Serve generated files | - |

---

*Last updated: January 15, 2024*
*API Version: 2.0*
