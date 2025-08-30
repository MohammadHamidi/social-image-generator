# Social Image Generator API

A powerful REST API for generating custom social media images with uploaded content, automatic background removal, and advanced styling options.

## 🚀 Features

- **Image Upload Endpoints** - Upload main images and watermarks
- **Automatic Background Removal** - AI-powered using rembg
- **Arabic Text Support** - Proper RTL rendering and Arabic fonts
- **Flexible Configuration** - Customize colors, layouts, and positioning
- **RESTful API** - Clean endpoints with JSON responses
- **File Management** - Automatic cleanup and unique filenames

## 📋 API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "2.0"
}
```

### 2. Upload Main Image
```http
POST /upload/main
Content-Type: multipart/form-data
```

**Request:**
```bash
curl -X POST -F "file=@main.png" http://localhost:5000/upload/main
```

**Response:**
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "20240101_120000_abc123.png",
  "url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png",
  "size": 2048576,
  "upload_time": "2024-01-01T12:00:00"
}
```

### 3. Upload Watermark Image
```http
POST /upload/watermark
Content-Type: multipart/form-data
```

**Request:**
```bash
curl -X POST -F "file=@watermark.png" http://localhost:5000/upload/watermark
```

### 4. Generate Social Media Image
```http
POST /generate
Content-Type: application/json
```

**Request:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "کت‌های زمستانی جدید",
    "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png",
    "watermark_image_url": "http://localhost:5000/uploads/watermark/20240101_120001_def456.png"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Image generated successfully",
  "download_url": "http://localhost:5000/generated/generated_abc123def.png",
  "filename": "generated_abc123def.png",
  "size": 2048576,
  "generated_at": "2024-01-01T12:00:00",
  "config": {
    "headline": "کت‌های زمستانی جدید",
    "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_used": true,
    "watermark_image_used": true
  }
}
```

### 5. Download Generated Image
```http
GET /generated/{filename}
```

**Example:**
```bash
curl http://localhost:5000/generated/generated_abc123def.png --output my_image.png
```

## 🛠️ Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Server
```bash
python run_server.py
```

### 3. Test API (Optional)
```bash
python api_client_example.py --demo
```

## 📝 Configuration Parameters

### Required Parameters
- `headline` (string) - Main headline text
- `subheadline` (string) - Subtitle text
- `brand` (string) - Brand/company name

### Optional Parameters
- `background_color` (array) - RGB color `[255, 255, 255]` (default: white)
- `main_image_url` (string) - URL of uploaded main image
- `watermark_image_url` (string) - URL of uploaded watermark image

## 🎨 Supported Image Formats

- PNG (recommended for transparency)
- JPEG/JPG
- GIF
- WebP

## 📏 Image Specifications

### Main Image
- **Max Size**: 16MB
- **Recommended**: 1024×1024 pixels (square)
- **Background**: Auto-removed using AI

### Watermark Image
- **Max Size**: 16MB
- **Recommended**: 178×108 pixels
- **Background**: Auto-removed using AI

## 🔄 Complete Workflow Example

### 1. Upload Main Image
```bash
curl -X POST -F "file=@my_main_image.png" http://localhost:5000/upload/main
# Returns: {"url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png"}
```

### 2. Upload Watermark Image
```bash
curl -X POST -F "file=@my_watermark.png" http://localhost:5000/upload/watermark
# Returns: {"url": "http://localhost:5000/uploads/watermark/20240101_120001_def456.png"}
```

### 3. Generate Image
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "کت‌های زمستانی جدید",
    "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png",
    "watermark_image_url": "http://localhost:5000/uploads/watermark/20240101_120001_def456.png"
  }'
```

### 4. Download Result
```bash
curl http://localhost:5000/generated/generated_xyz789.png --output final_social_image.png
```

## 🐛 Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "No file provided"
}
```

**404 Not Found:**
```json
{
  "error": "File not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Generation failed: [error message]"
}
```

## 🔒 Security Features

- File type validation
- Secure filename generation
- File size limits (16MB max)
- Unique filename generation
- CORS enabled for web applications

## 📊 Performance

- **Upload Speed**: Depends on file size and network
- **Generation Time**: 5-15 seconds (includes background removal)
- **Concurrent Requests**: Single-threaded (can be improved with Gunicorn)

## 🚀 Production Deployment

For production use, consider:

1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Reverse Proxy**: Nginx for static file serving
3. **Database**: For tracking uploads and generations
4. **Caching**: Redis for frequently used images
5. **Monitoring**: Add logging and metrics

## 📞 Support

If you encounter issues:

1. Check server logs in terminal
2. Verify image formats and sizes
3. Ensure server is running on port 5000
4. Check file permissions for upload directories

## 🎯 Example Use Cases

### E-commerce Product Images
- Upload product photos as main images
- Add brand logos as watermarks
- Generate consistent social media posts

### Blog/Article Thumbnails
- Upload article images
- Add publication branding
- Generate eye-catching thumbnails

### Event Promotion
- Upload event graphics
- Add sponsor logos
- Create promotional materials

---

**Ready to create stunning social media images? Start the server and upload your first image!** 🚀
