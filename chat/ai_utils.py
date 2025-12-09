import os
import json
import requests
import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def get_ai_response(messages):
    import time

    max_retries = 5
    base_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            if len(messages) > 1:
                history = messages[:-1]
                last_message = messages[-1]["parts"]
            else:
                history = []
                last_message = messages[0]["parts"] if messages else "Hello"

            # Check if this is a complex task that would benefit from tools
            tool_suggestion = analyze_task_for_tools(last_message)
            if tool_suggestion:
                # Check if this involves user preferences or keys - these should ask for confirmation
                message_lower = last_message.lower()
                sensitive_operations = [
                    "preference",
                    "setting",
                    "config",
                    "key",
                    "password",
                    "secret",
                    "token",
                    "api key",
                    "credential",
                    "auth",
                    "authentication",
                ]

                is_sensitive = any(
                    keyword in message_lower for keyword in sensitive_operations
                )

                if is_sensitive:
                    system_prompt = f"""You are an AI assistant with access to powerful tools. The user's request appears to involve sensitive operations (preferences, keys, or authentication).

Available tools (Secure Daytona Sandbox Operations):
- read file:/path/to/file.txt - Read file contents securely
- write file:/path/to/file.txt content:your content - Write to file securely  
- delete file:/path/to/file.txt - Delete a file securely
- list files:/path/to/directory - List directory contents securely
- info file:/path/to/file.txt - Get file information securely
- run code:your python code - Execute Python code securely
- search web:your query - Search the web for information

User request: {last_message}

Please respond naturally and use the appropriate tool if needed. Be helpful but cautious with sensitive operations."""
                else:
                    system_prompt = f"""You are an AI assistant with access to powerful tools for file operations, code execution, and web search.

Available tools (Secure Daytona Sandbox Operations):
- read file:/path/to/file.txt - Read file contents securely
- write file:/path/to/file.txt content:your content - Write to file securely  
- delete file:/path/to/file.txt - Delete a file securely
- list files:/path/to/directory - List directory contents securely
- info file:/path/to/file.txt - Get file information securely
- run code:your python code - Execute Python code securely
- search web:your query - Search the web for information

User request: {last_message}

Please respond naturally and use the appropriate tool if needed. Be helpful and efficient."""

                response = model.generate_content(system_prompt)

                # Check if the AI response contains tool commands and execute them
                ai_response = response.text
                executed_result = execute_tool_commands_from_response(ai_response)

                if executed_result:
                    return executed_result, True
                else:
                    return ai_response, True
            else:
                chat = model.start_chat(history=history)
                response = chat.send_message(last_message)
                return response.text, False

        except Exception as e:
            error_str = str(e).lower()

            # Check if it's a rate limit error
            if any(
                keyword in error_str
                for keyword in ["rate limit", "quota", "too many requests", "429"]
            ):
                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    delay = base_delay * (2**attempt)
                    time.sleep(delay)
                    continue
                else:
                    # All retries failed, return user-friendly message
                    return (
                        "I'm experiencing some technical difficulties right now. Please try again in a few moments.",
                        False,
                    )
            else:
                # Non-rate-limit error, return immediately
                return f"Error: {str(e)}", False

    # This should not be reached, but just in case
    return (
        "I'm experiencing some technical difficulties right now. Please try again in a few moments.",
        False,
    )


def generate_conversation_title(first_user_message):
    import time

    max_retries = 5
    base_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            prompt = f"""Generate a short, descriptive title (max 5 words) for a conversation that starts with this message: "{first_user_message}"
            
            Rules:
            - Maximum 5 words
            - No quotes or special characters
            - Descriptive and concise
            - Use title case
            Examples:
            "Python debugging help" -> "Python Debugging Session"
            "Recipe for chocolate cake" -> "Chocolate Cake Recipe"
            "Help with math homework" -> "Math Homework Help"
            """

            response = model.generate_content(prompt)
            title = response.text.strip()

            # Clean up the title
            title = title.strip("\"'").strip()
            if len(title.split()) > 5:
                title = " ".join(title.split()[:5])

            return title if title else "New Chat"

        except Exception as e:
            error_str = str(e).lower()

            # Check if it's a rate limit error
            if any(
                keyword in error_str
                for keyword in ["rate limit", "quota", "too many requests", "429"]
            ):
                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    delay = base_delay * (2**attempt)
                    time.sleep(delay)
                    continue
                else:
                    # All retries failed, return default title
                    return "New Chat"
            else:
                # Non-rate-limit error, return default title immediately
                return "New Chat"

    # This should not be reached, but just in case
    return "New Chat"


def format_messages_for_gemini(conversation_messages):
    messages = []
    for msg in conversation_messages:
        role = "user" if msg.is_user else "model"
        messages.append({"role": role, "parts": msg.content})
    return messages


# Import secure Daytona operations
try:
    from .secure_daytona_ops import secure_daytona_ops
except ImportError:
    # Fallback for direct execution
    from chat.secure_daytona_ops import secure_daytona_ops


def read_file(file_path):
    """Read content from a file using secure Daytona operations"""
    return secure_daytona_ops.read_file(file_path)


def write_file(file_path, content):
    """Write content to a file using secure Daytona operations"""
    return secure_daytona_ops.write_file(file_path, content)


def delete_file(file_path):
    """Delete a file using secure Daytona operations"""
    return secure_daytona_ops.delete_file(file_path)


def list_files(directory_path):
    """List files and directories using secure Daytona operations"""
    return secure_daytona_ops.list_files(directory_path)


def get_file_info(file_path):
    """Get file information using secure Daytona operations"""
    return secure_daytona_ops.get_file_info(file_path)


def execute_code(code, language="python"):
    """Execute code securely using Daytona sandbox"""
    return secure_daytona_ops.execute_code(code, language)


def web_search(query, num_results=5):
    """Perform web search using a free API"""
    try:
        # Using DuckDuckGo's instant answer API (no API key required)
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        results = []

        # Add abstract if available
        if data.get("Abstract"):
            results.append(f"Abstract: {data['Abstract']}")

        # Add related topics
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"][:num_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(f"• {topic['Text']}")

        if not results:
            return f"No results found for query: {query}"

        return f"Web search results for '{query}':\n\n" + "\n\n".join(results)

    except requests.RequestException as e:
        return f"Error performing web search: {str(e)}"
    except Exception as e:
        return f"Error during web search: {str(e)}"


def analyze_task_for_tools(user_message):
    """Analyze user message to determine if it's a complex task that would benefit from tools"""
    import re

    message_lower = user_message.lower()

    # Check for direct tool commands first
    tool_command_patterns = [
        r"read\s+file:",
        r"write\s+file:",
        r"delete\s+file:",
        r"list\s+files:",
        r"info\s+file:",
        r"run\s+code:",
        r"search\s+web:",
    ]

    for pattern in tool_command_patterns:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return "This appears to be a direct tool command. Execute the appropriate tool automatically."

    # Indicators of file-related tasks
    file_keywords = [
        "file",
        "code",
        "read",
        "write",
        "edit",
        "modify",
        "create",
        "delete",
        "directory",
        "folder",
        "list",
        "search",
        "find",
        "replace",
        "update",
    ]

    # Indicators of web research tasks
    research_keywords = [
        "research",
        "search",
        "find information",
        "look up",
        "web",
        "online",
        "current",
        "latest",
        "news",
        "documentation",
        "tutorial",
        "guide",
    ]

    # Indicators of complex development tasks
    dev_keywords = [
        "debug",
        "fix",
        "implement",
        "build",
        "develop",
        "create app",
        "setup",
        "configure",
        "install",
        "deploy",
        "test",
        "refactor",
        "optimize",
    ]

    # Check for file-related tasks
    if any(keyword in message_lower for keyword in file_keywords):
        if any(
            word in message_lower for word in ["multiple", "several", "all", "batch"]
        ):
            return "This appears to be a file management task. You can use file operations tools to read, write, delete, or list files efficiently."
        else:
            return "This appears to be a file-related task. You can use file operations tools to handle this efficiently."

    # Check for research tasks
    if any(keyword in message_lower for keyword in research_keywords):
        return "This appears to be a research task. You can use the web search tool to find current information and documentation."

    # Check for development tasks
    if any(keyword in message_lower for keyword in dev_keywords):
        return "This appears to be a development task. You can use file operations to manage code and web search to find documentation or solutions."

    # Check for multi-step tasks (indicated by sequence words)
    sequence_indicators = [
        "then",
        "after that",
        "next",
        "finally",
        "first",
        "second",
        "also",
    ]
    if any(indicator in message_lower for indicator in sequence_indicators):
        return "This appears to be a multi-step task. Using tools can help automate and streamline each step of the process."

    # Check for tasks involving specific file paths or code
    if "." in message_lower and any(
        ext in message_lower
        for ext in [".py", ".js", ".html", ".css", ".txt", ".json", ".md"]
    ):
        return "This involves specific file types. File operation tools can help you read, edit, and manage these files efficiently."

    return None


def execute_tool_commands_from_response(response_text):
    """Extract and execute tool commands from AI response"""
    import re

    # Remove backticks and clean the response
    clean_text = response_text.replace("`", "").strip()

    # Pattern to match tool commands in the response
    results = []

    # File read command
    read_matches = re.findall(r"read\s+file:(.+)", clean_text, re.IGNORECASE)
    for match in read_matches:
        try:
            result = read_file(match.strip())
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error reading file: {str(e)}")

    # File write command
    write_matches = re.findall(
        r"write\s+file:(.+?)\s+content:(.+)", clean_text, re.IGNORECASE | re.DOTALL
    )
    for match in write_matches:
        try:
            file_path, content = match[0].strip(), match[1].strip()
            result = write_file(file_path, content)
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error writing file: {str(e)}")

    # File delete command
    delete_matches = re.findall(r"delete\s+file:(.+)", clean_text, re.IGNORECASE)
    for match in delete_matches:
        try:
            result = delete_file(match.strip())
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error deleting file: {str(e)}")

    # List files command
    list_matches = re.findall(r"list\s+files:(.+)", clean_text, re.IGNORECASE)
    for match in list_matches:
        try:
            result = list_files(match.strip())
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error listing files: {str(e)}")

    # File info command
    info_matches = re.findall(r"info\s+file:(.+)", clean_text, re.IGNORECASE)
    for match in info_matches:
        try:
            result = get_file_info(match.strip())
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error getting file info: {str(e)}")

    # Code execution command
    code_matches = re.findall(r"run\s+code:(.+)", clean_text, re.IGNORECASE | re.DOTALL)
    for match in code_matches:
        try:
            result = execute_code(match.strip(), "python")
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error executing code: {str(e)}")

    # Web search command
    search_matches = re.findall(r"search\s+web:(.+)", clean_text, re.IGNORECASE)
    for match in search_matches:
        try:
            result = web_search(match.strip())
            if result:
                results.append(result)
        except Exception as e:
            results.append(f"Error performing web search: {str(e)}")

    if results:
        return "\n\n".join(results)
    return None


def execute_ai_command(user_message):
    """Parse and execute AI commands for file operations and web search"""
    import re

    # File read command: "read file:/path/to/file.txt"
    read_match = re.match(r"read\s+file:(.+)", user_message, re.IGNORECASE)
    if read_match:
        file_path = read_match.group(1).strip()
        result = read_file(file_path)
        return result, result

    # File write command: "write file:/path/to/file.txt content:your content here"
    write_match = re.match(
        r"write\s+file:(.+?)\s+content:(.+)", user_message, re.IGNORECASE | re.DOTALL
    )
    if write_match:
        file_path = write_match.group(1).strip()
        content = write_match.group(2).strip()
        result = write_file(file_path, content)
        return result, result

    # File delete command: "delete file:/path/to/file.txt"
    delete_match = re.match(r"delete\s+file:(.+)", user_message, re.IGNORECASE)
    if delete_match:
        file_path = delete_match.group(1).strip()
        result = delete_file(file_path)
        return result, result

    # List files command: "list files:/path/to/directory"
    list_match = re.match(r"list\s+files:(.+)", user_message, re.IGNORECASE)
    if list_match:
        directory_path = list_match.group(1).strip()
        result = list_files(directory_path)
        return result, result

    # File info command: "info file:/path/to/file.txt"
    info_match = re.match(r"info\s+file:(.+)", user_message, re.IGNORECASE)
    if info_match:
        file_path = info_match.group(1).strip()
        result = get_file_info(file_path)
        return result, result

    # Code execution command: "run code:your python code here"
    code_match = re.match(r"run\s+code:(.+)", user_message, re.IGNORECASE | re.DOTALL)
    if code_match:
        code = code_match.group(1).strip()
        result = execute_code(code, "python")
        return result, result

    # Web search command: "search web:your query here"
    search_match = re.match(r"search\s+web:(.+)", user_message, re.IGNORECASE)
    if search_match:
        query = search_match.group(1).strip()
        result = web_search(query)
        return result, result

    return None, None  # No command matched
