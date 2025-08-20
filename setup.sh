#!/bin/bash

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
SECRET_KEY=django-insecure-67a%z(i6pn@^v0-lkh7d2hq5e9#)a$^7j@*3-+wh_8-0iqj%2@
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_NAME=mental_health
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
PODCAST_INDEX_API_KEY=your_podcast_index_api_key
PODCAST_INDEX_API_SECRET=your_podcast_index_api_secret
EOL
    echo ".env file created."
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL before continuing."
    exit 1
fi

# Prompt for PostgreSQL credentials
read -p "Enter PostgreSQL username (default: postgres): " db_user
db_user=${db_user:-postgres}

read -s -p "Enter PostgreSQL password: " db_password
echo

# Create database if it doesn't exist
echo "Creating database if it doesn't exist..."
PGPASSWORD=$db_password psql -U $db_user -h localhost -c "CREATE DATABASE mental_health;" || true

# Update .env file with database credentials
sed -i "s/DB_USER=.*/DB_USER=$db_user/" .env
sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$db_password/" .env

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: admin/admin')
else:
    print('Superuser already exists.')
"

# Load initial data
echo "Loading initial data..."
python manage.py load_initial_data

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start development server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
