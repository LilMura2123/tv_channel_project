#!/usr/bin/env python
"""
Database setup script for TV Channel Django project.
This script creates the PostgreSQL database and user if they don't exist.
"""

import psycopg2
from psycopg2 import sql
import sys

# Database configuration (should match settings.py)
DB_NAME = "tv_channel_db"
DB_USER = "admin"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"
ADMIN_USER = "muradhutraev"  # PostgreSQL admin user

def create_database():
    """Create database and user if they don't exist"""
    try:
        # Connect to PostgreSQL as admin user
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=ADMIN_USER,
            password=input(f"Enter password for PostgreSQL user '{ADMIN_USER}': ")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create user if it doesn't exist
        print(f"Creating database user '{DB_USER}' if it doesn't exist...")
        try:
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                    sql.Identifier(DB_USER)
                ),
                [DB_PASSWORD]
            )
            print(f"User '{DB_USER}' created successfully.")
        except psycopg2.errors.DuplicateObject:
            print(f"User '{DB_USER}' already exists.")
        
        # Create database if it doesn't exist
        print(f"Creating database '{DB_NAME}' if it doesn't exist...")
        try:
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(DB_NAME),
                    sql.Identifier(DB_USER)
                )
            )
            print(f"Database '{DB_NAME}' created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{DB_NAME}' already exists.")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(DB_NAME),
                sql.Identifier(DB_USER)
            )
        )
        print("Privileges granted successfully.")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("Database setup complete!")
        print("="*50)
        print("\nNext steps:")
        print("1. Run migrations: python manage.py makemigrations")
        print("2. Run migrations: python manage.py migrate")
        print("3. Create a superuser: python manage.py createsuperuser")
        print("\nDatabase configuration:")
        print(f"  Name: {DB_NAME}")
        print(f"  User: {DB_USER}")
        print(f"  Host: {DB_HOST}")
        print(f"  Port: {DB_PORT}")
        
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. PostgreSQL service is started")
        print("3. You have the correct admin credentials")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()

