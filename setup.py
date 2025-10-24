#!/usr/bin/env python3
"""
Setup script for File Organizer package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="file-organizer",
    version="1.0.0",
    author="Juan Sebastian Gonzalez",
    author_email="juan.sebastian.gonzalez@southerncode.us",
    description="A Python package for organizing files by their extensions into categorized folders",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/JuanSebastianGB/python-demo",
    project_urls={
        "Bug Reports": "https://github.com/JuanSebastianGB/python-demo/issues",
        "Source": "https://github.com/JuanSebastianGB/python-demo",
        "Documentation": "https://github.com/JuanSebastianGB/python-demo#readme",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "pytest-xdist>=3.3.0",
            "coverage>=7.2.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "pytest-xdist>=3.3.0",
            "coverage>=7.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
