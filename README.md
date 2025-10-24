# 🐍 Python Demo Repository

A demonstration repository showcasing Python programming concepts and best practices. This repository contains a practical file organizer script that demonstrates object-oriented programming, command-line interfaces, and file system operations.

## 📁 Project Overview

This repository contains a **File Organizer** script that automatically organizes files in a directory by their file extensions. It's a practical tool that demonstrates:

- Object-oriented programming in Python
- Command-line argument parsing
- File system operations
- Error handling and logging
- Type hints and documentation

## 🚀 Features

### File Organizer (`file_organizer.py`)

- **Automatic File Categorization**: Organizes files into logical categories based on file extensions
- **Multiple File Types Support**: Handles images, documents, videos, audio, archives, code files, and executables
- **Safe Operations**: Includes dry-run mode to preview changes before execution
- **Flexible Configuration**: Easy to extend with new file types and categories
- **Comprehensive Logging**: Detailed output showing what files are being moved
- **Error Handling**: Robust error handling for file operations

### Supported File Categories

| Category | Extensions |
|----------|------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2 |
| **Code** | .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go |
| **Executables** | .exe, .msi, .deb, .rpm, .dmg, .app |
| **Other** | Any file type not in the above categories |

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JuanSebastianGB/python-demo.git
   cd python-demo
   ```

2. **Make the script executable (optional):**
   ```bash
   chmod +x file_organizer.py
   ```

## 📖 Usage

### Basic Usage

```bash
# Organize files in the current directory
python file_organizer.py /path/to/directory

# Organize files in the current directory
python file_organizer.py .
```

### Advanced Usage

```bash
# Preview what would be moved (dry run)
python file_organizer.py /path/to/directory --dry-run

# Create category folders without moving files
python file_organizer.py /path/to/directory --create-folders

# Get help
python file_organizer.py --help
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `directory` | Path to the directory to organize (required) |
| `--dry-run` | Show what would be moved without actually moving files |
| `--create-folders` | Create category folders without moving files |
| `--help` | Show help message and exit |

## 💡 Examples

### Example 1: Organize Downloads Folder

```bash
# Preview what would be organized
python file_organizer.py ~/Downloads --dry-run

# Actually organize the files
python file_organizer.py ~/Downloads
```

### Example 2: Create Folder Structure

```bash
# Create category folders without moving files
python file_organizer.py ~/Documents --create-folders
```

## 🏗️ Project Structure

```
python-demo/
├── file_organizer.py    # Main file organizer script
├── requirements.txt     # Dependencies (none required)
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## 🔧 Development

### Code Structure

The `FileOrganizer` class is designed with the following principles:

- **Single Responsibility**: Each method has a clear, single purpose
- **Type Hints**: Full type annotation for better code clarity
- **Error Handling**: Comprehensive error handling and user feedback
- **Documentation**: Detailed docstrings for all methods
- **Extensibility**: Easy to add new file categories and extensions

### Adding New File Categories

To add support for new file types, modify the `file_extensions` dictionary in the `FileOrganizer` class:

```python
self.file_extensions = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    # Add your new category here
    'NewCategory': ['.ext1', '.ext2', '.ext3'],
    # ... existing categories
}
```

## 🧪 Testing

### Manual Testing

1. **Create a test directory with various file types:**
   ```bash
   mkdir test_files
   # Add some files with different extensions
   ```

2. **Run dry-run to see what would happen:**
   ```bash
   python file_organizer.py test_files --dry-run
   ```

3. **Actually organize the files:**
   ```bash
   python file_organizer.py test_files
   ```

### Automated Testing

```bash
# Run with dry-run to test without side effects
python file_organizer.py test_directory --dry-run
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Add new file categories** and extensions
2. **Improve error handling** and user feedback
3. **Add new features** like recursive organization
4. **Enhance the CLI** with more options
5. **Add unit tests** for better code coverage

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Juan Sebastian Gonzalez**
- GitHub: [@JuanSebastianGB](https://github.com/JuanSebastianGB)
- Email: juan.sebastian.gonzalez@southerncode.us

## 🙏 Acknowledgments

- Python community for excellent documentation
- Contributors who help improve this project
- Users who provide feedback and suggestions

## 📊 Project Stats

- **Language**: Python 3.6+
- **Dependencies**: None (uses only standard library)
- **Lines of Code**: ~200
- **File Size**: ~6KB
- **Last Updated**: January 2025

---

**⭐ If you find this project useful, please give it a star!**