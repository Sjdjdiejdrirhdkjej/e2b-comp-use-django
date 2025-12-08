# AI Tools Integration Documentation

## Overview
Your Django chat application now includes powerful AI tools that allow users to interact with files and perform web searches directly through the chat interface.

## Available AI Commands

### 📁 File Operations

#### Read a File
```
read file:/path/to/file.txt
```
- Reads and displays the contents of a file
- Supports any text file format
- Restricted to project workspace for security

#### Write to a File
```
write file:/path/to/file.txt content:Your text here
```
- Creates or overwrites a file with specified content
- Automatically creates directories if they don't exist
- Supports multi-line content

#### Delete a File
```
delete file:/path/to/file.txt
```
- Permanently deletes a file
- Includes safety confirmation

#### List Directory Contents
```
list files:/path/to/directory
```
- Shows all files and subdirectories in a specified path
- Distinguishes between files and directories

### 🌐 Web Search

#### Search the Web
```
search web:your query here
```
- Performs web search using DuckDuckGo API
- Returns relevant search results
- No API key required

## Security Features

✅ **Path Restriction**: All file operations are limited to `/project/workspace/`  
✅ **Input Validation**: Commands are parsed and validated before execution  
✅ **Error Handling**: Comprehensive error messages for invalid operations  
✅ **Permission Checks**: Respects file system permissions  

## Integration Points

### Backend Changes
- **`chat/ai_utils.py`**: Added AI command parsing and execution functions
- **`chat/views.py`**: Integrated command execution in message handling
- **`requirements.txt`**: Added `requests` library for web search

### Frontend Changes
- **`templates/chat/conversation_detail.html`**: Added help section showing available commands

## Usage Examples

### Example 1: Project Documentation
```
User: write file:/project/workspace/README.md content:# My Project
This is my awesome project description.
```

### Example 2: Code Analysis
```
User: read file:/project/workspace/chat/views.py
```

### Example 3: Research
```
User: search web:Python Django best practices
```

### Example 4: File Management
```
User: list files:/project/workspace/chat/templates
```

## Error Handling

The system provides clear error messages for:
- File not found
- Permission denied
- Invalid paths
- Network errors
- Malformed commands

## Testing

Run the comprehensive test suite:
```bash
python comprehensive_test.py
```

This will test all AI tools functionality and verify security restrictions.

## Future Enhancements

Potential additions could include:
- File append operations
- Directory creation
- File copy/move operations
- More advanced web search options
- File upload/download through the interface

## Technical Implementation

The AI tools work by:
1. Intercepting user messages in the chat interface
2. Parsing messages for command patterns using regex
3. Executing corresponding Python functions
4. Returning results as chat responses
5. Falling back to regular AI chat if no command is detected

This seamless integration allows users to perform file operations and web searches without leaving the chat interface.