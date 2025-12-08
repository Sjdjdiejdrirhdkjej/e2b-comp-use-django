# 🚀 Daytona Sandbox Deployment Guide

## Quick Start

### 1. Using Daytona CLI (Recommended)

```bash
# Create a new Daytona workspace
daytona create --code https://github.com/your-repo/django-ai-chat

# Or clone and run locally
git clone <repository-url>
cd django-ai-chat
daytona code
```

### 2. Manual Setup in Any Environment

```bash
# Clone the repository
git clone <repository-url>
cd django-ai-chat

# Run the setup script
./setup.sh

# Start the application
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

## Environment Configuration

### Required Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your Google API Key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

## Accessing the Application

Once running, access the application at:
- **Main App**: `http://localhost:8000/chat/`
- **Admin Panel**: `http://localhost:8000/admin/`

## AI Commands

The chat interface supports these AI commands:

### File Operations
- `read file:/path/to/file.txt` - Read file contents
- `write file:/path/to/file.txt content:Your text` - Write to file
- `delete file:/path/to/file.txt` - Delete a file
- `list files:/path/to/directory` - List directory contents

### Web Search
- `search web:your query here` - Search the web

## Features

✅ **AI Chat**: Powered by Google Gemini  
✅ **File Operations**: Read, write, delete, list files  
✅ **Web Search**: Integrated search functionality  
✅ **Security**: Restricted to project workspace  
✅ **Mobile Responsive**: Works on all devices  
✅ **Real-time**: Instant AI responses  

## Testing

Run the comprehensive test suite:

```bash
python comprehensive_test.py
```

## Docker Support

For containerized deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t django-ai-chat .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key django-ai-chat
```

## Project Structure

```
django-ai-chat/
├── chat/                    # Main Django app
│   ├── ai_utils.py         # AI tools functionality
│   ├── models.py           # Database models
│   ├── views.py            # Main views
│   └── templates/          # HTML templates
├── aichat/                # Django project settings
├── staticfiles/           # Collected static files
├── venv/                 # Virtual environment
├── setup.sh              # Automated setup script
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image definition
├── daytona.json         # Daytona configuration
└── requirements.txt      # Python dependencies
```

## Security Features

- 🔒 File operations restricted to `/project/workspace/`
- 🛡️ Input validation and sanitization
- 🔐 CSRF protection enabled
- 🚫 No shell command execution
- ✅ Comprehensive error handling

## Troubleshooting

### Common Issues

1. **Google API Key Error**
   - Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
   - Get a key from https://makersuite.google.com/app/apikey

2. **Port Already in Use**
   ```bash
   # Kill existing processes
   pkill -f "python manage.py runserver"
   # Or use different port
   python manage.py runserver 0.0.0.0:8001
   ```

3. **Database Issues**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   ```

4. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Development

### Adding New AI Commands

1. Add command parsing in `chat/ai_utils.py` in `execute_ai_command()`
2. Implement the functionality as a separate function
3. Add tests in `comprehensive_test.py`

### Customization

- **AI Model**: Modify `chat/ai_utils.py` to use different models
- **UI Theme**: Edit templates in `chat/templates/`
- **Security**: Adjust path restrictions in file operation functions

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `aichat/settings.py`
2. Configure proper database (PostgreSQL recommended)
3. Set up production web server (Gunicorn + Nginx)
4. Configure environment variables securely
5. Set up SSL/TLS certificates

## Support

- 📖 Documentation: `AI_TOOLS_DOCUMENTATION.md`
- 🧪 Testing: `comprehensive_test.py`
- 🐳 Docker: `docker-compose.yml`
- ☁️ Daytona: `daytona.json`

---

**🎉 Your Django AI Chat is ready to use in Daytona sandbox!**