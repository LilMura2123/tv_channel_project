# TV Channel Django Project

A comprehensive Django web application for managing TV channel news and programs with PostgreSQL database integration, role-based access control, and a modern newspaper-themed user interface.

## Features

- **User Authentication**: Registration and login with password confirmation
- **Role-Based Access Control**: 
  - **Admin**: Can manage news, programs, and users
  - **Editor**: Can manage content (news and programs) but cannot manage users
  - **Regular User**: Can only view news, programs, and schedules
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for News and Programs
- **Search and Filtering**: Advanced search by title, content, date, and program name with sorting options
- **Statistics Dashboard**: Interactive charts and graphs showing user statistics, news articles, and programs
- **Admin Panel**: Django admin interface with role-based permissions
- **Modern UI**: Newspaper-themed design with red, white, and black colors using Roboto and Oswald fonts
- **Error Handling**: User-friendly error messages and validation

## Requirements

- Python 3.8+
- Django 5.2.8
- PostgreSQL 12+
- psycopg2-binary

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd tv_channel
   ```

2. **Install dependencies:**
   ```bash
   pip install django psycopg2-binary
   ```

3. **Set up PostgreSQL database:**

   **Option A: Using the shell script (Linux/Mac):**
   ```bash
   ./setup_database.sh
   ```

   **Option B: Using the Python script:**
   ```bash
   python setup_database.py
   ```

   **Option C: Manual setup:**
   
   Connect to PostgreSQL as the admin user (muradhutraev) and run:
   ```sql
   CREATE USER admin WITH PASSWORD '123456';
   CREATE DATABASE tv_channel_db OWNER admin;
   GRANT ALL PRIVILEGES ON DATABASE tv_channel_db TO admin;
   ```
   
   Or using psql command line:
   ```bash
   psql -U muradhutraev -c "CREATE USER admin WITH PASSWORD '123456';"
   psql -U muradhutraev -c "CREATE DATABASE tv_channel_db OWNER admin;"
   psql -U muradhutraev -c "GRANT ALL PRIVILEGES ON DATABASE tv_channel_db TO admin;"
   ```

4. **Update database settings (if needed):**
   
   Edit `tv_channel/settings.py` and update the database configuration if your PostgreSQL setup differs:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'tv_channel_db',
           'USER': 'admin',
           'PASSWORD': '123456',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
tv_channel/
├── manage.py
├── setup_database.sh          # Database setup script (shell)
├── setup_database.py          # Database setup script (Python)
├── news/                      # Main application
│   ├── models.py             # News, Program, and CustomUser models
│   ├── views.py              # All views (CRUD, auth, statistics)
│   ├── forms.py              # Forms for News, Program, and Registration
│   ├── admin.py              # Admin panel configuration
│   ├── urls.py               # URL routing
│   └── migrations/           # Database migrations
├── tv_channel/               # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   └── news/                # News app templates
│       ├── home.html
│       ├── news_list.html
│       ├── news_detail.html
│       ├── news_form.html
│       ├── program_list.html
│       ├── program_detail.html
│       ├── program_form.html
│       ├── register.html
│       ├── login.html
│       ├── statistics.html
│       ├── about.html
│       └── user_management.html
└── static/                   # Static files
    └── css/
        └── style.css        # Newspaper theme stylesheet
```

## Usage

### Creating Users

1. **Regular User Registration:**
   - Navigate to `/register/`
   - Fill in the registration form
   - New users are automatically assigned "Regular User" role

2. **Creating Admin/Editor Users:**
   - Only existing admins can create admin/editor accounts
   - Use the Django admin panel or create via shell:
     ```python
     python manage.py shell
     from news.models import CustomUser
     user = CustomUser.objects.create_user('username', 'email@example.com', 'password')
     user.role = 'admin'  # or 'editor'
     user.save()
     ```

### Managing Content

- **News Articles:**
  - View all: `/news/`
  - Create: `/news/create/` (Editor/Admin only)
  - Update: `/news/<id>/update/` (Editor/Admin only)
  - Delete: `/news/<id>/delete/` (Editor/Admin only)

- **Programs:**
  - View all: `/programs/`
  - Create: `/programs/create/` (Editor/Admin only)
  - Update: `/programs/<id>/update/` (Editor/Admin only)
  - Delete: `/programs/<id>/delete/` (Editor/Admin only)

### Search and Filtering

- **News:**
  - Search by title or content
  - Filter by date
  - Sort by title or date

- **Programs:**
  - Search by title or description
  - Filter by date and program name
  - Sort by title or start time

### Statistics

- Access statistics page at `/statistics/`
- View total users, news articles, and programs
- Interactive charts showing:
  - News articles by month
  - Programs by month
  - Users by role

## Database Models

### CustomUser
- Extends Django's AbstractUser
- Role field: 'admin', 'editor', or 'user'
- Methods: `is_admin()`, `is_editor()`

### News
- `title`: CharField (max_length=200)
- `content`: TextField
- `created_at`: DateTimeField (auto_now_add)
- `updated_at`: DateTimeField (auto_now)

### Program
- `title`: CharField (max_length=200)
- `description`: TextField
- `start_time`: DateTimeField
- `end_time`: DateTimeField
- `created_at`: DateTimeField (auto_now_add)
- `updated_at`: DateTimeField (auto_now)
- Property: `duration` (calculated from start_time and end_time)

## Role Permissions

| Action | Regular User | Editor | Admin |
|--------|-------------|--------|-------|
| View News | ✓ | ✓ | ✓ |
| View Programs | ✓ | ✓ | ✓ |
| Create News | ✗ | ✓ | ✓ |
| Edit News | ✗ | ✓ | ✓ |
| Delete News | ✗ | ✓ | ✓ |
| Create Programs | ✗ | ✓ | ✓ |
| Edit Programs | ✗ | ✓ | ✓ |
| Delete Programs | ✗ | ✓ | ✓ |
| Manage Users | ✗ | ✗ | ✓ |
| View Statistics | ✓ | ✓ | ✓ |

## Troubleshooting

### Database Connection Issues

1. **Check PostgreSQL is running:**
   ```bash
   pg_isready
   ```

2. **Verify database credentials in settings.py**

3. **Check database exists:**
   ```bash
   psql -U admin -d tv_channel_db -c "\dt"
   ```

### Migration Issues

If you encounter migration errors:
```bash
python manage.py makemigrations --empty news
python manage.py migrate
```

### Static Files Not Loading

Run collectstatic (for production):
```bash
python manage.py collectstatic
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

## License

This project is developed for educational purposes.

## Author

TV Channel Development Team

For more information, visit the [About page](/about/) in the application.

