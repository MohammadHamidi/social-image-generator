# Text Layout Features

This document describes the new text-based layout options that complement the existing product-focused layouts.

## Overview

The social image generator now supports **text-focused layouts** for creating social media content that doesn't rely on product images. These layouts are perfect for:

- Inspirational quotes
- Article excerpts and blog posts
- Announcements and promotions
- Lists and tips
- Customer testimonials

## Available Text Layouts

### 1. Quote Layout
**Perfect for**: Inspirational quotes, famous sayings, motivational content

**Required fields:**
- `quote`: The main quote text

**Optional fields:**
- `author`: Attribution for the quote
- `brand`: Your brand name

**Example:**
```json
{
  "layout_type": "quote",
  "content": {
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs",
    "brand": "Motivation Hub"
  }
}
```

### 2. Article Layout
**Perfect for**: Blog excerpts, article summaries, thought leadership content

**Required fields:**
- `title`: Article headline
- `body`: Main article text (supports multi-line with justified alignment)

**Optional fields:**
- `brand`: Your brand name

**Example:**
```json
{
  "layout_type": "article",
  "content": {
    "title": "The Future of Technology",
    "body": "Artificial Intelligence is revolutionizing industries across the globe. From healthcare to finance, AI technologies are enabling unprecedented efficiency and innovation.",
    "brand": "Tech Today"
  }
}
```

### 3. Announcement Layout
**Perfect for**: Product launches, events, sales, important updates

**Required fields:**
- `title`: Main announcement headline
- `description`: Details about the announcement

**Optional fields:**
- `cta`: Call-to-action text (appears in highlighted button)
- `brand`: Your brand name

**Example:**
```json
{
  "layout_type": "announcement",
  "content": {
    "title": "Big Sale Event!",
    "description": "Don't miss our biggest sale of the year. Save up to 70% on selected items.",
    "cta": "Shop Now",
    "brand": "Fashion Store"
  }
}
```

### 4. List Layout
**Perfect for**: Tips, guidelines, step-by-step instructions, feature lists

**Required fields:**
- `title`: List headline
- `items`: Array of list items

**Optional fields:**
- `brand`: Your brand name

**Example:**
```json
{
  "layout_type": "list",
  "content": {
    "title": "5 Essential Skills for 2024",
    "items": [
      "Digital literacy and computer skills",
      "Critical thinking and problem solving",
      "Emotional intelligence and empathy",
      "Adaptability and continuous learning",
      "Communication and collaboration"
    ],
    "brand": "Career Development"
  }
}
```

### 5. Testimonial Layout
**Perfect for**: Customer reviews, success stories, social proof

**Required fields:**
- `quote`: The testimonial text
- `person_name`: Name of the person giving the testimonial

**Optional fields:**
- `person_title`: Job title or company of the person
- `brand`: Your brand name

**Example:**
```json
{
  "layout_type": "testimonial",
  "content": {
    "quote": "This service exceeded all our expectations. The quality is outstanding and the support team is incredibly responsive.",
    "person_name": "Dr. Maria Rodriguez",
    "person_title": "Director of Operations, TechCorp",
    "brand": "Customer Reviews"
  }
}
```

## Key Features

### Multi-line Text Support
- **Automatic text wrapping**: Long text automatically wraps to fit the canvas
- **Justified alignment**: Body text can be justified for professional appearance
- **Smart line spacing**: Optimized spacing for readability

### Typography Hierarchy
- **Large headlines**: Eye-catching titles and quotes
- **Medium body text**: Readable content with proper sizing
- **Small attribution**: Subtle author and brand information

### Multilingual Support
- **Arabic/Farsi text**: Full support for RTL languages
- **Proper text reshaping**: Arabic text displays correctly
- **BiDi algorithm**: Handles mixed LTR/RTL content

### Responsive Design
- **Dynamic sizing**: Text scales based on content length
- **Consistent margins**: Professional spacing across all layouts
- **Clean backgrounds**: Beautiful gradient backgrounds

## Usage

### Python API

```python
from enhanced_social_generator import EnhancedSocialImageGenerator

# Initialize generator
generator = EnhancedSocialImageGenerator('config/text_layouts_config.json')

# Generate single layout
content = {
    "quote": "Innovation distinguishes between a leader and a follower.",
    "author": "Steve Jobs",
    "brand": "Leadership Quotes"
}
img = generator.generate_text_layout('quote', content)
img.save('quote_layout.png')

# Generate all layouts with same content
generator.generate_all_text_layouts(content, "inspiration_post")
```

### REST API

**Single Layout Generation:**
```bash
curl -X POST http://localhost:5000/generate_text \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "quote",
    "content": {
      "quote": "Success is not final, failure is not fatal.",
      "author": "Winston Churchill",
      "brand": "Daily Motivation"
    }
  }'
```

**Batch Generation:**
```bash
curl -X POST http://localhost:5000/generate_all_text \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "quote": "The best time to plant a tree was 20 years ago.",
      "author": "Chinese Proverb",
      "title": "Environmental Consciousness",
      "body": "Small actions today create significant impacts tomorrow.",
      "description": "Join our sustainability initiative.",
      "cta": "Get Involved",
      "items": ["Reduce waste", "Conserve energy", "Plant trees"],
      "person_name": "Emma Green",
      "person_title": "Environmental Activist",
      "brand": "Green Future"
    },
    "output_prefix": "sustainability_campaign"
  }'
```

**Get Layout Information:**
```bash
curl http://localhost:5000/text_layout_info
```

## Configuration

The text layouts can be customized using the `config/text_layouts_config.json` file:

```json
{
  "background": {
    "type": "gradient",
    "primary_color": [45, 55, 72],
    "secondary_color": [68, 90, 120],
    "gradient_direction": "diagonal"
  },
  "text_layouts": {
    "quote": {
      "quote_font_size": 42,
      "quote_color": [255, 255, 255],
      "author_color": [200, 200, 200],
      "margin": 80,
      "line_spacing": 15
    }
  }
}
```

## Testing

Test the text layout features:

```bash
# Test all layouts with sample content
python3 test_text_layouts.py

# Test API endpoints (requires running server)
python3 test_text_api.py
```

## Output Examples

All generated images are saved to the `output/` directory:

- `text_layout_quote.png`
- `text_layout_article.png`
- `text_layout_announcement.png`
- `text_layout_list.png`
- `text_layout_testimonial.png`

## Integration with Existing Features

Text layouts work alongside existing product layouts:

- Use the same configuration system
- Support custom backgrounds
- Compatible with all API endpoints
- Share the same output directory structure

## Best Practices

1. **Keep quotes concise**: Aim for 1-3 sentences for optimal readability
2. **Use hierarchy**: Important information should be in titles, details in body text
3. **Brand consistently**: Include your brand name for recognition
4. **Test different layouts**: The same content can work in multiple layout types
5. **Consider your audience**: Choose layouts that match your content style

## Troubleshooting

**Common issues:**

- **Text too long**: Content will auto-wrap, but very long text may look cramped
- **Arabic text issues**: Ensure you have Arabic fonts installed on your system
- **Layout spacing**: Adjust margin and line_spacing in config for custom spacing

**Solutions:**
- Break long content into shorter, more digestible pieces
- Use the article layout for longer content
- Test with different font sizes in the configuration
