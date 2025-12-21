#!/bin/bash

# Database setup script for TV Channel Django project
# This script creates the PostgreSQL database and user if they don't exist

# Database configuration (should match settings.py)
DB_NAME="tv_channel_db"
DB_USER="admin"
DB_PASSWORD="123456"
DB_HOST="localhost"
DB_PORT="5432"

echo "Setting up PostgreSQL database for TV Channel project..."

# Check if PostgreSQL is running
if ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
    echo "Error: PostgreSQL is not running on $DB_HOST:$DB_PORT"
    echo "Please start PostgreSQL and try again."
    exit 1
fi

# Create database user if it doesn't exist
echo "Creating database user '$DB_USER' if it doesn't exist..."
sudo -u muradhutraev psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User already exists or error occurred (this is OK if user exists)"

# Create database if it doesn't exist
echo "Creating database '$DB_NAME' if it doesn't exist..."
sudo -u muradhutraev psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || echo "Database already exists or error occurred (this is OK if database exists)"

# Grant privileges
echo "Granting privileges..."
sudo -u muradhutraev psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || echo "Privileges already granted or error occurred"

echo ""
echo "Database setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure you have installed psycopg2: pip install psycopg2-binary"
echo "2. Run migrations: python manage.py makemigrations"
echo "3. Run migrations: python manage.py migrate"
echo "4. Create a superuser: python manage.py createsuperuser"
echo ""
echo "Database configuration:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"

