# 🧠 Mental Health Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive Django-based mental health platform that provides resources, support, and community features for mental wellness, including podcast integration, resource sharing, and peer support networks.

## 📋 Table of Contents

- [🚀 Project Overview](#-project-overview)
- [🏗️ Technical Architecture](#️-technical-architecture)
- [📋 Prerequisites](#-prerequisites)
- [🚦 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 Configuration Details](#-configuration-details)
- [🛠️ Development Workflow](#️-development-workflow)
- [🧪 Testing](#-testing)
- [🔍 Troubleshooting](#-troubleshooting)
- [🔒 Security](#-security)
- [📈 Performance & Monitoring](#-performance--monitoring)
- [🚀 Deployment](#-deployment)
- [❓ FAQ](#-faq)
- [🤝 Contributing](#-contributing)
- [🗺️ Development Roadmap](#️-development-roadmap)
- [📞 Support & Contact](#-support--contact)

## 🚀 Project Overview

The Mental Health Platform is designed to provide comprehensive mental health support and resources to users, creating a safe and supportive community for mental wellness. The platform integrates various tools and resources to help users manage their mental health journey.

### Key Features (Planned)
- **Resource Library**: Comprehensive collection of mental health resources and articles
- **Podcast Integration**: Mental health podcasts and audio content
- **Community Support**: Peer support networks and discussion forums
- **Crisis Resources**: Emergency contact information and crisis intervention tools
- **Personalized Dashboard**: Track mental health goals and progress
- **Professional Directory**: Find mental health professionals and services
- **Wellness Tools**: Meditation guides, mood tracking, and coping strategies

## 🏗️ Technical Architecture

### Backend Framework
- **Django 5.2.4**: High-level Python web framework
- **Django REST Framework**: Powerful toolkit for building Web APIs
- **PostgreSQL**: Robust relational database for data persistence
- **Redis**: In-memory data structure store for caching and session management
- **Celery**: Distributed task queue for background processing

### Infrastructure
- **Docker**: Containerization for consistent deployment
- **Nginx**: High-performance web server and reverse proxy
- **pgAdmin**: Database administration interface

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 1.29 or higher)
- **Python 3.9+** (for local development)
- **Git** for version control

## 🚦 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ARMSTRONGOPONDO/scholarship-matcher.git
cd scholarship-matcher
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env  # or your preferred editor
```

### 3. Start with Docker
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec web python manage.py migrate

# Create superuser account
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application
- **Main Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin
- **Database Admin**: http://localhost:5051 (pgAdmin)

## 📁 Project Structure

```
mental-health-platform/
├── mental_health_core/         # Main Django project directory
│   ├── __init__.py
│   ├── settings.py            # Django settings and configuration
│   ├── urls.py               # URL routing configuration
│   ├── wsgi.py              # WSGI configuration for deployment
│   └── asgi.py              # ASGI configuration for async support
├── nginx/                     # Nginx configuration
│   └── conf.d/
│       └── default.conf      # Nginx server configuration
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Multi-container Docker application
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration Details

### Environment Variables
Key configuration settings in `.env`:

```bash
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=mental_health_db
DB_USER=mental_health_user
DB_PASSWORD=mental_health_pass
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# External Service Configuration
TWILIO_SID=your-twilio-sid
TWILIO_TOKEN=your-twilio-token
SENDGRID_API_KEY=your-sendgrid-key

# pgAdmin Configuration
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=securepassword
```

### Django Settings Highlights
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis-based caching for improved performance
- **Security**: CSRF protection, secure headers, and authentication
- **Background Tasks**: Celery integration for async processing

## 🛠️ Development Workflow

### Setting Up Development Environment

1. **Clone and Setup**:
```bash
git clone <repository-url>
cd mental-health-platform
cp .env.example .env
```

2. **Start Development Services**:
```bash
docker-compose up --build
```

3. **Run Migrations**:
```bash
docker-compose exec web python manage.py migrate
```

### Making Changes

1. **Create Feature Branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make Code Changes**:
   - Follow Django best practices
   - Write tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**:
```bash
# Run tests
docker-compose exec web python manage.py test

# Check code formatting
docker-compose exec web python -m black --check .
```

4. **Commit and Push**:
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### Code Review Process
1. Create pull request with detailed description
2. Ensure all tests pass
3. Address reviewer feedback
4. Merge after approval

## 🧪 Testing

### Running Tests
```bash
# Run all tests
docker-compose exec web python manage.py test

# Run specific app tests
docker-compose exec web python manage.py test mental_health_core

# Run with coverage
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

### Test Structure
- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions
- **API Tests**: Test REST API endpoints
- **UI Tests**: Test user interface functionality

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

**Port Already in Use**
```bash
# Check which process is using port 8000
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

**Permission Denied Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Static Files Not Loading**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Performance Issues

**Slow Database Queries**
- Enable Django Debug Toolbar in development
- Use database query optimization
- Consider database indexing

**Memory Usage**
- Monitor container resource usage
- Optimize Django queries
- Configure proper caching strategies

## 🔒 Security

### Security Best Practices

#### Environment Security
```bash
# Generate secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Use strong passwords for database
openssl rand -base64 32  # Generate random password
```

#### Production Security Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for all secrets
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up security headers (HSTS, CSP, etc.)
- [ ] Regular security updates for dependencies
- [ ] Database connection encryption
- [ ] Secure file upload handling
- [ ] Rate limiting for API endpoints
- [ ] Audit logging for sensitive operations

#### Security Configuration
```python
# Production security settings in settings.py
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📈 Performance & Monitoring

### Performance Optimization
- **Database**: Query optimization and proper indexing
- **Caching**: Redis caching strategy for frequent data
- **Static Files**: CDN integration for static assets
- **Background Tasks**: Celery for time-consuming operations

### Monitoring Setup
- **Health Checks**: Docker health checks for all services
- **Logging**: Structured logging with appropriate levels
- **Error Tracking**: Integration with error monitoring services
- **Performance Metrics**: Application performance monitoring

### Logging Configuration
```python
# settings.py - Enhanced logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'mental_health_core': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## 🚀 Deployment

### Local Development
```bash
# Start development environment
docker-compose up --build

# Access services
# - Application: http://localhost:8000
# - Admin: http://localhost:8000/admin
# - pgAdmin: http://localhost:5051
```

### Production Deployment

#### Docker Production Setup
1. **Environment Configuration**:
```bash
# Set production environment variables
export DEBUG=False
export SECRET_KEY="your-production-secret-key"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
```

2. **Docker Compose Production**:
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn mental_health_core.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DJANGO_SETTINGS_MODULE=mental_health_core.settings.production
    restart: unless-stopped

  celery-beat:
    build: .
    command: celery -A mental_health_core beat --loglevel=info
    environment:
      - DJANGO_SETTINGS_MODULE=mental_health_core.settings.production
    restart: unless-stopped
```

3. **SSL Certificate Setup**:
```bash
# Using Let's Encrypt with Certbot
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Post-Deployment Checklist
- [ ] SSL certificate installed and working
- [ ] Database migrations applied
- [ ] Static files collected and served
- [ ] Environment variables properly set
- [ ] Health checks passing
- [ ] Monitoring and logging configured
- [ ] Backup procedures in place
- [ ] Error tracking (Sentry) configured
- [ ] Performance monitoring setup
- [ ] Security headers configured

## ❓ FAQ

### General Questions

**Q: What is the Mental Health Platform?**
A: It's a Django-based platform that provides comprehensive mental health support, resources, and community features to help users manage their mental wellness journey.

**Q: Is this project ready for production use?**
A: Currently, this is a framework in development (Phase 1 complete). Core infrastructure is ready, but mental health specific features are still being developed.

**Q: What makes this different from other mental health platforms?**
A: Our platform focuses on comprehensive resource integration, community support, podcast integration, and personalized mental wellness tracking.

### Technical Questions

**Q: Can I contribute to the project?**
A: Yes! We welcome contributions. Please see the [Contributing](#-contributing) section for guidelines.

**Q: How do I report a bug or request a feature?**
A: Create an issue in the repository with detailed information about the bug or feature request.

**Q: Is the platform HIPAA compliant?**
A: HIPAA compliance features are planned for future releases. Current version focuses on general mental health resources and support.

### Deployment Questions

**Q: What are the minimum system requirements?**
A: 2GB RAM, 20GB storage, and Docker support. For production, recommend 4GB+ RAM and adequate bandwidth.

**Q: Can I deploy this on cloud platforms?**
A: Yes, the platform is designed to work with AWS, Google Cloud, Azure, and other cloud providers.

## 📚 API Documentation

The project uses Django REST Framework for API development. Once mental health apps are created:

- **API Root**: `/api/`
- **Admin Interface**: `/admin/`
- **API Documentation**: `/api/docs/` (planned with drf-spectacular)
- **API Schema**: `/api/schema/` (planned)

### Authentication
Future API will support:
- Token-based authentication
- Session authentication for web interface
- OAuth2 integration (planned)

### Future API Endpoints (Planned)

#### Resource Management
```python
# Get mental health resources
GET /api/resources/
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "title": "Managing Anxiety: A Comprehensive Guide",
            "category": "anxiety",
            "type": "article",
            "url": "https://example.com/anxiety-guide",
            "description": "Complete guide to understanding and managing anxiety",
            "created_at": "2024-12-31T12:00:00Z"
        }
    ]
}

# Get specific resource
GET /api/resources/{id}/
{
    "id": 1,
    "title": "Managing Anxiety: A Comprehensive Guide",
    "content": "Full resource content...",
    "tags": ["anxiety", "coping", "mental-health"],
    "rating": 4.5,
    "views": 1250
}
```

#### Podcast Integration
```python
# Get podcast episodes
GET /api/podcasts/
{
    "count": 25,
    "results": [
        {
            "id": 1,
            "title": "Understanding Depression",
            "description": "Expert discussion on depression symptoms and treatment",
            "audio_url": "https://example.com/episode1.mp3",
            "duration": "00:45:30",
            "published_at": "2024-12-31T12:00:00Z"
        }
    ]
}
```

#### User Wellness Tracking
```python
# Track mood/wellness
POST /api/wellness/mood/
{
    "mood_level": 7,
    "notes": "Feeling better today after meditation",
    "activities": ["meditation", "exercise"],
    "date": "2024-12-31"
}

# Get wellness history
GET /api/wellness/history/
{
    "mood_trends": [
        {"date": "2024-12-31", "mood_level": 7},
        {"date": "2024-12-30", "mood_level": 6}
    ],
    "activity_frequency": {
        "meditation": 15,
        "exercise": 10,
        "therapy": 4
    }
}
```

### API Testing
```bash
# Install testing dependencies
pip install pytest pytest-django

# Run API tests
pytest tests/test_api.py

# Test with curl
curl -H "Authorization: Token your-token" http://localhost:8000/api/resources/
```

## 🤝 Contributing

We welcome contributions to the Mental Health Platform! Here's how you can help:

### 🚀 Getting Started

1. **Fork the Repository**
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/scholarship-matcher.git
   ```
3. **Set Up Development Environment** (see Development Workflow)
4. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 📝 Development Guidelines

#### Code Standards
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

#### Testing Requirements
- Write tests for all new features
- Maintain minimum 80% test coverage
- Include both unit and integration tests
- Test error conditions and edge cases

#### Commit Message Format
```
type(scope): description

- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting changes
- refactor: code refactoring
- test: adding tests
- chore: maintenance tasks

Examples:
feat(resources): add mental health resource categorization
fix(api): resolve authentication token expiration
docs(readme): update deployment instructions
```

#### Pull Request Process
1. **Update** documentation if needed
2. **Ensure** all tests pass
3. **Add** screenshots for UI changes
4. **Request** review from maintainers
5. **Address** feedback promptly
6. **Squash** commits if requested

### 🎯 Areas for Contribution

#### High Priority
- [ ] **Mental Health Resource Management**
  - Resource categorization system
  - Content management interface
  - Resource rating and review system
  - Search and filtering capabilities

- [ ] **User Wellness Tracking**
  - Mood tracking system
  - Goal setting and progress tracking
  - Wellness analytics dashboard
  - Reminder and notification system

- [ ] **Community Features**
  - Discussion forums
  - Peer support groups
  - User-to-user messaging
  - Moderation tools

#### Medium Priority
- [ ] **API Development**
  - RESTful API endpoints
  - API documentation (drf-spectacular)
  - Rate limiting
  - API versioning

- [ ] **Frontend Development**
  - Modern UI/UX design
  - Responsive design
  - User dashboard
  - Admin interface improvements

- [ ] **Testing & Quality**
  - Unit test coverage
  - Integration tests
  - Performance tests
  - Security testing

#### Nice to Have
- [ ] **Analytics & Reporting**
  - User engagement metrics
  - Resource usage analytics
  - Platform health monitoring
  - Custom reports

- [ ] **Integration Features**
  - Third-party mental health APIs
  - Wearable device integration
  - Social media integration
  - Mobile app development

### 🛠️ Development Workflow

#### Setting Up Development Environment
1. Clone repository and create virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start development server: `python manage.py runserver`

#### Making Changes
1. Create feature branch from main
2. Make your changes with proper tests
3. Run tests: `python manage.py test`
4. Run linters: `flake8`, `black`
5. Commit changes with descriptive messages
6. Push branch and create pull request

#### Code Review Process
1. All changes require review from maintainers
2. Address feedback and make necessary changes
3. Ensure CI/CD pipeline passes
4. Maintainer will merge after approval

### 🏗️ Project Architecture

#### Backend Structure
- **Django Apps**: Modular approach with separate apps for different features
- **Database Models**: Well-designed schema with proper relationships
- **API Layer**: RESTful APIs using Django REST Framework
- **Background Tasks**: Celery for async processing
- **Caching**: Redis for performance optimization

#### Frontend Architecture (Planned)
- **Modern Framework**: React/Vue.js for interactive UI
- **Component Library**: Reusable UI components
- **State Management**: Redux/Vuex for application state
- **Responsive Design**: Mobile-first approach

### 📊 Performance Guidelines

- **Database Queries**: Use `select_related` and `prefetch_related`
- **Caching**: Implement appropriate caching strategies
- **API Response**: Pagination for large datasets
- **Static Files**: Use CDN for production
- **Background Tasks**: Use Celery for time-consuming operations

### 🔧 Tools and Resources

#### Development Tools
- **IDE**: PyCharm, VSCode, or Sublime Text
- **Database**: PostgreSQL with pgAdmin
- **API Testing**: Postman or Insomnia
- **Version Control**: Git with GitHub

#### Learning Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Mental Health Resources](https://www.nimh.nih.gov/)
- [Python Best Practices](https://realpython.com/)

### 🤝 Community

#### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community discussions
- **Email**: Direct contact for sensitive issues

#### Code of Conduct
- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Maintain professional communication
- Focus on the mental health mission

### 🎖️ Recognition

Contributors will be recognized in:
- README contributors section
- Release notes for significant contributions
- Community discussions and highlights
- Project documentation

## 🗺️ Development Roadmap

### Phase 1: Core Infrastructure ✅
- [x] Django project setup
- [x] Docker containerization
- [x] Database configuration
- [x] Environment management
- [x] Basic security setup

### Phase 2: User Management (In Progress)
- [ ] User authentication and authorization
- [ ] User profile models for mental health tracking
- [ ] Admin interface customization
- [ ] User registration and login APIs

### Phase 3: Mental Health Resources
- [ ] Resource database models
- [ ] CRUD operations for resources
- [ ] Resource categorization and tagging
- [ ] Search and filtering capabilities
- [ ] Resource rating and review system

### Phase 4: Wellness Tracking
- [ ] Mood tracking system
- [ ] Goal setting and progress monitoring
- [ ] Wellness analytics and reporting
- [ ] Personalized recommendations

### Phase 5: Community Features
- [ ] Discussion forums
- [ ] Peer support groups
- [ ] User-to-user messaging
- [ ] Community moderation tools

### Phase 6: Enhanced Features
- [ ] Mobile app development
- [ ] Podcast integration platform
- [ ] Crisis intervention tools
- [ ] Professional directory integration
- [ ] Advanced analytics and insights

## 📞 Support & Contact

### Getting Help
- **Documentation**: Check this README and project wiki
- **Issues**: Create GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for urgent issues

### Maintainers
- **Primary Maintainer**: [@ARMSTRONGOPONDO](https://github.com/ARMSTRONGOPONDO)
- **Contributors**: See [Contributors](https://github.com/ARMSTRONGOPONDO/scholarship-matcher/graphs/contributors)

### Project Links
- **Repository**: https://github.com/ARMSTRONGOPONDO/scholarship-matcher
- **Issues**: https://github.com/ARMSTRONGOPONDO/scholarship-matcher/issues
- **Wiki**: https://github.com/ARMSTRONGOPONDO/scholarship-matcher/wiki

## 📋 Changelog

### Version 0.1.0 (Current) - Framework Foundation
#### Added
- Django project structure with mental health focus
- Docker containerization setup
- PostgreSQL database configuration
- Redis caching and session management
- Basic security configurations
- Admin interface setup
- Development environment documentation

#### Changed
- Migrated from scholarship matcher to mental health platform focus
- Updated all configuration files for mental health core
- Restructured project for mental wellness features

### Upcoming Releases

#### Version 0.2.0 - User Management
- User authentication system
- Profile management for mental health tracking
- Basic wellness tracking models
- API authentication endpoints

#### Version 0.3.0 - Resource Management
- Mental health resource database
- Resource categorization system
- Search and filtering capabilities
- Admin interface for resource management

#### Version 0.4.0 - Community Features
- Discussion forums
- Basic peer support features
- User interaction capabilities
- Moderation tools

## 🙏 Acknowledgments

### Project Inspiration
This project was inspired by the critical need for accessible mental health resources and the power of community support in mental wellness journeys.

### Special Thanks
- **Django Community** - For building an amazing framework
- **Mental Health Advocates** - For inspiring this platform's mission
- **Open Source Contributors** - For the excellent tools and libraries
- **Mental Health Professionals** - For guidance on best practices
- **Community Members** - Who motivated us to build this platform

### Inspiration
This project was inspired by the need to make mental health resources more accessible and to create supportive communities for people on their mental wellness journeys.

---

<div align="center">

**📧 Stay Updated** | **🐛 Report Issues** | **💡 Suggest Features** | **🤝 Contribute**

Made with ❤️ by the Mental Health Platform Team

**⭐ Star this repo** if you find it helpful!

---

*"Mental health is not a destination, but a process. It's about how you drive, not where you're going."* - Noam Shpancer

</div>

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ **Commercial use** allowed
- ✅ **Modification** allowed
- ✅ **Distribution** allowed
- ✅ **Private use** allowed
- ❌ **Liability** - No warranty provided
- ❌ **Warranty** - Use at your own risk

### Using this Project
You are free to use this project for any purpose, including commercial applications. If you use this project as a foundation for your mental health platform, we'd appreciate:
- Attribution to the original project
- Sharing improvements back to the community
- Following ethical practices in mental health technology