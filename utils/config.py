"""Configuration management utilities"""

import json
import os
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG_PATH = Path.home() / '.useful_scripts' / 'config.json'


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from JSON file

    Args:
        config_path: Path to config file (uses default if None)

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    config_path = Path(config_path)

    if not config_path.exists():
        return get_default_config()

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config: {e}")
        return get_default_config()


def save_config(config: Dict[str, Any], config_path: str = None) -> bool:
    """
    Save configuration to JSON file

    Args:
        config: Configuration dictionary
        config_path: Path to config file (uses default if None)

    Returns:
        True if successful, False otherwise
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        "version": "2.0.0",
        "logging": {
            "level": "INFO",
            "log_dir": str(Path.home() / '.useful_scripts' / 'logs')
        },
        "paths": {
            "downloads": str(Path.home() / 'Downloads'),
            "documents": str(Path.home() / 'Documents'),
            "temp": "/tmp/useful_scripts"
        },
        "api_keys": {
            "openweathermap": "",
            "reddit_client_id": "",
            "reddit_client_secret": ""
        },
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender": "",
            "password": ""
        },
        "network": {
            "timeout": 10,
            "max_retries": 3,
            "user_agent": "Useful-Scripts/2.0"
        }
    }
