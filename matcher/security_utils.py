"""
Security utilities for file uploads and validation.
"""
import os
import magic
import hashlib
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage


class SecureFileValidator:
    """Secure file upload validator."""
    
    def __init__(self):
        self.allowed_extensions = getattr(
            settings, 
            'ALLOWED_UPLOAD_EXTENSIONS', 
            ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.gif']
        )
        self.max_file_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5242880)  # 5MB
        
        # MIME types for allowed extensions
        self.allowed_mime_types = {
            '.pdf': ['application/pdf'],
            '.doc': ['application/msword'],
            '.docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            '.txt': ['text/plain'],
            '.jpg': ['image/jpeg'],
            '.jpeg': ['image/jpeg'],
            '.png': ['image/png'],
            '.gif': ['image/gif'],
        }
    
    def validate_file(self, uploaded_file):
        """
        Comprehensive file validation.
        
        Args:
            uploaded_file: Django UploadedFile object
            
        Raises:
            ValidationError: If file fails validation
        """
        # Check file size
        if uploaded_file.size > self.max_file_size:
            raise ValidationError(
                f'File size too large. Maximum allowed size is '
                f'{self.max_file_size / (1024*1024):.1f}MB'
            )
        
        # Check file extension
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in self.allowed_extensions:
            raise ValidationError(
                f'File type not allowed. Allowed types: {", ".join(self.allowed_extensions)}'
            )
        
        # Check MIME type
        try:
            # Read a small chunk to determine MIME type
            uploaded_file.seek(0)
            file_content = uploaded_file.read(1024)
            uploaded_file.seek(0)
            
            mime_type = magic.from_buffer(file_content, mime=True)
            
            allowed_mimes = self.allowed_mime_types.get(file_ext, [])
            if allowed_mimes and mime_type not in allowed_mimes:
                raise ValidationError(
                    f'File content does not match extension. '
                    f'Expected: {allowed_mimes}, Got: {mime_type}'
                )
        except ImportError:
            # python-magic not available, skip MIME type check
            pass
        
        # Check for malicious content patterns
        self._scan_for_malicious_content(uploaded_file)
        
        return True
    
    def _scan_for_malicious_content(self, uploaded_file):
        """Basic scan for malicious content patterns."""
        # Read file content for scanning
        uploaded_file.seek(0)
        content = uploaded_file.read()
        uploaded_file.seek(0)
        
        # Convert to string for text-based files
        try:
            content_str = content.decode('utf-8', errors='ignore').lower()
        except:
            content_str = str(content).lower()
        
        # Malicious patterns to check for
        malicious_patterns = [
            '<script', 'javascript:', 'vbscript:', 'onload=', 'onerror=',
            '<?php', '<%', 'eval(', 'system(', 'exec(', 'passthru(',
            'shell_exec', 'base64_decode', 'gzinflate', 'strrev',
            'file_get_contents', 'file_put_contents', 'fopen', 'fwrite',
        ]
        
        for pattern in malicious_patterns:
            if pattern in content_str:
                raise ValidationError(
                    f'File contains potentially malicious content: {pattern}'
                )
    
    def generate_secure_filename(self, original_filename):
        """
        Generate a secure filename to prevent directory traversal and other attacks.
        
        Args:
            original_filename: Original filename from upload
            
        Returns:
            str: Secure filename
        """
        # Get file extension
        name, ext = os.path.splitext(original_filename)
        
        # Remove any path components
        name = os.path.basename(name)
        
        # Remove or replace dangerous characters
        safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
        safe_name = ''.join(c if c in safe_chars else '_' for c in name)
        
        # Ensure name is not empty
        if not safe_name:
            safe_name = 'upload'
        
        # Limit length
        safe_name = safe_name[:50]
        
        # Add timestamp hash to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        hash_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:8]
        
        return f"{safe_name}_{hash_suffix}{ext.lower()}"


def validate_uploaded_file(uploaded_file):
    """
    Convenience function for file validation.
    
    Args:
        uploaded_file: Django UploadedFile object
        
    Returns:
        str: Secure filename if validation passes
        
    Raises:
        ValidationError: If file fails validation
    """
    validator = SecureFileValidator()
    validator.validate_file(uploaded_file)
    return validator.generate_secure_filename(uploaded_file.name)


def scan_uploaded_files():
    """
    Scan all uploaded files for security issues.
    This can be run as a periodic task.
    """
    from django.core.files.storage import default_storage
    import os
    
    validator = SecureFileValidator()
    issues = []
    
    # Scan media directory
    try:
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        # Create a mock uploaded file object
                        class MockUploadedFile:
                            def __init__(self, file_obj, name):
                                self.file = file_obj
                                self.name = name
                                self.size = os.path.getsize(file_path)
                            
                            def read(self, size=None):
                                return self.file.read(size)
                            
                            def seek(self, pos):
                                return self.file.seek(pos)
                        
                        mock_file = MockUploadedFile(f, file)
                        validator.validate_file(mock_file)
                        
                except ValidationError as e:
                    issues.append(f"{file_path}: {str(e)}")
                except Exception as e:
                    issues.append(f"{file_path}: Scan error - {str(e)}")
    
    except Exception as e:
        issues.append(f"Directory scan error: {str(e)}")
    
    return issues