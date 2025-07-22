# Scholarship Matcher Project

A Django-based platform designed to intelligently match students with scholarship opportunities based on their academic profiles, financial needs, and eligibility criteria.

## 🚀 Project Overview

The Scholarship Matcher Project aims to simplify the scholarship discovery process by connecting students with relevant funding opportunities. The platform will analyze student profiles and automatically suggest scholarships that match their qualifications, reducing the time and effort required to find suitable financial aid.

### Key Features (Planned)
- **Intelligent Matching**: AI-powered algorithm to match students with scholarships
- **Comprehensive Database**: Extensive repository of scholarship opportunities
- **User Profiles**: Detailed student academic and financial profiles
- **Real-time Notifications**: Alerts for new matching opportunities and deadlines
- **Application Tracking**: Monitor scholarship application status
- **Analytics Dashboard**: Insights on matching success rates and trends

## 🏗️ Technical Architecture

### Backend Framework
- **Django 5.2.4**: High-level Python web framework
- **Django REST Framework**: Powerful toolkit for building Web APIs
- **PostgreSQL**: Robust relational database for data persistence
- **Redis**: In-memory data structure store for caching and message brokering
- **Celery**: Distributed task queue for background processing

### Communication & Notifications
- **Twilio**: SMS notifications and communication
- **SendGrid**: Email delivery service for notifications

### Deployment & Infrastructure
- **Docker**: Containerization for consistent development and deployment
- **Docker Compose**: Multi-container application orchestration
- **Nginx**: High-performance web server and reverse proxy
- **gunicorn**: Python WSGI HTTP Server for UNIX

### Development Tools
- **django-environ**: Environment variable management
- **psycopg2**: PostgreSQL adapter for Python
- **django-redis**: Redis cache backend for Django

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
Create a `.env` file from the example template:
```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:
```env
# Django Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=matcherdb
DB_USER=matcheruser
DB_PASSWORD=your-secure-password

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Communication Services
TWILIO_SID=your-twilio-account-sid
TWILIO_TOKEN=your-twilio-auth-token
SENDGRID_API_KEY=your-sendgrid-api-key

# Database Administration
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=secure-admin-password
```

### 3. Docker Setup (Recommended)
Build and start all services:
```bash
docker compose up --build
```

The application will be available at:
- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Database Admin (pgAdmin)**: http://localhost:5051
- **Nginx Proxy**: http://localhost:80

### 4. Local Development Setup (Alternative)
If you prefer local development without Docker:

#### Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Database Setup
Ensure PostgreSQL and Redis are running locally, then:
```bash
export $(grep -v '^#' .env | xargs)  # Load environment variables
python manage.py migrate
python manage.py createsuperuser
```

#### Run Development Server
```bash
python manage.py runserver
```

## 📁 Project Structure

```
scholarship-matcher/
├── matcher/                    # Main Django project directory
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
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Required |
| `DEBUG` | Enable/disable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed host/domain names | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `matcherdb` |
| `DB_USER` | PostgreSQL username | `matcheruser` |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `DB_HOST` | Database host | `db` (Docker) |
| `DB_PORT` | Database port | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |

### Django Settings Highlights
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis-based caching for improved performance
- **Security**: Production-ready security headers and SSL configuration
- **Static Files**: Configured for efficient static file serving
- **Internationalization**: Multi-language support ready
- **Time Zone**: UTC with timezone support

## 🛠️ Development Workflow

### Running Tests
```bash
# With Docker
docker compose exec web python manage.py test

# Local development
python manage.py test
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

### Celery Tasks (Background Processing)
```bash
# Start Celery worker (in separate terminal)
celery -A matcher worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A matcher beat --loglevel=info
```

## 📚 API Documentation

The project uses Django REST Framework for API development. Once custom apps are created:

- **API Root**: `/api/`
- **Admin Interface**: `/admin/`
- **API Documentation**: `/api/docs/` (planned)

### Future API Endpoints (Planned)
- `/api/students/` - Student profile management
- `/api/scholarships/` - Scholarship listings and search
- `/api/matches/` - Scholarship matching results
- `/api/applications/` - Application tracking
- `/api/notifications/` - Notification management

## 🚀 Deployment

### Production Deployment
1. Set `DEBUG=False` in environment variables
2. Configure proper `SECRET_KEY` and `ALLOWED_HOSTS`
3. Set up SSL certificates
4. Configure production database credentials
5. Set up monitoring and logging

### Docker Production
```bash
# Production build
docker compose -f docker-compose.prod.yml up --build -d
```

## 🤝 Contributing

We welcome contributions to the Scholarship Matcher Project! Here's how you can help:

### Development Process
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards
- Follow **PEP 8** Python style guidelines
- Write **comprehensive tests** for new features
- Include **docstrings** for all functions and classes
- Update **documentation** for any API changes

### Areas for Contribution
- **Scholarship matching algorithms**
- **User interface improvements**
- **API endpoint development**
- **Database optimization**
- **Test coverage improvement**
- **Documentation enhancement**

## 🗺️ Development Roadmap

### Phase 1: Core Infrastructure ✅
- [x] Django project setup
- [x] Docker containerization
- [x] Database configuration
- [x] Environment management
- [x] Basic security setup

### Phase 2: User Management (In Progress)
- [ ] User authentication and authorization
- [ ] Student profile models
- [ ] Admin interface customization
- [ ] User registration and login APIs

### Phase 3: Scholarship Management
- [ ] Scholarship database models
- [ ] CRUD operations for scholarships
- [ ] Scholarship search and filtering
- [ ] Administrative interfaces

### Phase 4: Matching Engine
- [ ] Matching algorithm development
- [ ] Eligibility criteria evaluation
- [ ] Scoring and ranking system
- [ ] Machine learning integration

### Phase 5: Application Management
- [ ] Application tracking system
- [ ] Document upload functionality
- [ ] Deadline management
- [ ] Status notifications

### Phase 6: Enhanced Features
- [ ] Real-time notifications
- [ ] Analytics dashboard
- [ ] Mobile responsiveness
- [ ] Advanced search capabilities
- [ ] Integration with external scholarship databases

## 📞 Support & Contact

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/ARMSTRONGOPONDO/scholarship-matcher/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/ARMSTRONGOPONDO/scholarship-matcher/discussions)
- **Documentation**: Comprehensive docs available in the `/docs` directory (coming soon)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Contributors and maintainers
- Scholarship organizations providing opportunities
- Students who inspire this project

---

**Note**: This project is under active development. Features and documentation will be continuously updated as the project evolves. We appreciate your patience and contributions as we build this platform together.
