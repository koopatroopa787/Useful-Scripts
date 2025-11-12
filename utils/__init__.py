"""
Useful Scripts - Shared Utilities Module
Provides common functions and helpers for all scripts
"""

__version__ = "2.0.0"
__author__ = "Useful Scripts Contributors"

from .logger import get_logger
from .config import load_config, save_config
from .validators import validate_email, validate_url, validate_path
from .helpers import format_bytes, format_duration, get_timestamp

__all__ = [
    'get_logger',
    'load_config',
    'save_config',
    'validate_email',
    'validate_url',
    'validate_path',
    'format_bytes',
    'format_duration',
    'get_timestamp'
]
