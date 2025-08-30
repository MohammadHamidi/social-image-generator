#!/bin/bash

# Quick run script for social image generator

echo "🎨 Social Image Generator"
echo "========================"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run setup first."
    exit 1
fi

# Check if user wants to run tests or generate images
if [ "$1" = "test" ]; then
    echo "🧪 Running tests..."
    python tests/test_generator.py
elif [ "$1" = "nodejs" ]; then
    echo "🚀 Running Node.js generator..."
    npm start
else
    echo "🎯 Generating social media images..."
    python src/social_image_generator.py
fi

echo "✅ Done! Check the output/ directory for your images."
