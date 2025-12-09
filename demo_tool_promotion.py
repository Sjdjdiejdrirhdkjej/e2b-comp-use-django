#!/usr/bin/env python
"""Demonstration of tool promotion for complex tasks"""

from chat.ai_utils import analyze_task_for_tools


def demonstrate_tool_promotion():
    """Show how tool promotion works for different types of user requests"""

    print("🤖 AI CHAT TOOL PROMOTION DEMONSTRATION")
    print("=" * 50)

    examples = [
        {
            "user_message": "I need to debug my Python application, can you help me find the error in main.py?",
            "category": "Development Task",
        },
        {
            "user_message": "Can you research the latest machine learning algorithms for me?",
            "category": "Research Task",
        },
        {
            "user_message": "I want to read the config.json file and update the database settings",
            "category": "File Management Task",
        },
        {
            "user_message": "What's the weather like today?",
            "category": "Simple Conversation",
        },
        {
            "user_message": "I need to build a web app, then deploy it, and finally write documentation",
            "category": "Multi-step Complex Task",
        },
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {example['category']}")
        print(f"User: {example['user_message']}")

        tool_suggestion = analyze_task_for_tools(example["user_message"])

        if tool_suggestion:
            print("🔧 AI Response with Tool Promotion:")
            print(
                f"I can help you with this task! Since this involves {example['category'].lower()}, "
            )
            print("I have access to powerful tools that can make this easier:\n")

            print("Available tools:")
            print("• read file:/path/to/file.txt - Read file contents")
            print(
                "• write file:/path/to/file.txt content:your content - Write to files"
            )
            print("• delete file:/path/to/file.txt - Delete files")
            print("• list files:/path/to/directory - List directory contents")
            print("• search web:your query - Perform web search\n")

            print(f"💡 Suggestion: {tool_suggestion}")
            print("\nWould you like me to use these tools to help you with your task?")
        else:
            print("💬 AI Response (Standard):")
            print("I'd be happy to help you with that! Let me assist you directly.")

        print("-" * 50)


if __name__ == "__main__":
    demonstrate_tool_promotion()
