#!/bin/bash
# Setup script for Kitchenware Marketplace
# Compatible with python3 and pip3

set -e

echo "🚀 Setting up Kitchenware Marketplace..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ Pip3 found: $(pip3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip3..."
pip3 install --upgrade pip setuptools wheel

# Install requirements
echo "📦 Installing requirements..."
pip3 install -r requirements.txt

# Create directories first (before migrations)
echo ""
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p media/listings
mkdir -p staticfiles

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your database credentials"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python3 manage.py migrate

# Collect static files
echo ""
echo "📦 Collecting static files..."
python3 manage.py collectstatic --noinput

# Create superuser prompt
echo ""
echo "👤 Create Django superuser (admin account)"
echo "Run: python3 manage.py createsuperuser"
echo ""

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development server, run:"
echo "   source venv/bin/activate"
echo "   python3 manage.py runserver"
echo ""
echo "� First time? Create a superuser:"
echo "   python3 manage.py createsuperuser"
echo ""
echo "�📖 Documentation:"
echo "   - GETTING_STARTED.md - Setup instructions"
echo "   - PROJECT_OVERVIEW.md - Project goals and features"
echo "   - PROJECT_STRUCTURE.md - App organization"
echo "   - DEVELOPMENT_PLAN.md - Phase-by-phase implementation"
