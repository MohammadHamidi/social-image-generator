# 🎨 Gradient Generation API - Curl Commands

## 📖 Overview
The gradient generation endpoint creates beautiful gradient backgrounds with customizable colors, sizes, and directions.

**Endpoint:** `POST /generate_gradient`
**Base URL:** `http://87.236.166.7:9009`

## 📋 Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `width` | integer | No | 1080 | Image width (100-4096) |
| `height` | integer | No | 1350 | Image height (100-4096) |
| `colors` | array | Yes | - | Array of colors (min 2) |
| `gradient_type` | string | No | "linear" | "linear", "radial", "diagonal" |
| `direction` | string | No | "vertical" | "vertical", "horizontal", "diagonal" |

## 🎨 Color Formats

### Hex Colors
```json
["#FF6B6B", "#4ECDC4", "#45B7D1", "#FDCB6E"]
```

### RGB Arrays
```json
[[255, 107, 107], [78, 205, 196], [69, 183, 209]]
```

## 🔧 Curl Examples

### 1. Simple Vertical Gradient (2 Colors)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4"],
    "gradient_type": "linear",
    "direction": "vertical"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 2. Multi-Color Horizontal Gradient
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FDCB6E"],
    "gradient_type": "linear",
    "direction": "horizontal"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 3. Radial Gradient (Center to Edge)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080,
    "colors": ["#FFFFFF", "#FF6B6B"],
    "gradient_type": "radial",
    "direction": "vertical"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 4. Diagonal Gradient
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1350,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "gradient_type": "diagonal",
    "direction": "diagonal"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 5. RGB Array Format
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 800,
    "height": 600,
    "colors": [[255, 107, 107], [78, 205, 196]],
    "gradient_type": "linear",
    "direction": "vertical"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 6. Instagram Story Size (9:16)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1920,
    "colors": ["#667EEA", "#764BA2"],
    "gradient_type": "linear",
    "direction": "vertical"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

### 7. Square Format (1:1)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "width": 1080,
    "height": 1080,
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
    "gradient_type": "radial",
    "direction": "vertical"
  }' \
  http://87.236.166.7:9009/generate_gradient
```

## 📊 Response Format

```json
{
  "success": true,
  "message": "Gradient generated successfully",
  "download_url": "http://87.236.166.7:9009/generated/gradient_abc123.png",
  "filename": "gradient_abc123.png",
  "size": 245680,
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
  "generated_at": "2024-01-15T10:30:45.123456"
}
```

## 🎯 Popular Color Combinations

### Ocean Breeze
```json
["#667EEA", "#764BA2"]
```

### Sunset
```json
["#FF6B6B", "#4ECDC4", "#45B7D1"]
```

### Forest
```json
["#134E5E", "#71B280"]
```

### Fire
```json
["#FF6B6B", "#FFE259", "#FFA751"]
```

### Ice
```json
["#667EEA", "#764BA2", "#F093FB"]
```

## 🔍 Documentation Endpoint

Get detailed information about gradient options:
```bash
curl -X GET http://87.236.166.7:9009/gradient_info
```

## ⚡ Tips

1. **File Size**: Larger images produce bigger files
2. **Performance**: Radial gradients take longer to generate than linear
3. **Colors**: Minimum 2 colors, maximum unlimited
4. **Formats**: Both hex (#FF6B6B) and RGB arrays ([255, 107, 107]) supported
5. **Quality**: All gradients are saved at 95% quality PNG

## 🚨 Error Handling

Common error responses:
- `400 Bad Request`: Invalid parameters
- `500 Internal Server Error`: Server-side generation error

Example error:
```json
{
  "error": "Colors must be an array with at least 2 color values"
}
```
