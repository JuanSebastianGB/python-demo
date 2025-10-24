#!/usr/bin/env python3
"""
Unit tests for FileOrganizer class.

Tests individual methods and functions in isolation using mocks.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

from file_organizer.file_organizer import FileOrganizer


class TestFileOrganizerUnit:
    """Unit tests for FileOrganizer class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.organizer = FileOrganizer(self.temp_dir)
    
    def teardown_method(self):
        """Clean up after each test method."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test FileOrganizer initialization."""
        assert self.organizer.directory == Path(self.temp_dir)
        assert isinstance(self.organizer.file_extensions, dict)
        assert 'Images' in self.organizer.file_extensions
        assert 'Documents' in self.organizer.file_extensions
    
    def test_get_file_extension_lowercase(self):
        """Test get_file_extension returns lowercase extension."""
        test_path = Path("test.JPG")
        result = self.organizer.get_file_extension(test_path)
        assert result == ".jpg"
    
    def test_get_file_extension_no_extension(self):
        """Test get_file_extension with file having no extension."""
        test_path = Path("testfile")
        result = self.organizer.get_file_extension(test_path)
        assert result == ""
    
    def test_get_file_extension_multiple_dots(self):
        """Test get_file_extension with multiple dots in filename."""
        test_path = Path("test.backup.txt")
        result = self.organizer.get_file_extension(test_path)
        assert result == ".txt"
    
    @pytest.mark.parametrize("filename,expected_category", [
        ("image.jpg", "Images"),
        ("document.pdf", "Documents"),
        ("video.mp4", "Videos"),
        ("audio.mp3", "Audio"),
        ("archive.zip", "Archives"),
        ("script.py", "Code"),
        ("program.exe", "Executables"),
        ("unknown.xyz", "Other"),
        ("noextension", "Other"),
    ])
    def test_categorize_file(self, filename, expected_category):
        """Test file categorization with various file types."""
        test_path = Path(filename)
        result = self.organizer.categorize_file(test_path)
        assert result == expected_category
    
    def test_categorize_file_case_insensitive(self):
        """Test file categorization is case insensitive."""
        test_path = Path("IMAGE.JPG")
        result = self.organizer.categorize_file(test_path)
        assert result == "Images"
    
    @patch('pathlib.Path.mkdir')
    def test_create_category_folders(self, mock_mkdir):
        """Test category folder creation."""
        self.organizer.create_category_folders()
        
        # Verify mkdir was called for each category
        expected_calls = len(self.organizer.file_extensions) + 1  # +1 for 'Other'
        assert mock_mkdir.call_count == expected_calls
    
    @patch('pathlib.Path.mkdir')
    def test_create_category_folders_existing_ok(self, mock_mkdir):
        """Test category folder creation with exist_ok=True."""
        self.organizer.create_category_folders()
        
        # Verify exist_ok=True was passed
        for call in mock_mkdir.call_args_list:
            assert call[1]['exist_ok'] is True
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    def test_organize_files_empty_directory(self, mock_iterdir, mock_exists):
        """Test organize_files with empty directory."""
        mock_exists.return_value = True
        mock_iterdir.return_value = []
        
        result = self.organizer.organize_files()
        
        # Should return empty dict for all categories
        for category_files in result.values():
            assert category_files == []
    
    @patch('pathlib.Path.exists')
    def test_organize_files_directory_not_exists(self, mock_exists):
        """Test organize_files when directory doesn't exist."""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            self.organizer.organize_files()
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    @patch('shutil.move')
    def test_organize_files_success(self, mock_move, mock_iterdir, mock_exists):
        """Test successful file organization."""
        mock_exists.return_value = True
        
        # Mock files
        mock_file1 = Mock()
        mock_file1.is_file.return_value = True
        mock_file1.name = "test.jpg"
        mock_file1.suffix = ".jpg"
        
        mock_file2 = Mock()
        mock_file2.is_file.return_value = True
        mock_file2.name = "test.pdf"
        mock_file2.suffix = ".pdf"
        
        mock_iterdir.return_value = [mock_file1, mock_file2]
        
        result = self.organizer.organize_files()
        
        # Verify files were categorized correctly
        assert "test.jpg" in result["Images"]
        assert "test.pdf" in result["Documents"]
        
        # Verify move was called
        assert mock_move.call_count == 2
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    def test_organize_files_dry_run(self, mock_iterdir, mock_exists):
        """Test organize_files in dry run mode."""
        mock_exists.return_value = True
        
        # Mock files
        mock_file = Mock()
        mock_file.is_file.return_value = True
        mock_file.name = "test.jpg"
        mock_file.suffix = ".jpg"
        mock_iterdir.return_value = [mock_file]
        
        result = self.organizer.organize_files(dry_run=True)
        
        # Verify file was categorized but not moved
        assert "test.jpg" in result["Images"]
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.iterdir')
    @patch('shutil.move')
    def test_organize_files_move_error(self, mock_move, mock_iterdir, mock_exists):
        """Test organize_files handles move errors gracefully."""
        mock_exists.return_value = True
        mock_move.side_effect = OSError("Permission denied")
        
        # Mock files
        mock_file = Mock()
        mock_file.is_file.return_value = True
        mock_file.name = "test.jpg"
        mock_file.suffix = ".jpg"
        mock_iterdir.return_value = [mock_file]
        
        # Should not raise exception
        result = self.organizer.organize_files()
        
        # File should not be in results due to error
        assert "test.jpg" not in result["Images"]
    
    def test_print_summary_empty(self, capsys):
        """Test print_summary with empty results."""
        empty_results = {category: [] for category in self.organizer.file_extensions.keys()}
        empty_results['Other'] = []
        
        self.organizer.print_summary(empty_results)
        
        captured = capsys.readouterr()
        assert "Total files organized: 0" in captured.out
    
    def test_print_summary_with_files(self, capsys):
        """Test print_summary with files."""
        results = {
            'Images': ['photo1.jpg', 'photo2.png'],
            'Documents': ['doc1.pdf'],
            'Other': [],
            'Videos': [],
            'Audio': [],
            'Archives': [],
            'Code': [],
            'Executables': []
        }
        
        self.organizer.print_summary(results)
        
        captured = capsys.readouterr()
        assert "Images: 2 files" in captured.out
        assert "Documents: 1 files" in captured.out
        assert "Total files organized: 3" in captured.out
        assert "photo1.jpg" in captured.out
        assert "doc1.pdf" in captured.out


class TestFileOrganizerEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_init_with_nonexistent_directory(self):
        """Test initialization with non-existent directory."""
        # Should not raise error during init
        organizer = FileOrganizer("/nonexistent/path")
        assert organizer.directory == Path("/nonexistent/path")
    
    def test_categorize_file_with_special_characters(self):
        """Test file categorization with special characters in filename."""
        organizer = FileOrganizer("/tmp")
        
        test_cases = [
            ("file with spaces.jpg", "Images"),
            ("file-with-dashes.pdf", "Documents"),
            ("file_with_underscores.mp4", "Videos"),
            ("file.with.dots.txt", "Documents"),
        ]
        
        for filename, expected_category in test_cases:
            test_path = Path(filename)
            result = organizer.categorize_file(test_path)
            assert result == expected_category
    
    def test_file_extensions_immutable(self):
        """Test that file_extensions dictionary is not modified externally."""
        organizer = FileOrganizer("/tmp")
        original_extensions = organizer.file_extensions.copy()
        
        # Try to modify (should not affect the original)
        organizer.file_extensions['NewCategory'] = ['.new']
        
        # The modification should not persist
        assert 'NewCategory' not in organizer.file_extensions
        assert organizer.file_extensions == original_extensions


@pytest.mark.unit
class TestFileOrganizerPerformance:
    """Performance and stress tests."""
    
    def test_categorize_file_performance(self):
        """Test categorization performance with many files."""
        organizer = FileOrganizer("/tmp")
        
        # Test with many different file types
        test_files = [
            f"file{i}.jpg" for i in range(100)
        ] + [
            f"doc{i}.pdf" for i in range(100)
        ] + [
            f"video{i}.mp4" for i in range(100)
        ]
        
        import time
        start_time = time.time()
        
        for filename in test_files:
            organizer.categorize_file(Path(filename))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (< 1 second)
        assert duration < 1.0