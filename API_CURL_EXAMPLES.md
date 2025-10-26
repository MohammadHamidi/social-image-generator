# Social Image Generator API - Complete cURL Reference

Complete reference for all REST API endpoints with example requests and responses.

**Base URL**: `http://localhost:5000`
**Default Port**: 5000 (configurable via `PORT` environment variable)

---

## Table of Contents

1. [System & Configuration Endpoints](#system--configuration-endpoints)
2. [File Upload Endpoints](#file-upload-endpoints)
3. [Image Generation Endpoints](#image-generation-endpoints)
4. [Information & Documentation Endpoints](#information--documentation-endpoints)
5. [File Serving & Utility Endpoints](#file-serving--utility-endpoints)

---

## System & Configuration Endpoints

### 1. GET `/` - API Documentation

Get API documentation and available endpoints.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/
```

**Example Response (200 OK):**
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
    "health": "/health",
    "config": "/config",
    "upload_main": "/upload/main",
    "upload_watermark": "/upload/watermark",
    "upload_background": "/upload/background",
    "generate": "/generate",
    "generate_text": "/generate_text",
    "generate_all_text": "/generate_all_text",
    "generate_gradient": "/generate_gradient",
    "text_layout_info": "/text_layout_info",
    "gradient_info": "/gradient_info"
  },
  "example_usage": {
    "basic": "Upload images and generate social media posts",
    "text_layouts": "Create text-based social media graphics",
    "gradients": "Generate custom gradient backgrounds"
  }
}
```

---

### 2. GET `/health` - Health Check

Check API server health and system status.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/health
```

**Example Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-26T10:30:45.123456",
  "version": "2.0",
  "system": {
    "python_version": "3.11.5",
    "platform": "Linux",
    "upload_ready": true,
    "generation_ready": true,
    "upload_limit_mb": 16
  },
  "storage": {
    "free_space_gb": 45.3,
    "total_space_gb": 100.0,
    "used_space_gb": 54.7
  }
}
```

**Example Response (500 Internal Server Error):**
```json
{
  "status": "unhealthy",
  "timestamp": "2025-10-26T10:30:45.123456",
  "error": "Failed to initialize upload directories"
}
```

---

### 3. GET `/config` - Get Configuration

Get current API configuration settings.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/config
```

**Example Response (200 OK):**
```json
{
  "return_full_urls": false,
  "description": "When True, returns full URLs. When False, returns relative paths.",
  "example": {
    "full_urls": "http://localhost:5000/generated/filename.png",
    "relative_paths": "/generated/filename.png"
  }
}
```

---

### 4. POST `/config` - Update Configuration

Update API configuration settings.

**cURL Command:**
```bash
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{
    "return_full_urls": true
  }'
```

**Request Body:**
```json
{
  "return_full_urls": true
}
```

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Configuration updated: return_full_urls = True",
  "return_full_urls": true
}
```

**Example Response (400 Bad Request):**
```json
{
  "error": "Invalid request data. Expected JSON with 'return_full_urls' boolean field."
}
```

---

## File Upload Endpoints

### 5. POST `/upload/main` - Upload Main Image

Upload main product/service image for social media posts.

**cURL Command:**
```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@/path/to/your/image.png"
```

**Example with JPG:**
```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@product-photo.jpg"
```

**Request Parameters:**
- `file` (required): Image file (PNG, JPG, JPEG, GIF, WebP)
- Max size: 16MB

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "1730012345_a1b2c3d4.png",
  "url": "/uploads/main/1730012345_a1b2c3d4.png",
  "size": 245678,
  "upload_time": "2025-10-26T10:32:25.123456"
}
```

**Example Response (400 Bad Request - No File):**
```json
{
  "error": "No file part in the request"
}
```

**Example Response (400 Bad Request - Invalid Type):**
```json
{
  "error": "Invalid file type. Allowed types: png, jpg, jpeg, gif, webp"
}
```

**Example Response (500 Internal Server Error):**
```json
{
  "error": "Failed to save file: [error details]"
}
```

---

### 6. POST `/upload/watermark` - Upload Watermark/Logo

Upload brand logo or watermark image.

**cURL Command:**
```bash
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@/path/to/logo.png"
```

**Example:**
```bash
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@company-logo.png"
```

**Request Parameters:**
- `file` (required): Image file (PNG, JPG, JPEG, GIF, WebP)
- Max size: 16MB

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Watermark image uploaded successfully",
  "filename": "1730012350_e5f6g7h8.png",
  "url": "/uploads/watermark/1730012350_e5f6g7h8.png",
  "size": 45678,
  "upload_time": "2025-10-26T10:32:30.123456"
}
```

---

### 7. POST `/upload/background` - Upload Background Image

Upload custom background image for canvas.

**cURL Command:**
```bash
curl -X POST http://localhost:5000/upload/background \
  -F "file=@/path/to/background.jpg"
```

**Example:**
```bash
curl -X POST http://localhost:5000/upload/background \
  -F "file=@gradient-background.jpg"
```

**Request Parameters:**
- `file` (required): Image file (PNG, JPG, JPEG, GIF, WebP)
- Max size: 16MB

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Background image uploaded and processed successfully",
  "filename": "1730012355_i9j0k1l2.jpg",
  "url": "/uploads/background/1730012355_i9j0k1l2.jpg",
  "local_path": "./uploads/background/1730012355_i9j0k1l2.jpg",
  "size": 567890,
  "upload_time": "2025-10-26T10:32:35.123456"
}
```

---

## Image Generation Endpoints

### 8. POST `/generate` - Generate Social Media Image

Generate complete social media image with text, images, and AI processing.

**cURL Command (Basic):**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "New Product Launch",
    "subheadline": "Coming Soon in 2025",
    "brand": "My Brand"
  }'
```

**cURL Command (With All Options):**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Summer Sale",
    "subheadline": "Up to 50% Off",
    "brand": "Fashion Store",
    "background_color": [255, 107, 107],
    "main_image_url": "/uploads/main/1730012345_a1b2c3d4.png",
    "watermark_image_url": "/uploads/watermark/1730012350_e5f6g7h8.png",
    "background_image_url": "/uploads/background/1730012355_i9j0k1l2.jpg",
    "watermark_position": "bottom-right"
  }'
```

**Request Body:**
```json
{
  "headline": "New Product Launch",
  "subheadline": "Coming Soon in 2025",
  "brand": "My Brand",
  "background_color": [255, 255, 255],
  "main_image_url": "/uploads/main/1730012345_a1b2c3d4.png",
  "watermark_image_url": "/uploads/watermark/1730012350_e5f6g7h8.png",
  "background_image_url": "/uploads/background/1730012355_i9j0k1l2.jpg",
  "watermark_position": "bottom-right"
}
```

**Request Parameters:**
- `headline` (required): Main headline text
- `subheadline` (optional): Subheadline text
- `brand` (optional): Brand name
- `background_color` (optional): RGB array [R, G, B], default: [255, 255, 255]
- `main_image_url` (optional): URL/path to uploaded main image
- `watermark_image_url` (optional): URL/path to uploaded watermark
- `background_image_url` (optional): URL/path to uploaded background
- `watermark_position` (optional): "bottom-right", "top-right", "bottom-center", "top-left", "bottom-left"

**Canvas Configuration:**
- Size: 1080x1350px (Instagram story format)
- Main image size: 500x400px
- Watermark size: 200x120px

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Image generated successfully",
  "download_url": "/generated/1730012400_m3n4o5p6.png",
  "filename": "1730012400_m3n4o5p6.png",
  "size": 789012,
  "generated_at": "2025-10-26T10:33:20.123456",
  "config": {
    "headline": "Summer Sale",
    "subheadline": "Up to 50% Off",
    "brand": "Fashion Store",
    "background_color": [255, 107, 107],
    "watermark_position": "bottom-right",
    "main_image_used": true,
    "watermark_image_used": true,
    "background_image_used": true
  }
}
```

**Example Response (400 Bad Request):**
```json
{
  "error": "Missing required parameter: headline"
}
```

**Example Response (500 Internal Server Error):**
```json
{
  "error": "Failed to generate image: [error details]"
}
```

---

### 9. POST `/generate_text` - Generate Text-Based Layout

Generate images using pre-defined text layout templates.

**cURL Command (Quote Layout):**
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

**cURL Command (Article Layout):**
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "article",
    "content": {
      "title": "10 Tips for Better Productivity",
      "body": "Discover effective strategies to boost your daily productivity and achieve your goals faster.",
      "brand": "Productivity Hub"
    }
  }'
```

**cURL Command (Announcement Layout):**
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "announcement",
    "content": {
      "title": "Big News!",
      "description": "We are launching our new product next week. Stay tuned for amazing features!",
      "cta": "Learn More",
      "brand": "Tech Startup"
    }
  }'
```

**cURL Command (List Layout):**
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "list",
    "content": {
      "title": "Top 5 Features",
      "items": [
        "Fast Performance",
        "Easy to Use",
        "Secure & Reliable",
        "24/7 Support",
        "Affordable Pricing"
      ],
      "brand": "Our Product"
    }
  }'
```

**cURL Command (Testimonial Layout):**
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "testimonial",
    "content": {
      "quote": "This product changed my life! Highly recommended.",
      "person_name": "John Doe",
      "person_title": "CEO, Acme Corp",
      "brand": "Customer Reviews"
    }
  }'
```

**Layout Types & Required Fields:**

| Layout Type | Required Fields | Optional Fields |
|-------------|----------------|-----------------|
| `quote` | `quote` | `author`, `brand` |
| `article` | `title`, `body` | `brand` |
| `announcement` | `title`, `description` | `cta`, `brand` |
| `list` | `title`, `items` (array) | `brand` |
| `testimonial` | `quote`, `person_name` | `person_title`, `brand` |

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Text layout quote generated successfully",
  "layout_type": "quote",
  "filename": "1730012500_q7r8s9t0.png",
  "download_url": "/generated/1730012500_q7r8s9t0.png",
  "size": 456789,
  "generated_at": "2025-10-26T10:35:00.123456",
  "content_used": {
    "quote": "Success is not final, failure is not fatal.",
    "author": "Winston Churchill",
    "brand": "Inspiration Daily"
  }
}
```

**Example Response (400 Bad Request - Invalid Layout):**
```json
{
  "error": "Invalid layout_type. Must be one of: quote, article, announcement, list, testimonial"
}
```

**Example Response (400 Bad Request - Missing Fields):**
```json
{
  "error": "Missing required field for quote layout: quote"
}
```

---

### 10. POST `/generate_all_text` - Generate All Text Layouts

Generate all available text layout variations at once.

**cURL Command:**
```bash
curl -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "Innovation distinguishes between a leader and a follower.",
      "author": "Steve Jobs",
      "title": "Leadership Insights",
      "body": "Great leaders inspire action through innovation and vision.",
      "description": "Join us for an exclusive leadership workshop",
      "cta": "Register Now",
      "items": ["Vision", "Courage", "Integrity", "Innovation"],
      "person_name": "Jane Smith",
      "person_title": "Leadership Coach",
      "brand": "Leadership Academy"
    },
    "output_prefix": "leadership_post"
  }'
```

**Request Body:**
```json
{
  "content": {
    "quote": "string",
    "author": "string",
    "title": "string",
    "body": "string",
    "description": "string",
    "cta": "string",
    "items": ["string", "string"],
    "person_name": "string",
    "person_title": "string",
    "brand": "string"
  },
  "output_prefix": "text_post"
}
```

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Generated 5 text layouts",
  "generated_files": [
    {
      "layout_type": "quote",
      "filename": "leadership_post_quote_1730012600.png",
      "download_url": "/generated/leadership_post_quote_1730012600.png",
      "size": 345678,
      "generated_at": "2025-10-26T10:36:40.123456"
    },
    {
      "layout_type": "article",
      "filename": "leadership_post_article_1730012601.png",
      "download_url": "/generated/leadership_post_article_1730012601.png",
      "size": 456789,
      "generated_at": "2025-10-26T10:36:41.234567"
    },
    {
      "layout_type": "announcement",
      "filename": "leadership_post_announcement_1730012602.png",
      "download_url": "/generated/leadership_post_announcement_1730012602.png",
      "size": 567890,
      "generated_at": "2025-10-26T10:36:42.345678"
    },
    {
      "layout_type": "list",
      "filename": "leadership_post_list_1730012603.png",
      "download_url": "/generated/leadership_post_list_1730012603.png",
      "size": 234567,
      "generated_at": "2025-10-26T10:36:43.456789"
    },
    {
      "layout_type": "testimonial",
      "filename": "leadership_post_testimonial_1730012604.png",
      "download_url": "/generated/leadership_post_testimonial_1730012604.png",
      "size": 345678,
      "generated_at": "2025-10-26T10:36:44.567890"
    }
  ],
  "content_used": {
    "quote": "Innovation distinguishes between a leader and a follower.",
    "author": "Steve Jobs",
    "title": "Leadership Insights",
    "body": "Great leaders inspire action through innovation and vision.",
    "description": "Join us for an exclusive leadership workshop",
    "cta": "Register Now",
    "items": ["Vision", "Courage", "Integrity", "Innovation"],
    "person_name": "Jane Smith",
    "person_title": "Leadership Coach",
    "brand": "Leadership Academy"
  },
  "output_prefix": "leadership_post"
}
```

**Example Response (400 Bad Request):**
```json
{
  "error": "No valid content provided for any text layout"
}
```

---

### 11. POST `/generate_gradient` - Generate Gradient Background

Generate gradient image with comprehensive options.

**cURL Command (Simple Linear Gradient):**
```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "vertical"
  }'
```

**cURL Command (Complex Gradient with All Options):**
```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1920,
    "height": 1080,
    "colors": ["#667eea", "#764ba2", "#f093fb"],
    "gradient_type": "radial",
    "direction": "diagonal",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.03,
    "apply_dither": true,
    "generate_harmony": true,
    "harmony_type": "triadic",
    "quality": 95
  }'
```

**cURL Command (RGB Colors):**
```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "colors": [[255, 107, 107], [78, 205, 196], [255, 187, 51]],
    "gradient_type": "diagonal",
    "add_noise": true
  }'
```

**Request Parameters:**

| Parameter | Type | Required | Default | Range/Options | Description |
|-----------|------|----------|---------|---------------|-------------|
| `width` | number | No | 1080 | 100-4096 | Image width in pixels |
| `height` | number | No | 1350 | 100-4096 | Image height in pixels |
| `colors` | array | Yes | - | Hex or RGB array | At least 1 color required |
| `gradient_type` | string | No | "linear" | linear, radial, diagonal | Gradient type |
| `direction` | string | No | "vertical" | vertical, horizontal, diagonal | Gradient direction |
| `use_hsl_interpolation` | boolean | No | true | - | Smoother color transitions |
| `add_noise` | boolean | No | true | - | Add texture noise |
| `noise_intensity` | number | No | 0.02 | 0-1 | Noise strength |
| `apply_dither` | boolean | No | false | - | Apply dithering |
| `generate_harmony` | boolean | No | false | - | Generate color harmony |
| `harmony_type` | string | No | "complementary" | complementary, triadic, analogous, split_complementary | Harmony type |
| `quality` | number | No | 95 | 1-100 | JPEG quality |

**Color Formats:**
- Hex: `"#FF6B6B"`, `"#4ECDC4"`
- RGB Array: `[255, 107, 107]`, `[78, 205, 196]`

**Example Response (200 OK):**
```json
{
  "success": true,
  "message": "Gradient generated successfully",
  "download_url": "/generated/gradient_1730012700_u1v2w3x4.png",
  "filename": "gradient_1730012700_u1v2w3x4.png",
  "size": 234567,
  "dimensions": {
    "width": 1920,
    "height": 1080
  },
  "gradient_config": {
    "type": "radial",
    "direction": "diagonal",
    "colors": ["#667eea", "#764ba2", "#f093fb"],
    "rgb_colors": [[102, 126, 234], [118, 75, 162], [240, 147, 251]]
  },
  "enhancements": {
    "hsl_interpolation": true,
    "noise_added": true,
    "noise_intensity": 0.03,
    "dither_applied": true,
    "harmony_generated": true,
    "harmony_type": "triadic",
    "quality": 95
  },
  "generated_at": "2025-10-26T10:38:20.123456"
}
```

**Example Response (400 Bad Request - Missing Colors):**
```json
{
  "error": "Missing required parameter: colors"
}
```

**Example Response (400 Bad Request - Invalid Dimensions):**
```json
{
  "error": "Width must be between 100 and 4096 pixels"
}
```

**Example Response (400 Bad Request - Invalid Color):**
```json
{
  "error": "Invalid color format: #GGGGGG. Use hex (#FF6B6B) or RGB array [255, 107, 107]"
}
```

---

## Information & Documentation Endpoints

### 12. GET `/text_layout_info` - Text Layout Documentation

Get comprehensive information about available text layout types.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/text_layout_info
```

**Example Response (200 OK):**
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
      "description": "Article excerpt with title and body",
      "required_fields": ["title", "body"],
      "optional_fields": ["brand"],
      "example": {
        "title": "10 Tips for Better Productivity",
        "body": "Discover effective strategies to boost your daily productivity.",
        "brand": "Productivity Hub"
      }
    },
    "announcement": {
      "description": "Announcement with title and description",
      "required_fields": ["title", "description"],
      "optional_fields": ["cta", "brand"],
      "example": {
        "title": "Big News!",
        "description": "We are launching our new product next week.",
        "cta": "Learn More",
        "brand": "Tech Startup"
      }
    },
    "list": {
      "description": "List layout with bulleted items",
      "required_fields": ["title", "items"],
      "optional_fields": ["brand"],
      "example": {
        "title": "Top 5 Features",
        "items": ["Fast", "Easy", "Secure", "Supported", "Affordable"],
        "brand": "Our Product"
      }
    },
    "testimonial": {
      "description": "Testimonial with quote and person info",
      "required_fields": ["quote", "person_name"],
      "optional_fields": ["person_title", "brand"],
      "example": {
        "quote": "This product changed my life!",
        "person_name": "John Doe",
        "person_title": "CEO, Acme Corp",
        "brand": "Customer Reviews"
      }
    }
  },
  "features": [
    "AI-powered background removal",
    "Multi-line text wrapping",
    "Arabic/Farsi RTL support",
    "Custom fonts and styling",
    "Professional typography"
  ],
  "usage": {
    "generate_single": "Use POST /generate_text with layout_type and content",
    "generate_all": "Use POST /generate_all_text with content for all layouts",
    "content_validation": "Required fields are validated automatically"
  }
}
```

---

### 13. GET `/gradient_info` - Gradient Generation Documentation

Get comprehensive information about gradient generation options.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/gradient_info
```

**Example Response (200 OK):**
```json
{
  "gradient_types": {
    "linear": {
      "description": "Linear gradient transition",
      "directions": ["vertical", "horizontal", "diagonal"],
      "example": {
        "colors": ["#FF6B6B", "#4ECDC4"],
        "gradient_type": "linear",
        "direction": "vertical"
      }
    },
    "radial": {
      "description": "Radial gradient from center",
      "directions": ["vertical", "horizontal", "diagonal"],
      "example": {
        "colors": ["#667eea", "#764ba2"],
        "gradient_type": "radial"
      }
    },
    "diagonal": {
      "description": "Diagonal gradient transition",
      "directions": ["vertical", "horizontal", "diagonal"],
      "example": {
        "colors": ["#f093fb", "#f5576c"],
        "gradient_type": "diagonal"
      }
    }
  },
  "color_formats": [
    "Hex strings: #FF6B6B, #4ECDC4",
    "RGB arrays: [255, 107, 107], [78, 205, 196]"
  ],
  "parameters": {
    "width": "Image width (100-4096px, default: 1080)",
    "height": "Image height (100-4096px, default: 1350)",
    "colors": "Array of colors (at least 1 required)",
    "gradient_type": "Type: linear, radial, diagonal (default: linear)",
    "direction": "Direction: vertical, horizontal, diagonal (default: vertical)",
    "use_hsl_interpolation": "Smoother transitions (default: true)",
    "add_noise": "Add texture noise (default: true)",
    "noise_intensity": "Noise strength 0-1 (default: 0.02)",
    "apply_dither": "Apply dithering (default: false)",
    "generate_harmony": "Generate color harmony (default: false)",
    "harmony_type": "complementary, triadic, analogous, split_complementary",
    "quality": "JPEG quality 1-100 (default: 95)"
  },
  "examples": {
    "simple": {
      "colors": ["#FF6B6B", "#4ECDC4"],
      "gradient_type": "linear"
    },
    "advanced": {
      "width": 1920,
      "height": 1080,
      "colors": ["#667eea", "#764ba2", "#f093fb"],
      "gradient_type": "radial",
      "add_noise": true,
      "noise_intensity": 0.03,
      "quality": 95
    }
  },
  "usage": {
    "endpoint": "POST /generate_gradient",
    "content_type": "application/json",
    "min_colors": 1,
    "max_colors": "unlimited"
  }
}
```

---

## File Serving & Utility Endpoints

### 14. GET `/uploads/<folder>/<filename>` - Serve Uploaded Files

Serve uploaded image files.

**cURL Commands:**
```bash
# Download main image
curl -X GET http://localhost:5000/uploads/main/1730012345_a1b2c3d4.png \
  --output downloaded_main.png

# Download watermark
curl -X GET http://localhost:5000/uploads/watermark/1730012350_e5f6g7h8.png \
  --output downloaded_watermark.png

# Download background
curl -X GET http://localhost:5000/uploads/background/1730012355_i9j0k1l2.jpg \
  --output downloaded_background.jpg
```

**Valid Folder Values:**
- `main` - Main product/service images
- `watermark` - Logo/watermark images
- `background` - Background images

**Response:**
- Content-Type: image/png, image/jpeg, etc.
- Binary image data

**Example Response (404 Not Found):**
```json
{
  "error": "File not found: 1730012345_a1b2c3d4.png"
}
```

**Example Response (400 Bad Request):**
```json
{
  "error": "Invalid folder. Must be: main, watermark, or background"
}
```

**Example Response (403 Forbidden):**
```json
{
  "error": "File is not readable: 1730012345_a1b2c3d4.png"
}
```

---

### 15. GET `/generated/<filename>` - Serve Generated Files

Serve generated image files.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/generated/1730012400_m3n4o5p6.png \
  --output downloaded_generated.png
```

**Response:**
- Content-Type: image/png
- Binary image data

**Example Response (404 Not Found):**
```json
{
  "error": "File not found: 1730012400_m3n4o5p6.png"
}
```

---

### 16. GET `/files` - List Uploaded Files

List all uploaded and generated files for debugging purposes.

**cURL Command:**
```bash
curl -X GET http://localhost:5000/files
```

**Example Response (200 OK):**
```json
{
  "main_images": [
    "1730012345_a1b2c3d4.png",
    "1730012346_b2c3d4e5.jpg"
  ],
  "total_main": 2,
  "watermark_images": [
    "1730012350_e5f6g7h8.png"
  ],
  "total_watermark": 1,
  "background_images": [
    "1730012355_i9j0k1l2.jpg",
    "1730012356_j0k1l2m3.png"
  ],
  "total_background": 2,
  "generated_images": [
    "1730012400_m3n4o5p6.png",
    "1730012500_q7r8s9t0.png",
    "gradient_1730012700_u1v2w3x4.png"
  ],
  "total_generated": 3
}
```

---

## Complete Workflow Examples

### Example 1: Generate Social Media Post with Uploaded Images

**Step 1: Upload main image**
```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@product.jpg"
```

**Step 2: Upload watermark**
```bash
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@logo.png"
```

**Step 3: Generate social media image**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "New Product Launch",
    "subheadline": "Available Now",
    "brand": "My Brand",
    "main_image_url": "/uploads/main/1730012345_a1b2c3d4.jpg",
    "watermark_image_url": "/uploads/watermark/1730012350_e5f6g7h8.png",
    "background_color": [78, 205, 196]
  }'
```

**Step 4: Download generated image**
```bash
curl -X GET http://localhost:5000/generated/1730012400_m3n4o5p6.png \
  --output final_post.png
```

---

### Example 2: Generate Multiple Text Layouts

**Generate all text layouts at once:**
```bash
curl -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "Think different.",
      "author": "Apple",
      "title": "Innovation Guide",
      "body": "Learn how to innovate and disrupt markets.",
      "description": "Join our innovation workshop",
      "cta": "Register",
      "items": ["Create", "Innovate", "Disrupt", "Lead"],
      "person_name": "Tim Cook",
      "person_title": "CEO",
      "brand": "Tech Leaders"
    },
    "output_prefix": "innovation"
  }'
```

---

### Example 3: Create Custom Gradient Background

**Generate gradient background:**
```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#667eea", "#764ba2", "#f093fb"],
    "gradient_type": "radial",
    "add_noise": true,
    "noise_intensity": 0.025,
    "quality": 95
  }'
```

**Upload as background:**
```bash
# First download the gradient
curl -X GET http://localhost:5000/generated/gradient_1730012700_u1v2w3x4.png \
  --output custom_gradient.png

# Then upload as background
curl -X POST http://localhost:5000/upload/background \
  -F "file=@custom_gradient.png"
```

---

## Error Handling

### Standard HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters or missing fields |
| 403 | Forbidden | File not readable |
| 404 | Not Found | Endpoint or file not found |
| 413 | Payload Too Large | File exceeds 16MB limit |
| 500 | Internal Server Error | Server-side error |

### Error Response Format

All errors return JSON with the following structure:
```json
{
  "error": "Detailed error message",
  "timestamp": "2025-10-26T10:40:00.123456"
}
```

---

## Configuration Notes

### Environment Variables

```bash
# Server port (default: 5000)
PORT=5000

# Flask environment (production/development)
FLASK_ENV=production
```

### File Upload Limits

- **Max file size**: 16MB per file
- **Allowed formats**: PNG, JPG, JPEG, GIF, WebP
- **Upload directories**: `./uploads/main/`, `./uploads/watermark/`, `./uploads/background/`
- **Generated directory**: `./generated/`

### Canvas Configuration

- **Default size**: 1080x1350px (Instagram story format)
- **Main image size**: 500x400px
- **Watermark size**: 200x120px

### Language Support

- **English**: Full support
- **Arabic/Farsi**: RTL text handling with proper reshaping

---

## Testing Commands

### Quick Health Check
```bash
curl -X GET http://localhost:5000/health | jq
```

### Test File Upload
```bash
# Create a test image (requires ImageMagick)
convert -size 500x400 xc:blue test_image.png

# Upload it
curl -X POST http://localhost:5000/upload/main \
  -F "file=@test_image.png" | jq
```

### Test Simple Generation
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"headline": "Test Post", "brand": "Test Brand"}' | jq
```

### List All Files
```bash
curl -X GET http://localhost:5000/files | jq
```

---

## Additional Notes

- **CORS**: Enabled for all routes
- **Authentication**: None required (add in production)
- **Rate Limiting**: Not implemented (add in production)
- **URL Mode**: Configurable via `/config` endpoint to return full URLs or relative paths
- **AI Features**: Background removal powered by rembg library
- **Image Processing**: Pillow (PIL) for advanced image manipulation

---

**Last Updated**: 2025-10-26
**API Version**: 2.0
**Documentation**: Complete
