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
    try:
        if len(messages) > 1:
            history = messages[:-1]
            last_message = messages[-1]["parts"]
        else:
            history = []
            last_message = messages[0]["parts"] if messages else "Hello"

        chat = model.start_chat(history=history)
        response = chat.send_message(last_message)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_conversation_title(first_user_message):
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
        return "New Chat"


def format_messages_for_gemini(conversation_messages):
    messages = []
    for msg in conversation_messages:
        role = "user" if msg.is_user else "model"
        messages.append({"role": role, "parts": msg.content})
    return messages


def read_file(file_path):
    """Read content from a file"""
    try:
        # Security: restrict to project directory
        if not file_path.startswith("/project/workspace"):
            return "Error: Access denied - can only read files within project workspace"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"File content from {file_path}:\n\n{content}"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except PermissionError:
        return f"Error: Permission denied reading '{file_path}'"
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


def write_file(file_path, content):
    """Write content to a file"""
    try:
        # Security: restrict to project directory
        if not file_path.startswith("/project/workspace"):
            return (
                "Error: Access denied - can only write files within project workspace"
            )

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except PermissionError:
        return f"Error: Permission denied writing to '{file_path}'"
    except Exception as e:
        return f"Error writing to file '{file_path}': {str(e)}"


def delete_file(file_path):
    """Delete a file"""
    try:
        # Security: restrict to project directory
        if not file_path.startswith("/project/workspace"):
            return (
                "Error: Access denied - can only delete files within project workspace"
            )

        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist"

        os.remove(file_path)
        return f"Successfully deleted {file_path}"
    except PermissionError:
        return f"Error: Permission denied deleting '{file_path}'"
    except Exception as e:
        return f"Error deleting file '{file_path}': {str(e)}"


def list_files(directory_path):
    """List files and directories in a path"""
    try:
        # Security: restrict to project directory
        if not directory_path.startswith("/project/workspace"):
            return "Error: Access denied - can only list files within project workspace"

        if not os.path.exists(directory_path):
            return f"Error: Directory '{directory_path}' does not exist"

        if not os.path.isdir(directory_path):
            return f"Error: '{directory_path}' is not a directory"

        items = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            item_type = "DIR" if os.path.isdir(item_path) else "FILE"
            items.append(f"{item_type}: {item}")

        return f"Contents of {directory_path}:\n\n" + "\n".join(sorted(items))
    except PermissionError:
        return f"Error: Permission denied accessing '{directory_path}'"
    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"


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


def execute_ai_command(user_message):
    """Parse and execute AI commands for file operations and web search"""
    import re

    # File read command: "read file:/path/to/file.txt"
    read_match = re.match(r"read\s+file:(.+)", user_message, re.IGNORECASE)
    if read_match:
        file_path = read_match.group(1).strip()
        return read_file(file_path)

    # File write command: "write file:/path/to/file.txt content:your content here"
    write_match = re.match(
        r"write\s+file:(.+?)\s+content:(.+)", user_message, re.IGNORECASE | re.DOTALL
    )
    if write_match:
        file_path = write_match.group(1).strip()
        content = write_match.group(2).strip()
        return write_file(file_path, content)

    # File delete command: "delete file:/path/to/file.txt"
    delete_match = re.match(r"delete\s+file:(.+)", user_message, re.IGNORECASE)
    if delete_match:
        file_path = delete_match.group(1).strip()
        return delete_file(file_path)

    # List files command: "list files:/path/to/directory"
    list_match = re.match(r"list\s+files:(.+)", user_message, re.IGNORECASE)
    if list_match:
        directory_path = list_match.group(1).strip()
        return list_files(directory_path)

    # Web search command: "search web:your query here"
    search_match = re.match(r"search\s+web:(.+)", user_message, re.IGNORECASE)
    if search_match:
        query = search_match.group(1).strip()
        return web_search(query)

    return None  # No command matched
