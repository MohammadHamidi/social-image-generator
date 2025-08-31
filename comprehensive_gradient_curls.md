# 🎨 Complete Enhanced Gradient Generation - Curl Commands

## 📖 Overview
The enhanced gradient generation API now supports advanced features for creating beautiful, professional gradients.

**Base URL:** `http://87.236.166.7:9009`
**Endpoint:** `POST /generate_gradient`

---

## 🔧 Basic Enhanced Gradients

### 1. HSL Interpolation (Smoother Colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true
  }'
```

### 2. With Subtle Noise Texture
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
    "noise_intensity": 0.03
  }'
```

---

## 🎨 Auto Color Harmony Generation

### 3. Triadic Harmony (3 Colors, 120° Apart)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
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
```

### 4. Complementary Harmony (Opposite Colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B"],
    "gradient_type": "radial",
    "direction": "vertical",
    "generate_harmony": true,
    "harmony_type": "complementary",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.025
  }'
```

### 5. Analogous Harmony (Similar Colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#667EEA"],
    "gradient_type": "linear",
    "direction": "vertical",
    "generate_harmony": true,
    "harmony_type": "analogous",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

### 6. Split Complementary Harmony
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B"],
    "gradient_type": "diagonal",
    "direction": "diagonal",
    "generate_harmony": true,
    "harmony_type": "split_complementary",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.03
  }'
```

---

## 🌈 Gradient Type Variations

### 7. Enhanced Linear Vertical
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.025
  }'
```

### 8. Enhanced Linear Horizontal
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FDCB6E"],
    "gradient_type": "linear",
    "direction": "horizontal",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

### 9. Enhanced Radial Gradient
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080,
    "colors": ["#FFFFFF", "#FF6B6B"],
    "gradient_type": "radial",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.015
  }'
```

### 10. Enhanced Diagonal Gradient
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "gradient_type": "diagonal",
    "direction": "diagonal",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.03
  }'
```

---

## 🎯 Popular Enhanced Combinations

### 11. Ocean Dream (Instagram Story Size)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1920,
    "colors": ["#667EEA"],
    "gradient_type": "radial",
    "direction": "vertical",
    "generate_harmony": true,
    "harmony_type": "analogous",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.01
  }'
```

### 12. Sunset Vibes
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "horizontal",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.025,
    "apply_dither": true
  }'
```

### 13. Forest Harmony
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#134E5E"],
    "gradient_type": "linear",
    "direction": "vertical",
    "generate_harmony": true,
    "harmony_type": "complementary",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

### 14. Fire Gradient
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#FFE259", "#FFA751"],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.03
  }'
```

### 15. Ice Blue Triadic
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#667EEA", "#764BA2", "#F093FB"],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02,
    "quality": 95
  }'
```

---

## 🛠️ Advanced Settings Examples

### 16. Maximum Quality (No Compression)
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
    "noise_intensity": 0.01,
    "quality": 100,
    "apply_dither": true
  }'
```

### 17. Minimal Noise (Subtle Texture)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "radial",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.005
  }'
```

### 18. High Contrast (No Noise)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#000000", "#FFFFFF"],
    "gradient_type": "linear",
    "direction": "horizontal",
    "use_hsl_interpolation": true,
    "add_noise": false
  }'
```

---

## 📊 RGB Array Format Examples

### 19. RGB Array Colors
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 800,
    "height": 600,
    "colors": [[255, 107, 107], [78, 205, 196], [69, 183, 209]],
    "gradient_type": "linear",
    "direction": "vertical",
    "use_hsl_interpolation": true,
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

---

## 🔍 Utility Endpoints

### 20. Get Gradient Documentation
```bash
curl -X GET http://87.236.166.7:9009/gradient_info
```

### 21. Check API Health
```bash
curl -X GET http://87.236.166.7:9009/health
```

### 22. List Generated Files
```bash
curl -X GET http://87.236.166.7:9009/files
```

---

## 📋 Response Format

All gradient generation requests return:
```json
{
  "success": true,
  "message": "Gradient generated successfully",
  "download_url": "http://87.236.166.7:9009/generated/gradient_abc123.png",
  "filename": "gradient_abc123.png",
  "size": 2878404,
  "dimensions": {
    "width": 1080,
    "height": 1350
  },
  "gradient_config": {
    "colors": ["#ff6b6b", "#6dff6b", "#6d6bff"],
    "direction": "vertical",
    "rgb_colors": [[255, 107, 107], [109, 255, 107], [109, 107, 255]],
    "type": "linear"
  },
  "enhancements": {
    "hsl_interpolation": true,
    "noise_added": true,
    "noise_intensity": 0.03,
    "harmony_generated": true,
    "harmony_type": "triadic",
    "dither_applied": false,
    "quality": 95
  },
  "generated_at": "2025-08-31T09:56:33.333222"
}
```

---

## 💡 Quick Copy-Paste Commands

**Most Beautiful Gradient:**
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B"],"gradient_type":"linear","direction":"vertical","generate_harmony":true,"harmony_type":"triadic","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.03}'
```

**Professional Background:**
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1920,"colors":["#667EEA"],"gradient_type":"radial","generate_harmony":true,"harmony_type":"analogous","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.01}'
```

**Social Media Ready:**
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B","#4ECDC4"],"gradient_type":"linear","direction":"horizontal","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.025}'
```
