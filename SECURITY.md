# Security Guide for Scholarship Matcher

This document outlines the security measures implemented in the Scholarship Matcher application and provides guidelines for maintaining security.

## 🔒 Security Features Implemented

### 1. Environment & Configuration Security

#### Secret Key Management
- **Removed insecure default SECRET_KEY** - No fallback values in production
- SECRET_KEY must be explicitly set via environment variables
- Generate secure keys using: `python manage.py security_check --generate-secret-key`

#### Environment Variables
- All sensitive data stored in environment variables
- `.env.example` provides secure templates with warnings
- No hardcoded credentials in source code

#### Debug Mode Protection
- DEBUG defaults to False (secure by default)
- Debug-specific settings are conditionally applied
- ALLOWED_HOSTS properly configured for production

### 2. HTTP Security Headers

#### Implemented Headers
- **HSTS (HTTP Strict Transport Security)**: Forces HTTPS connections
- **X-Content-Type-Options**: Prevents MIME type sniffing attacks
- **X-XSS-Protection**: Enables browser XSS filtering
- **X-Frame-Options**: Prevents clickjacking attacks
- **Referrer-Policy**: Controls referrer information
- **Permissions-Policy**: Restricts access to browser features
- **Expect-CT**: Certificate transparency enforcement

#### Content Security Policy (CSP)
- Basic CSP configuration implemented
- Prevents XSS attacks and data injection
- Customize CSP directives based on your requirements

### 3. Authentication & Session Security

#### Password Validation
- Minimum length increased to 12 characters
- Similarity checking against user attributes
- Common password validation
- Numeric password prevention

#### Session Security
- Session timeout set to 1 hour
- Sessions expire at browser close
- HTTPOnly cookies (prevents XSS access)
- Secure cookies in production (HTTPS only)
- SameSite cookie protection

#### CSRF Protection
- HTTPOnly CSRF cookies
- Secure CSRF cookies in production
- Session-based CSRF tokens
- Custom CSRF failure view

### 4. Database Security

#### Connection Security
- Environment-based configuration
- No hardcoded database credentials
- Connection pooling with Redis
- Prepared statements (Django ORM default)

#### Data Protection
- Strong password validation for user accounts
- Secure session storage
- Audit logging for sensitive operations

### 5. File Upload Security

#### Upload Restrictions
- File size limits (5MB default)
- File type validation by extension
- MIME type verification
- Malicious content scanning
- Secure filename generation

#### File Storage
- Proper file permissions (644 for files, 755 for directories)
- Separate media directory
- No execution permissions on uploaded files

### 6. API Security (Django REST Framework)

#### Authentication
- Session-based authentication
- Token-based authentication
- Default authentication requirement

#### Rate Limiting
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour
- Endpoint-specific rate limiting

#### Data Validation
- JSON-only API responses
- Secure parsers configuration
- Pagination to prevent data exposure

### 7. Rate Limiting & DOS Protection

#### Custom Middleware
- IP-based rate limiting
- Endpoint-specific limits
- Suspicious pattern detection
- Security event logging

#### Redis-based Tracking
- Distributed rate limiting
- Configurable time windows
- Automatic cleanup

### 8. Security Monitoring & Logging

#### Security Events
- Failed authentication attempts
- Rate limit violations
- Suspicious request patterns
- Exception logging with IP tracking

#### Log Management
- Separate security log files
- Structured logging format
- Log rotation and retention

### 9. Docker Security

#### Container Security
- Non-root user execution
- Resource limits (CPU, memory)
- Read-only volumes where possible
- Security scanning integration

#### Service Isolation
- Network segmentation
- Minimal exposed ports
- Health checks for services

## 🚨 Security Checklist

### Deployment Security

#### Pre-Deployment
- [ ] Generate strong SECRET_KEY (50+ characters)
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure security headers
- [ ] Review file upload limits
- [ ] Set up monitoring and logging

#### Production Environment
- [ ] Use PostgreSQL (not SQLite)
- [ ] Enable database connection encryption
- [ ] Configure Redis authentication
- [ ] Set up SSL certificates
- [ ] Configure firewall rules
- [ ] Enable log monitoring
- [ ] Set up backup procedures
- [ ] Configure error tracking (e.g., Sentry)

#### Ongoing Security
- [ ] Regular dependency updates
- [ ] Security patch monitoring
- [ ] Log review and analysis
- [ ] Penetration testing
- [ ] Security audit reviews
- [ ] Backup testing
- [ ] Incident response procedures

## 🛠️ Security Tools & Commands

### Security Validation
```bash
# Run comprehensive security checks
python manage.py security_check --check-config

# Generate secure SECRET_KEY
python manage.py security_check --generate-secret-key

# Fix file permissions
python manage.py security_check --fix-permissions

# Django security check
python manage.py check --deploy
```

### File Security Scanning
```bash
# Scan uploaded files for security issues
python manage.py shell -c "
from matcher.security_utils import scan_uploaded_files
issues = scan_uploaded_files()
for issue in issues:
    print(issue)
"
```

### Rate Limiting Configuration
```python
# In views.py, for custom rate limiting:
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes

@throttle_classes([UserRateThrottle])
def sensitive_endpoint(request):
    # Your view logic here
    pass
```

## 🚧 Security Considerations for Development

### Development vs Production
- Different security settings for each environment
- Conditional middleware and headers
- Environment-specific logging levels
- Debug toolbar only in development

### Code Security
- Input validation for all user data
- SQL injection prevention (use ORM)
- XSS prevention (template escaping)
- CSRF protection for state-changing operations
- Proper error handling (don't expose internals)

### Third-Party Integrations
- Secure API key storage
- Input validation for external data
- Rate limiting for external API calls
- Timeout configuration for external requests

## 📋 Incident Response

### Security Incident Procedure
1. **Identify**: Monitor logs for security events
2. **Contain**: Block malicious IPs, disable compromised accounts
3. **Eradicate**: Remove malicious content, patch vulnerabilities
4. **Recover**: Restore services, verify integrity
5. **Learn**: Update security measures, document lessons

### Emergency Contacts
- Security team: [Configure as needed]
- System administrators: [Configure as needed]
- External security consultants: [Configure as needed]

## 🔄 Regular Security Tasks

### Daily
- Review security logs
- Monitor failed login attempts
- Check system resource usage

### Weekly
- Review user access permissions
- Check for security updates
- Analyze security metrics

### Monthly
- Full security audit
- Penetration testing
- Security training updates
- Backup testing

## 📚 Additional Resources

### Security Best Practices
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django REST Framework Security](https://www.django-rest-framework.org/topics/api-guide/authentication/)

### Security Tools
- [Bandit](https://bandit.readthedocs.io/) - Python security linter
- [Safety](https://pyup.io/safety/) - Dependency vulnerability scanner
- [Semgrep](https://semgrep.dev/) - Static analysis tool

### Monitoring Services
- [Sentry](https://sentry.io/) - Error tracking and performance monitoring
- [DataDog](https://www.datadoghq.com/) - Infrastructure monitoring
- [New Relic](https://newrelic.com/) - Application performance monitoring

---

**Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update your security measures as threats evolve and your application grows.