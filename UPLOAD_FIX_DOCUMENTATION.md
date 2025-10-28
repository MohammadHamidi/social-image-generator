# Upload and Image Loading Fix Documentation

## Problem Summary

The image upload and loading flow had critical issues that prevented uploaded images from being used in post generation:

### Issues Identified

1. **Path Mismatch**: Upload endpoints returned Flask URL paths (`/uploads/main/file.png`) but the AssetManager expected filesystem paths (`uploads/main/file.png` or `/app/uploads/main/file.png`)

2. **Incomplete Path Resolution**: The AssetManager's path resolution logic didn't handle all edge cases for Docker and local environments

3. **Missing Method**: The `fit_to_bounds()` method was referenced in layouts but didn't exist in AssetManager

## Fixes Applied

### 1. Enhanced Upload Response

**File**: `social_image_api.py`

All upload endpoints (`/upload/main`, `/upload/watermark`, `/upload/background`) now return **both**:
- `url`: Flask route URL for serving the file via HTTP (e.g., `/uploads/main/file.png`)
- `path`: Filesystem path for direct loading (e.g., `uploads/main/20250128_123456_abc123.png`)

**Example Response:**
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "20250128_123456_abc123.png",
  "url": "/uploads/main/20250128_123456_abc123.png",
  "path": "uploads/main/20250128_123456_abc123.png",
  "size": 45678,
  "upload_time": "2025-01-28T12:34:56.789"
}
```

### 2. Improved Path Resolution

**File**: `src/asset_manager.py` - `_resolve_path()` method

Enhanced to try multiple path variations:
1. Original path (as-is)
2. Flask URL paths → Docker absolute (`/uploads/...` → `/app/uploads/...`)
3. Docker absolute → Relative (`/app/uploads/...` → `uploads/...`)
4. Absolute → Relative (any `/path` → `path`)
5. Relative → CWD-based (`path` → `/full/path/to/path`)

**Benefits:**
- Works in Docker containers
- Works in local development
- Works with both URL paths and filesystem paths
- Comprehensive logging for debugging

### 3. Added Missing Method

**File**: `src/asset_manager.py`

Added `fit_to_bounds()` method as an alias to `resize_to_fit()` for compatibility with layout code.

## Usage Guide

### Correct Usage (Recommended)

When uploading images and using them in generation, use the `path` field:

```python
import requests

# 1. Upload image
with open('my_image.png', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/upload/main',
        files={'file': f}
    )

upload_data = response.json()

# 2. Use the 'path' field for generation
payload = {
    "layout_type": "headline_promo",
    "content": {
        "headline": "My Headline"
    },
    "assets": {
        # ✅ CORRECT: Use 'path' field
        "hero_image_url": upload_data['path']
    }
}

response = requests.post(
    'http://localhost:5000/generate_post',
    json=payload
)
```

### Also Works (Thanks to Enhanced Path Resolution)

The improved path resolution also handles URL paths:

```python
# ✅ ALSO WORKS: Using 'url' field
payload = {
    "layout_type": "headline_promo",
    "content": {
        "headline": "My Headline"
    },
    "assets": {
        # This works too (path resolution will handle it)
        "hero_image_url": upload_data['url']
    }
}
```

## Testing the Fix

Run the test script to verify everything works:

```bash
# Make sure API is running first
python social_image_api.py

# In another terminal, run the test
python test_upload_flow.py
```

The test script will:
1. Create test images
2. Upload them to the API
3. Generate posts using both `path` and `url` fields
4. Report success/failure

## API Endpoints Reference

### Upload Endpoints

#### POST /upload/main
Upload main/hero image for posts

**Request:**
```bash
curl -X POST http://localhost:5000/upload/main \
  -F "file=@my_image.png"
```

**Response:**
```json
{
  "success": true,
  "message": "Main image uploaded successfully",
  "filename": "20250128_123456_abc123.png",
  "url": "/uploads/main/20250128_123456_abc123.png",
  "path": "uploads/main/20250128_123456_abc123.png",
  "size": 45678,
  "upload_time": "2025-01-28T12:34:56.789"
}
```

#### POST /upload/watermark
Upload logo/watermark image

**Request:**
```bash
curl -X POST http://localhost:5000/upload/watermark \
  -F "file=@logo.png"
```

**Response:** Same structure as main upload

#### POST /upload/background
Upload custom background image

**Request:**
```bash
curl -X POST http://localhost:5000/upload/background \
  -F "file=@background.jpg"
```

**Response:** Same structure as main upload

### Generation Endpoint

#### POST /generate_post
Generate Instagram post with uploaded images

**Request:**
```bash
curl -X POST http://localhost:5000/generate_post \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "headline_promo",
    "content": {
      "headline": "Summer Sale",
      "subheadline": "Up to 50% Off"
    },
    "assets": {
      "hero_image_url": "uploads/main/20250128_123456_abc123.png",
      "watermark_url": "uploads/watermark/20250128_123457_def456.png"
    },
    "background": {
      "mode": "gradient",
      "gradient": {
        "colors": [[255, 107, 107], [253, 187, 45]],
        "direction": "vertical"
      }
    },
    "options": {
      "remove_hero_background": false,
      "remove_watermark_background": true
    }
  }'
```

## Debugging

If you encounter path issues, check the logs for:

```
✅ Path resolved (original): <path>
```

Or for variations:

```
✅ Path resolved (variation 2): /uploads/main/file.png -> uploads/main/file.png
```

If all variations fail:

```
❌ Path not found after trying 8 variations:
   1. /uploads/main/file.png
   2. /app/uploads/main/file.png
   3. uploads/main/file.png
   ... and 5 more
```

This indicates the file doesn't exist at any expected location.

## Common Issues and Solutions

### Issue: "File not found" error after upload

**Solution:** Make sure you're using the `path` field from the upload response, not constructing your own path.

### Issue: Docker path issues

**Solution:** The enhanced path resolution should handle Docker paths automatically. The system tries:
- `/app/uploads/...` (Docker absolute)
- `uploads/...` (relative)
- Current working directory variations

### Issue: Background removal not working

**Solution:** Make sure to set the background removal options:

```json
{
  "options": {
    "remove_hero_background": true,
    "bg_removal_method": "auto"
  }
}
```

## Changes Made

### Files Modified

1. **social_image_api.py**
   - Lines 337-348: Added `path` field to main upload response
   - Lines 386-397: Added `path` field to watermark upload response
   - Lines 436-449: Added `path` field to background upload response

2. **src/asset_manager.py**
   - Lines 229-289: Enhanced `_resolve_path()` method
   - Lines 454-469: Added `fit_to_bounds()` method

### Files Created

1. **test_upload_flow.py** - Comprehensive test script
2. **UPLOAD_FIX_DOCUMENTATION.md** - This documentation

## Backward Compatibility

The fix maintains backward compatibility:
- Old code using `url` field will still work (thanks to enhanced path resolution)
- New `path` field is additional, not replacing anything
- All existing API endpoints continue to work as before

## Performance Impact

- Minimal: Path resolution adds negligible overhead
- Path variations are tried in order of likelihood (fast in most cases)
- Results are cached by AssetManager for subsequent uses

## Future Improvements

Potential enhancements for the future:
1. Add path validation before returning from upload endpoints
2. Implement path normalization utility
3. Add more detailed error messages for specific path issues
4. Consider using absolute paths everywhere for consistency
