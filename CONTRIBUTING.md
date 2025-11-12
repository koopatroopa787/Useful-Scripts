# Contributing to Useful Scripts

Thank you for your interest in contributing to Useful Scripts! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Adding New Scripts](#adding-new-scripts)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful, inclusive, and professional in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** or screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear use case** for the enhancement
- **Detailed description** of the proposed functionality
- **Examples** of how it would work
- **Potential implementation** approach (optional)

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Useful-Scripts.git
cd Useful-Scripts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pylint black
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Code Example

```python
def process_data(input_path: str, output_path: str) -> bool:
    """
    Process data from input file and save to output file.

    Args:
        input_path: Path to input file
        output_path: Path to output file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return False
```

### Documentation Standards

- Add comprehensive docstrings
- Include usage examples in script help text
- Update README.md when adding new scripts
- Add inline comments for complex logic

## Adding New Scripts

When adding a new script:

### 1. Choose the Right Category

Place your script in the appropriate directory:
- `scripts/system/` - System monitoring and management
- `scripts/file_management/` - File operations
- `scripts/media/` - Media processing
- `scripts/web/` - Web utilities
- `scripts/network/` - Network tools
- `scripts/automation/` - Automation tasks
- `scripts/data_processing/` - Data analysis and conversion
- `scripts/security/` - Security tools

### 2. Script Template

```python
#!/usr/bin/env python3
"""
Script Name - Brief description
Detailed description of what the script does
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Description of your script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s example1
  %(prog)s example2 --option value
        """
    )

    # Add arguments
    parser.add_argument('input', help='Input parameter')
    parser.add_argument('-o', '--output', help='Output file')

    args = parser.parse_args()

    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 3. Update Documentation

- Add script to README.md in the appropriate category
- Add entry to `useful_scripts.py` script mappings
- Include usage examples

### 4. Testing

- Test your script with various inputs
- Handle edge cases and errors gracefully
- Ensure cross-platform compatibility where possible

### 5. Dependencies

- Add any new dependencies to `requirements.txt`
- Use standard library when possible
- Document version requirements

## Submitting Changes

### Commit Messages

Write clear, concise commit messages:

```
Add port scanner script with multi-threading support

- Implements concurrent port scanning
- Supports both single ports and ranges
- Includes common port detection
- Adds comprehensive help documentation
```

### Pull Request Process

1. **Update documentation** - Ensure README and other docs are current
2. **Test thoroughly** - Verify your changes work as expected
3. **Clean commit history** - Squash commits if necessary
4. **Fill PR template** - Provide detailed description of changes
5. **Link issues** - Reference related issues in PR description
6. **Be responsive** - Address review feedback promptly

### PR Review Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added
- [ ] Error handling is implemented
- [ ] Cross-platform compatibility considered
- [ ] Examples are provided

## Questions?

If you have questions or need help:

- Open an issue with the `question` label
- Join our discussions on GitHub
- Contact maintainers via email

Thank you for contributing to Useful Scripts!
