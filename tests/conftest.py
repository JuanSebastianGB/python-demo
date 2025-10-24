#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_files():
    """Sample files for testing."""
    return {
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


@pytest.fixture
def organizer_with_files(temp_directory, sample_files):
    """Create FileOrganizer with sample files."""
    from file_organizer import FileOrganizer
    
    # Create sample files
    for filename in sample_files.keys():
        (temp_directory / filename).touch()
    
    organizer = FileOrganizer(str(temp_directory))
    return organizer, sample_files


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "mock: mark test as using mocks"
    )