#!/usr/bin/env python3
"""
Integration tests for FileOrganizer class.

Tests the complete workflow with real file system operations.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from file_organizer.file_organizer import FileOrganizer


@pytest.mark.integration
class TestFileOrganizerIntegration:
    """Integration tests for FileOrganizer with real file operations."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.organizer = FileOrganizer(str(self.temp_dir))
    
    def teardown_method(self):
        """Clean up after each test method."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_workflow_success(self):
        """Test complete file organization workflow."""
        # Create test files
        test_files = {
            "image1.jpg": "Images",
            "image2.png": "Images", 
            "document1.pdf": "Documents",
            "document2.txt": "Documents",
            "video1.mp4": "Videos",
            "audio1.mp3": "Audio",
            "archive1.zip": "Archives",
            "script1.py": "Code",
            "program1.exe": "Executables",
            "unknown1.xyz": "Other"
        }
        
        # Create files
        for filename in test_files.keys():
            (self.temp_dir / filename).touch()
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify files were moved to correct directories
        for filename, expected_category in test_files.items():
            category_dir = self.temp_dir / expected_category
            file_path = category_dir / filename
            
            assert file_path.exists(), f"File {filename} not found in {expected_category}"
            assert filename in result[expected_category]
        
        # Verify original files are gone
        for filename in test_files.keys():
            original_path = self.temp_dir / filename
            assert not original_path.exists(), f"Original file {filename} still exists"
    
    def test_dry_run_integration(self):
        """Test dry run mode with real files."""
        # Create test files
        test_files = ["image.jpg", "document.pdf", "video.mp4"]
        for filename in test_files:
            (self.temp_dir / filename).touch()
        
        # Run dry run
        result = self.organizer.organize_files(dry_run=True)
        
        # Verify files were categorized but not moved
        assert "image.jpg" in result["Images"]
        assert "document.pdf" in result["Documents"]
        assert "video.mp4" in result["Videos"]
        
        # Verify files are still in original location
        for filename in test_files:
            original_path = self.temp_dir / filename
            assert original_path.exists(), f"File {filename} was moved during dry run"
        
        # Verify no category directories were created
        for category in self.organizer.file_extensions.keys():
            category_dir = self.temp_dir / category
            assert not category_dir.exists(), f"Category directory {category} was created during dry run"
    
    def test_create_folders_only(self):
        """Test creating category folders without moving files."""
        # Create test files
        test_files = ["image.jpg", "document.pdf"]
        for filename in test_files:
            (self.temp_dir / filename).touch()
        
        # Create folders only
        self.organizer.create_category_folders()
        
        # Verify category directories were created
        for category in self.organizer.file_extensions.keys():
            category_dir = self.temp_dir / category
            assert category_dir.exists(), f"Category directory {category} was not created"
            assert category_dir.is_dir(), f"Category directory {category} is not a directory"
        
        # Verify files are still in original location
        for filename in test_files:
            original_path = self.temp_dir / filename
            assert original_path.exists(), f"File {filename} was moved when only creating folders"
    
    def test_mixed_file_types(self):
        """Test organizing directory with mixed file types."""
        # Create files with various extensions
        test_files = [
            "photo1.jpg", "photo2.jpeg", "photo3.png",
            "doc1.pdf", "doc2.docx", "doc3.txt",
            "movie1.mp4", "movie2.avi",
            "song1.mp3", "song2.wav",
            "backup1.zip", "backup2.rar",
            "script1.py", "script2.js",
            "app1.exe", "app2.msi",
            "unknown1.xyz", "unknown2.abc"
        ]
        
        for filename in test_files:
            (self.temp_dir / filename).touch()
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify all files were categorized
        total_files = sum(len(files) for files in result.values())
        assert total_files == len(test_files), f"Expected {len(test_files)} files, got {total_files}"
        
        # Verify specific categorizations
        assert "photo1.jpg" in result["Images"]
        assert "doc1.pdf" in result["Documents"]
        assert "movie1.mp4" in result["Videos"]
        assert "song1.mp3" in result["Audio"]
        assert "backup1.zip" in result["Archives"]
        assert "script1.py" in result["Code"]
        assert "app1.exe" in result["Executables"]
        assert "unknown1.xyz" in result["Other"]
    
    def test_empty_directory(self):
        """Test organizing empty directory."""
        result = self.organizer.organize_files()
        
        # Should return empty results
        for category_files in result.values():
            assert category_files == []
    
    def test_directory_with_subdirectories(self):
        """Test that subdirectories are not affected."""
        # Create subdirectory with files
        subdir = self.temp_dir / "subdirectory"
        subdir.mkdir()
        (subdir / "file_in_subdir.txt").touch()
        
        # Create file in main directory
        (self.temp_dir / "file_in_main.txt").touch()
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify only main directory file was organized
        assert "file_in_main.txt" in result["Documents"]
        assert len(result["Documents"]) == 1
        
        # Verify subdirectory file was not moved
        subdir_file = subdir / "file_in_subdir.txt"
        assert subdir_file.exists(), "File in subdirectory was moved"
    
    def test_file_name_edge_cases(self):
        """Test files with special characters and edge cases."""
        edge_case_files = [
            "file with spaces.jpg",
            "file-with-dashes.pdf",
            "file_with_underscores.mp4",
            "file.with.dots.txt",
            "UPPERCASE.JPG",
            "mixedCase.Pdf",
            "file123.jpg",
            "file.123.jpg",  # Multiple dots
            "file",  # No extension
            ".hidden",  # Hidden file
        ]
        
        for filename in edge_case_files:
            (self.temp_dir / filename).touch()
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify files were categorized correctly
        assert "file with spaces.jpg" in result["Images"]
        assert "file-with-dashes.pdf" in result["Documents"]
        assert "file_with_underscores.mp4" in result["Videos"]
        assert "file.with.dots.txt" in result["Documents"]
        assert "UPPERCASE.JPG" in result["Images"]
        assert "mixedCase.Pdf" in result["Documents"]
        assert "file123.jpg" in result["Images"]
        assert "file.123.jpg" in result["Images"]
        assert "file" in result["Other"]
        assert ".hidden" in result["Other"]
    
    def test_permission_handling(self):
        """Test handling of files with permission issues."""
        # Create a file
        test_file = self.temp_dir / "test.txt"
        test_file.touch()
        
        # Make file read-only (on Unix systems)
        try:
            test_file.chmod(0o444)  # Read-only
            
            # Try to organize (should handle gracefully)
            result = self.organizer.organize_files()
            
            # File should still be in original location due to permission error
            assert test_file.exists(), "File was moved despite permission error"
            
        except (OSError, NotImplementedError):
            # Skip test on systems where chmod doesn't work as expected
            pytest.skip("Permission testing not supported on this system")
        finally:
            # Restore permissions for cleanup
            try:
                test_file.chmod(0o644)
            except (OSError, NotImplementedError):
                pass
    
    def test_large_number_of_files(self):
        """Test performance with large number of files."""
        # Create many files
        file_count = 100
        test_files = []
        
        for i in range(file_count):
            filename = f"file{i}.jpg"
            (self.temp_dir / filename).touch()
            test_files.append(filename)
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify all files were organized
        assert len(result["Images"]) == file_count
        
        # Verify all files are in the Images directory
        images_dir = self.temp_dir / "Images"
        actual_files = [f.name for f in images_dir.iterdir() if f.is_file()]
        assert len(actual_files) == file_count
        
        # Verify all expected files are present
        for filename in test_files:
            assert filename in result["Images"]
            assert (images_dir / filename).exists()


@pytest.mark.integration
@pytest.mark.slow
class TestFileOrganizerStress:
    """Stress tests for FileOrganizer."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.organizer = FileOrganizer(str(self.temp_dir))
    
    def teardown_method(self):
        """Clean up after each test method."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_many_different_file_types(self):
        """Test with many different file types."""
        # Create files with various extensions
        extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.pdf', '.doc', '.docx', '.txt', '.rtf',
            '.mp4', '.avi', '.mkv', '.mov',
            '.mp3', '.wav', '.flac', '.aac',
            '.zip', '.rar', '.7z', '.tar',
            '.py', '.js', '.html', '.css',
            '.exe', '.msi', '.deb'
        ]
        
        file_count = 0
        for ext in extensions:
            for i in range(5):  # 5 files per extension
                filename = f"file{i}{ext}"
                (self.temp_dir / filename).touch()
                file_count += 1
        
        # Organize files
        result = self.organizer.organize_files()
        
        # Verify all files were organized
        total_organized = sum(len(files) for files in result.values())
        assert total_organized == file_count
        
        # Verify files are in correct categories
        assert len(result["Images"]) == 25  # 5 files * 5 image extensions
        assert len(result["Documents"]) == 25  # 5 files * 5 document extensions
        assert len(result["Videos"]) == 20  # 5 files * 4 video extensions
        assert len(result["Audio"]) == 20  # 5 files * 4 audio extensions
        assert len(result["Archives"]) == 20  # 5 files * 4 archive extensions
        assert len(result["Code"]) == 20  # 5 files * 4 code extensions
        assert len(result["Executables"]) == 10  # 5 files * 2 executable extensions