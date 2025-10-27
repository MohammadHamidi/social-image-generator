#!/usr/bin/env python3
"""
Social Image Generator API Server
Provides endpoints for uploading images and generating custom social media images.
Enhanced version with robust error handling and better diagnostics.
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
from PIL import Image, ImageDraw
import numpy as np
import colorsys
import random
import stat

# Add src to path for imports
sys.path.append('src')
from enhanced_social_generator import EnhancedSocialImageGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# URL Configuration - Set to False to return relative paths instead of full URLs
RETURN_FULL_URLS = False

def safe_makedirs(path, exist_ok=True):
    """
    Safely create directories with proper error handling and permission fixes.

    Args:
        path (str): Directory path to create
        exist_ok (bool): Don't raise error if directory exists

    Returns:
        bool: True if directory exists/created successfully, False otherwise
    """
    try:
        # Try to create the directory
        os.makedirs(path, exist_ok=exist_ok)

        # For Docker volumes, we might not be able to change permissions
        # but the directory might still be usable
        if os.path.exists(path):
            # Try to make it writable if possible
            try:
                current_stat = os.stat(path)
                # Try to add write permission for owner
                os.chmod(path, current_stat.st_mode | stat.S_IWUSR)
                if os.access(path, os.W_OK):
                    print(f"✅ Directory ready: {path}")
                    return True
            except (PermissionError, OSError):
                # If we can't change permissions, that's OK for Docker volumes
                # The volume might still be writable from the host perspective
                pass

            # Even if we can't write, the directory exists (for Docker volumes)
            print(f"✅ Directory exists: {path}")
            return True
        else:
            print(f"⚠️  Directory creation failed: {path}")
            return False

    except PermissionError as pe:
        print(f"⚠️  Permission denied creating {path}: {pe}")
        print(f"💡 This is normal for Docker volumes - functionality may still work")
        # For Docker volumes, permission denied might not be fatal
        if os.path.exists(path):
            print(f"✅ Directory exists despite permission error: {path}")
            return True
        return False
    except Exception as e:
        print(f"❌ Failed to create directory {path}: {e}")
        return False

def generate_url(endpoint, **kwargs):
    """
    Generate URL based on configuration setting.
    
    Args:
        endpoint (str): Flask endpoint name
        **kwargs: Arguments for url_for
        
    Returns:
        str: Relative path or full URL based on RETURN_FULL_URLS setting
    """
    if RETURN_FULL_URLS:
        return url_for(endpoint, _external=True, **kwargs)
    else:
        return url_for(endpoint, _external=False, **kwargs)

def initialize_directories():
    """Initialize all required directories with proper error handling"""
    print("📁 Initializing directory structure...")
    
    required_dirs = [
        UPLOAD_FOLDER,
        GENERATED_FOLDER,
        os.path.join(UPLOAD_FOLDER, 'main'),
        os.path.join(UPLOAD_FOLDER, 'watermark'), 
        os.path.join(UPLOAD_FOLDER, 'background'),
        'output'  # For the generator's output
    ]
    
    success_count = 0
    for dir_path in required_dirs:
        if safe_makedirs(dir_path):
            success_count += 1
        else:
            print(f"⚠️  Directory {dir_path} may not be writable - uploads may fail")
    
    print(f"📊 Directory initialization: {success_count}/{len(required_dirs)} successful")
    
    if success_count < len(required_dirs):
        print("⚠️  Some directories could not be created or are not writable")
        print("💡 The API will continue but file uploads may fail")
        print("💡 Check Docker permissions and volume mounts")
    
    return success_count == len(required_dirs)

# Initialize directories at startup
directories_ok = initialize_directories()

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

def safe_file_operation(operation, filepath, *args, **kwargs):
    """
    Safely perform file operations with better error handling for Docker volumes.

    Args:
        operation (callable): File operation to perform (e.g., file.save)
        filepath (str): Target file path
        *args, **kwargs: Arguments for the operation

    Returns:
        tuple: (success: bool, error_message: str)
    """
    try:
        # For Docker volumes, permission checks might not work as expected
        # Try the operation first, then verify
        operation(filepath, *args, **kwargs)

        # Verify file was created
        if os.path.exists(filepath):
            # Try to check if readable, but don't fail if we can't
            try:
                if os.access(filepath, os.R_OK):
                    return True, None
                else:
                    # File exists but we can't check permissions - might still work
                    return True, None
            except (OSError, PermissionError):
                # Permission check failed, but file exists - might still work
                return True, None
        else:
            return False, f"File not created: {filepath}"

    except PermissionError as pe:
        return False, f"Permission denied: {pe}"
    except Exception as e:
        return False, f"Operation failed: {e}"

@app.route('/')
def index():
    """API documentation endpoint with system status"""
    return jsonify({
        'name': 'Social Image Generator API',
        'version': '2.0',
        'description': 'Generate custom social media images with uploaded content',
        'status': {
            'directories_initialized': directories_ok,
            'upload_ready': os.access(app.config['UPLOAD_FOLDER'], os.W_OK) if os.path.exists(app.config['UPLOAD_FOLDER']) else False,
            'generation_ready': os.access(app.config['GENERATED_FOLDER'], os.W_OK) if os.path.exists(app.config['GENERATED_FOLDER']) else False
        },
        'endpoints': {
            'POST /upload/main': 'Upload main image',
            'POST /upload/watermark': 'Upload watermark/blueprint image',
            'POST /upload/background': 'Upload custom background image',
            'POST /generate': 'Generate social media image',
            'POST /generate_text': 'Generate text-based layouts',
            'POST /generate_all_text': 'Generate all text layouts',
            'GET /text_layout_info': 'Text layout documentation',
            'GET /health': 'Health check',
            'GET /files': 'List uploaded files'
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
    """Health check endpoint with comprehensive system status"""
    try:
        # Check directory permissions
        upload_ready = os.access(app.config['UPLOAD_FOLDER'], os.W_OK) if os.path.exists(app.config['UPLOAD_FOLDER']) else False
        generation_ready = os.access(app.config['GENERATED_FOLDER'], os.W_OK) if os.path.exists(app.config['GENERATED_FOLDER']) else False
        
        # Check disk space
        try:
            statvfs = os.statvfs('.')
            free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
            total_space_gb = (statvfs.f_frsize * statvfs.f_blocks) / (1024**3)
            used_space_gb = total_space_gb - free_space_gb
        except Exception:
            free_space_gb = None
            total_space_gb = None
            used_space_gb = None

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0',
            'system': {
                'python_version': sys.version,
                'platform': sys.platform,
                'upload_ready': upload_ready,
                'generation_ready': generation_ready,
                'upload_limit_mb': app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
            },
            'storage': {
                'free_space_gb': round(free_space_gb, 2) if free_space_gb else None,
                'total_space_gb': round(total_space_gb, 2) if total_space_gb else None,
                'used_space_gb': round(used_space_gb, 2) if used_space_gb else None
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/config', methods=['GET', 'POST'])
def manage_config():
    """Manage API configuration settings"""
    global RETURN_FULL_URLS
    
    if request.method == 'GET':
        return jsonify({
            'return_full_urls': RETURN_FULL_URLS,
            'description': 'When True, returns full URLs. When False, returns relative paths.',
            'example': {
                'full_urls': 'http://localhost:5000/generated/filename.png',
                'relative_paths': '/generated/filename.png'
            }
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            if 'return_full_urls' in data:
                RETURN_FULL_URLS = bool(data['return_full_urls'])
                return jsonify({
                    'success': True,
                    'message': f'Configuration updated: return_full_urls = {RETURN_FULL_URLS}',
                    'return_full_urls': RETURN_FULL_URLS
                })
            else:
                return jsonify({'error': 'Missing return_full_urls parameter'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Failed to update configuration: {str(e)}'}), 500

@app.route('/upload/main', methods=['POST'])
def upload_main_image():
    """Upload main image endpoint with robust error handling"""
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

        # Check if target directory exists and is writable
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'main')
        if not os.path.exists(target_dir):
            if not safe_makedirs(target_dir):
                return jsonify({'error': 'Upload directory not available'}), 500
        
        if not os.access(target_dir, os.W_OK):
            return jsonify({'error': 'Upload directory not writable'}), 500

        # Save file with error handling
        success, error_msg = safe_file_operation(file.save, filepath)
        if not success:
            return jsonify({'error': f'File upload failed: {error_msg}'}), 500

        # Generate URL
        file_url = generate_url('uploaded_file', folder='main', filename=filename)

        return jsonify({
            'success': True,
            'message': 'Main image uploaded successfully',
            'filename': filename,
            'url': file_url,
            'size': os.path.getsize(filepath),
            'upload_time': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Upload main image error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/upload/watermark', methods=['POST'])
def upload_watermark_image():
    """Upload watermark/blueprint image endpoint with robust error handling"""
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

        # Check if target directory exists and is writable
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark')
        if not os.path.exists(target_dir):
            if not safe_makedirs(target_dir):
                return jsonify({'error': 'Upload directory not available'}), 500
        
        if not os.access(target_dir, os.W_OK):
            return jsonify({'error': 'Upload directory not writable'}), 500

        # Save file with error handling
        success, error_msg = safe_file_operation(file.save, filepath)
        if not success:
            return jsonify({'error': f'File upload failed: {error_msg}'}), 500

        # Generate URL
        file_url = generate_url('uploaded_file', folder='watermark', filename=filename)

        return jsonify({
            'success': True,
            'message': 'Watermark image uploaded successfully',
            'filename': filename,
            'url': file_url,
            'size': os.path.getsize(filepath),
            'upload_time': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Upload watermark image error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/upload/background', methods=['POST'])
def upload_background_image():
    """Upload custom background image endpoint with robust error handling"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP'}), 400

        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'background')
        
        # Ensure target directory exists and is writable
        if not os.path.exists(target_dir):
            if not safe_makedirs(target_dir):
                return jsonify({'error': 'Upload directory not available'}), 500
        
        if not os.access(target_dir, os.W_OK):
            return jsonify({'error': 'Upload directory not writable'}), 500
        
        # Generate unique filename
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(target_dir, filename)

        # Save file with error handling
        success, error_msg = safe_file_operation(file.save, filepath)
        if not success:
            return jsonify({'error': f'File upload failed: {error_msg}'}), 500

        # Generate URL
        filename = os.path.basename(filepath)
        file_url = generate_url('uploaded_file', folder='background', filename=filename)

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
        print(f"Upload background image error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    """Serve uploaded files with enhanced error handling"""
    if folder not in ['main', 'watermark', 'background']:
        return jsonify({'error': 'Invalid folder'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    if not os.access(filepath, os.R_OK):
        return jsonify({'error': 'File not readable'}), 403

    try:
        return send_file(filepath)
    except Exception as e:
        print(f"Error serving file {filepath}: {str(e)}")
        return jsonify({'error': 'Failed to serve file'}), 500

@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate social media image endpoint with comprehensive error handling"""
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
        watermark_position = data.get('watermark_position', 'bottom-right')

        # Validate required fields
        if not headline:
            return jsonify({'error': 'Headline is required'}), 400

        # Validate background color format
        if not isinstance(background_color, list) or len(background_color) != 3:
            return jsonify({'error': 'background_color must be an RGB array [r, g, b]'}), 400

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

        # Handle image URLs with better error handling
        if main_image_url:
            main_filename = f"main_{uuid.uuid4().hex[:8]}.png"
            main_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'main', main_filename)

            try:
                import requests
                response = requests.get(main_image_url, timeout=10)
                response.raise_for_status()

                # Verify it's actually an image
                try:
                    test_image = Image.open(io.BytesIO(response.content))
                    test_image.verify()
                except Exception:
                    return jsonify({'error': 'Main image URL does not contain a valid image'}), 400

                with open(main_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['main_image_path'] = main_filepath

            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Failed to download main image: {str(e)}'}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to process main image: {str(e)}'}), 400

        if watermark_image_url:
            watermark_filename = f"watermark_{uuid.uuid4().hex[:8]}.png"
            watermark_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark', watermark_filename)

            try:
                import requests
                response = requests.get(watermark_image_url, timeout=10)
                response.raise_for_status()

                # Verify it's actually an image
                try:
                    test_image = Image.open(io.BytesIO(response.content))
                    test_image.verify()
                except Exception:
                    return jsonify({'error': 'Watermark image URL does not contain a valid image'}), 400

                with open(watermark_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['blueprint_image_path'] = watermark_filepath

            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Failed to download watermark image: {str(e)}'}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to process watermark image: {str(e)}'}), 400

        if background_image_url:
            background_filename = f"background_{uuid.uuid4().hex[:8]}.png"
            background_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'background', background_filename)

            try:
                import requests
                response = requests.get(background_image_url, timeout=10)
                response.raise_for_status()

                # Verify it's actually an image
                try:
                    test_image = Image.open(io.BytesIO(response.content))
                    test_image.verify()
                except Exception:
                    return jsonify({'error': 'Background image URL does not contain a valid image'}), 400

                with open(background_filepath, 'wb') as f:
                    f.write(response.content)

                config['custom_images']['background_image_path'] = background_filepath

            except requests.exceptions.RequestException as e:
                return jsonify({'error': f'Failed to download background image: {str(e)}'}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to process background image: {str(e)}'}), 400

        # Ensure generated directory is available
        if not os.path.exists(app.config['GENERATED_FOLDER']):
            if not safe_makedirs(app.config['GENERATED_FOLDER']):
                return jsonify({'error': 'Generated directory not available'}), 500

        if not os.access(app.config['GENERATED_FOLDER'], os.W_OK):
            return jsonify({'error': 'Generated directory not writable'}), 500

        # Create temporary config file
        config_filename = f"temp_config_{uuid.uuid4().hex[:8]}.json"
        config_filepath = os.path.join(app.config['GENERATED_FOLDER'], config_filename)

        try:
            with open(config_filepath, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            return jsonify({'error': f'Failed to create config file: {str(e)}'}), 500

        # Generate image
        print("🔄 Generating enhanced social media image...")
        try:
            generator = EnhancedSocialImageGenerator(config_filepath)
            img = generator.generate_enhanced_hero_layout(headline, subheadline, brand)
        except Exception as e:
            # Clean up temp config on generator error
            try:
                os.remove(config_filepath)
            except:
                pass
            print(f"Generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Image generation failed: {str(e)}'}), 500

        # Save generated image
        output_filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        output_filepath = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        
        try:
            img.save(output_filepath, 'PNG')
        except Exception as e:
            # Clean up temp config on save error
            try:
                os.remove(config_filepath)
            except:
                pass
            return jsonify({'error': f'Failed to save generated image: {str(e)}'}), 500

        # Generate download URL
        download_url = generate_url('generated_file', filename=output_filename)

        # Clean up temp config
        try:
            os.remove(config_filepath)
        except Exception as e:
            print(f"Warning: Could not remove temp config {config_filepath}: {e}")

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
                'watermark_position': watermark_position,
                'main_image_used': bool(main_image_url),
                'watermark_image_used': bool(watermark_image_url),
                'background_image_used': bool(background_image_url)
            }
        })

    except Exception as e:
        print(f"Generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/generated/<filename>')
def generated_file(filename):
    """Serve generated image files with enhanced error handling"""
    filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Generated file not found'}), 404

    if not os.access(filepath, os.R_OK):
        return jsonify({'error': 'Generated file not readable'}), 403

    try:
        return send_file(filepath, mimetype='image/png')
    except Exception as e:
        print(f"Error serving generated file {filepath}: {str(e)}")
        return jsonify({'error': 'Failed to serve generated file'}), 500

@app.route('/files')
def list_files():
    """List all uploaded files for debugging with enhanced error handling"""
    try:
        file_info = {}
        
        # List main images
        main_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'main')
        if os.path.exists(main_dir):
            file_info['main_images'] = os.listdir(main_dir)
            file_info['total_main'] = len(file_info['main_images'])
        else:
            file_info['main_images'] = []
            file_info['total_main'] = 0
        
        # List watermark images
        watermark_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'watermark')
        if os.path.exists(watermark_dir):
            file_info['watermark_images'] = os.listdir(watermark_dir)
            file_info['total_watermark'] = len(file_info['watermark_images'])
        else:
            file_info['watermark_images'] = []
            file_info['total_watermark'] = 0
        
        # List background images
        background_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'background')
        if os.path.exists(background_dir):
            file_info['background_images'] = os.listdir(background_dir)
            file_info['total_background'] = len(file_info['background_images'])
        else:
            file_info['background_images'] = []
            file_info['total_background'] = 0
        
        # List generated images
        generated_dir = app.config['GENERATED_FOLDER']
        if os.path.exists(generated_dir):
            file_info['generated_images'] = os.listdir(generated_dir)
            file_info['total_generated'] = len(file_info['generated_images'])
        else:
            file_info['generated_images'] = []
            file_info['total_generated'] = 0

        return jsonify(file_info)

    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

@app.route('/generate_text', methods=['POST'])
def generate_text_layout():
    """Generate text-based social media image layouts with robust error handling"""
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
        
        # Validate content based on layout type
        if layout_type == 'quote' and not content.get('quote'):
            return jsonify({'error': 'Quote layout requires "quote" field in content'}), 400
        elif layout_type == 'article' and (not content.get('title') or not content.get('body')):
            return jsonify({'error': 'Article layout requires "title" and "body" fields in content'}), 400
        elif layout_type == 'announcement' and (not content.get('title') or not content.get('description')):
            return jsonify({'error': 'Announcement layout requires "title" and "description" fields in content'}), 400
        elif layout_type == 'list' and (not content.get('title') or not content.get('items')):
            return jsonify({'error': 'List layout requires "title" and "items" fields in content'}), 400
        elif layout_type == 'testimonial' and (not content.get('quote') or not content.get('person_name')):
            return jsonify({'error': 'Testimonial layout requires "quote" and "person_name" fields in content'}), 400
        
        # Load configuration
        config_path = data.get('config', 'config/text_layouts_config.json')
        if not os.path.exists(config_path):
            config_path = None  # Use default config
        
        # Ensure generated directory is available
        if not os.path.exists(app.config['GENERATED_FOLDER']):
            if not safe_makedirs(app.config['GENERATED_FOLDER']):
                return jsonify({'error': 'Generated directory not available'}), 500

        if not os.access(app.config['GENERATED_FOLDER'], os.W_OK):
            return jsonify({'error': 'Generated directory not writable'}), 500
        
        # Initialize generator
        try:
            generator = EnhancedSocialImageGenerator(config_path)
        except Exception as e:
            return jsonify({'error': f'Failed to initialize generator: {str(e)}'}), 500
        
        # Generate image
        try:
            img = generator.generate_text_layout(layout_type, content)
        except Exception as e:
            print(f"Text layout generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Text layout generation failed: {str(e)}'}), 500
        
        # Save generated image
        output_filename = f"text_{layout_type}_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        
        try:
            img.save(output_path, 'PNG', quality=95)
        except Exception as e:
            return jsonify({'error': f'Failed to save generated image: {str(e)}'}), 500
        
        # Return response
        return jsonify({
            'success': True,
            'message': f'Text layout {layout_type} generated successfully',
            'layout_type': layout_type,
            'filename': output_filename,
            'download_url': generate_url('generated_file', filename=output_filename),
            'size': os.path.getsize(output_path),
            'generated_at': datetime.now().isoformat(),
            'content_used': content
        })
        
    except Exception as e:
        print(f"Generate text layout error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_all_text', methods=['POST'])
def generate_all_text_layouts():
    """Generate all text layout variations with comprehensive error handling"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        content = data.get('content', {})
        output_prefix = data.get('output_prefix', 'text_post')
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Load configuration
        config_path = data.get('config', 'config/text_layouts_config.json')
        if not os.path.exists(config_path):
            config_path = None
        
        # Ensure generated directory is available
        if not os.path.exists(app.config['GENERATED_FOLDER']):
            if not safe_makedirs(app.config['GENERATED_FOLDER']):
                return jsonify({'error': 'Generated directory not available'}), 500

        if not os.access(app.config['GENERATED_FOLDER'], os.W_OK):
            return jsonify({'error': 'Generated directory not writable'}), 500
        
        # Initialize generator
        try:
            generator = EnhancedSocialImageGenerator(config_path)
            generator.output_dir = app.config['GENERATED_FOLDER']
        except Exception as e:
            return jsonify({'error': f'Failed to initialize generator: {str(e)}'}), 500
        
        # Generate all layouts
        try:
            generator.generate_all_text_layouts(content, output_prefix)
        except Exception as e:
            print(f"Generate all text layouts error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Text layouts generation failed: {str(e)}'}), 500
        
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
                    'download_url': generate_url('generated_file', filename=filename),
                    'size': os.path.getsize(filepath),
                    'generated_at': datetime.now().isoformat()
                })
        
        if not generated_files:
            return jsonify({'error': 'No text layouts were generated successfully'}), 500
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(generated_files)} text layouts',
            'generated_files': generated_files,
            'content_used': content,
            'output_prefix': output_prefix
        })
        
    except Exception as e:
        print(f"Generate all text layouts error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(rgb):
    """Convert RGB to HSL"""
    r, g, b = [x/255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h, s, l)

def hsl_to_rgb(hsl):
    """Convert HSL to RGB"""
    h, s, l = hsl
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))

def interpolate_hsl(color1, color2, factor):
    """Interpolate between two colors in HSL space for smoother transitions"""
    hsl1 = rgb_to_hsl(color1)
    hsl2 = rgb_to_hsl(color2)

    # Handle hue wraparound
    h1, s1, l1 = hsl1
    h2, s2, l2 = hsl2

    if abs(h1 - h2) > 0.5:
        if h1 < h2:
            h1 = h1 + 1.0
        else:
            h2 = h2 + 1.0

    h = h1 + (h2 - h1) * factor
    s = s1 + (s2 - s1) * factor
    l = l1 + (l2 - l1) * factor

    # Handle hue wraparound
    if h >= 1:
        h = h - 1.0
    elif h < 0:
        h = h + 1.0

    return hsl_to_rgb((h, s, l))

def add_subtle_noise(img, intensity=0.05):
    """Add subtle noise to make gradients more interesting"""
    img_array = np.array(img)

    # Generate noise
    noise = np.random.normal(0, intensity * 255, img_array.shape)

    # Add noise to each channel
    for i in range(3):  # RGB channels
        img_array[:, :, i] = np.clip(img_array[:, :, i] + noise[:, :, i], 0, 255)

    return Image.fromarray(img_array.astype('uint8'))

def generate_color_harmony(base_color, harmony_type="complementary"):
    """Generate harmonious color combinations"""
    if isinstance(base_color, str):
        rgb = hex_to_rgb(base_color)
    else:
        rgb = tuple(base_color)

    hsl = rgb_to_hsl(rgb)
    h, s, l = hsl

    harmonies = {
        "complementary": [hsl, ((h + 0.5) % 1, hsl[1], hsl[2])],
        "triadic": [hsl, ((h + 0.33) % 1, hsl[1], hsl[2]), ((h + 0.67) % 1, hsl[1], hsl[2])],
        "analogous": [hsl, ((h + 0.083) % 1, hsl[1], hsl[2]), ((h - 0.083) % 1, hsl[1], hsl[2])],
        "split_complementary": [hsl, ((h + 0.5 + 0.083) % 1, hsl[1], hsl[2]), ((h + 0.5 - 0.083) % 1, hsl[1], hsl[2])]
    }

    if harmony_type not in harmonies:
        harmony_type = "complementary"

    hsl_colors = harmonies[harmony_type]
    rgb_colors = []

    for hsl_color in hsl_colors:
        rgb_colors.append(hsl_to_rgb(hsl_color))

    return rgb_colors

def apply_dithering(img):
    """Apply ordered dithering for smoother gradients

    This applies a subtle dithering effect to reduce color banding in gradients
    while preserving the gradient's color information.
    """
    img_array = np.array(img, dtype=np.float32)

    # Bayer 4x4 dithering matrix (normalized to -0.5 to 0.5 range for subtle effect)
    dither_matrix = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ], dtype=np.float32) / 16.0 - 0.5  # Center around 0 for bidirectional dithering

    height, width = img_array.shape[:2]
    dither_height, dither_width = dither_matrix.shape

    # Create a full-size dither pattern by tiling
    dither_pattern = np.tile(dither_matrix, (height // dither_height + 1, width // dither_width + 1))[:height, :width]

    # Apply subtle dithering (scale factor controls intensity)
    dither_strength = 3.0  # Subtle dithering to prevent banding

    # Add dither pattern to each color channel
    for channel in range(img_array.shape[2] if len(img_array.shape) > 2 else 1):
        if len(img_array.shape) > 2:
            img_array[:, :, channel] += dither_pattern * dither_strength
        else:
            img_array += dither_pattern * dither_strength

    # Clip to valid range and convert back to uint8
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)

    return Image.fromarray(img_array)

@app.route('/generate_gradient', methods=['POST'])
def generate_gradient():
    """Generate gradient image endpoint with comprehensive error handling"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Extract parameters
        width = data.get('width', 1080)
        height = data.get('height', 1350)
        colors = data.get('colors', ['#FF6B6B', '#4ECDC4'])
        gradient_type = data.get('gradient_type', 'linear')  # linear, radial, diagonal
        direction = data.get('direction', 'vertical')  # vertical, horizontal, diagonal

        # Enhanced features
        use_hsl_interpolation = data.get('use_hsl_interpolation', True)  # Better color transitions
        add_noise = data.get('add_noise', True)  # Subtle texture
        noise_intensity = data.get('noise_intensity', 0.02)  # Noise strength (0-1)
        apply_dither = data.get('apply_dither', False)  # Dithering for smoothness
        generate_harmony = data.get('generate_harmony', False)  # Auto-generate color harmony
        harmony_type = data.get('harmony_type', 'complementary')  # complementary, triadic, analogous
        quality = data.get('quality', 95)  # PNG quality (1-100)

        # Validate parameters
        if not isinstance(width, int) or not isinstance(height, int):
            return jsonify({'error': 'Width and height must be integers'}), 400

        if width < 100 or width > 4096 or height < 100 or height > 4096:
            return jsonify({'error': 'Width and height must be between 100 and 4096 pixels'}), 400

        if not isinstance(colors, list) or len(colors) < 1:
            return jsonify({'error': 'Colors must be an array with at least 1 color value'}), 400

        if gradient_type not in ['linear', 'radial', 'diagonal']:
            return jsonify({'error': 'gradient_type must be one of: linear, radial, diagonal'}), 400

        if direction not in ['vertical', 'horizontal', 'diagonal']:
            return jsonify({'error': 'direction must be one of: vertical, horizontal, diagonal'}), 400

        # Convert color strings to RGB tuples
        rgb_colors = []
        for color in colors:
            try:
                # Handle hex colors
                if isinstance(color, str) and color.startswith('#'):
                    rgb_colors.append(tuple(int(color[i:i+2], 16) for i in (1, 3, 5)))
                # Handle RGB arrays
                elif isinstance(color, list) and len(color) == 3:
                    rgb_colors.append(tuple(color))
                else:
                    return jsonify({'error': f'Invalid color format: {color}. Use hex (#RRGGBB) or RGB arrays [r,g,b]'}), 400
            except (ValueError, IndexError):
                return jsonify({'error': f'Invalid color format: {color}'}), 400

        # Generate color harmony if requested
        if generate_harmony and len(rgb_colors) >= 1:
            base_color = rgb_colors[0] if len(rgb_colors) == 1 else rgb_colors
            if len(rgb_colors) == 1:
                harmony_colors = generate_color_harmony(base_color, harmony_type)
                rgb_colors = harmony_colors
                colors = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in rgb_colors]
            else:
                # If multiple colors provided, generate harmony from the first one
                harmony_colors = generate_color_harmony(base_color, harmony_type)
                rgb_colors = harmony_colors
                colors = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b in rgb_colors]

        # Ensure we have at least 2 colors for gradient generation
        if len(rgb_colors) < 2:
            return jsonify({'error': 'At least 2 colors are required for gradient generation. Use generate_harmony=true for automatic color generation.'}), 400

        # Create gradient image
        img = Image.new('RGB', (width, height), rgb_colors[0])
        draw = ImageDraw.Draw(img)

        # Generate gradient based on type
        if gradient_type == 'linear':
            if direction == 'vertical':
                # Vertical linear gradient with enhanced interpolation
                for y in range(height):
                    ratio = y / (height - 1)
                    if len(rgb_colors) == 2:
                        if use_hsl_interpolation:
                            r, g, b = interpolate_hsl(rgb_colors[0], rgb_colors[1], ratio)
                        else:
                            r = int(rgb_colors[0][0] + (rgb_colors[1][0] - rgb_colors[0][0]) * ratio)
                            g = int(rgb_colors[0][1] + (rgb_colors[1][1] - rgb_colors[0][1]) * ratio)
                            b = int(rgb_colors[0][2] + (rgb_colors[1][2] - rgb_colors[0][2]) * ratio)
                        draw.line([(0, y), (width, y)], fill=(r, g, b))
                    else:
                        # Multi-color gradient with enhanced interpolation
                        segment_height = height / (len(rgb_colors) - 1)
                        segment_idx = int(y / segment_height)
                        if segment_idx >= len(rgb_colors) - 1:
                            segment_idx = len(rgb_colors) - 2
                        local_ratio = (y % segment_height) / segment_height

                        if use_hsl_interpolation:
                            r, g, b = interpolate_hsl(rgb_colors[segment_idx], rgb_colors[segment_idx + 1], local_ratio)
                        else:
                            r = int(rgb_colors[segment_idx][0] + (rgb_colors[segment_idx + 1][0] - rgb_colors[segment_idx][0]) * local_ratio)
                            g = int(rgb_colors[segment_idx][1] + (rgb_colors[segment_idx + 1][1] - rgb_colors[segment_idx][1]) * local_ratio)
                            b = int(rgb_colors[segment_idx][2] + (rgb_colors[segment_idx + 1][2] - rgb_colors[segment_idx][2]) * local_ratio)
                        draw.line([(0, y), (width, y)], fill=(r, g, b))

            elif direction == 'horizontal':
                # Horizontal linear gradient with enhanced interpolation
                for x in range(width):
                    ratio = x / (width - 1)
                    if len(rgb_colors) == 2:
                        if use_hsl_interpolation:
                            r, g, b = interpolate_hsl(rgb_colors[0], rgb_colors[1], ratio)
                        else:
                            r = int(rgb_colors[0][0] + (rgb_colors[1][0] - rgb_colors[0][0]) * ratio)
                            g = int(rgb_colors[0][1] + (rgb_colors[1][1] - rgb_colors[0][1]) * ratio)
                            b = int(rgb_colors[0][2] + (rgb_colors[1][2] - rgb_colors[0][2]) * ratio)
                        draw.line([(x, 0), (x, height)], fill=(r, g, b))
                    else:
                        # Multi-color gradient with enhanced interpolation
                        segment_width = width / (len(rgb_colors) - 1)
                        segment_idx = int(x / segment_width)
                        if segment_idx >= len(rgb_colors) - 1:
                            segment_idx = len(rgb_colors) - 2
                        local_ratio = (x % segment_width) / segment_width

                        if use_hsl_interpolation:
                            r, g, b = interpolate_hsl(rgb_colors[segment_idx], rgb_colors[segment_idx + 1], local_ratio)
                        else:
                            r = int(rgb_colors[segment_idx][0] + (rgb_colors[segment_idx + 1][0] - rgb_colors[segment_idx][0]) * local_ratio)
                            g = int(rgb_colors[segment_idx][1] + (rgb_colors[segment_idx + 1][1] - rgb_colors[segment_idx][1]) * local_ratio)
                            b = int(rgb_colors[segment_idx][2] + (rgb_colors[segment_idx + 1][2] - rgb_colors[segment_idx][2]) * local_ratio)
                        draw.line([(x, 0), (x, height)], fill=(r, g, b))

            else:  # diagonal
                # Diagonal linear gradient (optimized with NumPy)
                max_dimension = max(width, height)

                # Create coordinate grids
                x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

                # Calculate ratio for each pixel
                ratio = (x_coords + y_coords) / (2 * max_dimension - 2)
                ratio = np.clip(ratio, 0.0, 1.0)

                # Create RGB array
                img_array = np.zeros((height, width, 3), dtype=np.uint8)

                if len(rgb_colors) == 2:
                    # Simple two-color gradient
                    for channel in range(3):
                        img_array[:, :, channel] = (
                            rgb_colors[0][channel] + (rgb_colors[1][channel] - rgb_colors[0][channel]) * ratio
                        ).astype(np.uint8)
                else:
                    # Multi-color gradient
                    segment_ratio = ratio * (len(rgb_colors) - 1)
                    segment_idx = np.clip(segment_ratio.astype(int), 0, len(rgb_colors) - 2)
                    local_ratio = segment_ratio - segment_idx

                    for channel in range(3):
                        # Get start and end colors for each segment
                        start_colors = np.array([rgb_colors[i][channel] for i in range(len(rgb_colors))])
                        start_color = start_colors[segment_idx]
                        end_color = start_colors[np.clip(segment_idx + 1, 0, len(rgb_colors) - 1)]

                        img_array[:, :, channel] = (
                            start_color + (end_color - start_color) * local_ratio
                        ).astype(np.uint8)

                img = Image.fromarray(img_array)

        elif gradient_type == 'radial':
            # Radial gradient (optimized with NumPy)
            center_x, center_y = width // 2, height // 2
            max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5

            # Create coordinate grids
            x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

            # Calculate distance from center for each pixel
            distance = np.sqrt((x_coords - center_x) ** 2 + (y_coords - center_y) ** 2)
            ratio = np.clip(distance / max_distance, 0.0, 1.0)

            # Create RGB array
            img_array = np.zeros((height, width, 3), dtype=np.uint8)

            if len(rgb_colors) == 2:
                # Simple two-color radial gradient
                for channel in range(3):
                    img_array[:, :, channel] = (
                        rgb_colors[0][channel] + (rgb_colors[1][channel] - rgb_colors[0][channel]) * ratio
                    ).astype(np.uint8)
            else:
                # Multi-color radial gradient
                segment_ratio = ratio * (len(rgb_colors) - 1)
                segment_idx = np.clip(segment_ratio.astype(int), 0, len(rgb_colors) - 2)
                local_ratio = segment_ratio - segment_idx

                for channel in range(3):
                    # Get start and end colors for each segment
                    start_colors = np.array([rgb_colors[i][channel] for i in range(len(rgb_colors))])
                    start_color = start_colors[segment_idx]
                    end_color = start_colors[np.clip(segment_idx + 1, 0, len(rgb_colors) - 1)]

                    img_array[:, :, channel] = (
                        start_color + (end_color - start_color) * local_ratio
                    ).astype(np.uint8)

            img = Image.fromarray(img_array)

        # Apply enhancement effects
        if add_noise:
            img = add_subtle_noise(img, noise_intensity)

        if apply_dither:
            img = apply_dithering(img)

        # Save gradient image
        output_filename = f"gradient_{uuid.uuid4().hex[:8]}.png"
        output_filepath = os.path.join(app.config['GENERATED_FOLDER'], output_filename)

        try:
            img.save(output_filepath, 'PNG', quality=quality)
        except Exception as e:
            return jsonify({'error': f'Failed to save gradient image: {str(e)}'}), 500

        # Generate download URL
        download_url = generate_url('generated_file', filename=output_filename)

        return jsonify({
            'success': True,
            'message': 'Gradient generated successfully',
            'download_url': download_url,
            'filename': output_filename,
            'size': os.path.getsize(output_filepath),
            'dimensions': {
                'width': width,
                'height': height
            },
            'gradient_config': {
                'type': gradient_type,
                'direction': direction,
                'colors': colors,
                'rgb_colors': rgb_colors
            },
            'enhancements': {
                'hsl_interpolation': use_hsl_interpolation,
                'noise_added': add_noise,
                'noise_intensity': noise_intensity if add_noise else None,
                'dither_applied': apply_dither,
                'harmony_generated': generate_harmony,
                'harmony_type': harmony_type if generate_harmony else None,
                'quality': quality
            },
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Generate gradient error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Gradient generation failed: {str(e)}'}), 500

@app.route('/gradient_info', methods=['GET'])
def gradient_info():
    """Get comprehensive information about gradient generation options"""
    return jsonify({
        'gradient_types': {
            'linear': {
                'description': 'Linear gradient with smooth color transitions',
                'directions': ['vertical', 'horizontal', 'diagonal'],
                'examples': [
                    {'direction': 'vertical', 'description': 'Top to bottom gradient'},
                    {'direction': 'horizontal', 'description': 'Left to right gradient'},
                    {'direction': 'diagonal', 'description': 'Corner to corner gradient'}
                ]
            },
            'radial': {
                'description': 'Radial gradient emanating from center',
                'directions': ['vertical'],
                'examples': [
                    {'direction': 'vertical', 'description': 'Circular gradient from center'}
                ]
            },
            'diagonal': {
                'description': 'Diagonal linear gradient',
                'directions': ['diagonal'],
                'examples': [
                    {'direction': 'diagonal', 'description': '45-degree diagonal gradient'}
                ]
            }
        },
        'color_formats': [
            'Hex colors: #FF6B6B, #4ECDC4, #45B7D1',
            'RGB arrays: [255, 107, 107], [78, 205, 196], [69, 183, 209]'
        ],
        'parameters': {
            'width': {'type': 'integer', 'min': 100, 'max': 4096, 'default': 1080},
            'height': {'type': 'integer', 'min': 100, 'max': 4096, 'default': 1350},
            'colors': {'type': 'array', 'min_items': 2, 'description': 'Array of color values'},
            'gradient_type': {'type': 'string', 'options': ['linear', 'radial', 'diagonal'], 'default': 'linear'},
            'direction': {'type': 'string', 'options': ['vertical', 'horizontal', 'diagonal'], 'default': 'vertical'}
        },
        'examples': {
            'simple_vertical': {
                'width': 1080,
                'height': 1350,
                'colors': ['#FF6B6B', '#4ECDC4'],
                'gradient_type': 'linear',
                'direction': 'vertical'
            },
            'multi_color_horizontal': {
                'width': 1080,
                'height': 1350,
                'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FDCB6E'],
                'gradient_type': 'linear',
                'direction': 'horizontal'
            },
            'radial_gradient': {
                'width': 1080,
                'height': 1080,
                'colors': ['#FFFFFF', '#FF6B6B'],
                'gradient_type': 'radial',
                'direction': 'vertical'
            },
            'diagonal_rgb': {
                'width': 1080,
                'height': 1350,
                'colors': [[255, 107, 107], [78, 205, 196]],
                'gradient_type': 'diagonal',
                'direction': 'diagonal'
            }
        },
        'usage': {
            'curl_example': 'curl -X POST -H "Content-Type: application/json" -d \'{"width": 1080, "height": 1350, "colors": ["#FF6B6B", "#4ECDC4"], "gradient_type": "linear", "direction": "vertical"}\' http://localhost:5000/generate_gradient'
        }
    })

@app.route('/text_layout_info', methods=['GET'])
def text_layout_info():
    """Get comprehensive information about available text layout types and their content structure"""
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
                    'body': 'Artificial intelligence is transforming every industry and changing how we work, communicate, and solve complex problems.',
                    'brand': 'Tech Insights'
                }
            },
            'announcement': {
                'description': 'Announcement with title, description, and call-to-action',
                'required_fields': ['title', 'description'],
                'optional_fields': ['cta', 'brand'],
                'example': {
                    'title': 'New Product Launch',
                    'description': 'Revolutionary innovation for your workflow that will transform how you work',
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
                    'items': ['Keep it simple and clean', 'Use consistent typography', 'Test with real users', 'Focus on user needs', 'Iterate based on feedback'],
                    'brand': 'Design Studio'
                }
            },
            'testimonial': {
                'description': 'Testimonial with quote and person information',
                'required_fields': ['quote', 'person_name'],
                'optional_fields': ['person_title', 'brand'],
                'example': {
                    'quote': 'This product completely transformed our business operations and increased our productivity by 300%.',
                    'person_name': 'Sarah Johnson',
                    'person_title': 'CEO, Tech Startup',
                    'brand': 'Product Reviews'
                }
            }
        },
        'features': [
            'Multi-line text wrapping with intelligent line breaks',
            'Justified text alignment for professional appearance',
            'Full Arabic/Farsi text support with proper RTL handling',
            'Customizable fonts and colors based on design system',
            'Responsive layouts that adapt to content length',
            'Professional typography with proper spacing'
        ],
        'usage': {
            'generate_single': 'POST /generate_text with layout_type and content',
            'generate_all': 'POST /generate_all_text with content and optional output_prefix',
            'content_validation': 'Each layout type validates its required fields'
        }
    })

@app.route('/generate_post', methods=['POST'])
def generate_post():
    """
    Universal endpoint for generating Instagram posts with any layout type.

    Enhanced with request/response logging for debugging.

    This is the new unified endpoint that supports all layout types via the
    LayoutEngine architecture.

    Request JSON Format:
    {
        "layout_type": "headline_promo | quote | product_showcase | ...",
        "content": {
            // Layout-specific content fields
        },
        "assets": {
            "hero_image_url": "...", // optional
            "logo_image_url": "...", // optional
            // ... other assets
        },
        "background": {
            "mode": "gradient | solid_color | image",
            "gradient": {...}, // if mode=gradient
            "color": [R,G,B], // if mode=solid_color
            "image_url": "..." // if mode=image
        },
        "options": {
            "width": 1080,
            "height": 1350,
            // ... layout-specific options
        }
    }

    Returns:
    {
        "success": true,
        "layout_type": "headline_promo",
        "generated_files": [
            {
                "slide": 1,
                "download_url": "/generated/file.png",
                "filename": "file.png",
                "width": 1080,
                "height": 1350
            }
        ],
        "generated_at": "2025-10-26T..."
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Extract parameters
        layout_type = data.get('layout_type')
        if not layout_type:
            return jsonify({
                'error': 'layout_type is required',
                'available_layouts': list(_get_available_layouts().keys())
            }), 400

        content = data.get('content', {})
        assets = data.get('assets', {})
        background = data.get('background', {})
        options = data.get('options', {})

        # LOG REQUEST for debugging
        print(f"\n{'='*60}")
        print(f"📝 GENERATE POST REQUEST")
        print(f"{'='*60}")
        print(f"Layout Type: {layout_type}")
        print(f"Content Fields: {list(content.keys())}")
        if content:
            # Log actual content values (truncated for readability)
            for key, value in content.items():
                if isinstance(value, str):
                    display_value = value[:100] + '...' if len(value) > 100 else value
                    print(f"  • {key}: {display_value}")
                else:
                    print(f"  • {key}: {value}")
        print(f"Assets: {list(assets.keys()) if assets else 'None'}")
        print(f"Background Mode: {background.get('mode', 'default')}")
        print(f"Options: {list(options.keys()) if options else 'None'}")
        print(f"{'='*60}\n")

        # Import layout system
        from src.layouts import get_layout_engine, list_available_layouts

        # Get layout engine class
        try:
            LayoutClass = get_layout_engine(layout_type)
        except ValueError as e:
            available = list_available_layouts()
            return jsonify({
                'error': f'Unknown layout type: {layout_type}',
                'available_layouts': list(available.keys()),
                'message': str(e)
            }), 400

        # Create layout instance
        try:
            layout = LayoutClass(
                content=content,
                assets=assets,
                background=background,
                options=options
            )
        except ValueError as e:
            return jsonify({
                'error': 'Invalid content or assets',
                'message': str(e),
                'layout_type': layout_type
            }), 400

        # Render layout
        try:
            images = layout.render()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Rendering failed',
                'message': str(e),
                'layout_type': layout_type
            }), 500

        # Save generated images
        generated_files = []

        for idx, img in enumerate(images):
            # Generate unique filename
            slide_num = idx + 1
            filename = f"{layout_type}_{uuid.uuid4().hex[:8]}_slide{slide_num}.png"
            filepath = os.path.join(app.config['GENERATED_FOLDER'], filename)

            try:
                # Ensure RGB mode for PNG saving
                if img.mode == 'RGBA':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                    rgb_img.save(filepath, 'PNG', quality=95)
                else:
                    img.save(filepath, 'PNG', quality=95)

                # Generate download URL
                download_url = generate_url('generated_file', filename=filename)

                generated_files.append({
                    'slide': slide_num,
                    'download_url': download_url,
                    'filename': filename,
                    'width': img.width,
                    'height': img.height,
                    'size_bytes': os.path.getsize(filepath)
                })

            except Exception as e:
                return jsonify({
                    'error': f'Failed to save image {slide_num}',
                    'message': str(e)
                }), 500

        # LOG SUCCESS
        print(f"\n{'='*60}")
        print(f"✅ GENERATION SUCCESS")
        print(f"{'='*60}")
        print(f"Layout Type: {layout_type}")
        print(f"Generated Files: {len(generated_files)}")
        for file_info in generated_files:
            print(f"  • {file_info['filename']} ({file_info['width']}x{file_info['height']}, {file_info['size_bytes']} bytes)")
        print(f"{'='*60}\n")

        return jsonify({
            'success': True,
            'layout_type': layout_type,
            'generated_files': generated_files,
            'total_slides': len(generated_files),
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Post generation failed',
            'message': str(e)
        }), 500

def _get_available_layouts():
    """Get list of available layout types (helper function)."""
    try:
        from src.layouts import list_available_layouts
        return list_available_layouts()
    except:
        return {
            'quote': {'description': 'Quote layout (legacy)'},
            'headline_promo': {'description': 'Headline promo layout (new)'}
        }

@app.route('/layouts', methods=['GET'])
def list_layouts():
    """
    List all available layout types and their schemas.

    Returns:
    {
        "layouts": {
            "quote": {...},
            "headline_promo": {...},
            ...
        },
        "count": 2
    }
    """
    try:
        layouts = _get_available_layouts()
        return jsonify({
            'layouts': layouts,
            'count': len(layouts),
            'categories': {
                'text_focused': ['quote', 'announcement', 'headline_promo'],
                'photo_text_mixed': ['split_image_text', 'product_showcase'],
                'marketing': ['headline_promo', 'product_showcase'],
                'educational': ['checklist', 'step_guide']
            }
        })
    except Exception as e:
        return jsonify({
            'error': 'Failed to list layouts',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Enhanced 404 error handler"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            'GET /',
            'GET /health',
            'POST /upload/main',
            'POST /upload/watermark',
            'POST /upload/background',
            'POST /generate_gradient',
            'POST /generate',
            'POST /generate_text',
            'POST /generate_all_text',
            'GET /gradient_info',
            'GET /text_layout_info',
            'GET /files'
        ]
    }), 404

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    max_size_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
    return jsonify({
        'error': 'File too large',
        'message': f'File size exceeds {max_size_mb}MB limit',
        'max_size_mb': max_size_mb
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    """Enhanced 500 error handler"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    # Get port from environment variable (for Coolify/Docker compatibility)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') != 'production'

    print("🚀 Social Image Generator API Server")
    print("=" * 60)

    if not directories_ok:
        print("⚠️  WARNING: Some directories could not be initialized")
        print("💡 Check Docker permissions and volume mounts")
        print("💡 Some upload functionality may not work properly")
    else:
        print("✅ All directories initialized successfully")

    print(f"📡 Starting server on http://0.0.0.0:{port}")
    print(f"📖 API Documentation: http://localhost:{port}")
    print(f"💡 Health Check: http://localhost:{port}/health")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    print()
    print("📤 Upload Endpoints:")
    print("   POST /upload/main - Upload main image")
    print("   POST /upload/watermark - Upload watermark image")
    print("   POST /upload/background - Upload background image")
    print()
    print("🎨 Generation Endpoints:")
    print("   POST /generate_post - 🆕 Universal endpoint (all layouts)")
    print("   POST /generate_gradient - Generate gradient backgrounds")
    print("   POST /generate - Generate social media image")
    print("   POST /generate_text - Generate text-based layouts")
    print("   POST /generate_all_text - Generate all text layouts")
    print()
    print("📋 Layout Information:")
    print("   GET /layouts - List all available layout types")
    print("   GET /gradient_info - Gradient generation documentation")
    print("   GET /text_layout_info - Text layout documentation")
    print()
    print("🔍 Utility Endpoints:")
    print("   GET /files - List uploaded files")
    print("   GET /uploads/<folder>/<filename> - Serve uploaded files")
    print("   GET /generated/<filename> - Serve generated files")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    app.run(debug=debug, host='0.0.0.0', port=port)