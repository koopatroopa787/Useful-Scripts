# 🚀 Useful Scripts

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**A comprehensive collection of Python utilities for system management, automation, data processing, and web operations.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Script Categories](#-script-categories)
  - [System Utilities](#-system-utilities)
  - [File Management](#-file-management)
  - [Media Processing](#-media-processing)
  - [Web Utilities](#-web-utilities)
  - [Network Tools](#-network-tools)
  - [Automation](#-automation)
  - [Data Processing](#-data-processing)
  - [Security](#-security)
- [Unified CLI Tool](#-unified-cli-tool)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎯 **30+ Production-Ready Scripts** - Organized by category for easy discovery
- 🔗 **Unified CLI Interface** - Run all scripts through a single command-line tool
- ⚙️ **Shared Configuration** - Centralized config management across all scripts
- 📊 **Comprehensive Logging** - Built-in logging system with colored output
- 🔧 **Modular Architecture** - Reusable utility modules for common functions
- 📝 **Extensive Documentation** - Detailed help for every script
- 🚄 **High Performance** - Multi-threaded operations where applicable
- 🎨 **Clean Code** - Well-structured, maintainable, and pythonic

---

## 🔧 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/Useful-Scripts.git
cd Useful-Scripts

# Install dependencies
pip install -r requirements.txt

# Make CLI executable (optional)
chmod +x useful_scripts.py
```

### Development Install

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/Useful-Scripts.git
cd Useful-Scripts
pip install -e .
```

---

## 🚀 Quick Start

### Using the Unified CLI

```bash
# List all available scripts
python useful_scripts.py list

# Run a specific script
python useful_scripts.py port-scan 192.168.1.1 --common

# Get help for any script
python useful_scripts.py port-scan --help
```

### Running Scripts Directly

```bash
# Run scripts directly from their directories
python scripts/network/port_scanner.py 192.168.1.1 -p 80,443,8080
python scripts/automation/backup_utility.py ~/Documents ~/Backups
```

---

## 📦 Script Categories

### 🖥️ System Utilities

Monitor and manage system resources

| Script | Description | Usage |
|--------|-------------|-------|
| **cpu.py** | Monitor CPU and memory usage in real-time | `python scripts/system/cpu.py` |
| **shutONdown.py** | Auto shutdown when downloads complete | `python scripts/system/shutONdown.py` |

**Example:**
```bash
python useful_scripts.py cpu
```

---

### 📁 File Management

Organize, process, and manage your files

| Script | Description | Usage |
|--------|-------------|-------|
| **duplicate_remover.py** | Find and remove duplicate files using MD5 hashing | `python scripts/file_management/duplicate_remover.py /path/to/dir` |
| **sorter.py** | Automatically organize files into categories | `python scripts/file_management/sorter.py /path/to/folder` |
| **image_resizer.py** | Batch resize images to specified dimensions | `python scripts/file_management/image_resizer.py` |

**Example:**
```bash
# Organize Downloads folder
python useful_scripts.py sorter ~/Downloads

# Remove duplicates
python useful_scripts.py duplicate-remover ~/Documents
```

---

### 🎨 Media Processing

Process videos, images, documents, and audio

| Script | Description | Usage |
|--------|-------------|-------|
| **pdf2text.py** | Extract text content from PDF documents | `python scripts/media/pdf2text.py document.pdf` |
| **url2qr.py** | Generate QR codes from URLs | `python scripts/media/url2qr.py https://example.com` |
| **web2ebook.py** | Convert web articles to ePub format | `python scripts/media/web2ebook.py <url>` |
| **text2speech.py** | Convert text to speech audio | `python scripts/media/text2speech.py` |

**Example:**
```bash
# Generate QR code
python useful_scripts.py url2qr https://github.com

# Convert PDF to text
python useful_scripts.py pdf2text document.pdf -o output.txt
```

---

### 🌐 Web Utilities

Web scraping, monitoring, and automation

| Script | Description | Usage |
|--------|-------------|-------|
| **webmaster.py** | Check website availability and response times | `python scripts/web/webmaster.py <url>` |
| **reddit.py** | Fetch and email Reddit posts from subreddits | `python scripts/web/reddit.py` |
| **weather.py** | Get weather information using OpenWeatherMap | `python scripts/web/weather.py <city>` |
| **link_checker.py** | Verify URL availability and status codes | `python scripts/web/link_checker.py -f urls.txt` |
| **sitemap_generator.py** | Generate XML sitemaps for websites | `python scripts/web/sitemap_generator.py https://example.com` |

**Example:**
```bash
# Check multiple URLs
python useful_scripts.py link-checker https://google.com https://github.com

# Generate sitemap
python useful_scripts.py sitemap https://example.com -m 500
```

---

### 🔌 Network Tools

Network diagnostics, scanning, and monitoring

| Script | Description | Usage |
|--------|-------------|-------|
| **port_scanner.py** | Scan ports on target hosts with multi-threading | `python scripts/network/port_scanner.py <host> -r 1-1000` |
| **ip_info.py** | Get detailed geolocation and network info for IPs | `python scripts/network/ip_info.py [ip]` |
| **network_monitor.py** | Monitor network bandwidth usage in real-time | `python scripts/network/network_monitor.py` |
| **ping_sweep.py** | Discover active hosts on a network | `python scripts/network/ping_sweep.py 192.168.1.0/24` |

**Example:**
```bash
# Scan common ports
python useful_scripts.py port-scan example.com --common

# Get IP information
python useful_scripts.py ip-info 8.8.8.8

# Monitor network
python useful_scripts.py network-monitor -i 2
```

---

### 🤖 Automation

Automate repetitive tasks and workflows

| Script | Description | Usage |
|--------|-------------|-------|
| **file_watcher.py** | Monitor directories and trigger actions on changes | `python scripts/automation/file_watcher.py /path -c "echo {file}"` |
| **backup_utility.py** | Create compressed backups with rotation | `python scripts/automation/backup_utility.py <source> <dest>` |
| **task_scheduler.py** | Cron-like task scheduler for recurring tasks | `python scripts/automation/task_scheduler.py run` |

**Example:**
```bash
# Watch directory for changes
python useful_scripts.py file-watcher ~/Downloads -p "*.pdf" -c "mv {file} ~/Documents/"

# Create backup
python useful_scripts.py backup ~/Projects ~/Backups/Projects --keep-count 5

# Schedule a task
python useful_scripts.py scheduler add "Daily Backup" "python backup.py" daily "02:00"
```

---

### 📊 Data Processing

Analyze, convert, and generate data

| Script | Description | Usage |
|--------|-------------|-------|
| **csv_json_converter.py** | Convert between CSV and JSON formats | `python scripts/data_processing/csv_json_converter.py data.csv --to-json` |
| **log_analyzer.py** | Analyze log files for patterns and statistics | `python scripts/data_processing/log_analyzer.py access.log` |
| **data_generator.py** | Generate fake test data in various formats | `python scripts/data_processing/data_generator.py users 100 -o users.json` |

**Example:**
```bash
# Convert CSV to JSON
python useful_scripts.py csv-json data.csv --to-json

# Analyze logs
python useful_scripts.py log-analyzer /var/log/nginx/access.log

# Generate test data
python useful_scripts.py data-generator users 1000 -o test_users.json
```

---

### 🔐 Security

Password management and security tools

| Script | Description | Usage |
|--------|-------------|-------|
| **password.py** | Secure password generator and manager | `python scripts/security/password.py` |

**Example:**
```bash
python useful_scripts.py password --generate --length 20
```

---

## 🎛️ Unified CLI Tool

The `useful_scripts.py` CLI provides a centralized interface for all scripts:

```bash
# List all scripts
python useful_scripts.py list

# List scripts by category
python useful_scripts.py list network

# Run a script (both syntaxes work)
python useful_scripts.py port-scan 192.168.1.1
python useful_scripts.py run port-scan 192.168.1.1

# View configuration
python useful_scripts.py config
```

---

## ⚙️ Configuration

Scripts use a centralized configuration file located at `~/.useful_scripts/config.json`:

```json
{
  "version": "2.0.0",
  "logging": {
    "level": "INFO",
    "log_dir": "~/.useful_scripts/logs"
  },
  "paths": {
    "downloads": "~/Downloads",
    "documents": "~/Documents",
    "temp": "/tmp/useful_scripts"
  },
  "api_keys": {
    "openweathermap": "your_api_key",
    "reddit_client_id": "your_client_id"
  },
  "network": {
    "timeout": 10,
    "max_retries": 3
  }
}
```

**Note:** Configuration file is created automatically on first run with default values.

---

## 💡 Examples

### Automation Pipeline

```bash
# Watch for new CSV files and auto-convert to JSON
python useful_scripts.py file-watcher ~/data/csv -p "*.csv" \
  -c "python useful_scripts.py csv-json {file} --to-json"
```

### Network Security Audit

```bash
# Discover hosts and scan them
python useful_scripts.py ping-sweep 192.168.1.0/24
python useful_scripts.py port-scan 192.168.1.100 --common
```

### Automated Backups

```bash
# Schedule daily backups
python useful_scripts.py scheduler add "Daily DB Backup" \
  "python useful_scripts.py backup /var/db ~/backups/db --keep-count 7" \
  daily "03:00"
```

### Web Monitoring

```bash
# Check website links periodically
python useful_scripts.py scheduler add "Link Check" \
  "python useful_scripts.py link-checker -f urls.txt -o report.txt" \
  interval 3600
```

---

## 📚 Documentation

### Individual Script Documentation

Each script has comprehensive built-in help:

```bash
python scripts/network/port_scanner.py --help
python scripts/automation/backup_utility.py --help
```

### Additional Resources

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing
- **[examples/](examples/)** - Sample outputs and use cases
- **[docs/](docs/)** - Detailed documentation for complex scripts

---

## 🤝 Contributing

We love contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

```bash
# Fork the repository
git clone https://github.com/yourusername/Useful-Scripts.git
cd Useful-Scripts

# Create a new branch
git checkout -b feature/amazing-script

# Make your changes and test
python -m pytest tests/

# Submit a pull request
```

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new scripts

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

If you find this project useful, please consider giving it a star!

---

## 👥 Authors

- **Original Author** - Initial work and maintenance
- **Contributors** - See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the list of contributors

---

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Built with Python and various open-source libraries
- Inspired by the need for simple, effective automation tools

---

## 📬 Contact & Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/Useful-Scripts/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/Useful-Scripts/discussions)
- 📧 **Email**: support@example.com

---

<div align="center">

**Made with ❤️ by the Useful Scripts Team**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/Useful-Scripts?style=social)](https://github.com/yourusername/Useful-Scripts/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/Useful-Scripts?style=social)](https://github.com/yourusername/Useful-Scripts/network/members)

</div>
