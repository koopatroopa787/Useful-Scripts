"""Validation utilities"""

import re
import os
from pathlib import Path
from urllib.parse import urlparse


def validate_email(email: str) -> bool:
    """
    Validate email address format

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_path(path: str, must_exist: bool = False) -> bool:
    """
    Validate file/directory path

    Args:
        path: Path to validate
        must_exist: If True, path must exist

    Returns:
        True if valid, False otherwise
    """
    try:
        p = Path(path)
        if must_exist:
            return p.exists()
        return True
    except Exception:
        return False


def validate_ip(ip: str) -> bool:
    """
    Validate IPv4 address

    Args:
        ip: IP address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False

    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def validate_port(port: int) -> bool:
    """
    Validate port number

    Args:
        port: Port number to validate

    Returns:
        True if valid, False otherwise
    """
    return isinstance(port, int) and 1 <= port <= 65535
