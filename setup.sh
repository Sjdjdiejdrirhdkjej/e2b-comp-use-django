#!/bin/bash

# Django AI Chat - Daytona Sandbox Setup Script
# This script sets up the Django AI Chat application in a Daytona sandbox

set -e

echo "🚀 Setting up Django AI Chat in Daytona Sandbox..."
echo "=================================================="

# Check if we're in a Daytona environment
if [ -z "$DAYTONA_ENVIRONMENT" ]; then
    echo "⚠️  Warning: Not running in Daytona environment, but continuing anyway..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "🔑 IMPORTANT: Edit .env file and add your GOOGLE_API_KEY"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo ""
echo "👤 Would you like to create a Django superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Test AI tools
echo ""
echo "🧪 Testing AI tools functionality..."
python comprehensive_test.py

echo ""
echo "✅ Setup completed successfully!"
echo "=================================="
echo ""
echo "🌐 To start the application:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "📱 The application will be available at:"
echo "   http://localhost:8000/chat/"
echo ""
echo "🤖 AI Commands available:"
echo "   read file:/path/to/file.txt"
echo "   write file:/path/to/file.txt content:Your text"
echo "   delete file:/path/to/file.txt"
echo "   list files:/path/to/directory"
echo "   search web:your query here"
echo ""
echo "📚 For more information, see AI_TOOLS_DOCUMENTATION.md"
echo ""
echo "🎉 Happy coding with AI Chat!"