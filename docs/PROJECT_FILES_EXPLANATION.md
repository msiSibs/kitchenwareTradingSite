# Kitchenware Marketplace - Project Files Overview

## 📁 Project Structure & File Explanations

This document explains the purpose and function of each major file in the Kitchenware Marketplace Django project.

---

## 🏗️ Root Level Files

### `manage.py`
**Purpose**: Django's command-line utility for administrative tasks
- **Location**: `/manage.py`
- **Key Functions**:
  - `python manage.py runserver` - Start development server
  - `python manage.py migrate` - Apply database migrations
  - `python manage.py createsuperuser` - Create admin user
  - `python manage.py makemigrations` - Create migration files
  - `python manage.py collectstatic` - Collect static files for production

### `requirements.txt`
**Purpose**: Python package dependencies specification
- **Location**: `/requirements.txt`
- **Contents**:
  - Django 4.2.7 - Web framework
  - psycopg2-binary - PostgreSQL database driver
  - Pillow - Image processing
  - python-dotenv - Environment variable management
  - django-filter - Advanced filtering
  - django-crispy-forms - Form styling
  - crispy-bootstrap5 - Bootstrap integration

### `.env` & `.env.example`
**Purpose**: Environment configuration files
- **Location**: `/.env` (actual config), `/.env.example` (template)
- **Contains**:
  - Database connection settings
  - Django SECRET_KEY
  - DEBUG mode setting
  - Static/media file paths

### `setup.sh`
**Purpose**: Automated project setup script
- **Location**: `/setup.sh`
- **Functions**:
  - Creates virtual environment
  - Installs Python packages
  - Creates necessary directories
  - Runs database migrations
  - Collects static files

---

## ⚙️ Configuration Directory (`config/`)

### `config/__init__.py`
**Purpose**: Marks directory as Python package
- **Location**: `config/__init__.py`
- **Contents**: Empty file (required for Python package)

### `config/settings.py`
**Purpose**: Main Django configuration file
- **Location**: `config/settings.py`
- **Key Sections**:
  - **Installed Apps**: Lists all Django apps (core, users, marketplace, etc.)
  - **Database**: PostgreSQL connection settings
  - **Static/Media Files**: File handling configuration
  - **Templates**: Template engine settings
  - **Authentication**: User model and auth settings
  - **Logging**: Error and debug logging configuration

### `config/urls.py`
**Purpose**: URL routing configuration
- **Location**: `config/urls.py`
- **Contents**:
  - Admin panel URL (`/admin/`)
  - Homepage URL (`/`)
  - App-specific URL includes (users, marketplace, messaging, etc.)
  - Static/media file serving in development

### `config/wsgi.py`
**Purpose**: WSGI configuration for production deployment
- **Location**: `config/wsgi.py`
- **Purpose**: Entry point for WSGI-compatible web servers (Apache, Nginx, etc.)
- **Usage**: Used when deploying to production servers

### `config/asgi.py`
**Purpose**: ASGI configuration for async deployment
- **Location**: `config/asgi.py`
- **Purpose**: Entry point for ASGI-compatible web servers (Daphne, Uvicorn)
- **Usage**: For async features and WebSocket support

---

## 📱 Django Apps

### Core App (`core/`)

#### `core/__init__.py`
**Purpose**: Marks core directory as Python package

#### `core/apps.py`
**Purpose**: App configuration
- **Location**: `core/apps.py`
- **Contents**: CoreConfig class defining app settings

#### `core/models.py`
**Purpose**: Database models for core functionality
- **Location**: `core/models.py`
- **Current**: Empty (models will be added as needed)

#### `core/views.py`
**Purpose**: View functions for core pages
- **Location**: `core/views.py`
- **Current**: Empty (views will be added as needed)

#### `core/urls.py`
**Purpose**: URL patterns for core app
- **Location**: `core/urls.py`
- **Current**: Empty (URLs will be added as needed)

#### `core/admin.py`
**Purpose**: Django admin configuration
- **Location**: `core/admin.py`
- **Current**: Empty (admin registrations will be added)

#### `core/templates/base.html`
**Purpose**: Master template inherited by all pages
- **Location**: `core/templates/base.html`
- **Features**:
  - Bootstrap 5 CSS/JS includes
  - Navigation bar
  - Message display area
  - Footer
  - Block placeholders for content

#### `core/templates/navbar.html`
**Purpose**: Navigation bar component
- **Location**: `core/templates/navbar.html`
- **Features**:
  - Brand logo/link
  - Navigation links (Browse Items, Sell Item, Messages, etc.)
  - User authentication status
  - User dropdown menu

#### `core/templates/index.html`
**Purpose**: Homepage template
- **Location**: `core/templates/index.html`
- **Features**:
  - Hero section
  - Featured items preview
  - Call-to-action buttons
  - Site description

#### `core/static/css/main.css`
**Purpose**: Custom CSS styles
- **Location**: `core/static/css/main.css`
- **Contents**:
  - Color variables
  - Responsive design rules
  - Component styling
  - Custom classes

#### `core/static/js/main.js`
**Purpose**: Custom JavaScript functionality
- **Location**: `core/static/js/main.js`
- **Contents**:
  - Interactive features
  - Form enhancements
  - AJAX calls (to be added)

---

### Users App (`users/`)

#### `users/models.py`
**Purpose**: User-related database models
- **Location**: `users/models.py`
- **Future Contents**: UserProfile, SellerProfile models

#### `users/views.py`
**Purpose**: User authentication views
- **Location**: `users/views.py`
- **Current**: Stub functions (login, register, profile, etc.)
- **Future**: Full authentication implementation

#### `users/urls.py`
**Purpose**: URL patterns for user pages
- **Location**: `users/urls.py`
- **Routes**:
  - `/users/login/` - Login page
  - `/users/register/` - Registration page
  - `/users/profile/` - User profile
  - `/users/profile/edit/` - Edit profile

#### `users/forms.py` (Future)
**Purpose**: User-related forms
- **Future Contents**: RegistrationForm, ProfileForm, etc.

---

### Marketplace App (`marketplace/`)

#### `marketplace/models.py`
**Purpose**: Item and category models
- **Location**: `marketplace/models.py`
- **Future Contents**: Item, Category, ItemImage models

#### `marketplace/views.py`
**Purpose**: Item CRUD operations
- **Location**: `marketplace/views.py`
- **Current**: Stub functions
- **Future**: List, create, edit, delete item views

#### `marketplace/urls.py`
**Purpose**: URL patterns for marketplace
- **Location**: `marketplace/urls.py`
- **Routes**:
  - `/marketplace/` - Item list
  - `/marketplace/create/` - Create item
  - `/marketplace/<id>/` - Item detail
  - `/marketplace/<id>/edit/` - Edit item

#### `marketplace/forms.py` (Future)
**Purpose**: Item-related forms
- **Future Contents**: ItemForm, SearchForm, etc.

---

### Messaging App (`messaging/`)

#### `messaging/models.py`
**Purpose**: Message and conversation models
- **Location**: `messaging/models.py`
- **Future Contents**: Message, Conversation models

#### `messaging/views.py`
**Purpose**: Messaging functionality
- **Location**: `messaging/views.py`
- **Current**: Stub functions
- **Future**: Inbox, conversation, send message views

#### `messaging/urls.py`
**Purpose**: URL patterns for messaging
- **Location**: `messaging/urls.py`
- **Routes**:
  - `/messaging/inbox/` - Message inbox
  - `/messaging/conversation/<user_id>/` - Conversation view

---

### Transactions App (`transactions/`)

#### `transactions/models.py`
**Purpose**: Transaction and payment models
- **Location**: `transactions/models.py`
- **Future Contents**: Transaction, Payment models

#### `transactions/views.py`
**Purpose**: Transaction management
- **Location**: `transactions/views.py`
- **Current**: Stub functions
- **Future**: Transaction list, detail, create views

#### `transactions/urls.py`
**Purpose**: URL patterns for transactions
- **Location**: `transactions/urls.py`
- **Routes**:
  - `/transactions/` - Transaction list
  - `/transactions/<id>/` - Transaction detail

---

### Reviews App (`reviews/`)

#### `reviews/models.py`
**Purpose**: Review and rating models
- **Location**: `reviews/models.py`
- **Future Contents**: Review, Rating models

#### `reviews/views.py`
**Purpose**: Review functionality
- **Location**: `reviews/views.py`
- **Current**: Stub functions
- **Future**: Create, view, delete review views

#### `reviews/urls.py`
**Purpose**: URL patterns for reviews
- **Location**: `reviews/urls.py`
- **Routes**:
  - `/reviews/create/<item_id>/` - Create review
  - `/reviews/<id>/` - Review detail

---

## 📁 Directory Structure

### Static Files (`staticfiles/`)
**Purpose**: Collected static files for production
- **Location**: `/staticfiles/`
- **Contents**: CSS, JS, images served by web server
- **Created by**: `python manage.py collectstatic`

### Media Files (`media/`)
**Purpose**: User-uploaded files (images, documents)
- **Location**: `/media/`
- **Subdirectories**:
  - `listings/` - Item photos
  - `profiles/` - User profile pictures

### Logs (`logs/`)
**Purpose**: Application log files
- **Location**: `/logs/`
- **Files**:
  - `debug.log` - Debug information
  - `django.log` - Django system logs

### Virtual Environment (`venv/`)
**Purpose**: Isolated Python environment
- **Location**: `/venv/`
- **Contents**: Python interpreter and installed packages
- **Created by**: `python3 -m venv venv`

---

## 📋 File Status Overview

| File Type | Status | Notes |
|-----------|--------|-------|
| Configuration | ✅ Complete | All Django settings configured |
| Templates | ✅ Complete | Base templates with Bootstrap 5 |
| Static Files | ✅ Complete | CSS and JS ready |
| URL Routing | ✅ Complete | All apps have URL patterns |
| Database | ✅ Complete | PostgreSQL configured and migrated |
| Views | ⚠️ Stub | Placeholder functions (to be implemented) |
| Models | ❌ Empty | No custom models yet (Phase 2+) |
| Forms | ❌ Missing | No forms yet (Phase 2+) |
| Tests | ❌ Missing | No tests yet (future phases) |

---

## 🚀 Development Workflow

### Starting Development
1. **Activate virtual environment**: `source venv/bin/activate`
2. **Run server**: `python manage.py runserver`
3. **Access site**: `http://localhost:8000/`

### Making Changes
1. **Edit models** in `app/models.py`
2. **Create migrations**: `python manage.py makemigrations`
3. **Apply migrations**: `python manage.py migrate`
4. **Create views** in `app/views.py`
5. **Add URLs** in `app/urls.py`
6. **Create templates** in `app/templates/`

### Database Operations
- **View data**: Visit `/admin/` (requires superuser)
- **Reset database**: Delete `db.sqlite3`, run `migrate`
- **Backup data**: Use `dumpdata` and `loaddata` commands

---

## 📚 Key Concepts

### Django MTV Pattern
- **Model**: Database structure (`models.py`)
- **Template**: HTML presentation (`templates/`)
- **View**: Business logic (`views.py`)

### URL Dispatch
- **urls.py**: Maps URLs to views
- **Namespace**: `app_name` prevents URL conflicts
- **Named URLs**: Used in templates with `{% url %}`

### Static vs Media Files
- **Static**: App assets (CSS, JS) - managed by Django
- **Media**: User uploads - served directly by web server

### Environment Variables
- **Security**: Keep secrets out of code
- **Flexibility**: Different settings for dev/prod
- **Management**: Use `python-dotenv` for loading

---

**Last Updated**: November 5, 2025
**Phase**: 1 Complete (Setup & Configuration)
**Next Phase**: 2 (User Authentication)