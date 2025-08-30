# Enhanced Social Media Image Generator API Reference

## 📡 Base URLs

### Local Development
- **Base URL**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`
- **API Documentation**: `http://localhost:5000`

### Docker Container
- **Base URL**: `http://localhost:5000` (when running with Docker)
- **Container Health**: Access via Docker container IP

### Production Deployment
- Configure your web server to proxy requests to the Flask application
- Set appropriate environment variables for production use

## 🚀 Quick Start

### 1. Start the API Server

#### Local Development
```bash
# Using Python directly
python social_image_api.py

# Or using the launcher script
python run_server.py
```

#### Docker
```bash
# Start with Docker Compose
docker-compose up --build

# Or run directly
docker run -p 5000:5000 -v $(pwd)/output:/app/output social-image-generator
```

### 2. Health Check
```bash
curl http://localhost:5000/health
```

### 3. View API Documentation
```bash
curl http://localhost:5000
```

## 📋 API Endpoints

### 1. GET `/` - API Documentation
Get comprehensive API documentation and usage examples.

**Response:**
```json
{
  "name": "Social Image Generator API",
  "version": "2.0",
  "description": "Generate custom social media images with uploaded content",
  "endpoints": {
    "POST /upload/main": "Upload main image",
    "POST /upload/watermark": "Upload watermark image",
    "POST /upload/background": "Upload background image",
    "POST /generate": "Generate social media image",
    "GET /health": "Health check"
  },
  "example_usage": {
    "upload_main": "curl -X POST -F \"file=@main.png\" http://localhost:5000/upload/main",
    "upload_watermark": "curl -X POST -F \"file=@watermark.png\" http://localhost:5000/upload/watermark",
    "generate": "curl -X POST http://localhost:5000/generate -H \"Content-Type: application/json\" -d '{\"headline\": \"Premium Collection\", \"subheadline\": \"Exceptional Quality\", \"brand\": \"Fashion Store\"}'"
  }
}
```

### 2. GET `/health` - Health Check
Check if the API server is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "version": "2.0"
}
```

---

## 📤 Upload Endpoints

### 3. POST `/upload/main` - Upload Main Image
Upload the main product/service image for social media posts.

**Request:**
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with file

```bash
curl -X POST \
  -F "file=@path/to/your/main-image.png" \
  http://localhost:5000/upload/main
```

**Parameters:**
- `file`: Image file (PNG, JPG, JPEG, GIF, WebP) - Max 16MB

**Success Response (200):**
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "20240115_103000_abc12345.png",
  "url": "http://localhost:5000/uploads/main/20240115_103000_abc12345.png",
  "size": 245760,
  "upload_time": "2024-01-15T10:30:00.123456"
}
```

**Error Responses:**
- `400`: No file provided or invalid file type
- `500`: Upload failed

### 4. POST `/upload/watermark` - Upload Watermark/Brand Logo
Upload brand logo or watermark image.

**Request:**
```bash
curl -X POST \
  -F "file=@path/to/your/logo.png" \
  http://localhost:5000/upload/watermark
```

**Parameters:**
- `file`: Image file (PNG, JPG, JPEG, GIF, WebP) - Max 16MB

**Success Response (200):**
```json
{
  "success": true,
  "message": "Watermark image uploaded successfully",
  "filename": "20240115_103001_def67890.png",
  "url": "http://localhost:5000/uploads/watermark/20240115_103001_def67890.png",
  "size": 51200,
  "upload_time": "2024-01-15T10:30:01.234567"
}
```

### 5. POST `/upload/background` - Upload Background Image
Upload custom background image for the canvas.

**Request:**
```bash
curl -X POST \
  -F "file=@path/to/your/background.jpg" \
  http://localhost:5000/upload/background
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Background image uploaded and processed successfully",
  "filename": "20240115_103002_ghi12345.png",
  "url": "http://localhost:5000/uploads/background/20240115_103002_ghi12345.png",
  "local_path": "/app/uploads/background/20240115_103002_ghi12345.png",
  "size": 1024000,
  "upload_time": "2024-01-15T10:30:02.345678"
}
```

---

## 🎨 Generation Endpoints

### 6. POST `/generate` - Generate Social Media Image
Generate a complete social media image with text, uploaded images, and AI processing.

**Request:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Premium Collection",
    "subheadline": "Exceptional Quality & Design",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_url": "http://localhost:5000/uploads/main/20240115_103000_abc12345.png",
    "watermark_image_url": "http://localhost:5000/uploads/watermark/20240115_103001_def67890.png",
    "watermark_position": "bottom-right"
  }'
```

**Parameters:**
- `headline` (string, required): Main headline text
- `subheadline` (string, optional): Secondary text
- `brand` (string, optional): Brand/company name (ignored if watermark provided)
- `background_color` (array, optional): RGB color array, default: [255, 255, 255]
- `main_image_url` (string, optional): URL to main image
- `watermark_image_url` (string, optional): URL to watermark/logo
- `background_image_url` (string, optional): URL to background image
- `watermark_position` (string, optional): Position for watermark - "bottom-right", "top-right", "bottom-center", "top-left", "bottom-left"

**Success Response (200):**
```json
{
  "success": true,
  "message": "Image generated successfully",
  "download_url": "http://localhost:5000/generated/generated_abc123def456.png",
  "filename": "generated_abc123def456.png",
  "size": 524288,
  "generated_at": "2024-01-15T10:30:05.123456",
  "config": {
    "headline": "Premium Collection",
    "subheadline": "Exceptional Quality & Design",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_used": true,
    "watermark_image_used": true
  }
}
```

**Error Responses:**
- `400`: Missing required parameters or invalid data
- `500`: Generation failed

### 7. POST `/generate_text` - Generate Text-Based Layout
Generate images using pre-defined text layout templates.

**Request:**
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

**Parameters:**
- `layout_type` (string, required): Type of text layout
- `content` (object, required): Content data for the layout
- `config` (string, optional): Path to config file

**Supported Layout Types:**
- `quote`: Large quote with attribution
- `article`: Article excerpt with title and body
- `announcement`: Announcement with call-to-action
- `list`: List layout with bulleted items
- `testimonial`: Testimonial with quote and person info

### 8. POST `/generate_all_text` - Generate All Text Layouts
Generate all available text layout variations at once.

**Request:**
```bash
curl -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "Success is not final, failure is not fatal.",
      "author": "Winston Churchill",
      "brand": "Inspiration Daily"
    },
    "output_prefix": "inspiration_quote"
  }'
```

---

## 📋 Information Endpoints

### 9. GET `/text_layout_info` - Text Layout Documentation
Get detailed information about available text layout types.

**Response:**
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
    }
    // ... more layout types
  },
  "features": [
    "Multi-line text wrapping",
    "Justified text alignment",
    "Arabic/Farsi text support",
    "Customizable fonts and colors",
    "Responsive layouts"
  ]
}
```

### 10. GET `/files` - List Uploaded Files
List all uploaded files (for debugging purposes).

**Response:**
```json
{
  "main_images": ["20240115_103000_abc12345.png"],
  "watermark_images": ["20240115_103001_def67890.png"],
  "generated_images": ["generated_xyz789.png"],
  "total_main": 1,
  "total_watermark": 1,
  "total_generated": 1
}
```

---

## 📁 File Serving Endpoints

### 11. GET `/uploads/{folder}/{filename}` - Serve Uploaded Files
Serve uploaded image files.

**Parameters:**
- `folder`: "main", "watermark", or "background"
- `filename`: Name of the uploaded file

**Example:**
```
GET http://localhost:5000/uploads/main/20240115_103000_abc12345.png
```

### 12. GET `/generated/{filename}` - Serve Generated Files
Serve generated image files.

**Example:**
```
GET http://localhost:5000/generated/generated_abc123def456.png
```

---

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Set to `/app/src` for proper imports
- `PYTHONDONTWRITEBYTECODE`: Disable Python bytecode generation

### Upload Limits
- **Max File Size**: 16MB per file
- **Allowed Formats**: PNG, JPG, JPEG, GIF, WebP
- **Upload Directories**:
  - `/app/uploads/main/` - Main images
  - `/app/uploads/watermark/` - Brand logos/watermarks
  - `/app/uploads/background/` - Background images

### CORS Support
All endpoints support Cross-Origin Resource Sharing (CORS) for web applications.

---

## 📖 Usage Examples

### Complete Workflow Example

```bash
#!/bin/bash

# 1. Upload main image
MAIN_RESPONSE=$(curl -s -X POST -F "file=@product.png" http://localhost:5000/upload/main)
MAIN_URL=$(echo $MAIN_RESPONSE | jq -r '.url')

# 2. Upload logo
LOGO_RESPONSE=$(curl -s -X POST -F "file=@logo.png" http://localhost:5000/upload/watermark)
LOGO_URL=$(echo $LOGO_RESPONSE | jq -r '.url')

# 3. Generate image
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

### JavaScript/Node.js Example

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Upload main image
async function uploadMainImage() {
  const form = new FormData();
  form.append('file', fs.createReadStream('product.png'));

  const response = await axios.post('http://localhost:5000/upload/main', form, {
    headers: form.getHeaders()
  });

  return response.data.url;
}

// Generate image
async function generateImage() {
  const mainImageUrl = await uploadMainImage();

  const response = await axios.post('http://localhost:5000/generate', {
    headline: "Premium Collection",
    subheadline: "Exceptional Quality & Design",
    brand: "Fashion Store",
    main_image_url: mainImageUrl,
    watermark_position: "bottom-right"
  });

  console.log('Download URL:', response.data.download_url);
}

generateImage();
```

### Python Example

```python
import requests

# Upload main image
with open('product.png', 'rb') as f:
    response = requests.post('http://localhost:5000/upload/main',
                           files={'file': f})
    main_url = response.json()['url']

# Generate image
response = requests.post('http://localhost:5000/generate', json={
    'headline': 'Premium Collection',
    'subheadline': 'Exceptional Quality & Design',
    'brand': 'Fashion Store',
    'main_image_url': main_url,
    'watermark_position': 'bottom-right'
})

download_url = response.json()['download_url']
print(f'Download your image: {download_url}')
```

---

## 🚨 Error Handling

### Common Error Codes

- **400 Bad Request**: Invalid parameters or missing required fields
- **404 Not Found**: File or endpoint not found
- **413 Payload Too Large**: File exceeds 16MB limit
- **415 Unsupported Media Type**: Invalid file format
- **500 Internal Server Error**: Server-side processing error

### Error Response Format

```json
{
  "error": "Detailed error message",
  "timestamp": "2024-01-15T10:30:00.123456",
  "endpoint": "/generate"
}
```

---

## 🔒 Security Considerations

### File Upload Security
- Files are validated by extension and MIME type
- Unique filenames prevent conflicts
- File size limits prevent abuse
- Files are served from protected directories

### API Security
- CORS enabled for web applications
- Input validation on all endpoints
- Error messages don't expose sensitive information
- Rate limiting should be implemented in production

---

## 📊 Performance

### Processing Times
- **Simple text generation**: < 2 seconds
- **Image with background removal**: 5-15 seconds
- **Complex layouts with multiple images**: 10-30 seconds

### Optimization Tips
- Use appropriate image sizes (recommended: 1000x1000px for main images)
- Compress images before upload
- Reuse uploaded images via URLs
- Use background removal only when needed

---

## 🐳 Docker Deployment

### Production Docker Setup

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/uploads
      - ./output:/app/output
```

### Environment Variables for Production

```bash
export FLASK_ENV=production
export PYTHONPATH=/app/src
export MAX_CONTENT_LENGTH=16777216  # 16MB
```

---

## 📞 Support

For API support and questions:
- Check the health endpoint: `GET /health`
- View API documentation: `GET /`
- Review example requests in this documentation
- Check server logs for detailed error information

---

## 🔄 API Version History

### Version 2.0 (Current)
- ✅ AI-powered background removal with rembg
- ✅ Multi-language text support (English, Arabic, Farsi)
- ✅ Dynamic layout positioning
- ✅ Brand logo integration with aspect ratio preservation
- ✅ RESTful API design
- ✅ Docker containerization
- ✅ Comprehensive error handling

### Version 1.0
- ✅ Basic image generation
- ✅ File upload support
- ✅ Simple text overlay
- ✅ Platform-specific configurations
