# Enhanced Social Media Image Generator

A professional-grade Python library for generating high-quality social media images with AI-powered background removal, dynamic layout positioning, and multi-language text support.

## 🚀 Features

- **🤖 AI-Powered Background Removal**: Uses rembg with ONNX Runtime for professional background removal
- **🎨 Dynamic Layout System**: Automatically adapts to content size and available space
- **🌍 Multi-Language Support**: Full support for English, Arabic, and Farsi text with proper reshaping
- **📐 Professional Typography**: Custom fonts with background panels and text shadows
- **🔄 Aspect Ratio Preservation**: Maintains original image proportions
- **🎯 Collision Avoidance**: Smart positioning to prevent element overlap
- **📱 Platform Optimization**: Pre-configured settings for Instagram, Facebook, Twitter, etc.
- **🐳 Docker Ready**: Complete containerization for easy deployment

## 📦 Installation

### Option 1: Docker (Recommended)

#### Windows Deployment
```bash
# Clone the repository
git clone <repository-url>
cd social-image-generator

# Build and run with Docker
docker-compose up --build -d

# Or use the enhanced test script
.\test_docker.ps1
```

#### Linux Deployment
```bash
# Clone the repository
git clone <repository-url>
cd social-image-generator

# Use Linux-specific build script
./build-linux.sh

# Or use Docker Compose with Linux config
docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d

# Traditional Docker Compose (if Linux config not needed)
docker-compose up --build -d
```

#### Environment Configuration
Create a `.env` file for custom configuration:
```bash
cp env.example .env
# Edit .env with your preferred settings
```

Available environment variables:
- `PORT`: API port (default: 5000)
- `DEV_PORT`: Development port (default: 8000)
- `FLASK_ENV`: Flask environment (default: production)

### Option 2: Local Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install rembg for AI background removal
pip install rembg

# Optional: Install ONNX Runtime for better performance
pip install onnxruntime
```

## 🛠️ API Reference

### EnhancedSocialImageGenerator

The main class for generating social media images.

#### Constructor

```python
EnhancedSocialImageGenerator(config_path: str = None)
```

**Parameters:**
- `config_path` (str, optional): Path to JSON configuration file. Uses default if None.

**Example:**
```python
# Using default configuration
generator = EnhancedSocialImageGenerator()

# Using platform-specific configuration
generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
```

#### generate_improved_hero_layout()

Generate a professional hero layout with dynamic positioning.

```python
generate_improved_hero_layout(headline: str, subheadline: str, brand: str = None) -> PIL.Image.Image
```

**Parameters:**
- `headline` (str): Main headline text. Supports English, Arabic, and Farsi.
- `subheadline` (str): Secondary text below headline. Supports all languages.
- `brand` (str, optional): Brand/company name. Ignored if brand logo is configured.

**Returns:**
- `PIL.Image.Image`: Generated image with RGBA mode for transparency.

**Example:**
```python
generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')

img = generator.generate_improved_hero_layout(
    headline="Premium Collection",
    subheadline="Exceptional Quality & Design",
    brand="Fashion Store"
)

img.save('output/social_post.png', 'PNG')
```

## 📁 Project Structure

```
social-image-generator/
├── src/
│   └── enhanced_social_generator.py    # Main generator class
├── config/
│   ├── platforms/                      # Platform-specific configs
│   │   ├── instagram_post.json
│   │   ├── facebook_post.json
│   │   ├── story.json
│   │   └── ...
│   └── fixed_user_images.json          # Default user configuration
├── uploads/                            # User-uploaded images
│   ├── main/                          # Main product images
│   ├── background/                    # Background images
│   └── watermark/                     # Brand logos/watermarks
├── output/                            # Generated images
├── assets/                            # Fonts and default assets
├── tests/                             # Test files
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker Compose setup
└── requirements.txt                   # Python dependencies
```

## ⚙️ Configuration

### Platform Configurations

Pre-configured settings for different social media platforms:

```json
{
  "canvas_width": 1080,
  "canvas_height": 1080,
  "custom_images": {
    "use_custom_images": true,
    "main_image_path": "uploads/main/main.png",
    "blueprint_image_path": "uploads/watermark/watermark.png",
    "background_image_path": "uploads/background/bg.png",
    "preserve_aspect_ratio": true,
    "remove_background": true
  }
}
```

### Image Requirements

- **Main Image**: Product/service image (recommended: 1000x1000px or larger)
- **Brand Logo**: Company logo/icon (recommended: 200x200px, maintains aspect ratio)
- **Background**: Canvas background image (matches platform dimensions)

## 🎨 Usage Examples

### Basic Usage

```python
from enhanced_social_generator import EnhancedSocialImageGenerator

# Initialize generator
generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')

# Generate image
img = generator.generate_improved_hero_layout(
    headline="New Collection Launch",
    subheadline="Discover our latest premium designs",
    brand="Your Brand Name"
)

# Save result
img.save('output/instagram_post.png', 'PNG')
```

### Multi-Language Support

```python
# English
img_en = generator.generate_improved_hero_layout(
    "Premium Collection",
    "Exceptional Quality & Design",
    "Fashion Store"
)

# Arabic (automatically reshaped)
img_ar = generator.generate_improved_hero_layout(
    "المجموعة المتميزة",
    "جودة وتصميم استثنائي",
    "متجر الأزياء"
)

# Mixed content
img_mixed = generator.generate_improved_hero_layout(
    "Premium Collection مجموعة مميزة",
    "Exceptional Quality جودة استثنائية",
    "Fashion Store متجر الأزياء"
)
```

### Custom Configuration

```python
# Custom canvas size
custom_config = {
    "canvas_width": 1200,
    "canvas_height": 630,  # Facebook link dimensions
    "custom_images": {
        "use_custom_images": true,
        "main_image_path": "uploads/main/product.jpg",
        "blueprint_image_path": "uploads/watermark/logo.png",
        "preserve_aspect_ratio": true,
        "remove_background": true
    }
}

# Save custom config
with open('config/custom.json', 'w') as f:
    json.dump(custom_config, f)

# Use custom config
generator = EnhancedSocialImageGenerator('config/custom.json')
```

## 🐳 Docker Deployment

### Cross-Platform Compatibility

This project is designed to work seamlessly across different operating systems:

#### Windows
- Uses PowerShell scripts for automation
- Handles Windows-specific path formats
- Includes emoji-free logging for compatibility

#### Linux
- Uses Bash scripts for automation
- Includes Linux-specific Docker configurations
- Handles user permissions automatically

#### macOS
- Compatible with standard Docker Compose commands
- Uses system fonts as fallbacks

### Build and Run

#### Windows
```bash
# Enhanced build with validation
.\test_docker.ps1

# Or standard Docker commands
docker-compose up --build -d
```

#### Linux
```bash
# Linux-specific build script
./build-linux.sh

# Or with Linux configuration
docker-compose -f docker-compose.yml -f docker-compose.linux.yml up --build -d

# Or standard Docker commands
docker-compose up --build -d
```

#### Manual Docker Commands
```bash
# Build the image
docker build -t social-image-generator .

# Run container (adjust volume paths for your OS)
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/generated:/app/generated \
  -v $(pwd)/output:/app/output \
  social-image-generator
```

### Docker Compose Services

```yaml
version: '3.8'
services:
  generator:
    build: .
    volumes:
      - ./output:/app/output
      - ./uploads:/app/uploads
    environment:
      - PYTHONPATH=/app/src
```

## 🔧 Advanced Features

### AI Background Removal

The generator automatically uses rembg for professional background removal:

```python
# Background removal is automatic
generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
# Main image background is removed using AI
```

### Dynamic Layout System

The layout automatically adapts to content:

```python
# Short text - compact layout
img1 = generator.generate_improved_hero_layout("Sale", "50% Off", "Brand")

# Long text - expanded layout
img2 = generator.generate_improved_hero_layout(
    "Exclusive Luxury Designer Collection with Premium Materials",
    "Discover our premium fashion items with exceptional craftsmanship",
    "Elite Fashion House International"
)
```

### Font Management

Custom fonts are automatically loaded:

```python
# Fonts are loaded from assets/fonts/
# Supports: headline, subheadline, brand
# Automatic fallback to system fonts
```

## 📋 Dependencies

- Python 3.8+
- Pillow (PIL)
- rembg (AI background removal)
- arabic-reshaper (Arabic text support)
- python-bidi (Bidirectional text)
- numpy
- scipy (optional, enhanced processing)
- onnxruntime (optional, faster AI processing)

## 🚨 Error Handling

```python
try:
    generator = EnhancedSocialImageGenerator('config/platforms/instagram_post.json')
    img = generator.generate_improved_hero_layout("Headline", "Subheadline", "Brand")
    img.save('output/result.png', 'PNG')
except FileNotFoundError:
    print("Configuration or image file not found")
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Generation failed: {e}")
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the examples in the `tests/` directory
- Review the configuration files in `config/`

## 🔄 Changelog

### Version 2.0.0
- ✅ Added AI-powered background removal with rembg
- ✅ Implemented dynamic layout system
- ✅ Added multi-language text support
- ✅ Docker containerization
- ✅ Professional typography with panels
- ✅ Brand logo integration with aspect ratio preservation

### Version 1.0.0
- ✅ Basic image generation
- ✅ Font loading and text rendering
- ✅ Platform-specific configurations
- ✅ Custom image support