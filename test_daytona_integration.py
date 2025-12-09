#!/usr/bin/env python
"""Test Daytona container file operations"""

import sys
import os

# Add the workspace to Python path
sys.path.append("/home/runner/workspace")

# Import the Daytona operations
try:
    from chat.daytona_file_ops import daytona_ops

    print("✅ Successfully imported Daytona operations")
except ImportError as e:
    print(f"❌ Failed to import Daytona operations: {e}")
    sys.exit(1)


def test_daytona_operations():
    """Test Daytona container file operations"""
    print("\n🐳 Testing Daytona Container File Operations")
    print("=" * 50)

    # Test 1: List files in current directory
    print("\n📁 Test 1: List files in workspace")
    result = daytona_ops.list_files("/home/runner/workspace")
    print(f"Result: {result[:200]}...")

    # Test 2: Get file info for a known file
    print("\n📄 Test 2: Get file info for manage.py")
    result = daytona_ops.get_file_info("/home/runner/workspace/manage.py")
    print(f"Result: {result}")

    # Test 3: Read a small file
    print("\n📖 Test 3: Read requirements.txt")
    result = daytona_ops.read_file("/home/runner/workspace/requirements.txt")
    print(f"Result: {result[:200]}...")

    # Test 4: Write a test file
    print("\n✏️ Test 4: Write test file")
    test_content = "This is a test file created by Daytona container operations."
    result = daytona_ops.write_file(
        "/home/runner/workspace/test_daytona.txt", test_content
    )
    print(f"Result: {result}")

    # Test 5: Read back the test file
    print("\n🔍 Test 5: Read back test file")
    result = daytona_ops.read_file("/home/runner/workspace/test_daytona.txt")
    print(f"Result: {result}")

    # Test 6: Clean up - delete test file
    print("\n🗑️ Test 6: Delete test file")
    result = daytona_ops.delete_file("/home/runner/workspace/test_daytona.txt")
    print(f"Result: {result}")

    # Test 7: Security test - try to access outside workspace
    print("\n🔒 Test 7: Security test - access outside workspace")
    result = daytona_ops.read_file("/etc/passwd")
    print(f"Result: {result}")

    print("\n✅ Daytona container operations test completed!")


if __name__ == "__main__":
    test_daytona_operations()
