#!/usr/bin/env python3

import os
import sys
import json
import requests
import time

sys.path.append("/app")

from chat.ai_utils import execute_ai_command


def test_ai_tools():
    """Comprehensive test of AI tools functionality"""

    print("🤖 AI TOOLS COMPREHENSIVE TEST")
    print("=" * 60)

    test_results = {"passed": 0, "failed": 0}

    def run_test(name, command, expect_error=False):
        print(f"\n{name}")
        print("-" * 40)
        try:
            result, _ = execute_ai_command(command)
            print(result)
            if "Error" in result and not expect_error:
                test_results["failed"] += 1
                print("❌ TEST FAILED")
            else:
                test_results["passed"] += 1
                print("✅ TEST PASSED")
        except Exception as e:
            print(f"An exception occurred: {e}")
            test_results["failed"] += 1
            print("❌ TEST FAILED")

    # Test 1: List workspace files
    run_test("📁 TEST 1: Listing workspace files", f"list files:{os.getcwd()}")

    # Test 2: Create a test directory
    run_test("mkdir TEST 2: Creating a test directory", f"write file:{os.getcwd()}/test_dir/test.txt content:hello")

    # Test 2: Create a test file with content
    test_content = f"""# AI Tools Test File
This is a test file created by AI tools.
Created at: {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
    run_test("✏️  TEST 2: Creating a test file", f"write file:{os.getcwd()}/ai_test.md content:{test_content}")

    # Test 3: Read the created file
    run_test("📖 TEST 3: Reading the created file", f"read file:{os.getcwd()}/ai_test.md")

    # Test 4: List files in chat directory
    run_test("📂 TEST 4: Listing chat directory", f"list files:{os.getcwd()}/chat")

    # Test 5: Web search
    print("\n🌐 TEST 5: Web search for 'Django framework'")
    print("-" * 40)
    result = execute_ai_command("search web:Django framework")
    print(result[:400] + "..." if len(result) > 400 else result)

    # Test 6: Create a Python file
    python_code = """#!/usr/bin/env python3
# AI Generated Python Script
def greet_ai_tools():
    print("AI Tools are working perfectly! 🚀")
if __name__ == "__main__":
    greet_ai_tools()
"""
    run_test("🐍 TEST 6: Creating a Python script", f"write file:{os.getcwd()}/demo_script.py content:{python_code}")

    # Test 7: Read the Python file
    run_test("📄 TEST 7: Reading the Python script", f"read file:{os.getcwd()}/demo_script.py")

    # Test 8: Clean up - Delete test files
    run_test("🗑️  TEST 8: Cleaning up test files", f"delete file:{os.getcwd()}/ai_test.md")
    run_test("🗑️  TEST 8.1: Cleaning up test files", f"delete file:{os.getcwd()}/demo_script.py")
    run_test("🗑️  TEST 8.2: Cleaning up test files", f"delete file:{os.getcwd()}/test_dir/test.txt")


    # Test 9: Verify cleanup
    run_test("✅ TEST 9: Verifying cleanup", f"read file:{os.getcwd()}/ai_test.md", expect_error=True)

    print("\n" + "=" * 60)
    print("🎉 ALL AI TOOLS TESTS COMPLETED!")
    print(f"PASSED: {test_results['passed']}, FAILED: {test_results['failed']}")
    if test_results["failed"] > 0:
        print("🔴 SOME TESTS FAILED")
        sys.exit(1)
    else:
        print("✅ ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_ai_tools()
