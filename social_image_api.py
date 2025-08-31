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
from PIL import Image
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
        
        # Verify it exists and is writable
        if os.path.exists(path) and os.access(path, os.W_OK):
            print(f"✅ Directory ready: {path}")
            return True
        else:
            print(f"⚠️  Directory exists but not writable: {path}")
            
            # Try to fix permissions
            try:
                current_stat = os.stat(path)
                # Add write permission for owner
                os.chmod(path, current_stat.st_mode | stat.S_IWUSR)
                
                if os.access(path, os.W_OK):
                    print(f"✅ Fixed permissions for: {path}")
                    return True
                else:
                    print(f"❌ Could not fix permissions for: {path}")
                    return False
            except Exception as perm_error:
                print(f"❌ Permission fix failed for {path}: {perm_error}")
                return False
                
    except PermissionError as pe:
        print(f"❌ Permission denied creating {path}: {pe}")
        print(f"💡 Hint: Check Docker user permissions and volume mounts")
        return False
    except Exception as e:
        print(f"❌ Failed to create directory {path}: {e}")
        return False

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
    Safely perform file operations with better error handling.
    
    Args:
        operation (callable): File operation to perform (e.g., file.save)
        filepath (str): Target file path
        *args, **kwargs: Arguments for the operation
    
    Returns:
        tuple: (success: bool, error_message: str)
    """
    try:
        # Check if directory is writable
        directory = os.path.dirname(filepath)
        if not os.access(directory, os.W_OK):
            return False, f"Directory not writable: {directory}"
        
        # Perform the operation
        operation(filepath, *args, **kwargs)
        
        # Verify file was created and is readable
        if os.path.exists(filepath) and os.access(filepath, os.R_OK):
            return True, None
        else:
            return False, f"File not created or not readable: {filepath}"
            
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
    """Enhanced health check endpoint with detailed directory status"""
    # Check directory status
    dir_status = {}
    directories_to_check = [
        'uploads', 
        'uploads/main', 
        'uploads/watermark', 
        'uploads/background', 
        'generated',
        'output'
    ]
    
    for dir_name in directories_to_check:
        dir_path = dir_name
        dir_status[dir_name] = {
            'exists': os.path.exists(dir_path),
            'writable': os.access(dir_path, os.W_OK) if os.path.exists(dir_path) else False,
            'readable': os.access(dir_path, os.R_OK) if os.path.exists(dir_path) else False
        }
    
    # Check if generator can be imported
    generator_import_ok = True
    generator_error = None
    try:
        from enhanced_social_generator import EnhancedSocialImageGenerator
        generator = EnhancedSocialImageGenerator()
    except Exception as e:
        generator_import_ok = False
        generator_error = str(e)
    
    # Overall health status
    directories_healthy = all(
        status['exists'] and status['writable'] 
        for dir_name, status in dir_status.items() 
        if dir_name != 'output'  # output directory is optional
    )
    
    overall_status = 'healthy' if directories_healthy and generator_import_ok else 'degraded'
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0',
        'directories': dir_status,
        'permissions_ok': directories_healthy,
        'generator': {
            'import_ok': generator_import_ok,
            'error': generator_error
        },
        'system_info': {
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'upload_limit_mb': app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        }
    })

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
        download_url = url_for('generated_file', filename=output_filename, _external=True)

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
            'download_url': url_for('generated_file', filename=output_filename, _external=True),
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
                    'download_url': url_for('generated_file', filename=filename, _external=True),
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
            'POST /generate',
            'POST /generate_text',
            'POST /generate_all_text',
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
    print("🚀 Social Image Generator API Server")
    print("=" * 60)
    
    if not directories_ok:
        print("⚠️  WARNING: Some directories could not be initialized")
        print("💡 Check Docker permissions and volume mounts")
        print("💡 Some upload functionality may not work properly")
    else:
        print("✅ All directories initialized successfully")
    
    print(f"📡 Starting server on http://localhost:5000")
    print(f"📖 API Documentation: http://localhost:5000")
    print(f"💡 Health Check: http://localhost:5000/health")
    print()
    print("📤 Upload Endpoints:")
    print("   POST /upload/main - Upload main image")
    print("   POST /upload/watermark - Upload watermark image")
    print("   POST /upload/background - Upload background image")
    print()
    print("🎨 Generation Endpoints:")
    print("   POST /generate - Generate social media image")
    print("   POST /generate_text - Generate text-based layouts")
    print("   POST /generate_all_text - Generate all text layouts")
    print("   GET /text_layout_info - Text layout documentation")
    print()
    print("🔍 Utility Endpoints:")
    print("   GET /files - List uploaded files")
    print("   GET /uploads/<folder>/<filename> - Serve uploaded files")
    print("   GET /generated/<filename> - Serve generated files")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)