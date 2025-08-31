# 🎨 Enhanced Gradient Generation Examples

## ✨ New Enhanced Features

### 1. **HSL Color Interpolation** - Smoother Color Transitions
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

### 2. **Subtle Noise Texture** - More Organic Look
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "vertical",
    "add_noise": true,
    "noise_intensity": 0.03
  }'
```

### 3. **Auto Color Harmony Generation** - Professional Color Schemes
```bash
# Triadic Harmony (3 colors, 120° apart)
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
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

### 4. **Complete Enhancement Package** - Maximum Beauty
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
    "noise_intensity": 0.03,
    "generate_harmony": true,
    "harmony_type": "triadic",
    "quality": 95
  }'
```

## 🎯 Popular Enhanced Gradients

### **Ocean Dream**
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
    "add_noise": true,
    "noise_intensity": 0.01
  }'
```

### **Sunset Vibes**
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
    "noise_intensity": 0.025
  }'
```

### **Forest Harmony**
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
    "add_noise": true,
    "noise_intensity": 0.02
  }'
```

## 📊 Enhancement Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_hsl_interpolation` | boolean | `true` | Use HSL color space for smoother transitions |
| `add_noise` | boolean | `true` | Add subtle texture/noise |
| `noise_intensity` | number | `0.02` | Noise strength (0.01-0.1) |
| `generate_harmony` | boolean | `false` | Auto-generate harmonious colors |
| `harmony_type` | string | `"complementary"` | `complementary`, `triadic`, `analogous`, `split_complementary` |
| `apply_dither` | boolean | `false` | Apply dithering for banding reduction |
| `quality` | number | `95` | PNG quality (1-100) |

## 🔄 N8N Integration

Update your N8N workflow with enhanced gradients:

```json
{
  "requestMethod": "POST",
  "url": "http://87.236.166.7:9009/generate_gradient",
  "options": {
    "bodyContentType": "multipart-form-data"
  },
  "bodyParameters": {
    "parameters": [
      {
        "name": "width",
        "value": "1080"
      },
      {
        "name": "height",
        "value": "1350"
      },
      {
        "name": "colors",
        "value": "[\"#FF6B6B\", \"#4ECDC4\"]"
      },
      {
        "name": "use_hsl_interpolation",
        "value": "true"
      },
      {
        "name": "add_noise",
        "value": "true"
      },
      {
        "name": "generate_harmony",
        "value": "true"
      }
    ]
  }
}
```

## ✨ Results Comparison

### Before (Basic):
- RGB linear interpolation
- Flat, artificial look
- Limited color transitions

### After (Enhanced):
- ✅ HSL color space interpolation
- ✅ Subtle noise texture
- ✅ Auto color harmony generation
- ✅ Professional-grade gradients
- ✅ Smoother color transitions
- ✅ More natural, organic appearance

The enhanced gradients now look much more professional and visually appealing! 🎨✨
