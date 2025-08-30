# Bundled Fonts for Docker Container

This directory contains fonts that are bundled with the application for Docker deployment.

## Required Fonts

For the social image generator to work in a Docker container, you need to place the following font files in this directory:

### Latin Text Support
- `NotoSans-Regular.ttf` - Regular text
- `NotoSans-Bold.ttf` - Headlines and bold text
- `NotoSans-Medium.ttf` - Medium weight (optional)

### Arabic/Persian Text Support
- `NotoSansArabic-Regular.ttf` - Arabic regular text
- `NotoSansArabic-Bold.ttf` - Arabic headlines
- `NotoSansArabic-Medium.ttf` - Arabic medium weight (optional)

## How to Get the Fonts

### Option 1: Download from Google Fonts
```bash
# From the assets/fonts directory
curl -L -o "NotoSans-Regular.ttf" "https://fonts.google.com/download?family=Noto%20Sans"
curl -L -o "NotoSansArabic-Regular.ttf" "https://fonts.google.com/download?family=Noto%20Sans%20Arabic"
```

### Option 2: Use system fonts (for local development)
The font loading system will automatically fall back to system fonts if bundled fonts are not available.

### Option 3: Alternative fonts
You can use any TTF fonts that support the required character sets:
- **Inter** - Modern UI font with good Latin support
- **Source Sans Pro** - Adobe's open source font
- **Roboto** - Google's Android font
- **IBM Plex Sans** - IBM's corporate font with Arabic support

## Font Loading Priority

1. Bundled fonts in this directory (highest priority)
2. System fonts (fallback for development)
3. PIL default font (last resort)

## Docker Integration

The Dockerfile should copy these fonts and install them:

```dockerfile
# Install font utilities
RUN apt-get update && apt-get install -y fontconfig

# Copy fonts to container
COPY assets/fonts/*.ttf /usr/share/fonts/truetype/custom/

# Update font cache
RUN fc-cache -fv
```

## File Structure
```
assets/fonts/
├── README.md (this file)
├── NotoSans-Regular.ttf
├── NotoSans-Bold.ttf
├── NotoSansArabic-Regular.ttf
└── NotoSansArabic-Bold.ttf
```
