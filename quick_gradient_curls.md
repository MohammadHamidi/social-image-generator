# 🚀 Quick Gradient Generation Commands

## 🔥 Most Popular (Copy-Paste Ready)

### 1. Beautiful Triadic Gradient
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B"],"gradient_type":"linear","direction":"vertical","generate_harmony":true,"harmony_type":"triadic","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.03}'
```

### 2. Ocean Blue Harmony
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1920,"colors":["#667EEA"],"gradient_type":"radial","direction":"vertical","generate_harmony":true,"harmony_type":"analogous","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.01}'
```

### 3. Sunset Horizontal
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B","#4ECDC4"],"gradient_type":"linear","direction":"horizontal","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.025}'
```

### 4. Forest Green Complementary
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#134E5E"],"gradient_type":"linear","direction":"vertical","generate_harmony":true,"harmony_type":"complementary","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.02}'
```

### 5. Ice Blue Triadic
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#667EEA","#764BA2","#F093FB"],"gradient_type":"linear","direction":"vertical","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.02}'
```

## 🎨 By Gradient Type

### Linear Vertical
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B","#4ECDC4","#45B7D1"],"gradient_type":"linear","direction":"vertical","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.025}'
```

### Linear Horizontal
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B","#4ECDC4","#45B7D1","#FDCB6E"],"gradient_type":"linear","direction":"horizontal","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.02}'
```

### Radial
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1080,"colors":["#FFFFFF","#FF6B6B"],"gradient_type":"radial","direction":"vertical","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.015}'
```

### Diagonal
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B","#4ECDC4","#45B7D1"],"gradient_type":"diagonal","direction":"diagonal","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.03}'
```

## 🎯 By Harmony Type

### Triadic (3 colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B"],"generate_harmony":true,"harmony_type":"triadic","use_hsl_interpolation":true,"add_noise":true}'
```

### Complementary (2 colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#FF6B6B"],"generate_harmony":true,"harmony_type":"complementary","use_hsl_interpolation":true,"add_noise":true}'
```

### Analogous (3 similar colors)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1350,"colors":["#667EEA"],"generate_harmony":true,"harmony_type":"analogous","use_hsl_interpolation":true,"add_noise":true}'
```

## 📱 Social Media Sizes

### Instagram Story (9:16)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1920,"colors":["#667EEA"],"gradient_type":"radial","generate_harmony":true,"harmony_type":"analogous","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.01}'
```

### Instagram Post (1:1)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":1080,"height":1080,"colors":["#FF6B6B"],"generate_harmony":true,"harmony_type":"triadic","use_hsl_interpolation":true,"add_noise":true}'
```

### Facebook Cover (205:78)
```bash
curl -X POST http://87.236.166.7:9009/generate_gradient -H "Content-Type: application/json" -d '{"width":820,"height":312,"colors":["#667EEA","#764BA2"],"gradient_type":"linear","direction":"horizontal","use_hsl_interpolation":true,"add_noise":true,"noise_intensity":0.02}'
```

## 🛠️ Utility Commands

### Get Documentation
```bash
curl -X GET http://87.236.166.7:9009/gradient_info
```

### Check API Status
```bash
curl -X GET http://87.236.166.7:9009/health
```

### List Generated Files
```bash
curl -X GET http://87.236.166.7:9009/files
```

---

## 💡 Pro Tips:

1. **For best results**: Always use `use_hsl_interpolation: true`
2. **Natural look**: Add subtle noise with `noise_intensity: 0.02`
3. **Color harmony**: Use `generate_harmony: true` with single color input
4. **Quality**: Set `quality: 95` for best balance of size/quality
5. **Social media**: Use 1080 width for Instagram compatibility

**Copy any command above and run it directly in your terminal!** 🚀
