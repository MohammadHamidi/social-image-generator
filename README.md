# Social Image Generator

A programmatic social media image generator that creates Instagram-friendly posts with Farsi text support, decorative coat graphics, and multiple layout variations.

## Features

- 🎨 **Four Layout Variations**: Hero, Split, Top-heavy, Bottom-heavy
- 🔤 **Farsi Text Support**: Proper right-to-left text rendering
- 🧥 **Decorative Elements**: Colorful coat graphics with hangers
- 🖼️ **Custom Backgrounds**: Tinted abstract patterns
- ⚙️ **Configurable**: Colors, fonts, sizes, and spacing
- 🚀 **Dual Implementation**: Python (Pillow) and Node.js (HTML-to-image)

## Quick Start

### Python Implementation (Recommended)

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the generator:**
   ```bash
   python src/social_image_generator.py
   ```

3. **Run tests:**
   ```bash
   python tests/test_generator.py
   ```

### Node.js Alternative

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Generate images:**
   ```bash
   npm start
   ```

## Project Structure

```
social-image-generator/
├── src/
│   ├── social_image_generator.py    # Main Python generator
│   ├── create_sample_background.py  # Background pattern creator
│   └── nodejs_generator.js          # Node.js alternative
├── assets/
│   ├── fonts/                       # Font files
│   ├── backgrounds/                 # Background patterns
│   └── samples/                     # Sample images
├── config/
│   ├── default_config.json          # Default configuration
│   └── sample_content.json          # Sample content
├── output/                          # Generated images
├── tests/
│   └── test_generator.py           # Test script
└── requirements.txt                # Python dependencies
```

## Configuration

Edit `config/default_config.json` to customize:

- Canvas dimensions (default: 1080×1350)
- Colors and fonts
- Text sizes and positioning
- Number of coats and their colors

## Usage Examples

### Python API
```python
from src.social_image_generator import SocialImageGenerator

content = {
    'headline': 'کت‌های زمستانی جدید',
    'subheadline': 'مجموعه‌ای از بهترین طراحی‌ها',
    'brand': 'Fashion Store'
}

generator = SocialImageGenerator()
generator.generate_all_layouts(content, "my_post")
```

### Command Line
```bash
# Generate all layouts
python src/social_image_generator.py

# Run tests
python tests/test_generator.py
```

## Layout Types

1. **Hero Layout**: Centered content with prominent text panel
2. **Split Layout**: Text on left, coats on right
3. **Top-heavy Layout**: Large text area at top, coats below
4. **Bottom-heavy Layout**: Small text at top, large coat area below

## Requirements

- Python 3.7+
- Pillow (PIL)
- arabic-reshaper
- python-bidi
- Node.js (for alternative implementation)

## Customization

1. **Add new layouts**: Create new methods in `SocialImageGenerator` class
2. **Modify backgrounds**: Replace files in `assets/backgrounds/`
3. **Change fonts**: Add fonts to `assets/fonts/`
4. **Adjust colors**: Edit `config/default_config.json`

## Troubleshooting

- **Font issues**: Install Noto Sans Arabic or modify font paths
- **Text not displaying**: Check font encoding and bidi support
- **Background missing**: Run `python src/create_sample_background.py`

## License

MIT License - feel free to use and modify for your projects!
