# Installation Guide

## 📦 Installation Methods

### Method 1: Using pip (Recommended)

```bash
# Install from PyPI (when available)
pip install file-organizer

# Install in development mode
pip install -e .
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://github.com/JuanSebastianGB/python-demo.git
cd python-demo

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Method 3: Using Poetry

```bash
# Install poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## 🔧 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: None (uses only Python standard library)

## 🚀 Quick Installation

```bash
# For end users
pip install file-organizer

# For developers
git clone https://github.com/JuanSebastianGB/python-demo.git
cd python-demo
pip install -e ".[dev]"
```

## ✅ Verify Installation

```bash
# Check if the package is installed
python -c "import file_organizer; print('File Organizer installed successfully!')"

# Check CLI availability
file-organizer --version
```

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**: Make sure you have write permissions to the target directory
2. **Python Version**: Ensure you're using Python 3.8 or higher
3. **Path Issues**: Use absolute paths or ensure the directory exists

### Getting Help

If you encounter installation issues:

1. Check your Python version: `python --version`
2. Ensure pip is up to date: `pip install --upgrade pip`
3. Try installing in a virtual environment
4. Check the [troubleshooting section](troubleshooting.md) for more details
