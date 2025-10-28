"""
Asset Manager - Intelligent image loading, caching, and processing

Handles:
- Loading images from URLs or local paths
- Caching for performance
- Smart cropping and resizing
- Format conversion
- Asset validation
- AI-powered background removal
"""

from typing import Optional, Dict, Tuple, Union
from PIL import Image
import requests
import os
import hashlib
import time
from io import BytesIO
from urllib.parse import urlparse
import numpy as np

# Background removal imports
try:
    from rembg import remove as rembg_remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    rembg_remove = None

# Try to import scipy for advanced image processing
try:
    from scipy import ndimage
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class AssetManager:
    """
    Manages loading, caching, and processing of image assets.

    Features:
    - Automatic URL vs. local path detection
    - In-memory and disk caching
    - Smart image processing (crop, resize, mask)
    - Error handling and retries
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize asset manager.

        Args:
            cache_dir: Directory for disk cache (default: ./cache/assets)
        """
        self.cache_dir = cache_dir or os.path.join(os.getcwd(), 'cache', 'assets')
        self._memory_cache: Dict[str, Image.Image] = {}
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist."""
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_key(self, url_or_path: str) -> str:
        """
        Generate cache key from URL or path.

        Args:
            url_or_path: Asset URL or local path

        Returns:
            MD5 hash for cache key
        """
        return hashlib.md5(url_or_path.encode()).hexdigest()

    def _is_url(self, path: str) -> bool:
        """
        Check if path is a URL.

        Args:
            path: Path to check

        Returns:
            True if path is HTTP/HTTPS URL
        """
        parsed = urlparse(path)
        return parsed.scheme in ('http', 'https')

    def load_asset(self,
                   url_or_path: str,
                   role: str = 'unknown',
                   use_cache: bool = True,
                   remove_bg: bool = False,
                   bg_removal_method: str = 'auto',
                   alpha_matting: bool = True,
                   color_tolerance: int = 30) -> Image.Image:
        """
        Load image asset from URL or local path with optional background removal.

        Args:
            url_or_path: URL or local file path
            role: Asset role (hero_image, logo, etc.) for logging
            use_cache: Whether to use cache (default: True)
            remove_bg: Whether to remove background (default: False)
            bg_removal_method: Method to use ('auto', 'edge', 'color')
            alpha_matting: Enable alpha matting for rembg
            color_tolerance: Tolerance for color threshold method

        Returns:
            PIL Image object

        Raises:
            ValueError: If asset cannot be loaded
        """
        # Generate cache key with background removal suffix if needed
        cache_key = self._get_cache_key(url_or_path)
        if remove_bg:
            cache_key += f"_nobg_{bg_removal_method}"

        # Check memory cache first
        if use_cache and cache_key in self._memory_cache:
            return self._memory_cache[cache_key].copy()

        # Check disk cache
        if use_cache:
            disk_cached = self._load_from_disk_cache(cache_key)
            if disk_cached:
                self._memory_cache[cache_key] = disk_cached
                return disk_cached.copy()

        # Load from source
        try:
            if self._is_url(url_or_path):
                image = self._load_from_url(url_or_path)
            else:
                image = self._load_from_path(url_or_path)

            # Apply background removal if requested
            if remove_bg:
                print(f"🎨 Removing background from {role} (method: {bg_removal_method})")
                image = self.remove_background(
                    image,
                    method=bg_removal_method,
                    alpha_matting=alpha_matting,
                    color_tolerance=color_tolerance
                )

            # Cache it
            if use_cache:
                self._memory_cache[cache_key] = image
                self._save_to_disk_cache(cache_key, image)

            return image.copy()

        except Exception as e:
            raise ValueError(f"Failed to load {role} asset from {url_or_path}: {str(e)}")

    def _load_from_url(self, url: str, timeout: int = 30, retries: int = 3) -> Image.Image:
        """
        Load image from URL with retry logic.

        Args:
            url: Image URL
            timeout: Request timeout in seconds
            retries: Number of retry attempts

        Returns:
            PIL Image object

        Raises:
            ValueError: If download fails after retries
        """
        last_error = None

        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=timeout, stream=True)
                response.raise_for_status()

                # Load image from bytes
                image_data = BytesIO(response.content)
                image = Image.open(image_data)

                # Convert to RGB if needed (handle RGBA, P, etc.)
                if image.mode not in ('RGB', 'RGBA'):
                    image = image.convert('RGB')

                return image

            except Exception as e:
                last_error = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

        raise ValueError(f"Failed to download image after {retries} attempts: {last_error}")

    def _load_from_path(self, path: str) -> Image.Image:
        """
        Load image from local file path with intelligent path resolution.

        Args:
            path: Local file path

        Returns:
            PIL Image object

        Raises:
            ValueError: If file doesn't exist or can't be loaded
        """
        # Try to resolve the path intelligently
        resolved_path = self._resolve_path(path)
        
        if not os.path.exists(resolved_path):
            raise ValueError(f"File not found: {path} (tried: {resolved_path})")

        try:
            image = Image.open(resolved_path)

            # Convert to RGB if needed
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGB')

            return image

        except Exception as e:
            raise ValueError(f"Failed to open image file {resolved_path}: {str(e)}")
    
    def _resolve_path(self, path: str) -> str:
        """
        Resolve path variations for Docker container and local filesystems.

        Tries multiple path variations:
        1. Original path (as-is)
        2. If starts with /uploads/, try /app/uploads/... (Docker absolute)
        3. If starts with /app/uploads/, try uploads/... (relative)
        4. If absolute path, try as relative
        5. If relative, try with current working directory

        Args:
            path: Original path (could be URL path or filesystem path)

        Returns:
            Resolved path that exists, or original path if none found
        """
        # List of path variations to try
        variations = [path]  # Try original first

        # Build all possible variations
        if path.startswith('/uploads/'):
            # Flask URL path -> convert to filesystem paths
            variations.append('/app' + path)  # Docker absolute
            variations.append(path[1:])  # Remove leading slash for relative
            variations.append(os.path.join(os.getcwd(), path[1:]))  # CWD + relative

        if path.startswith('/app/uploads/'):
            # Docker absolute -> try relative
            variations.append(path[5:])  # Remove '/app/' prefix
            variations.append(os.path.join(os.getcwd(), path[5:]))

        if path.startswith('/') and not path.startswith('/app/'):
            # Other absolute paths -> try relative
            variations.append(path.lstrip('/'))
            variations.append(os.path.join(os.getcwd(), path.lstrip('/')))

        if not path.startswith('/'):
            # Relative path -> try with CWD
            variations.append(os.path.join(os.getcwd(), path))
            variations.append('/' + path)  # Try as absolute
            variations.append('/app/' + path)  # Try with Docker prefix

        # Try each variation
        for idx, variation in enumerate(variations):
            if os.path.exists(variation):
                if idx == 0:
                    print(f"✅ Path resolved (original): {variation}")
                else:
                    print(f"✅ Path resolved (variation {idx}): {path} -> {variation}")
                return variation

        # No variation worked
        print(f"❌ Path not found after trying {len(variations)} variations:")
        for i, v in enumerate(variations[:5]):  # Show first 5 attempts
            print(f"   {i+1}. {v}")
        if len(variations) > 5:
            print(f"   ... and {len(variations) - 5} more")

        print(f"⚠️  Returning original path: {path}")
        return path

    def _load_from_disk_cache(self, cache_key: str) -> Optional[Image.Image]:
        """
        Load image from disk cache.

        Args:
            cache_key: Cache key

        Returns:
            PIL Image or None if not cached
        """
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.png")

        if os.path.exists(cache_path):
            try:
                return Image.open(cache_path)
            except Exception:
                # Cache file corrupted, remove it
                os.remove(cache_path)

        return None

    def _save_to_disk_cache(self, cache_key: str, image: Image.Image):
        """
        Save image to disk cache.

        Args:
            cache_key: Cache key
            image: Image to cache
        """
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.png")

        try:
            # Convert RGBA to RGB for PNG saving
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                rgb_image.save(cache_path, 'PNG')
            else:
                image.save(cache_path, 'PNG')
        except Exception:
            # Silently fail on cache save errors
            pass

    def smart_crop(self,
                   image: Image.Image,
                   target_size: Tuple[int, int],
                   focus: str = 'center') -> Image.Image:
        """
        Smart crop image to target size with focus point.

        Args:
            image: Source image
            target_size: Target (width, height)
            focus: Focus point ('center', 'top', 'bottom', 'left', 'right')

        Returns:
            Cropped image
        """
        img_width, img_height = image.size
        target_width, target_height = target_size

        # Calculate aspect ratios
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height

        # Resize to fill target dimensions
        if img_ratio > target_ratio:
            # Image is wider - fit to height
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller - fit to width
            new_width = target_width
            new_height = int(new_width / img_ratio)

        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Calculate crop position based on focus
        if focus == 'center':
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
        elif focus == 'top':
            left = (new_width - target_width) // 2
            top = 0
        elif focus == 'bottom':
            left = (new_width - target_width) // 2
            top = new_height - target_height
        elif focus == 'left':
            left = 0
            top = (new_height - target_height) // 2
        elif focus == 'right':
            left = new_width - target_width
            top = (new_height - target_height) // 2
        else:
            # Default to center
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2

        # Crop
        right = left + target_width
        bottom = top + target_height

        return resized.crop((left, top, right, bottom))

    def apply_circle_mask(self, image: Image.Image) -> Image.Image:
        """
        Apply circular mask to image (useful for profile photos).

        Args:
            image: Source image (should be square for best results)

        Returns:
            Image with circular mask
        """
        # Make sure image is square
        size = min(image.size)
        image = self.smart_crop(image, (size, size), focus='center')

        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Apply mask
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(image, (0, 0))
        output.putalpha(mask)

        return output

    def resize_to_fit(self,
                     image: Image.Image,
                     max_width: int,
                     max_height: int,
                     maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image to fit within max dimensions.

        Args:
            image: Source image
            max_width: Maximum width
            max_height: Maximum height
            maintain_aspect: Maintain aspect ratio (default: True)

        Returns:
            Resized image
        """
        if not maintain_aspect:
            return image.resize((max_width, max_height), Image.Resampling.LANCZOS)

        img_width, img_height = image.size
        width_ratio = max_width / img_width
        height_ratio = max_height / img_height

        # Use smaller ratio to fit inside bounds
        ratio = min(width_ratio, height_ratio)

        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def fit_to_bounds(self,
                      image: Image.Image,
                      bounds: Tuple[int, int],
                      maintain_aspect: bool = True) -> Image.Image:
        """
        Fit image to bounding box dimensions (alias for resize_to_fit).

        Args:
            image: Source image
            bounds: (max_width, max_height) tuple
            maintain_aspect: Maintain aspect ratio (default: True)

        Returns:
            Resized image
        """
        return self.resize_to_fit(image, bounds[0], bounds[1], maintain_aspect)

    def remove_background(self,
                          image: Image.Image,
                          method: str = 'auto',
                          alpha_matting: bool = True,
                          color_tolerance: int = 30) -> Image.Image:
        """
        Remove background from image using specified method.
        
        Args:
            image: PIL Image to process
            method: Background removal method ('auto', 'edge', 'color')
            alpha_matting: Enable alpha matting for rembg (better edges)
            color_tolerance: Tolerance for color threshold method
            
        Returns:
            PIL Image with background removed (RGBA mode)
        """
        # For images that already have transparency, check if we should preserve it
        if image.mode == 'RGBA':
            alpha_channel = image.split()[-1]
            if alpha_channel.getextrema()[0] < 255:  # Has some transparency
                print("ℹ️  Image already has transparency, processing anyway")
        
        if method == 'auto':
            return self._remove_background_rembg(image, alpha_matting)
        elif method == 'edge':
            return self._remove_background_edge(image)
        elif method == 'color':
            return self._remove_background_color(image, color_tolerance)
        else:
            # Default to auto
            return self._remove_background_rembg(image, alpha_matting)
    
    def _remove_background_rembg(self, image: Image.Image, alpha_matting: bool = True) -> Image.Image:
        """
        Remove background using rembg AI with fallback to edge detection.
        
        Args:
            image: PIL Image to process
            alpha_matting: Enable alpha matting for better edge quality
            
        Returns:
            PIL Image with background removed
        """
        if not REMBG_AVAILABLE:
            print("⚠️  rembg not available, using enhanced edge detection")
            return self._remove_background_edge(image)
        
        try:
            print("🤖 Using rembg AI for professional background removal...")
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Use rembg with optimized settings
            result_bytes = rembg_remove(
                img_byte_arr,
                session=None,  # Auto-select best model
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            result_image = Image.open(BytesIO(result_bytes)).convert('RGBA')
            
            # Verify the result is valid
            if result_image.size[0] > 0 and result_image.size[1] > 0:
                # Check if we have meaningful transparency
                alpha = result_image.split()[-1]
                alpha_stats = alpha.getextrema()
                has_transparency = alpha_stats[0] < 255
                
                if has_transparency:
                    print("✅ rembg AI background removal successful!")
                    print(f"   Alpha range: {alpha_stats}")
                    
                    # Calculate foreground percentage
                    alpha_array = np.array(alpha)
                    total_pixels = alpha_array.size
                    transparent_pixels = np.sum(alpha_array == 0)
                    opaque_pixels = total_pixels - transparent_pixels
                    opaque_ratio = opaque_pixels / total_pixels
                    print(f"   Opaque ratio: {opaque_ratio:.1%}")
                    return result_image
                else:
                    print("⚠️  rembg completed but no transparency detected, using enhanced edge detection")
                    return self._remove_background_edge(image)
            else:
                print("⚠️  rembg returned invalid image, using enhanced edge detection")
                return self._remove_background_edge(image)
        
        except Exception as e:
            print(f"❌ rembg failed ({e}), using enhanced edge detection")
            return self._remove_background_edge(image)
    
    def _remove_background_edge(self, image: Image.Image) -> Image.Image:
        """
        Remove background using enhanced edge detection with multiple strategies.
        
        Args:
            image: PIL Image to process
            
        Returns:
            PIL Image with background removed
        """
        # Convert to RGBA
        img = image.convert('RGBA')
        data = np.array(img)
        
        print(f"🎨 Using enhanced edge detection for background removal")
        
        # Strategy 1: Multi-sample background detection
        corners = [
            data[0, 0][:3],      # Top-left
            data[0, -1][:3],     # Top-right
            data[-1, 0][:3],     # Bottom-left
            data[-1, -1][:3],    # Bottom-right
            data[10, 10][:3] if data.shape[0] > 20 and data.shape[1] > 20 else data[0, 0][:3],
            data[10, -11][:3] if data.shape[0] > 20 and data.shape[1] > 20 else data[0, -1][:3],
            data[-11, 10][:3] if data.shape[0] > 20 and data.shape[1] > 20 else data[-1, 0][:3],
            data[-11, -11][:3] if data.shape[0] > 20 and data.shape[1] > 20 else data[-1, -1][:3]
        ]
        
        # Remove outliers and get robust background color
        corner_colors = np.array(corners)
        mean_color = np.mean(corner_colors, axis=0)
        std_color = np.std(corner_colors, axis=0)
        
        # Use robust background color (exclude outliers)
        valid_corners = []
        for corner in corners:
            if np.all(np.abs(corner - mean_color) < 2 * std_color):
                valid_corners.append(corner)
        
        if valid_corners:
            bg_color = np.mean(valid_corners, axis=0).astype(int)
        else:
            bg_color = mean_color.astype(int)
        
        print(f"   Detected background color: {bg_color}")
        
        # Strategy 2: Adaptive thresholding
        color_variance = np.var(data[:, :, :3])
        base_threshold = max(25, min(80, color_variance / 200))
        threshold = base_threshold
        min_foreground_ratio = 0.12
        
        print(f"   Adaptive threshold: {threshold:.1f}")
        
        # Strategy 3: Enhanced color difference calculation
        diff = np.sqrt(np.sum((data[:, :, :3] - bg_color) ** 2, axis=2))
        
        # Apply Gaussian blur to reduce noise
        if SCIPY_AVAILABLE:
            diff = ndimage.gaussian_filter(diff, sigma=0.5)
        
        # Strategy 4: Create mask
        primary_mask = diff > threshold
        secondary_mask = diff > (threshold * 0.7)
        mask = primary_mask.copy()
        
        # Refine edges using secondary mask
        edge_pixels = primary_mask & ~secondary_mask
        if np.any(edge_pixels):
            mask = secondary_mask
        
        # Strategy 5: Morphological cleanup
        if SCIPY_AVAILABLE:
            # Close small holes
            mask = ndimage.binary_closing(mask, structure=np.ones((2, 2)))
            # Remove small noise
            mask = ndimage.binary_opening(mask, structure=np.ones((2, 2)))
            # Fill larger holes
            mask = ndimage.binary_fill_holes(mask)
        
        # Strategy 6: Quality assessment
        foreground_pixels = np.sum(mask)
        total_pixels = mask.size
        foreground_ratio = foreground_pixels / total_pixels
        
        print(f"   Final foreground ratio: {foreground_ratio:.2f}")
        
        # Quality check - try progressive relaxation if needed
        if foreground_ratio < min_foreground_ratio:
            print(f"⚠️  Insufficient foreground detected ({foreground_ratio:.2f}), trying relaxation")
            
            for relax_factor in [0.8, 0.6, 0.4]:
                relaxed_threshold = threshold * relax_factor
                relaxed_mask = diff > relaxed_threshold
                
                if SCIPY_AVAILABLE:
                    relaxed_mask = ndimage.binary_closing(relaxed_mask, structure=np.ones((2, 2)))
                    relaxed_mask = ndimage.binary_fill_holes(relaxed_mask)
                
                relaxed_foreground = np.sum(relaxed_mask)
                relaxed_ratio = relaxed_foreground / total_pixels
                
                if relaxed_ratio >= min_foreground_ratio:
                    print(f"   Using relaxed threshold: {relaxed_threshold:.1f} (ratio: {relaxed_ratio:.2f})")
                    mask = relaxed_mask
                    foreground_ratio = relaxed_ratio
                    break
            
            if foreground_ratio < min_foreground_ratio:
                print("   ⚠️  Unable to achieve good background removal, keeping original")
                return img
        
        # Apply final mask
        data[:, :, 3] = mask.astype(np.uint8) * 255
        
        print(f"✅ Enhanced background removal completed - {foreground_ratio:.2f} foreground retained")
        return Image.fromarray(data, 'RGBA')
    
    def _remove_background_color(self, image: Image.Image, tolerance: int = 30) -> Image.Image:
        """
        Remove background using color threshold (assumes white/solid background).
        
        Args:
            image: PIL Image to process
            tolerance: Color difference tolerance
            
        Returns:
            PIL Image with background removed
        """
        img = image.convert('RGBA')
        data = np.array(img)
        
        # Assume white background (most common)
        white_bg = np.array([255, 255, 255])
        
        print(f"🎨 Using color threshold method (tolerance: {tolerance})")
        
        # Create mask based on color difference
        diff = np.sqrt(np.sum((data[:, :, :3] - white_bg) ** 2, axis=2))
        mask = diff > tolerance
        
        # Apply mask
        data[:, :, 3] = mask.astype(np.uint8) * 255
        
        foreground_ratio = np.sum(mask) / mask.size
        print(f"✅ Color threshold removal completed - {foreground_ratio:.2f} foreground retained")
        
        return Image.fromarray(data, 'RGBA')

    def clear_cache(self):
        """Clear in-memory cache."""
        self._memory_cache.clear()

    def clear_disk_cache(self):
        """Clear disk cache."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            self._ensure_cache_dir()

    def get_cache_stats(self) -> Dict[str, any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        disk_size = 0
        disk_count = 0

        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    disk_size += os.path.getsize(filepath)
                    disk_count += 1

        return {
            'memory_cached': len(self._memory_cache),
            'disk_cached': disk_count,
            'disk_size_mb': round(disk_size / (1024 * 1024), 2)
        }


# Global singleton instance
_asset_manager: Optional[AssetManager] = None


def get_asset_manager() -> AssetManager:
    """
    Get global asset manager instance (singleton).

    Returns:
        AssetManager instance
    """
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager
