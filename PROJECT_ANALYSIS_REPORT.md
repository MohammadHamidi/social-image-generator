# Social Image Generator - Comprehensive Project Analysis Report

**Analysis Date:** 2025-11-06
**Analyst:** Claude Code
**Project:** Social Media Image Generator API

## Executive Summary

This report provides a comprehensive analysis of the Social Image Generator project, identifying security vulnerabilities, code quality issues, known bugs, and improvement opportunities. The project is a Flask-based API for generating social media images with AI-powered features.

**Overall Assessment:** The project has a solid foundation but contains **several critical and high-priority issues** that need immediate attention, particularly in security, error handling, and text rendering.

---

## 🔴 CRITICAL Issues

### 1. Path Traversal Vulnerability in File Serving Endpoints

**Severity:** CRITICAL
**Location:** `social_image_api.py:455-472` (uploaded_file endpoint)

**Issue:**
The `/uploads/<folder>/<filename>` endpoint validates the folder name but doesn't properly sanitize the filename parameter. While `secure_filename()` is used during upload, the serving endpoint doesn't validate that the requested file wasn't crafted to escape the directory.

**Vulnerable Code:**
```python
@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    if folder not in ['main', 'watermark', 'background']:
        return jsonify({'error': 'Invalid folder'}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    # No validation that filename doesn't contain path traversal sequences
```

**Attack Scenario:**
An attacker could craft a request like:
```
GET /uploads/main/../../social_image_api.py
```

**Recommendation:**
```python
from werkzeug.security import safe_join

@app.route('/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    if folder not in ['main', 'watermark', 'background']:
        return jsonify({'error': 'Invalid folder'}), 400

    # Use safe_join to prevent path traversal
    base_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    filepath = safe_join(base_path, filename)

    if not filepath:
        return jsonify({'error': 'Invalid filename'}), 400
```

---

### 2. SSRF (Server-Side Request Forgery) Vulnerability

**Severity:** CRITICAL
**Location:** `social_image_api.py:531-607`

**Issue:**
The `/generate` endpoint accepts arbitrary URLs for downloading images without validation. An attacker could:
- Access internal network resources (e.g., `http://169.254.169.254/` for cloud metadata)
- Scan internal ports
- Exfiltrate data from internal services
- Perform DoS attacks by pointing to large files

**Vulnerable Code:**
```python
if main_image_url:
    response = requests.get(main_image_url, timeout=10)  # No URL validation!
    response.raise_for_status()
```

**Recommendation:**
```python
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = ['http', 'https']
BLOCKED_IPS = [
    ipaddress.ip_network('127.0.0.0/8'),      # Localhost
    ipaddress.ip_network('10.0.0.0/8'),       # Private
    ipaddress.ip_network('172.16.0.0/12'),    # Private
    ipaddress.ip_network('192.168.0.0/16'),   # Private
    ipaddress.ip_network('169.254.0.0/16'),   # Link-local
]

def validate_url(url):
    """Validate URL to prevent SSRF attacks"""
    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ALLOWED_SCHEMES:
            raise ValueError(f"Unsupported scheme: {parsed.scheme}")

        # Resolve hostname to IP
        import socket
        hostname = parsed.hostname
        if not hostname:
            raise ValueError("No hostname in URL")

        ip = ipaddress.ip_address(socket.gethostbyname(hostname))

        # Check if IP is blocked
        for blocked_network in BLOCKED_IPS:
            if ip in blocked_network:
                raise ValueError(f"Access to {ip} is blocked")

        return True
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")

# Then use it:
if main_image_url:
    validate_url(main_image_url)  # Add this line
    response = requests.get(main_image_url, timeout=10)
```

---

### 3. Unvalidated Config Path Injection

**Severity:** HIGH
**Location:** `social_image_api.py:792-794`

**Issue:**
The `/generate_text` endpoint accepts a `config` path parameter without validation, potentially allowing path traversal to read arbitrary files.

**Vulnerable Code:**
```python
config_path = data.get('config', 'config/text_layouts_config.json')
if not os.path.exists(config_path):
    config_path = None
```

**Recommendation:**
```python
ALLOWED_CONFIGS = [
    'config/text_layouts_config.json',
    'config/platforms/instagram_post.json',
    'config/platforms/facebook_post.json',
]

config_path = data.get('config', 'config/text_layouts_config.json')
if config_path not in ALLOWED_CONFIGS:
    return jsonify({'error': 'Invalid config path'}), 400
```

---

## 🟠 HIGH Priority Issues

### 4. Number Format Issues in Multi-language Text

**Severity:** HIGH (User-facing bug)
**Location:** `src/enhanced_social_generator.py:758` (_get_font_for_text method)
**Status:** KNOWN BUG (documented in ISSUES_REPORT.md)

**Issue:**
English text displays Farsi/Eastern Arabic numerals (۰-۹) instead of Western numerals (0-9). For example, "300%" displays as "۳۰۰%".

**Root Cause:**
Font selection logic doesn't detect English text with numbers properly, causing IRANYekan fonts to convert numerals.

**Impact:**
- Breaks language consistency
- Confuses users expecting Western numerals
- Makes English content appear incorrectly

**Examples:**
- "Summer Sale 2024" renders as "Summer Sale ۲۰۲۴"
- "50%" renders as "۵۰%"

**Recommendation:**
Add explicit numeral detection in font selection:
```python
import re

def _get_font_for_text(self, text: str, font_type: str) -> ImageFont.ImageFont:
    # Detect if text contains Western numerals
    has_western_numbers = bool(re.search(r'[0-9]', text))
    is_arabic = self._is_arabic_text(text)

    # Force Latin font for English text with Western numbers
    if has_western_numbers and not is_arabic:
        return self._get_latin_font(font_type)

    # Rest of existing logic...
```

---

### 5. Text Truncation in Farsi/Arabic Content

**Severity:** HIGH (User-facing bug)
**Location:** `src/enhanced_social_generator.py:1007-1037` (_wrap_arabic_text method)
**Status:** KNOWN BUG (documented in ISSUES_REPORT.md)

**Issue:**
Long Farsi text gets cut off mid-word at line endings because the wrapping logic only breaks on spaces.

**Examples:**
- Text ending "میدهد" gets truncated to "میدهـ"

**Recommendation:**
Add character-level fallback for extremely long words:
```python
def _wrap_arabic_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    lines = []
    current_line = ""
    words = text.split()

    for word in words:
        test_line = current_line + " " + word if current_line else word
        processed_test = self._prepare_arabic_text(test_line)
        bbox = font.getbbox(processed_test)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
                current_line = word
            else:
                # Word is too long - wrap at character level
                char_lines = self._wrap_word_character_level(word, font, max_width)
                lines.extend(char_lines[:-1])
                current_line = char_lines[-1] if char_lines else word

    if current_line:
        lines.append(current_line.strip())
    return lines
```

---

### 6. Missing CORS Configuration

**Severity:** HIGH
**Location:** `social_image_api.py:28`

**Issue:**
CORS is enabled for ALL origins without restriction:
```python
CORS(app)  # Enable CORS for all routes
```

This allows any website to make requests to your API, potentially enabling:
- Cross-site request forgery (CSRF)
- Data exfiltration
- Unauthorized API usage

**Recommendation:**
```python
from flask_cors import CORS

# Configure CORS with specific origins
CORS(app, resources={
    r"/*": {
        "origins": os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})
```

---

### 7. Insufficient Input Validation

**Severity:** HIGH
**Location:** Multiple endpoints

**Issue:**
Missing validation on critical input parameters:

1. **Canvas dimensions** (`/generate` endpoint):
   - No limit on canvas_width/canvas_height
   - Could cause memory exhaustion with extremely large values

2. **Text length** (all text generation endpoints):
   - No limit on headline, subheadline, body text length
   - Could cause performance issues or DoS

3. **Array sizes** (`/generate_all_text` endpoint):
   - No limit on list items count
   - Could exhaust memory

**Recommendation:**
```python
# Add validation constants
MAX_CANVAS_SIZE = 8192
MAX_TEXT_LENGTH = 5000
MAX_LIST_ITEMS = 50

# In endpoints:
def generate_image():
    data = request.get_json()

    # Validate canvas size
    width = data.get('canvas_width', 1080)
    height = data.get('canvas_height', 1350)
    if width > MAX_CANVAS_SIZE or height > MAX_CANVAS_SIZE:
        return jsonify({'error': 'Canvas size too large'}), 400

    # Validate text length
    headline = data.get('headline', '')
    if len(headline) > MAX_TEXT_LENGTH:
        return jsonify({'error': 'Text too long'}), 400
```

---

## 🟡 MEDIUM Priority Issues

### 8. Insecure File Upload Handling

**Severity:** MEDIUM
**Location:** `social_image_api.py:305-353` (upload endpoints)

**Issues:**
1. **Weak file extension validation:** Only checks extension, not actual file content
2. **No file size validation before processing:** Could cause DoS
3. **No antivirus scanning:** Uploaded files not scanned for malware
4. **Predictable filenames:** UUID-based but timestamp included

**Current validation:**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

**Problems:**
- File extension can be spoofed (e.g., `malware.exe.png`)
- No magic byte validation
- No image content verification until after upload

**Recommendation:**
```python
from PIL import Image
import magic

def validate_image_file(file):
    """Validate that uploaded file is a legitimate image"""
    # Check file size first (before reading)
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset

    if size > MAX_FILE_SIZE:
        raise ValueError("File too large")

    # Read first chunk for magic byte check
    header = file.read(512)
    file.seek(0)

    # Verify magic bytes
    file_type = magic.from_buffer(header, mime=True)
    if file_type not in ['image/png', 'image/jpeg', 'image/gif', 'image/webp']:
        raise ValueError("Invalid image file")

    # Verify PIL can open it
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        return True
    except Exception as e:
        raise ValueError(f"Invalid image: {str(e)}")
```

---

### 9. Lack of Rate Limiting

**Severity:** MEDIUM
**Location:** All API endpoints

**Issue:**
No rate limiting on any endpoints, allowing:
- DoS attacks via rapid requests
- Resource exhaustion
- API abuse

**Recommendation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Apply to expensive endpoints
@app.route('/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_image():
    # ...
```

---

### 10. Missing Authentication/Authorization

**Severity:** MEDIUM
**Location:** All endpoints

**Issue:**
API has no authentication mechanism. Anyone can:
- Upload files
- Generate images
- List files
- Consume resources

**Recommendation:**
```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in VALID_API_KEYS:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/generate', methods=['POST'])
@require_api_key
def generate_image():
    # ...
```

---

### 11. Insufficient Error Information Security

**Severity:** MEDIUM
**Location:** Multiple endpoints

**Issue:**
Error messages expose internal paths and implementation details:
```python
return jsonify({'error': f'Upload failed: {str(e)}'}), 500
```

This leaks information like:
- File system paths
- Python stack traces
- Internal structure

**Recommendation:**
```python
import logging

logger = logging.getLogger(__name__)

# Log detailed error internally
logger.error(f"Upload failed: {str(e)}", exc_info=True)

# Return generic message to user
return jsonify({'error': 'Upload failed. Please try again.'}), 500
```

---

### 12. Docker Security Issues

**Severity:** MEDIUM
**Location:** `Dockerfile`

**Issues:**

1. **Container runs as root eventually:**
```dockerfile
# Line 96: Switches to appuser
USER appuser
```
But the app server (Flask) has no additional security restrictions.

2. **Dummy health check:**
```dockerfile
HEALTHCHECK CMD echo "healthy"
```
This doesn't actually check if the app is working.

**Recommendations:**
```dockerfile
# Better healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Add security options in docker run
# --read-only (make filesystem read-only except volumes)
# --cap-drop=ALL --cap-add=NET_BIND_SERVICE (minimal capabilities)
# --security-opt=no-new-privileges:true
```

---

## 🔵 LOW Priority Issues

### 13. Deprecated PIL Image.verify() Usage

**Severity:** LOW
**Location:** `social_image_api.py:542-543, 568-569, 594-595`

**Issue:**
Using `Image.verify()` makes the image file object unusable after:
```python
test_image = Image.open(io.BytesIO(response.content))
test_image.verify()  # File object is now unusable
```

**Recommendation:**
```python
# Verify without corrupting the file object
test_image = Image.open(io.BytesIO(response.content))
test_image.load()  # This validates the image
test_image.close()
```

---

### 14. Hardcoded Configuration Values

**Severity:** LOW
**Location:** Multiple files

**Issues:**
- Port hardcoded: `PORT=5000`
- Max file size: `16 * 1024 * 1024`
- Timeout values: `timeout=10`
- Canvas sizes hardcoded in multiple places

**Recommendation:**
Use environment variables with sensible defaults:
```python
import os

PORT = int(os.getenv('PORT', 5000))
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
```

---

### 15. Incomplete TODO Items

**Severity:** LOW
**Location:** `src/layouts/base.py`

**Issue:**
Found TODO comment indicating unimplemented feature:
```python
# TODO: Implement slide number rendering
```

---

### 16. Missing Type Hints

**Severity:** LOW
**Location:** Throughout codebase

**Issue:**
Inconsistent use of type hints. Some functions have them, many don't:
```python
def generate_unique_filename(original_filename):  # No type hints
    # ...
```

**Recommendation:**
Add type hints for better code quality:
```python
def generate_unique_filename(original_filename: str) -> str:
    # ...
```

---

### 17. No Logging Configuration

**Severity:** LOW
**Location:** `social_image_api.py`

**Issue:**
Using print() statements instead of proper logging:
```python
print(f"Upload main image error: {str(e)}")
```

**Recommendation:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.error(f"Upload main image error: {str(e)}")
```

---

## 📊 Code Quality Issues

### 18. Long Functions and Code Complexity

**Location:** `social_image_api.py:474-689` (generate_image function is 215 lines)

**Issue:**
Very long functions that do too many things, violating Single Responsibility Principle.

**Recommendation:**
Refactor into smaller functions:
```python
def generate_image():
    data = validate_generate_request()
    config = build_config(data)
    image_paths = download_images(data)
    update_config_with_images(config, image_paths)
    output_path = generate_and_save_image(config, data)
    return build_response(output_path, data)
```

---

### 19. Duplicate Code

**Issue:**
Similar code repeated in upload_main_image, upload_watermark_image, and upload_background_image endpoints (80% identical).

**Recommendation:**
Create a generic upload handler:
```python
def handle_upload(folder_name: str):
    """Generic upload handler for all image types"""
    # Common upload logic here
```

---

### 20. Missing Unit Tests

**Issue:**
No unit tests found. Only integration/deployment tests exist:
- `test_production_deployment.py`
- `test_upload_flow.py`

**Recommendation:**
Add pytest-based unit tests:
```python
# tests/test_api.py
def test_allowed_file():
    assert allowed_file('image.png') == True
    assert allowed_file('image.jpg') == True
    assert allowed_file('script.exe') == False
    assert allowed_file('noextension') == False
```

---

## 🔍 Dependency and Configuration Issues

### 21. Unversioned Dependencies

**Severity:** LOW
**Location:** `requirements.txt`

**Issue:**
Dependencies use minimum version (`>=`) instead of pinned versions:
```txt
Pillow>=10.0.0
Flask>=3.0.0
```

This can lead to:
- Inconsistent builds
- Breaking changes from upstream
- Security vulnerabilities in new versions

**Recommendation:**
```txt
# Use exact versions or compatible ranges
Pillow==10.4.0
Flask==3.0.3
Flask-CORS==4.0.1
```

---

### 22. Missing .env File

**Issue:**
`.env` file is in `.gitignore` but required for configuration. No .env.example provided (only .env.coolify).

**Recommendation:**
Create comprehensive `.env.example` with all options documented.

---

## 🎯 Best Practice Improvements

### 23. API Versioning

Add API versioning for future compatibility:
```python
@app.route('/api/v1/generate', methods=['POST'])
```

---

### 24. Request ID Tracking

Add request IDs for debugging:
```python
import uuid
from flask import g

@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())

@app.after_request
def after_request(response):
    response.headers['X-Request-ID'] = g.request_id
    return response
```

---

### 25. Health Check Enhancement

**Current:** `HEALTHCHECK CMD echo "healthy"`

**Improved:**
```python
@app.route('/health')
def health_check():
    checks = {
        'api': 'ok',
        'disk_space': check_disk_space(),
        'dependencies': check_dependencies(),
        'upload_dir': check_upload_writable()
    }

    all_ok = all(v == 'ok' for v in checks.values())
    status_code = 200 if all_ok else 503

    return jsonify(checks), status_code
```

---

## 📈 Performance Issues

### 26. No Image Caching

**Issue:**
Every request downloads and processes images without caching, causing:
- Slow response times
- Redundant processing
- High bandwidth usage

**Recommendation:**
Implement caching with Redis or filesystem:
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_processed_image(url_hash):
    # Cache processed images
    pass
```

---

### 27. Synchronous Image Processing

**Issue:**
All image generation is synchronous, blocking the API during generation.

**Recommendation:**
Use async processing with Celery or background workers:
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def generate_image_async(config):
    # Generate image in background
    pass

@app.route('/generate_async', methods=['POST'])
def generate_async():
    task = generate_image_async.delay(config)
    return jsonify({'task_id': task.id})
```

---

## 🔐 Security Recommendations Summary

### Immediate Actions Required:

1. ✅ **Fix path traversal vulnerability** in file serving
2. ✅ **Add SSRF protection** for URL downloads
3. ✅ **Validate config paths** to prevent injection
4. ✅ **Configure CORS** with allowed origins
5. ✅ **Add input validation** on all parameters
6. ✅ **Implement rate limiting** on all endpoints
7. ✅ **Add authentication** (API keys minimum)
8. ✅ **Sanitize error messages** to hide internal details

---

## 📋 Priority Matrix

| Priority | Count | Examples |
|----------|-------|----------|
| Critical | 3 | Path traversal, SSRF, Config injection |
| High | 7 | Number format bug, Text truncation, CORS |
| Medium | 9 | File upload validation, Rate limiting, Auth |
| Low | 8 | Type hints, Logging, TODOs |

---

## 🎬 Recommended Action Plan

### Phase 1: Security Fixes (Week 1)
1. Fix path traversal vulnerability
2. Add SSRF protection
3. Fix config path injection
4. Configure CORS properly
5. Add input validation

### Phase 2: Critical Bugs (Week 2)
1. Fix number format issues
2. Fix text truncation
3. Improve font selection logic

### Phase 3: Security Hardening (Week 3)
1. Add authentication
2. Implement rate limiting
3. Improve file upload validation
4. Add proper logging
5. Sanitize error messages

### Phase 4: Code Quality (Week 4)
1. Refactor long functions
2. Remove duplicate code
3. Add unit tests
4. Add type hints
5. Pin dependency versions

---

## 📚 Additional Resources

### Security Testing Tools:
- **OWASP ZAP**: For API security testing
- **Bandit**: Python security linter
- **Safety**: Check dependencies for known vulnerabilities

### Commands to Run:
```bash
# Check for known vulnerabilities
pip install safety
safety check -r requirements.txt

# Run security linter
pip install bandit
bandit -r . -ll

# Check code style
pip install pylint
pylint social_image_api.py
```

---

## 🏁 Conclusion

The Social Image Generator project has a solid foundation with good features, but contains **several critical security vulnerabilities** that need immediate attention. The known text rendering bugs are well-documented and have clear solutions.

**Overall Risk Level:** 🔴 **HIGH**

**Key Concerns:**
1. SSRF vulnerability could allow internal network access
2. Path traversal could expose sensitive files
3. No authentication allows unlimited API abuse
4. Text rendering bugs affect user experience

**Positive Aspects:**
- Good documentation
- Uses secure_filename for uploads
- Docker containerization
- Multi-language support
- Well-structured codebase

**Recommendation:** Address critical and high-priority security issues immediately before deploying to production. Implement authentication and rate limiting as minimum viable security measures.

---

*End of Report*
