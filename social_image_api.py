#!/usr/bin/env python3
"""
Social Image Generator API Server
Provides endpoints for uploading images and generating custom social media images.
"""

from flask import Flask, request, jsonify, send_file, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import json
from datetime import datetime
import sys
import io
from PIL import Image

# Add src to path for imports
sys.path.append('src')
from enhanced_social_generator import EnhancedSocialImageGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'main'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'watermark'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'background'), exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """Generate a unique filename to prevent conflicts"""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{timestamp}_{unique_id}.{ext}"

@app.route('/')
def index():
    """API documentation endpoint"""
    return jsonify({
        'name': 'Social Image Generator API',
        'version': '2.0',
        'description': 'Generate custom social media images with uploaded content',
        'endpoints': {
            'POST /upload/main': 'Upload main image',
            'POST /upload/watermark': 'Upload watermark/blueprint image',
            'POST /upload/background': 'Upload custom background image',
            'POST /generate': 'Generate social media image',
            'GET /health': 'Health check'
        },
        'example_usage': {
            'upload_main': 'curl -X POST -F "file=@main.png" http://localhost:5000/upload/main',
            'upload_watermark': 'curl -X POST -F "file=@watermark.png" http://localhost:5000/upload/watermark',
            'generate': '''
curl -X POST http://localhost:5000/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "headline": "کت‌های زمستانی جدید",
    "subheadline": "مجموعه‌ای از بهترین طراحی‌ها",
    "brand": "Fashion Store",
    "background_color": [255, 255, 255],
    "main_image_url": "http://localhost:5000/uploads/main/20240101_120000_abc123.png",
    "watermark_image_url": "http://localhost:5000/uploads/watermark/20240101_120001_def456.png"
  }'
            '''
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0'
    })

@app.route('/upload/main', methods=['POST'])
def upload_main_image():
    """Upload main image endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP'}), 400

        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'main', filename)

        # Save file
        file.save(filepath)

        # Generate URL
        file_url = url_for('uploaded_file', folder='main', filename=filename, _external=True)

        return jsonify({
            'success': True,
            'message': 'Main image uploaded successfully',
            'filename': filename,
            'url': file_url,
            'size': os.path.getsize(filepath),
            'upload_time': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/upload/watermark', methods=['POST'])
def upload_watermark_image():
    """Upload watermark/blueprint image endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP'}), 400

        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark', filename)

        # Save file
        file.save(filepath)

        # Generate URL
        file_url = url_for('uploaded_file', folder='watermark', filename=filename, _external=True)

        return jsonify({
            'success': True,
            'message': 'Watermark image uploaded successfully',
            'filename': filename,
            'url': file_url,
            'size': os.path.getsize(filepath),
            'upload_time': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/upload/background', methods=['POST'])
def upload_background_image():
    """Upload custom background image endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'background')
        
        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(target_dir, filename)

        # Save file
        file.save(filepath)

        # Generate URL
        filename = os.path.basename(filepath)
        file_url = url_for('uploaded_file', folder='background', filename=filename, _external=True)

        return jsonify({
            'success': True,
            'message': 'Background image uploaded and processed successfully',
            'filename': filename,
            'url': file_url,
            'local_path': filepath,
            'size': os.path.getsize(filepath),
            'upload_time': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    """Serve uploaded files"""
    if folder not in ['main', 'watermark', 'background']:
        return jsonify({'error': 'Invalid folder'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(filepath)

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate social media image endpoint"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Extract required fields
        headline = data.get('headline', '')
        subheadline = data.get('subheadline', '')
        brand = data.get('brand', '')

        # Extract optional configuration
        background_color = data.get('background_color', [255, 255, 255])
        main_image_url = data.get('main_image_url')
        watermark_image_url = data.get('watermark_image_url')
        background_image_url = data.get('background_image_url')
        watermark_position = data.get('watermark_position', 'bottom-right')  # bottom-right, top-right, bottom-center

        # Validate required fields
        if not headline:
            return jsonify({'error': 'Headline is required'}), 400

        # Calculate watermark position based on choice
        watermark_positions = {
            'bottom-right': [860, 1200],
            'top-right': [860, 50],  
            'bottom-center': [440, 1200],
            'top-left': [20, 50],
            'bottom-left': [20, 1200]
        }
        
        watermark_pos = watermark_positions.get(watermark_position, [860, 1200])

        # Create configuration
        config = {
            'canvas_width': 1080,
            'canvas_height': 1350,
            'background_color': background_color,
            'use_custom_images': bool(main_image_url or watermark_image_url or background_image_url),
            'custom_images': {
                'remove_background': True,
                'background_removal_method': 'auto',
                'main_image_size': [500, 400],
                'blueprint_image_size': [200, 120],
                'main_image_position': [290, 500],
                'blueprint_image_position': watermark_pos
            }
        }

        # Handle image URLs
        if main_image_url:
            # Download and save main image
            main_filename = f"main_{uuid.uuid4().hex[:8]}.png"
            main_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'main', main_filename)

            try:
                import requests
                response = requests.get(main_image_url, timeout=10)
                response.raise_for_status()

                with open(main_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['main_image_path'] = main_filepath

            except Exception as e:
                return jsonify({'error': f'Failed to download main image: {str(e)}'}), 400

        if watermark_image_url:
            # Download and save watermark image
            watermark_filename = f"watermark_{uuid.uuid4().hex[:8]}.png"
            watermark_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark', watermark_filename)

            try:
                import requests
                response = requests.get(watermark_image_url, timeout=10)
                response.raise_for_status()

                with open(watermark_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['blueprint_image_path'] = watermark_filepath

            except Exception as e:
                return jsonify({'error': f'Failed to download watermark image: {str(e)}'}), 400

        if background_image_url:
            # Download and save background image
            background_filename = f"background_{uuid.uuid4().hex[:8]}.png"
            background_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'background', background_filename)

            try:
                import requests
                response = requests.get(background_image_url, timeout=10)
                response.raise_for_status()

                with open(background_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['background_image_path'] = background_filepath

            except Exception as e:
                return jsonify({'error': f'Failed to download background image: {str(e)}'}), 400

        # Create temporary config file
        config_filename = f"temp_config_{uuid.uuid4().hex[:8]}.json"
        config_filepath = os.path.join(app.config['GENERATED_FOLDER'], config_filename)

        with open(config_filepath, 'w') as f:
            json.dump(config, f)

        # Generate image
        print("🔄 Generating enhanced social media image...")
        generator = EnhancedSocialImageGenerator(config_filepath)
        img = generator.generate_enhanced_hero_layout(headline, subheadline, brand)

        # Save generated image
        output_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        output_filepath = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        img.save(output_filepath, 'PNG')

        # Generate download URL
        download_url = url_for('generated_file', filename=output_filename, _external=True)

        # Clean up temp config
        try:
            os.remove(config_filepath)
        except:
            pass

        return jsonify({
            'success': True,
            'message': 'Image generated successfully',
            'download_url': download_url,
            'filename': output_filename,
            'size': os.path.getsize(output_filepath),
            'generated_at': datetime.now().isoformat(),
            'config': {
                'headline': headline,
                'subheadline': subheadline,
                'brand': brand,
                'background_color': background_color,
                'main_image_used': bool(main_image_url),
                'watermark_image_used': bool(watermark_image_url)
            }
        })

    except Exception as e:
        print(f"Generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/generated/<filename>')
def generated_file(filename):
    """Serve generated image files"""
    filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Generated file not found'}), 404

    return send_file(filepath, mimetype='image/png')

@app.route('/files')
def list_files():
    """List all uploaded files for debugging"""
    main_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'main'))
    watermark_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'watermark'))
    generated_files = os.listdir(app.config['GENERATED_FOLDER'])

    return jsonify({
        'main_images': main_files,
        'watermark_images': watermark_files,
        'generated_images': generated_files,
        'total_main': len(main_files),
        'total_watermark': len(watermark_files),
        'total_generated': len(generated_files)
    })

@app.route('/generate_text', methods=['POST'])
def generate_text_layout():
    """Generate text-based social media image layouts"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        layout_type = data.get('layout_type')
        content = data.get('content', {})
        
        if not layout_type:
            return jsonify({'error': 'layout_type is required'}), 400
        
        # Supported text layout types
        valid_layouts = ['quote', 'article', 'announcement', 'list', 'testimonial']
        
        if layout_type not in valid_layouts:
            return jsonify({
                'error': f'Invalid layout_type. Must be one of: {", ".join(valid_layouts)}'
            }), 400
        
        # Load configuration
        config_path = data.get('config', 'config/text_layouts_config.json')
        if not os.path.exists(config_path):
            config_path = None  # Use default config
        
        # Initialize generator
        generator = EnhancedSocialImageGenerator(config_path)
        
        # Generate image
        img = generator.generate_text_layout(layout_type, content)
        
        # Save generated image
        output_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        img.save(output_path, 'PNG', quality=95)
        
        # Return response
        return jsonify({
            'success': True,
            'message': f'Text layout {layout_type} generated successfully',
            'layout_type': layout_type,
            'filename': output_filename,
            'download_url': url_for('generated_file', filename=output_filename, _external=True),
            'content_used': content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_all_text', methods=['POST'])
def generate_all_text_layouts():
    """Generate all text layout variations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        content = data.get('content', {})
        output_prefix = data.get('output_prefix', 'text_post')
        
        # Load configuration
        config_path = data.get('config', 'config/text_layouts_config.json')
        if not os.path.exists(config_path):
            config_path = None
        
        # Initialize generator
        generator = EnhancedSocialImageGenerator(config_path)
        
        # Set output directory to generated folder
        generator.output_dir = app.config['GENERATED_FOLDER']
        
        # Generate all layouts
        generator.generate_all_text_layouts(content, output_prefix)
        
        # List generated files
        generated_files = []
        text_layouts = ['quote', 'article', 'announcement', 'list', 'testimonial']
        
        for layout_type in text_layouts:
            filename = f"{output_prefix}_{layout_type}.png"
            filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
            if os.path.exists(filepath):
                generated_files.append({
                    'layout_type': layout_type,
                    'filename': filename,
                    'download_url': url_for('generated_file', filename=filename, _external=True)
                })
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(generated_files)} text layouts',
            'generated_files': generated_files,
            'content_used': content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/text_layout_info', methods=['GET'])
def text_layout_info():
    """Get information about available text layout types and their content structure"""
    return jsonify({
        'text_layouts': {
            'quote': {
                'description': 'Large quote with attribution',
                'required_fields': ['quote'],
                'optional_fields': ['author', 'brand'],
                'example': {
                    'quote': 'Success is not final, failure is not fatal.',
                    'author': 'Winston Churchill',
                    'brand': 'Inspiration Daily'
                }
            },
            'article': {
                'description': 'Article excerpt with title and body text',
                'required_fields': ['title', 'body'],
                'optional_fields': ['brand'],
                'example': {
                    'title': 'The Future of Technology',
                    'body': 'Artificial intelligence is transforming every industry...',
                    'brand': 'Tech Insights'
                }
            },
            'announcement': {
                'description': 'Announcement with title, description, and call-to-action',
                'required_fields': ['title', 'description'],
                'optional_fields': ['cta', 'brand'],
                'example': {
                    'title': 'New Product Launch',
                    'description': 'Revolutionary innovation for your workflow',
                    'cta': 'Learn More',
                    'brand': 'Innovation Co.'
                }
            },
            'list': {
                'description': 'List layout with title and bulleted items',
                'required_fields': ['title', 'items'],
                'optional_fields': ['brand'],
                'example': {
                    'title': '5 Tips for Better Design',
                    'items': ['Keep it simple', 'Use consistent typography', 'Test with users'],
                    'brand': 'Design Studio'
                }
            },
            'testimonial': {
                'description': 'Testimonial with quote and person information',
                'required_fields': ['quote', 'person_name'],
                'optional_fields': ['person_title', 'brand'],
                'example': {
                    'quote': 'This product transformed our business operations.',
                    'person_name': 'Sarah Johnson',
                    'person_title': 'CEO, Tech Startup',
                    'brand': 'Product Reviews'
                }
            }
        },
        'features': [
            'Multi-line text wrapping',
            'Justified text alignment',
            'Arabic/Farsi text support',
            'Customizable fonts and colors',
            'Responsive layouts'
        ]
    })

if __name__ == '__main__':
    print("🚀 Social Image Generator API Server")
    print("=" * 50)
    print("📡 Starting server on http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000")
    print("💡 Health Check: http://localhost:5000/health")
    print()
    print("📤 Upload Endpoints:")
    print("   POST /upload/main - Upload main image")
    print("   POST /upload/watermark - Upload watermark image")
    print()
    print("🎨 Generation:")
    print("   POST /generate - Generate social media image")
    print("   POST /generate_text - Generate text-based layouts")
    print("   POST /generate_all_text - Generate all text layouts")
    print("   GET /text_layout_info - Text layout documentation")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
