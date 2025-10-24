#!/usr/bin/env python3
"""
File Organizer Script

A Python script that organizes files in a directory by their file extensions.
Creates folders for different file types and moves files accordingly.

Author: Juan Sebastian Gonzalez
Date: 2025-01-27
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
import argparse


class FileOrganizer:
    """A class to organize files by their extensions."""
    
    def __init__(self, directory: str):
        """
        Initialize the FileOrganizer.
        
        Args:
            directory (str): The directory path to organize
        """
        self.directory = Path(directory)
        self._file_extensions = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
            'Executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app']
        }
    
    @property
    def file_extensions(self):
        """Return a copy of the file extensions dictionary."""
        return {k: v.copy() for k, v in self._file_extensions.items()}
    
    def get_file_extension(self, file_path: Path) -> str:
        """
        Get the file extension in lowercase.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            str: File extension in lowercase
        """
        return file_path.suffix.lower()
    
    def categorize_file(self, file_path: Path) -> str:
        """
        Categorize a file based on its extension.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            str: Category name for the file
        """
        extension = self.get_file_extension(file_path)
        
        for category, extensions in self._file_extensions.items():
            if extension in extensions:
                return category
        
        return 'Other'
    
    def create_category_folders(self) -> None:
        """Create folders for each file category."""
        categories = list(self._file_extensions.keys()) + ['Other']
        
        for category in categories:
            folder_path = self.directory / category
            folder_path.mkdir(exist_ok=True)
            print(f"Created folder: {category}")
    
    def organize_files(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """
        Organize files into their respective category folders.
        
        Args:
            dry_run (bool): If True, only show what would be moved without actually moving files
            
        Returns:
            Dict[str, List[str]]: Dictionary with categories and moved files
        """
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory {self.directory} does not exist")
        
        moved_files = {category: [] for category in list(self._file_extensions.keys()) + ['Other']}
        
        # Get all files in the directory (not subdirectories)
        files = [f for f in self.directory.iterdir() if f.is_file()]
        
        if not files:
            print("No files found to organize.")
            return moved_files
        
        print(f"Found {len(files)} files to organize...")
        
        # Create category folders first (only if not dry run)
        if not dry_run:
            self.create_category_folders()
        
        for file_path in files:
            category = self.categorize_file(file_path)
            destination = self.directory / category / file_path.name
            
            try:
                if not dry_run:
                    shutil.move(str(file_path), str(destination))
                    moved_files[category].append(file_path.name)
                    print(f"Moved: {file_path.name} -> {category}/")
                else:
                    moved_files[category].append(file_path.name)
                    print(f"Would move: {file_path.name} -> {category}/")
                    
            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")
        
        return moved_files
    
    def print_summary(self, moved_files: Dict[str, List[str]]) -> None:
        """
        Print a summary of organized files.
        
        Args:
            moved_files (Dict[str, List[str]]): Dictionary with categories and moved files
        """
        print("\n" + "="*50)
        print("ORGANIZATION SUMMARY")
        print("="*50)
        
        total_files = 0
        for category, files in moved_files.items():
            if files:
                print(f"\n{category}: {len(files)} files")
                for file in files:
                    print(f"  - {file}")
                total_files += len(files)
        
        print(f"\nTotal files organized: {total_files}")


def main():
    """Main function to run the file organizer."""
    parser = argparse.ArgumentParser(description="Organize files by their extensions")
    parser.add_argument("directory", help="Directory path to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without actually moving files")
    parser.add_argument("--create-folders", action="store_true", help="Create category folders without moving files")
    
    args = parser.parse_args()
    
    try:
        organizer = FileOrganizer(args.directory)
        
        if args.create_folders:
            organizer.create_category_folders()
            print("Category folders created successfully!")
            return
        
        # Create folders first
        organizer.create_category_folders()
        
        # Organize files
        moved_files = organizer.organize_files(dry_run=args.dry_run)
        
        # Print summary
        organizer.print_summary(moved_files)
        
        if args.dry_run:
            print("\nThis was a dry run. No files were actually moved.")
            print("Run without --dry-run to actually organize the files.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())