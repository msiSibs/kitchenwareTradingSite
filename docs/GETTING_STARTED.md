# Getting Started with Kitchenware Marketplace

This guide covers setup and initial run for the Kitchenware Marketplace project using `python3` and `pip3`.

## Prerequisites

Make sure you have the following installed:
- **Python 3.8+** - Check with: `python3 --version`
- **pip3** - Check with: `pip3 --version`
- **PostgreSQL** (optional, but recommended) or SQLite (default)
- **Git** (for version control)

## Automated Setup (Recommended)

If you're on macOS or Linux, use the automated setup script:

```bash
cd /Users/msisibanyoni/VSProjects/kitchenwareTradingSite
chmod +x setup.sh
./setup.sh
```

This script will:
1. ✅ Check for python3 and pip3
2. ✅ Create a virtual environment
3. ✅ Install all dependencies
4. ✅ Create `.env` file
5. ✅ Run database migrations
6. ✅ Create necessary directories
7. ✅ Collect static files

Then skip to **Step 4: Create Superuser** below.

---

## Manual Setup (Step-by-Step)

### Step 1: Create Virtual Environment

```bash
cd /Users/msisibanyoni/VSProjects/kitchenwareTradingSite
python3 -m venv venv
```

This creates a `venv` directory with an isolated Python environment.

### Step 2: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt when activated.

### Step 3: Install Dependencies

Upgrade pip first:
```bash
pip3 install --upgrade pip setuptools wheel
```

Then install all requirements:
```bash
pip3 install -r requirements.txt
```

This installs:
- Django 4.2.7
- psycopg2-binary (PostgreSQL driver)
- Pillow (image processing)
- django-crispy-forms (form styling)
- crispy-bootstrap5 (Bootstrap integration)
- django-filter (advanced search)
- python-dotenv (environment variables)

### Step 4: Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

**For SQLite (Development - No Setup Needed):**
```
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**For PostgreSQL (Production Ready):**
```
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=kitchenware_db
DB_USER=postgres
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Set Up Database

**Option A: PostgreSQL Setup (macOS)**

```bash
# Install PostgreSQL if not already installed
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb kitchenware_db

# Create user (if needed)
psql -U postgres -c "CREATE USER postgres WITH PASSWORD 'your-password';"
```

**Option B: SQLite (Default - No Setup Needed)**

SQLite will automatically create `db.sqlite3` on first migration.

### Step 6: Run Database Migrations

```bash
python3 manage.py migrate
```

Output should show:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 7: Create Directories

```bash
mkdir -p logs
mkdir -p media/listings
mkdir -p staticfiles
```

### Step 8: Collect Static Files

```bash
python3 manage.py collectstatic --noinput
```

### Step 9: Create Superuser (Admin Account)

```bash
python3 manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

### Step 10: Run Development Server

```bash
python3 manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🌐 Access the Application

Once the server is running:

- **Homepage**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
  - Login with your superuser credentials

---

## Useful Commands

### Virtual Environment

```bash
# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Check installed packages
pip3 list

# Freeze installed packages
pip3 freeze > requirements.txt
```

### Django Management

```bash
# Run development server
python3 manage.py runserver

# Run on specific port
python3 manage.py runserver 8080

# Create database migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Access Django shell
python3 manage.py shell

# Collect static files
python3 manage.py collectstatic

# Run tests
python3 manage.py test

# Check project for issues
python3 manage.py check
```

### Database

```bash
# Create database (PostgreSQL)
createdb kitchenware_db

# Drop database (PostgreSQL)
dropdb kitchenware_db

# Connect to database (PostgreSQL)
psql kitchenware_db

# List all databases (PostgreSQL)
psql -l
```

---

## Troubleshooting

### Issue: `python3: command not found`
**Solution**: Install Python 3 from https://www.python.org or use Homebrew:
```bash
brew install python3
```

### Issue: `pip3: command not found`
**Solution**: Install pip with:
```bash
python3 -m pip install --upgrade pip
```

### Issue: `ModuleNotFoundError: No module named 'django'`
**Solution**: Make sure virtual environment is activated and run:
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

### Issue: `FATAL: Ident authentication failed for user "postgres"`
**Solution**: Edit `pg_hba.conf` or use SQLite for development:
```
DB_ENGINE=django.db.backends.sqlite3
```

### Issue: `Port 8000 already in use`
**Solution**: Run on different port:
```bash
python3 manage.py runserver 8080
```

### Issue: `django.db.utils.OperationalError: no such table`
**Solution**: Run migrations:
```bash
python3 manage.py migrate
```

---

## Next Steps

1. ✅ Virtual environment created and activated
2. ✅ Dependencies installed
3. ✅ Database configured
4. ✅ Superuser created
5. ✅ Development server running

**You're ready to start development!**

### Phase 1 Complete! 🎉

Next: **Read DEVELOPMENT_PLAN.md** to understand the project phases

---

## Documentation Files

- **PROJECT_OVERVIEW.md** - Project goals, features, and tech stack
- **PROJECT_STRUCTURE.md** - App organization and file layout
- **DEVELOPMENT_PLAN.md** - Detailed phase-by-phase implementation
- **PHASE_1_SETUP.md** - Phase 1 completion details

---

**Last Updated**: November 5, 2025  
**Compatible With**: Python 3.8+, pip3, macOS/Linux/Windows
