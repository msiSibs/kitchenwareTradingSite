# Kitchenware Marketplace - Project Structure

## Directory Layout

```
kitchenware_marketplace/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── config/                          # Project settings & configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/                           # User authentication & profiles
│   ├── migrations/
│   ├── templates/
│   │   ├── users/
│   │   │   ├── register.html
│   │   │   ├── login.html
│   │   │   ├── profile.html
│   │   │   ├── edit_profile.html
│   │   │   └── seller_profile.html
│   ├── static/
│   │   └── users/
│   │       └── profile_styles.css
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests.py
│
├── marketplace/                     # Core marketplace functionality
│   ├── migrations/
│   ├── templates/
│   │   ├── marketplace/
│   │   │   ├── index.html
│   │   │   ├── listing_detail.html
│   │   │   ├── listing_create.html
│   │   │   ├── listing_edit.html
│   │   │   ├── listing_list.html
│   │   │   ├── search_results.html
│   │   │   └── dashboard.html
│   ├── static/
│   │   └── marketplace/
│   │       ├── marketplace_styles.css
│   │       └── marketplace_scripts.js
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── filters.py
│   └── tests.py
│
├── messaging/                       # Messaging system
│   ├── migrations/
│   ├── templates/
│   │   ├── messaging/
│   │   │   ├── inbox.html
│   │   │   ├── conversation.html
│   │   │   └── message_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests.py
│
├── transactions/                    # Purchase history & status
│   ├── migrations/
│   ├── templates/
│   │   ├── transactions/
│   │   │   ├── transaction_list.html
│   │   │   ├── transaction_detail.html
│   │   │   └── checkout.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests.py
│
├── reviews/                         # Ratings & reviews
│   ├── migrations/
│   ├── templates/
│   │   └── reviews/
│   │       └── review_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── tests.py
│
├── core/                            # Shared utilities & templates
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   └── navbar.html
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   └── js/
│   │       └── main.js
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── context_processors.py
│   └── tests.py
│
├── static/                          # Global static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                           # User-uploaded files
│   └── listings/
│
└── tests/                           # Test configuration
    ├── conftest.py
    └── test_*.py
```

---

## App Organization

### `config/` - Project Configuration
Core Django settings and URL routing. This is the central hub for project-wide configuration.

**Key Files**:
- `settings.py` - Database, installed apps, middleware, static files
- `urls.py` - Main URL dispatcher routes to app URLs
- `wsgi.py` / `asgi.py` - Production server entry points

---

### `users/` - User Management
Handles user authentication, registration, login, and profile management.

**Responsibilities**:
- User registration and validation
- Login/logout functionality
- User profile CRUD
- Seller profile display
- Email verification (optional)

**Key Files**:
- `models.py` - `UserProfile` model with seller info
- `views.py` - `RegisterView`, `LoginView`, `ProfileView`, etc.
- `forms.py` - Registration and profile forms
- `templates/` - Registration, login, profile pages

---

### `marketplace/` - Core Listing Functionality
Central app for item listings - the core of the marketplace.

**Responsibilities**:
- Item CRUD operations
- Category management
- Image handling
- Item filtering and search
- Seller dashboard

**Key Files**:
- `models.py` - `Item`, `Category`, `ItemImage` models
- `views.py` - Listing views (list, detail, create, edit, delete)
- `forms.py` - Item creation/editing forms
- `filters.py` - Search and filter logic
- `templates/` - Listing pages and forms
- `admin.py` - Admin customization

---

### `messaging/` - Communication System
Direct messaging between buyers and sellers.

**Responsibilities**:
- Create and manage conversations
- Send and receive messages
- Display inbox and conversation threads
- Track message read status

**Key Files**:
- `models.py` - `Conversation`, `Message` models
- `views.py` - `InboxView`, `ConversationDetailView`, `SendMessageView`
- `forms.py` - Message form
- `templates/` - Inbox and conversation pages

---

### `transactions/` - Purchase Management
Tracks all transactions and purchase status.

**Responsibilities**:
- Create transactions from purchases
- Track transaction status
- Purchase history for buyers and sellers
- Transaction confirmation workflow

**Key Files**:
- `models.py` - `Transaction` model with status tracking
- `views.py` - Transaction list, detail, and checkout views
- `forms.py` - Purchase confirmation forms
- `templates/` - Purchase history and transaction details

---

### `reviews/` - Ratings & Reviews
User feedback and trust system.

**Responsibilities**:
- Create reviews after transactions
- Rate sellers (1-5 stars)
- Display reviews on seller profiles
- Calculate average ratings

**Key Files**:
- `models.py` - `Review` model with ratings
- `views.py` - Review creation and editing views
- `forms.py` - Review creation form
- `templates/` - Review forms and display

---

### `core/` - Shared Components
Reusable utilities and base templates used across all apps.

**Responsibilities**:
- Base template with navigation
- Global static files (CSS, JS)
- Shared utility functions
- Context processors for template data
- Error pages (404, 500)

**Key Files**:
- `templates/base.html` - Main template inherited by all pages
- `templates/navbar.html` - Navigation component
- `static/css/main.css` - Global styles
- `static/js/main.js` - Global JavaScript
- `context_processors.py` - Template context helpers

---

## Key Files Reference

### Configuration Files
| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Template for environment variables |
| `.gitignore` | Git ignore patterns |
| `config/settings.py` | Django settings |
| `config/urls.py` | URL routing |

### Models Files (Core Data)
| App | File | Contains |
|-----|------|----------|
| `users` | `models.py` | `UserProfile` |
| `marketplace` | `models.py` | `Item`, `Category`, `ItemImage` |
| `messaging` | `models.py` | `Conversation`, `Message` |
| `transactions` | `models.py` | `Transaction` |
| `reviews` | `models.py` | `Review` |

### Views Files (Business Logic)
Each app has a `views.py` containing class-based or function-based views for handling requests.

### Templates Organization
Templates are organized by app and inherited from `core/templates/base.html`:
```
templates/
├── base.html                    (root template)
├── navbar.html                  (nav component)
├── 404.html / 500.html          (error pages)
├── users/
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   └── ...
├── marketplace/
│   ├── index.html
│   ├── listing_detail.html
│   └── ...
├── messaging/
│   ├── inbox.html
│   └── ...
└── ...
```

### Static Files Organization
```
static/
├── css/
│   └── main.css                 (global styles)
├── js/
│   └── main.js                  (global scripts)
└── images/                      (logos, icons, etc.)

users/static/users/
├── profile_styles.css

marketplace/static/marketplace/
├── marketplace_styles.css
└── marketplace_scripts.js
```

### Media Files
```
media/
└── listings/                    (user-uploaded item images)
    ├── item_id_1.jpg
    ├── item_id_2.jpg
    └── ...
```

---

## Django Project Structure Best Practices

### App Naming Conventions
- Use **lowercase, plural names** where applicable: `users`, `items`, `messages`
- Keep names **concise and descriptive**
- One app = One responsibility (Single Responsibility Principle)

### File Organization Within Apps
```
app_name/
├── migrations/          (database schema changes)
├── templates/           (HTML files - django/app_name/)
├── static/              (CSS, JS, images - app_name/)
├── __init__.py          (makes it a Python package)
├── admin.py             (Django admin configuration)
├── apps.py              (app configuration)
├── forms.py             (ModelForm classes)
├── models.py            (database models)
├── urls.py              (app-level URL routing)
├── views.py             (request handlers)
├── tests.py             (unit tests)
└── (optional: filters.py, signals.py, managers.py)
```

### URL Structure (Hierarchy)
```
config/urls.py          (main router)
├── users/urls.py       (/users/)
├── marketplace/urls.py (/marketplace/)
├── messaging/urls.py   (/messaging/)
├── transactions/urls.py(/transactions/)
└── reviews/urls.py     (/reviews/)
```

---

## Getting Started with Project Structure

1. **Create the Django project**:
   ```bash
   django-admin startproject config .
   ```

2. **Create each app**:
   ```bash
   python manage.py startapp users
   python manage.py startapp marketplace
   python manage.py startapp messaging
   python manage.py startapp transactions
   python manage.py startapp reviews
   python manage.py startapp core
   ```

3. **Configure settings.py**:
   - Add apps to `INSTALLED_APPS`
   - Configure database (PostgreSQL)
   - Set up media and static file directories

4. **Create directory structure manually**:
   - Create `templates/` in each app
   - Create `static/` in each app
   - Create `migrations/` directories

---

**Last Updated**: November 2025  
**Version**: 1.0
