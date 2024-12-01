# Useful Scripts

A collection of Python and JavaScript utilities for system management, file operations, and web automation.

## Features

This repository contains utilities for:
- System monitoring and management
- File operations and organization
- Media processing and conversion
- Web scraping and automation
- Security and password management
- Game development and AI
- PDF and document processing
- Network and website utilities

## Scripts Overview

### System Utilities
- `cpu.py` - CPU and memory usage monitoring
- `shutONdown.py` - Automatic system shutdown when downloads complete

### File Management
- `duplicate_remover.py` - Find duplicate files using MD5 hashing
- `sorter.py` - Organize files into categories
- `image_resizer.py` - Batch resize images

### Media and Document Processing
- `pdf2text.py` - Extract text from PDF documents
- `url2qr.py` - Generate QR codes from URLs
- `web2ebook.py` - Convert web articles to ePub format

### Web and Network
- `webmaster.py` - Check website availability
- `reddit.py` - Fetch and email Reddit posts
- `weather.py` - Weather monitoring using OpenWeatherMap API

### Security
- `pass_script.py` - Basic password protection implementation

### Game Development
- `script.js` - AI-powered Pong game using Phaser and TensorFlow.js

## Requirements

Most scripts require Python 3.6+ and various libraries listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/useful-scripts.git
cd useful-scripts
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Each script can be run independently. Before running, make sure to:
1. Check script-specific requirements
2. Update any configuration variables (API keys, paths, etc.)
3. Install required dependencies

Example:
```bash
python cpu.py
python sorter.py
```

## Important Notes

- Some scripts require API keys (weather.py, reddit.py)
- Update hardcoded paths before running file management scripts
- Configure email credentials for scripts that send emails
- Review security-related scripts before use in production

---
⭐ Don't forget to star this repository if you find it useful!
