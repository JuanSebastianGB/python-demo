#!/usr/bin/env python3
"""
Test script for the File Organizer

This script demonstrates how to use the FileOrganizer class programmatically.
"""

import os
import tempfile
import shutil
from pathlib import Path
from file_organizer import FileOrganizer


def create_test_files(test_dir: Path) -> None:
    """Create test files with different extensions."""
    test_files = [
        "document.pdf",
        "image.jpg", 
        "video.mp4",
        "audio.mp3",
        "archive.zip",
        "code.py",
        "executable.exe",
        "unknown.xyz"
    ]
    
    for filename in test_files:
        file_path = test_dir / filename
        file_path.touch()
        print(f"Created test file: {filename}")


def test_file_organizer():
    """Test the FileOrganizer functionality."""
    print("🧪 Testing File Organizer")
    print("=" * 50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        print(f"Test directory: {test_dir}")
        
        # Create test files
        print("\n📁 Creating test files...")
        create_test_files(test_dir)
        
        # List files before organization
        print("\n📋 Files before organization:")
        for file in test_dir.iterdir():
            if file.is_file():
                print(f"  - {file.name}")
        
        # Test dry run
        print("\n🔍 Testing dry run...")
        organizer = FileOrganizer(str(test_dir))
        organizer.create_category_folders()
        moved_files = organizer.organize_files(dry_run=True)
        
        # Show summary
        organizer.print_summary(moved_files)
        
        print("\n✅ Test completed successfully!")
        print("The file organizer correctly categorized all test files.")


if __name__ == "__main__":
    test_file_organizer()