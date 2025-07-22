"""
Custom security middleware for the scholarship matcher application.
"""
import logging
import time
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
from django.utils.deprecation import MiddlewareMixin
import ipaddress

logger = logging.getLogger('django.security')


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add additional security headers to all responses.
    """
    
    def process_response(self, request, response):
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy (Feature Policy replacement)
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )
        
        # Expect-CT header for certificate transparency
        if not settings.DEBUG:
            response['Expect-CT'] = 'max-age=86400, enforce'
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Basic rate limiting middleware to prevent abuse.
    """
    
    def get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, ip, endpoint, limit=100, window=3600):
        """
        Check if the IP is rate limited for a specific endpoint.
        
        Args:
            ip: Client IP address
            endpoint: API endpoint or view name
            limit: Number of requests allowed
            window: Time window in seconds
        """
        cache_key = f"rate_limit:{ip}:{endpoint}"
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= limit:
            logger.warning(f"Rate limit exceeded for IP {ip} on endpoint {endpoint}")
            return True
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, window)
        return False
    
    def process_request(self, request):
        # Skip rate limiting for admin and static files
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/')):
            return None
        
        client_ip = self.get_client_ip(request)
        endpoint = request.path
        
        # Different limits for different types of requests
        if request.path.startswith('/api/'):
            # API endpoints - stricter limits
            if self.is_rate_limited(client_ip, endpoint, limit=200, window=3600):
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded. Please try again later."
                )
        else:
            # Regular web requests
            if self.is_rate_limited(client_ip, endpoint, limit=500, window=3600):
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded. Please try again later."
                )
        
        return None


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Log security-relevant events and suspicious activities.
    """
    
    def process_request(self, request):
        # Log suspicious patterns
        self.check_suspicious_patterns(request)
        return None
    
    def check_suspicious_patterns(self, request):
        """Check for common attack patterns."""
        suspicious_patterns = [
            '../', '..\\', '<script', 'javascript:', 'vbscript:',
            'onload=', 'onerror=', 'eval(', 'union select',
            'drop table', 'insert into', 'delete from',
            '<?php', '<%', 'system(', 'exec(', 'passthru(',
        ]
        
        # Check URL, query string, and POST data
        check_strings = [
            request.path,
            request.META.get('QUERY_STRING', ''),
        ]
        
        if hasattr(request, 'body'):
            try:
                check_strings.append(request.body.decode('utf-8', errors='ignore'))
            except:
                pass
        
        for check_string in check_strings:
            check_lower = check_string.lower()
            for pattern in suspicious_patterns:
                if pattern in check_lower:
                    client_ip = self.get_client_ip(request)
                    logger.warning(
                        f"Suspicious pattern '{pattern}' detected from IP {client_ip} "
                        f"in {request.method} {request.path}"
                    )
                    break
    
    def get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def process_exception(self, request, exception):
        """Log exceptions for security monitoring."""
        client_ip = self.get_client_ip(request)
        logger.error(
            f"Exception {exception.__class__.__name__} from IP {client_ip} "
            f"on {request.method} {request.path}: {str(exception)}"
        )
        return None


class IPWhitelistMiddleware(MiddlewareMixin):
    """
    Optional IP whitelist middleware for admin access.
    Configure ADMIN_IP_WHITELIST in settings to enable.
    """
    
    def process_request(self, request):
        # Only apply to admin paths
        if not request.path.startswith('/admin/'):
            return None
        
        # Check if IP whitelisting is configured
        admin_whitelist = getattr(settings, 'ADMIN_IP_WHITELIST', None)
        if not admin_whitelist:
            return None
        
        client_ip = self.get_client_ip(request)
        
        # Check if IP is in whitelist
        allowed = False
        for allowed_ip in admin_whitelist:
            try:
                if ipaddress.ip_address(client_ip) in ipaddress.ip_network(allowed_ip):
                    allowed = True
                    break
            except ValueError:
                # Invalid IP format
                continue
        
        if not allowed:
            logger.warning(f"Admin access denied for IP {client_ip}")
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access denied from your IP address.")
        
        return None
    
    def get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip