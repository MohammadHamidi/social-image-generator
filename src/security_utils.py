"""
Security utilities for the Social Image Generator API
Provides SSRF protection, path validation, and other security features
"""
import ipaddress
import socket
from urllib.parse import urlparse
from typing import List, Optional
import os

# Try to import werkzeug's safe_join, fall back to manual implementation
try:
    from werkzeug.security import safe_join as _werkzeug_safe_join
    HAS_WERKZEUG = True
except ImportError:
    HAS_WERKZEUG = False


class SSRFProtection:
    """
    Server-Side Request Forgery (SSRF) protection
    Prevents API from being used to access internal resources
    """

    ALLOWED_SCHEMES = ['http', 'https']

    # Block private and special-use IP ranges
    BLOCKED_NETWORKS = [
        ipaddress.ip_network('127.0.0.0/8'),      # Loopback
        ipaddress.ip_network('10.0.0.0/8'),       # Private
        ipaddress.ip_network('172.16.0.0/12'),    # Private
        ipaddress.ip_network('192.168.0.0/16'),   # Private
        ipaddress.ip_network('169.254.0.0/16'),   # Link-local
        ipaddress.ip_network('224.0.0.0/4'),      # Multicast
        ipaddress.ip_network('240.0.0.0/4'),      # Reserved
        ipaddress.ip_network('::1/128'),          # IPv6 loopback
        ipaddress.ip_network('fe80::/10'),        # IPv6 link-local
        ipaddress.ip_network('fc00::/7'),         # IPv6 private
    ]

    @classmethod
    def validate_url(cls, url: str, allowed_domains: Optional[List[str]] = None) -> None:
        """
        Validate URL to prevent SSRF attacks

        Args:
            url: URL to validate
            allowed_domains: Optional whitelist of allowed domains

        Raises:
            ValueError: If URL is invalid or blocked
        """
        if not url:
            raise ValueError("URL cannot be empty")

        try:
            parsed = urlparse(url)

            # Check scheme
            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                raise ValueError(f"Unsupported URL scheme: {parsed.scheme}. Only {', '.join(cls.ALLOWED_SCHEMES)} allowed")

            # Extract hostname
            hostname = parsed.hostname
            if not hostname:
                raise ValueError("No hostname found in URL")

            # Check domain whitelist if provided
            if allowed_domains:
                if not any(hostname.endswith(domain) for domain in allowed_domains):
                    raise ValueError(f"Domain {hostname} not in allowed list")

            # Resolve hostname to IP addresses
            try:
                # Get all IP addresses for the hostname
                addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
                ips = set(info[4][0] for info in addr_info)
            except socket.gaierror as e:
                raise ValueError(f"Cannot resolve hostname {hostname}: {str(e)}")

            # Check each resolved IP against blocked networks
            for ip_str in ips:
                try:
                    ip = ipaddress.ip_address(ip_str)

                    # Check if IP is in any blocked network
                    for blocked_network in cls.BLOCKED_NETWORKS:
                        if ip in blocked_network:
                            raise ValueError(f"Access to {ip} ({blocked_network}) is blocked for security reasons")

                except ValueError as e:
                    # If IP parsing fails, that's also suspicious
                    raise ValueError(f"Invalid IP address {ip_str}: {str(e)}")

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"URL validation failed: {str(e)}")

    @classmethod
    def is_safe_url(cls, url: str, allowed_domains: Optional[List[str]] = None) -> bool:
        """
        Check if URL is safe without raising exceptions

        Args:
            url: URL to check
            allowed_domains: Optional whitelist of allowed domains

        Returns:
            True if URL is safe, False otherwise
        """
        try:
            cls.validate_url(url, allowed_domains)
            return True
        except ValueError:
            return False


class PathValidator:
    """
    Path validation to prevent directory traversal attacks
    """

    @staticmethod
    def safe_join_path(base_directory: str, *paths: str) -> Optional[str]:
        """
        Safely join paths preventing directory traversal

        Args:
            base_directory: Base directory (trusted)
            *paths: Path components to join

        Returns:
            Safe path or None if path traversal detected
        """
        # Use werkzeug's safe_join if available, otherwise manual implementation
        if HAS_WERKZEUG:
            result = _werkzeug_safe_join(base_directory, *paths)
        else:
            # Manual safe join implementation
            try:
                # Join paths normally
                result = os.path.normpath(os.path.join(base_directory, *paths))
            except Exception:
                return None

        # Additional check: ensure result is within base_directory
        if result:
            abs_base = os.path.abspath(base_directory)
            abs_result = os.path.abspath(result)

            # Check if result is actually under base directory
            if not abs_result.startswith(abs_base + os.sep) and abs_result != abs_base:
                return None

        return result

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """
        Validate filename for security issues

        Args:
            filename: Filename to validate

        Returns:
            True if filename is safe
        """
        if not filename:
            return False

        # Check for path separators (directory traversal attempts)
        if '/' in filename or '\\' in filename:
            return False

        # Check for null bytes
        if '\x00' in filename:
            return False

        # Check for relative path indicators
        if filename in ['.', '..'] or filename.startswith('.'):
            return False

        return True


class InputValidator:
    """
    Input validation for API parameters
    """

    # Configuration limits
    MAX_CANVAS_SIZE = 8192
    MIN_CANVAS_SIZE = 100
    MAX_TEXT_LENGTH = 5000
    MAX_LIST_ITEMS = 50
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

    @classmethod
    def validate_canvas_size(cls, width: int, height: int) -> None:
        """
        Validate canvas dimensions

        Args:
            width: Canvas width
            height: Canvas height

        Raises:
            ValueError: If dimensions are invalid
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Canvas dimensions must be integers")

        if width < cls.MIN_CANVAS_SIZE or width > cls.MAX_CANVAS_SIZE:
            raise ValueError(f"Canvas width must be between {cls.MIN_CANVAS_SIZE} and {cls.MAX_CANVAS_SIZE}")

        if height < cls.MIN_CANVAS_SIZE or height > cls.MAX_CANVAS_SIZE:
            raise ValueError(f"Canvas height must be between {cls.MIN_CANVAS_SIZE} and {cls.MAX_CANVAS_SIZE}")

        # Check total pixel count to prevent memory exhaustion
        max_pixels = cls.MAX_CANVAS_SIZE * cls.MAX_CANVAS_SIZE
        if width * height > max_pixels:
            raise ValueError(f"Total canvas pixels ({width * height}) exceeds maximum ({max_pixels})")

    @classmethod
    def validate_text_length(cls, text: str, field_name: str = "Text") -> None:
        """
        Validate text length

        Args:
            text: Text to validate
            field_name: Name of field for error messages

        Raises:
            ValueError: If text is too long
        """
        if text and len(text) > cls.MAX_TEXT_LENGTH:
            raise ValueError(f"{field_name} exceeds maximum length of {cls.MAX_TEXT_LENGTH} characters")

    @classmethod
    def validate_color(cls, color: List[int], field_name: str = "Color") -> None:
        """
        Validate RGB/RGBA color values

        Args:
            color: Color array [r, g, b] or [r, g, b, a]
            field_name: Name of field for error messages

        Raises:
            ValueError: If color format is invalid
        """
        if not isinstance(color, (list, tuple)):
            raise ValueError(f"{field_name} must be an array")

        if len(color) not in [3, 4]:
            raise ValueError(f"{field_name} must have 3 (RGB) or 4 (RGBA) values")

        for i, value in enumerate(color):
            if not isinstance(value, int):
                raise ValueError(f"{field_name}[{i}] must be an integer")

            if value < 0 or value > 255:
                raise ValueError(f"{field_name}[{i}] must be between 0 and 255")

    @classmethod
    def validate_array_size(cls, array: List, max_size: int, field_name: str = "Array") -> None:
        """
        Validate array size

        Args:
            array: Array to validate
            max_size: Maximum allowed size
            field_name: Name of field for error messages

        Raises:
            ValueError: If array is too large
        """
        if not isinstance(array, (list, tuple)):
            raise ValueError(f"{field_name} must be an array")

        if len(array) > max_size:
            raise ValueError(f"{field_name} exceeds maximum size of {max_size}")

    @classmethod
    def validate_list_items(cls, items: List, field_name: str = "Items") -> None:
        """
        Validate list items count

        Args:
            items: List items
            field_name: Name of field for error messages

        Raises:
            ValueError: If too many items
        """
        cls.validate_array_size(items, cls.MAX_LIST_ITEMS, field_name)
