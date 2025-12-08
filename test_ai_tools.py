#!/usr/bin/env python3

import os
import sys

sys.path.append("/project/workspace")

# Test the AI tools functionality
from chat.ai_utils import execute_ai_command

print("Testing AI Tools...")
print("=" * 50)

# Test 1: List files
print("\n1. Testing 'list files:/project/workspace':")
result = execute_ai_command("list files:/project/workspace")
print(result[:200] + "..." if len(result) > 200 else result)

# Test 2: Write a file
print("\n2. Testing 'write file:/project/workspace/test.txt content:Hello World':")
result = execute_ai_command(
    "write file:/project/workspace/test.txt content:Hello World"
)
print(result)

# Test 3: Read the file
print("\n3. Testing 'read file:/project/workspace/test.txt':")
result = execute_ai_command("read file:/project/workspace/test.txt")
print(result)

# Test 4: Web search
print("\n4. Testing 'search web:Python programming':")
result = execute_ai_command("search web:Python programming")
print(result[:300] + "..." if len(result) > 300 else result)

# Test 5: Delete the file
print("\n5. Testing 'delete file:/project/workspace/test.txt':")
result = execute_ai_command("delete file:/project/workspace/test.txt")
print(result)

print("\n" + "=" * 50)
print("AI Tools test completed!")
