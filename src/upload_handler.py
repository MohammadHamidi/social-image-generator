"""
Upload Handler - Refactored upload logic
Provides unified upload handling for all image types
"""
import os
from datetime import datetime
from typing import Tuple, Optional, Any
from PIL import Image
import uuid

# Werkzeug is a Flask dependency, but make it optional for testing
try:
    from werkzeug.datastructures import FileStorage
    from werkzeug.utils import secure_filename
    HAS_WERKZEUG = True
except ImportError:
    HAS_WERKZEUG = False
    FileStorage = Any  # Type hint fallback

    def secure_filename(filename: str) -> str:
        """Fallback secure_filename implementation"""
        import re
        filename = str(filename).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', filename)


class UploadHandler:
    """
    Handles file uploads with validation and security checks
    """

    def __init__(self, base_upload_folder: str, allowed_extensions: set):
        """
        Initialize upload handler

        Args:
            base_upload_folder: Base directory for uploads
            allowed_extensions: Set of allowed file extensions
        """
        self.base_upload_folder = base_upload_folder
        self.allowed_extensions = allowed_extensions

    def _allowed_file(self, filename: str) -> bool:
        """
        Check if file extension is allowed

        Args:
            filename: Filename to check

        Returns:
            True if extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def _generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename to prevent conflicts

        Args:
            original_filename: Original uploaded filename

        Returns:
            Unique filename with timestamp and UUID
        """
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{unique_id}.{ext}"

    def _validate_image_content(self, file: FileStorage) -> None:
        """
        Validate that uploaded file is actually an image

        Args:
            file: Uploaded file

        Raises:
            ValueError: If file is not a valid image
        """
        try:
            # Save current position
            position = file.tell()

            # Try to open with PIL
            img = Image.open(file)

            # Load the image to verify it's valid
            img.load()

            # Get basic info
            width, height = img.size
            format_type = img.format

            # Restore file position
            file.seek(position)

            # Basic sanity checks
            if width <= 0 or height <= 0:
                raise ValueError("Invalid image dimensions")

            if width > 16384 or height > 16384:
                raise ValueError("Image dimensions too large (max 16384x16384)")

        except Exception as e:
            file.seek(0)  # Reset position
            raise ValueError(f"Invalid image file: {str(e)}")

    def _ensure_directory(self, directory: str) -> Tuple[bool, Optional[str]]:
        """
        Ensure upload directory exists and is writable

        Args:
            directory: Directory path

        Returns:
            Tuple of (success, error_message)
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            if not os.access(directory, os.W_OK):
                return False, "Directory not writable"

            return True, None

        except Exception as e:
            return False, str(e)

    def handle_upload(
        self,
        file: FileStorage,
        folder_type: str,
        max_file_size: int = 16 * 1024 * 1024
    ) -> Tuple[bool, dict]:
        """
        Handle file upload with validation

        Args:
            file: Uploaded file
            folder_type: Type of upload (main, watermark, background)
            max_file_size: Maximum file size in bytes

        Returns:
            Tuple of (success, result_dict)
            result_dict contains either file info or error message
        """
        try:
            # Validate file was provided
            if not file or file.filename == '':
                return False, {'error': 'No file selected'}

            # Validate file extension
            if not self._allowed_file(file.filename):
                return False, {
                    'error': f'File type not allowed. Use: {", ".join(sorted(self.allowed_extensions)).upper()}'
                }

            # Validate file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset

            if file_size > max_file_size:
                max_mb = max_file_size / (1024 * 1024)
                return False, {'error': f'File too large (max {max_mb}MB)'}

            if file_size == 0:
                return False, {'error': 'File is empty'}

            # Validate image content
            try:
                self._validate_image_content(file)
            except ValueError as e:
                return False, {'error': str(e)}

            # Prepare target directory
            target_dir = os.path.join(self.base_upload_folder, folder_type)
            success, error = self._ensure_directory(target_dir)
            if not success:
                return False, {'error': f'Upload directory not available: {error}'}

            # Generate secure filename
            secure_name = secure_filename(file.filename)
            unique_filename = self._generate_unique_filename(secure_name)
            filepath = os.path.join(target_dir, unique_filename)

            # Save file
            file.save(filepath)

            # Verify file was saved
            if not os.path.exists(filepath):
                return False, {'error': 'File save failed'}

            # Return success info
            return True, {
                'success': True,
                'message': f'{folder_type.capitalize()} image uploaded successfully',
                'filename': unique_filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'upload_time': datetime.now().isoformat(),
                'folder': folder_type
            }

        except Exception as e:
            return False, {'error': f'Upload failed: {str(e)}'}


def create_upload_response(
    success: bool,
    result: dict,
    url_generator=None,
    folder_type: str = None
) -> Tuple[dict, int]:
    """
    Create standardized upload response

    Args:
        success: Whether upload succeeded
        result: Result dictionary from handle_upload
        url_generator: Function to generate file URLs
        folder_type: Folder type for URL generation

    Returns:
        Tuple of (response_dict, status_code)
    """
    if not success:
        return result, 400 if 'error' in result else 500

    # Add URL if generator provided
    if url_generator and folder_type:
        result['url'] = url_generator('uploaded_file', folder=folder_type, filename=result['filename'])

    return result, 200
