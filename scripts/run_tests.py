#!/usr/bin/env python3
"""
Test runner script for the file organizer project.

Provides convenient commands to run different types of tests.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def run_unit_tests():
    """Run unit tests only."""
    cmd = ["python", "-m", "pytest", "tests/test_file_organizer_unit.py", "-v", "-m", "unit"]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests only."""
    cmd = ["python", "-m", "pytest", "tests/test_file_organizer_integration.py", "-v", "-m", "integration"]
    return run_command(cmd, "Integration Tests")


def run_all_tests():
    """Run all tests."""
    cmd = ["python", "-m", "pytest", "tests/", "-v"]
    return run_command(cmd, "All Tests")


def run_tests_with_coverage():
    """Run tests with coverage report."""
    cmd = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--cov=file_organizer",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    return run_command(cmd, "Tests with Coverage")


def run_fast_tests():
    """Run only fast tests (exclude slow tests)."""
    cmd = ["python", "-m", "pytest", "tests/", "-v", "-m", "not slow"]
    return run_command(cmd, "Fast Tests")


def run_linting():
    """Run code linting."""
    cmd = ["python", "-m", "flake8", "file_organizer.py", "tests/"]
    return run_command(cmd, "Code Linting")


def run_type_checking():
    """Run type checking."""
    cmd = ["python", "-m", "mypy", "file_organizer.py"]
    return run_command(cmd, "Type Checking")


def run_formatting():
    """Run code formatting."""
    cmd = ["python", "-m", "black", "--check", "file_organizer.py", "tests/"]
    return run_command(cmd, "Code Formatting Check")


def main():
    """Main function to run tests based on command line arguments."""
    parser = argparse.ArgumentParser(description="Test runner for file organizer project")
    parser.add_argument(
        "test_type",
        choices=["unit", "integration", "all", "coverage", "fast", "lint", "type", "format"],
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    # Check if pytest is available
    try:
        subprocess.run(["python", "-m", "pytest", "--version"], 
                      check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest not found. Please install it with: pip install pytest")
        sys.exit(1)
    
    success = False
    
    if args.test_type == "unit":
        success = run_unit_tests()
    elif args.test_type == "integration":
        success = run_integration_tests()
    elif args.test_type == "all":
        success = run_all_tests()
    elif args.test_type == "coverage":
        success = run_tests_with_coverage()
    elif args.test_type == "fast":
        success = run_fast_tests()
    elif args.test_type == "lint":
        success = run_linting()
    elif args.test_type == "type":
        success = run_type_checking()
    elif args.test_type == "format":
        success = run_formatting()
    
    if success:
        print("\n🎉 All operations completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some operations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()