#!/bin/bash

# Test script for gradient generation endpoint
echo "🧪 Testing Gradient Generation API"
echo "=================================="

# Test 1: Simple vertical gradient
echo -e "\n📊 Test 1: Simple Vertical Gradient"
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

# Test 2: Multi-color horizontal gradient
echo -e "\n\n🌈 Test 2: Multi-Color Horizontal Gradient"
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

# Test 3: Radial gradient
echo -e "\n\n🔵 Test 3: Radial Gradient"
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

# Test 4: RGB array format
echo -e "\n\n📐 Test 4: RGB Array Format"
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

# Test 5: Diagonal gradient
echo -e "\n\n🔄 Test 5: Diagonal Gradient"
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

echo -e "\n\n✅ Gradient tests completed!"
