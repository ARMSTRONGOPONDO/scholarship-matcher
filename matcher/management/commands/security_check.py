"""
Security validation management command for the scholarship matcher application.
"""
import os
import secrets
import string
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Command(BaseCommand):
    help = 'Perform security validation checks and generate secure configurations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generate-secret-key',
            action='store_true',
            help='Generate a new secure SECRET_KEY',
        )
        parser.add_argument(
            '--check-config',
            action='store_true',
            help='Check security configuration',
        )
        parser.add_argument(
            '--fix-permissions',
            action='store_true',
            help='Fix file permissions for security',
        )

    def handle(self, *args, **options):
        if options['generate_secret_key']:
            self.generate_secret_key()
        
        if options['check_config']:
            self.check_security_config()
        
        if options['fix_permissions']:
            self.fix_file_permissions()
        
        if not any(options.values()):
            # Default: run all checks
            self.check_security_config()

    def generate_secret_key(self):
        """Generate a cryptographically secure SECRET_KEY."""
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
        secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
        
        self.stdout.write(
            self.style.SUCCESS(f'Generated SECRET_KEY: {secret_key}')
        )
        self.stdout.write(
            self.style.WARNING(
                'Add this to your .env file: SECRET_KEY=' + secret_key
            )
        )

    def check_security_config(self):
        """Perform comprehensive security configuration checks."""
        self.stdout.write(self.style.SUCCESS('Running security configuration checks...'))
        
        issues = []
        warnings = []
        
        # Check SECRET_KEY
        try:
            secret_key = settings.SECRET_KEY
            if not secret_key:
                issues.append("SECRET_KEY is empty")
            elif len(secret_key) < 50:
                warnings.append("SECRET_KEY should be at least 50 characters long")
            elif secret_key.startswith('django-insecure-'):
                issues.append("SECRET_KEY is using Django's insecure default")
        except Exception:
            issues.append("SECRET_KEY is not configured")

        # Check DEBUG setting
        if settings.DEBUG:
            warnings.append("DEBUG is enabled - should be False in production")

        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS and not settings.DEBUG:
            issues.append("ALLOWED_HOSTS is empty in production mode")
        elif '*' in settings.ALLOWED_HOSTS:
            issues.append("ALLOWED_HOSTS contains '*' - too permissive")

        # Check database configuration
        db_config = settings.DATABASES.get('default', {})
        if db_config.get('ENGINE') == 'django.db.backends.sqlite3' and not settings.DEBUG:
            warnings.append("Using SQLite in production - consider PostgreSQL")

        # Check session security
        if not getattr(settings, 'SESSION_COOKIE_SECURE', False) and not settings.DEBUG:
            warnings.append("SESSION_COOKIE_SECURE should be True in production")
        
        if not getattr(settings, 'CSRF_COOKIE_SECURE', False) and not settings.DEBUG:
            warnings.append("CSRF_COOKIE_SECURE should be True in production")

        # Check HTTPS settings
        if not settings.DEBUG:
            if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
                warnings.append("SECURE_SSL_REDIRECT should be True in production")
            
            if not getattr(settings, 'SECURE_HSTS_SECONDS', 0):
                warnings.append("SECURE_HSTS_SECONDS should be set in production")

        # Check file upload limits
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None)
        if not max_size or max_size > 10485760:  # 10MB
            warnings.append("FILE_UPLOAD_MAX_MEMORY_SIZE is too large or not set")

        # Check logging configuration
        if not getattr(settings, 'LOGGING', None):
            warnings.append("LOGGING is not configured")

        # Check admin IP whitelist (if configured)
        admin_whitelist = getattr(settings, 'ADMIN_IP_WHITELIST', None)
        if admin_whitelist and '*' in admin_whitelist:
            issues.append("ADMIN_IP_WHITELIST contains '*' - defeats the purpose")

        # Report results
        if issues:
            self.stdout.write(self.style.ERROR('\nSECURITY ISSUES FOUND:'))
            for issue in issues:
                self.stdout.write(self.style.ERROR(f'  ❌ {issue}'))

        if warnings:
            self.stdout.write(self.style.WARNING('\nSECURITY WARNINGS:'))
            for warning in warnings:
                self.stdout.write(self.style.WARNING(f'  ⚠️  {warning}'))

        if not issues and not warnings:
            self.stdout.write(self.style.SUCCESS('✅ All security checks passed!'))
        else:
            total_issues = len(issues) + len(warnings)
            self.stdout.write(
                self.style.ERROR(f'\n{total_issues} security issues found. Please address them.')
            )

    def fix_file_permissions(self):
        """Fix file permissions for security."""
        self.stdout.write('Fixing file permissions...')
        
        base_dir = settings.BASE_DIR
        
        # Directories that should be writable
        writable_dirs = [
            os.path.join(base_dir, 'logs'),
            os.path.join(base_dir, 'media'),
            os.path.join(base_dir, 'staticfiles'),
        ]
        
        for dir_path in writable_dirs:
            if os.path.exists(dir_path):
                try:
                    os.chmod(dir_path, 0o755)
                    self.stdout.write(f'Fixed permissions for {dir_path}')
                except PermissionError:
                    self.stdout.write(
                        self.style.WARNING(f'Could not fix permissions for {dir_path}')
                    )
        
        # Files that should not be executable
        sensitive_files = [
            os.path.join(base_dir, '.env'),
            os.path.join(base_dir, 'manage.py'),
        ]
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                try:
                    if file_path.endswith('.env'):
                        os.chmod(file_path, 0o600)  # Only owner can read/write
                    else:
                        os.chmod(file_path, 0o644)  # Standard file permissions
                    self.stdout.write(f'Fixed permissions for {file_path}')
                except PermissionError:
                    self.stdout.write(
                        self.style.WARNING(f'Could not fix permissions for {file_path}')
                    )
        
        self.stdout.write(self.style.SUCCESS('File permissions check completed.'))