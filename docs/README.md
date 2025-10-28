# API Documentation

This directory contains comprehensive API documentation for the Social Image Generator.

## Files

- **openapi.yaml** - OpenAPI 3.0 specification with all endpoints, schemas, and examples

## Using the OpenAPI Documentation

### Method 1: Swagger UI (Recommended)

**Online Swagger Editor:**
1. Go to [swagger.io/tools/swagger-editor](https://editor.swagger.io/)
2. Click **File** → **Import file**
3. Upload `openapi.yaml`
4. Explore the API interactively

**Local Swagger UI with Docker:**
```bash
# From project root
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/docs/openapi.yaml \
  -v $(pwd)/docs:/docs \
  swaggerapi/swagger-ui

# Open browser to http://localhost:8080
```

### Method 2: Redoc

**View with Redoc:**
```bash
# Install redoc-cli
npm install -g redoc-cli

# Generate HTML documentation
redoc-cli bundle docs/openapi.yaml -o docs/api-documentation.html

# Open docs/api-documentation.html in browser
```

### Method 3: VSCode Extension

1. Install "OpenAPI (Swagger) Editor" extension
2. Open `openapi.yaml` in VSCode
3. Click "Preview" icon in top-right corner

## API Quick Reference

### Base URL
- Development: `http://localhost:5000`
- Production: Set via environment variables

### Main Endpoints

#### Upload Endpoints
- `POST /upload/main` - Upload main/hero images
- `POST /upload/watermark` - Upload logos/watermarks
- `POST /upload/background` - Upload background images

#### Generation Endpoints
- `POST /generate_post` - **Universal endpoint** for all layout types
- `POST /generate_gradient` - Generate gradient backgrounds
- `POST /generate` - Legacy endpoint for social images
- `POST /generate_text` - Generate text-based layouts

#### Information Endpoints
- `GET /` - API documentation
- `GET /health` - System health check
- `GET /layouts` - List available layouts
- `GET /gradient_info` - Gradient generation docs
- `GET /text_layout_info` - Text layout docs

#### Utility Endpoints
- `GET /files` - List uploaded files
- `GET /uploads/{folder}/{filename}` - Serve uploaded files
- `GET /generated/{filename}` - Serve generated files

## Example Requests

### Generate Yuan Payment Post

```bash
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "headline_promo",
    "content": {
      "headline": "راهنمای کامل",
      "subheadline": "واردات و پرداخت به چین",
      "cta": "برای اطلاعات بیشتر بکشید ←"
    },
    "assets": {
      "logo_url": "uploads/watermark/yuan-payment-logo.png"
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
      "logo_size": 120,
      "cta_bg_color": [255, 215, 0],
      "cta_text_color": [200, 16, 46]
    }
  }'
```

### Generate Gradient Background

```bash
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#C8102E", "#FFD700"],
    "gradient_type": "diagonal",
    "use_hsl_interpolation": true,
    "add_noise": true
  }'
```

### Upload Image

```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@/path/to/image.png"
```

### Health Check

```bash
curl http://localhost:5000/health
```

## Response Formats

All endpoints return JSON responses.

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "download_url": "/generated/filename.png",
  "generated_at": "2025-10-28T12:00:00"
}
```

**Error Response:**
```json
{
  "error": "Error type",
  "message": "Detailed error description",
  "timestamp": "2025-10-28T12:00:00"
}
```

## Layout Types

### Available Layouts

1. **headline_promo** - Big headline with optional CTA button
2. **split_image_text** - Text on one side, image on other
3. **overlay_text** - Text overlaid on background image
4. **caption_box** - Image with caption overlay
5. **product_showcase** - Centered product display
6. **checklist** - List with checkmarks
7. **testimonial** - Testimonial with attribution

### Layout-Specific Fields

Each layout type has specific required and optional fields. Use:
- `GET /layouts` - Get schemas for all layouts
- `GET /text_layout_info` - Get text layout documentation

## Background Removal

The API supports AI-powered background removal:

```json
{
  "options": {
    "remove_hero_background": true,
    "bg_removal_method": "auto",
    "bg_removal_alpha_matting": false
  }
}
```

**Methods:**
- `auto` - AI-powered with rembg (best quality)
- `edge` - Enhanced edge detection
- `color` - Color threshold-based

## Color Formats

Colors can be specified in two formats:

**RGB Arrays:**
```json
{
  "color": [200, 16, 46]
}
```

**Hex Strings (gradients only):**
```json
{
  "colors": ["#C8102E", "#FFD700"]
}
```

## Testing the API

### Using curl

```bash
# Test health endpoint
curl http://localhost:5000/health

# List available layouts
curl http://localhost:5000/layouts

# Generate a simple gradient
curl -X POST http://localhost:5000/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{"colors": ["#FF6B6B", "#4ECDC4"]}'
```

### Using Python

```python
import requests

# Generate post
response = requests.post('http://localhost:5000/generate_post', json={
    'layout_type': 'headline_promo',
    'content': {
        'headline': 'Test',
        'subheadline': 'Subheadline'
    },
    'background': {
        'mode': 'gradient',
        'gradient': {
            'colors': [[255, 107, 107], [78, 205, 196]],
            'direction': 'vertical'
        }
    }
})

result = response.json()
print(f"Download URL: {result['generated_files'][0]['download_url']}")
```

### Using Postman

1. Import `openapi.yaml` into Postman
2. Postman will auto-create a collection with all endpoints
3. Use the built-in examples to test each endpoint

## Rate Limiting

Currently no rate limiting is implemented. Add your own middleware if needed.

## Authentication

Currently no authentication is required. To add authentication:

1. Implement JWT or API key authentication
2. Update OpenAPI spec with `securitySchemes`
3. Add authentication middleware to Flask app

## Error Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `403` - Forbidden (file not readable)
- `404` - Not Found (file/endpoint not found)
- `413` - Request Entity Too Large (file too big)
- `500` - Internal Server Error

## Support

For issues or questions:
- Check the OpenAPI spec for detailed schemas
- Review example requests in this README
- Consult the main project README
- Open an issue on GitHub

## Version History

- **v2.0** - Added universal `POST /generate_post` endpoint
- **v2.0** - Background removal support
- **v2.0** - Enhanced error handling
- **v1.0** - Initial API release

## License

MIT License - See project root LICENSE file
