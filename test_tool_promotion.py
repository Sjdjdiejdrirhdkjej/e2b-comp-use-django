#!/usr/bin/env python
"""Test script to verify tool promotion functionality"""

import os
import sys
import django

# Setup Django
sys.path.append("/home/runner/workspace")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aichat.settings")
django.setup()

from chat.ai_utils import analyze_task_for_tools, get_ai_response


def test_tool_analysis():
    """Test the tool analysis function"""
    print("Testing tool analysis for complex tasks...")

    # Test cases
    test_cases = [
        ("I need to debug my Python code", "development task"),
        ("Can you help me research machine learning algorithms", "research task"),
        ("Read the file config.json and update it", "file management task"),
        ("Hello, how are you?", "simple conversation"),
        ("I want to build a web application and then deploy it", "multi-step task"),
        ("Find all .py files in the project", "file operations task"),
    ]

    for message, expected_type in test_cases:
        result = analyze_task_for_tools(message)
        print(f"Message: '{message}'")
        print(f"Expected: {expected_type}")
        print(f"Tool suggestion: {'Yes' if result else 'No'}")
        if result:
            print(f"Suggestion: {result}")
        print("-" * 50)


def test_ai_response_with_tools():
    """Test AI response with tool suggestions"""
    print("\nTesting AI response with tool promotion...")

    # Test message that should trigger tool suggestion
    messages = [
        {
            "role": "user",
            "parts": "I need to debug my Python application and find the error in main.py",
        }
    ]

    try:
        response, tool_suggested = get_ai_response(messages)
        print(f"Tool suggested: {'Yes' if tool_suggested else 'No'}")
        print(f"AI Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_tool_analysis()
    test_ai_response_with_tools()
    print("\nTool promotion functionality test completed!")
