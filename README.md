# Django AI Chat Application

A powerful Django chat application with integrated AI tools for file operations and web search.

## Features

- 🤖 AI-powered chat using Google Gemini
- 📁 File operations (read, write, delete, list)
- 🌐 Web search capabilities
- 📱 Responsive mobile-friendly interface
- 🔒 Security-restricted file access

## Quick Start with Daytona

### Prerequisites
- Daytona CLI installed

### Launch the Sandbox
```bash
daytona create --code https://github.com/your-repo/django-ai-chat
```

### Setup Instructions
1. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. **Access the application:**
   - Open your browser and navigate to the Daytona-provided URL
   - The app will be available at `/chat/`

## AI Commands

### File Operations
- `read file:/path/to/file.txt` - Read file contents
- `write file:/path/to/file.txt content:Your text` - Write to file
- `delete file:/path/to/file.txt` - Delete a file
- `list files:/path/to/directory` - List directory contents

### Web Search
- `search web:your query here` - Search the web

## Security

All file operations are restricted to the project workspace for security. The application includes comprehensive input validation and error handling.

## Testing

Run the comprehensive test suite:
```bash
python comprehensive_test.py
```

## Development

This application is designed to run seamlessly in Daytona sandbox environments with all dependencies pre-configured.