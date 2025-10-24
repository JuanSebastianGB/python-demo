#!/usr/bin/env python3
"""
Command Line Interface for File Organizer.

This module provides the CLI interface for the file organizer package.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .file_organizer import FileOrganizer


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Organize files by their extensions into categorized folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/directory              # Organize files in directory
  %(prog)s . --dry-run                     # Preview what would be organized
  %(prog)s ~/Downloads --create-folders    # Create folders without moving files
        """,
    )
    
    parser.add_argument(
        "directory",
        help="Directory path to organize"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without actually moving files"
    )
    
    parser.add_argument(
        "--create-folders",
        action="store_true",
        help="Create category folders without moving files"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        organizer = FileOrganizer(args.directory)
        
        if args.create_folders:
            organizer.create_category_folders()
            print("✅ Category folders created successfully!")
            return 0
        
        # Create folders first
        organizer.create_category_folders()
        
        # Organize files
        moved_files = organizer.organize_files(dry_run=args.dry_run)
        
        # Print summary
        organizer.print_summary(moved_files)
        
        if args.dry_run:
            print("\n🔍 This was a dry run. No files were actually moved.")
            print("Run without --dry-run to actually organize the files.")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except PermissionError as e:
        print(f"❌ Permission Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
