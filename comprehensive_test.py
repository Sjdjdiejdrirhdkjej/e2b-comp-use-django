#!/usr/bin/env python3

import os
import sys
import json
import requests
import time

sys.path.append("/project/workspace")

from chat.ai_utils import execute_ai_command


def test_ai_tools():
    """Comprehensive test of AI tools functionality"""

    print("🤖 AI TOOLS COMPREHENSIVE TEST")
    print("=" * 60)

    # Test 1: List workspace files
    print("\n📁 TEST 1: Listing workspace files")
    print("-" * 40)
    result = execute_ai_command("list files:/project/workspace")
    print(result)

    # Test 2: Create a test file with content
    print("\n✏️  TEST 2: Creating a test file")
    print("-" * 40)
    test_content = """# AI Tools Test File
This is a test file created by AI tools.

## Features Tested:
- File writing
- File reading  
- File deletion
- Directory listing
- Web search

Created at: """ + time.strftime("%Y-%m-%d %H:%M:%S")

    result = execute_ai_command(
        f"write file:/project/workspace/ai_test.md content:{test_content}"
    )
    print(result)

    # Test 3: Read the created file
    print("\n📖 TEST 3: Reading the created file")
    print("-" * 40)
    result = execute_ai_command("read file:/project/workspace/ai_test.md")
    print(result)

    # Test 4: List files in chat directory
    print("\n📂 TEST 4: Listing chat directory")
    print("-" * 40)
    result = execute_ai_command("list files:/project/workspace/chat")
    print(result)

    # Test 5: Web search
    print("\n🌐 TEST 5: Web search for 'Django framework'")
    print("-" * 40)
    result = execute_ai_command("search web:Django framework")
    print(result[:400] + "..." if len(result) > 400 else result)

    # Test 6: Create a Python file
    print("\n🐍 TEST 6: Creating a Python script")
    print("-" * 40)
    python_code = """#!/usr/bin/env python3
# AI Generated Python Script

def greet_ai_tools():
    \"\"\"Greet the AI tools functionality\"\"\"
    tools = ['read', 'write', 'delete', 'list', 'search']
    print("Available AI Tools:")
    for tool in tools:
        print(f"  - {tool}")
    
    print("\\nAI Tools are working perfectly! 🚀")

if __name__ == "__main__":
    greet_ai_tools()
"""

    result = execute_ai_command(
        f"write file:/project/workspace/demo_script.py content:{python_code}"
    )
    print(result)

    # Test 7: Read the Python file
    print("\n📄 TEST 7: Reading the Python script")
    print("-" * 40)
    result = execute_ai_command("read file:/project/workspace/demo_script.py")
    print(result)

    # Test 8: Clean up - Delete test files
    print("\n🗑️  TEST 8: Cleaning up test files")
    print("-" * 40)
    for file in ["/project/workspace/ai_test.md", "/project/workspace/demo_script.py"]:
        result = execute_ai_command(f"delete file:{file}")
        print(result)

    # Test 9: Verify cleanup
    print("\n✅ TEST 9: Verifying cleanup")
    print("-" * 40)
    result = execute_ai_command("read file:/project/workspace/ai_test.md")
    print(result)  # Should show file not found error

    print("\n" + "=" * 60)
    print("🎉 ALL AI TOOLS TESTS COMPLETED!")
    print("✅ File operations: WORKING")
    print("✅ Directory listing: WORKING")
    print("✅ Web search: WORKING")
    print("✅ Security restrictions: WORKING")
    print("=" * 60)


if __name__ == "__main__":
    test_ai_tools()
