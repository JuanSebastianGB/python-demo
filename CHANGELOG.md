# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Professional project structure with `src/` layout
- Comprehensive documentation in `docs/` directory
- Professional `setup.py` and `pyproject.toml` configuration
- CLI module for command-line interface
- Makefile for development workflow
- MIT License
- Professional CI/CD pipeline
- Development dependencies management

### Changed
- Moved source code to `src/file_organizer/` directory
- Updated all imports to use new package structure
- Enhanced CI/CD pipeline for professional development
- Improved project organization and maintainability

### Fixed
- All 37 tests now pass consistently
- Automatic folder creation in `organize_files()` method
- Immutable file extensions using property pattern
- Flexible permission handling for cross-platform compatibility
- Corrected test expectations for executable file counts

## [1.0.0] - 2025-01-27

### Added
- Initial release of File Organizer
- Automatic file categorization by extensions
- Support for 7 main file categories (Images, Documents, Videos, Audio, Archives, Code, Executables)
- Dry-run mode for safe preview
- Comprehensive test suite with 37 tests
- GitHub Actions CI/CD pipeline
- Support for Python 3.8+

### Features
- **File Categorization**: Automatically organizes files into logical categories
- **Multiple File Types**: Handles images, documents, videos, audio, archives, code files, and executables
- **Safe Operations**: Dry-run mode to preview changes before execution
- **Flexible Configuration**: Easy to extend with new file types
- **Comprehensive Logging**: Detailed output showing file movements
- **Error Handling**: Robust error handling for file operations

### Supported File Categories
- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico
- **Documents**: .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma
- **Archives**: .zip, .rar, .7z, .tar, .gz, .bz2
- **Code**: .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go
- **Executables**: .exe, .msi, .deb, .rpm, .dmg, .app
- **Other**: Any file type not in the above categories

## [0.1.0] - 2025-01-27

### Added
- Initial development version
- Basic file organization functionality
- Unit and integration tests
- Basic CLI interface
