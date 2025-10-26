"""
Asset Manager - Intelligent image loading, caching, and processing

Handles:
- Loading images from URLs or local paths
- Caching for performance
- Smart cropping and resizing
- Format conversion
- Asset validation
"""

from typing import Optional, Dict, Tuple, Union
from PIL import Image
import requests
import os
import hashlib
import time
from io import BytesIO
from urllib.parse import urlparse


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
                   use_cache: bool = True) -> Image.Image:
        """
        Load image asset from URL or local path.

        Args:
            url_or_path: URL or local file path
            role: Asset role (hero_image, logo, etc.) for logging
            use_cache: Whether to use cache (default: True)

        Returns:
            PIL Image object

        Raises:
            ValueError: If asset cannot be loaded
        """
        # Check memory cache first
        cache_key = self._get_cache_key(url_or_path)

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
        Load image from local file path.

        Args:
            path: Local file path

        Returns:
            PIL Image object

        Raises:
            ValueError: If file doesn't exist or can't be loaded
        """
        if not os.path.exists(path):
            raise ValueError(f"File not found: {path}")

        try:
            image = Image.open(path)

            # Convert to RGB if needed
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGB')

            return image

        except Exception as e:
            raise ValueError(f"Failed to open image file {path}: {str(e)}")

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
