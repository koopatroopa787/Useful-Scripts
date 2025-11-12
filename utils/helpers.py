"""Helper functions and utilities"""

from datetime import datetime
from typing import Union


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable string

    Args:
        bytes_value: Number of bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Format seconds to human-readable duration

    Args:
        seconds: Number of seconds

    Returns:
        Formatted string (e.g., "2h 30m 15s")
    """
    seconds = int(seconds)

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def get_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp as formatted string

    Args:
        format_str: strftime format string

    Returns:
        Formatted timestamp
    """
    return datetime.now().strftime(format_str)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length

    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_filename(filename: str) -> str:
    """
    Convert string to safe filename

    Args:
        filename: Original filename

    Returns:
        Safe filename
    """
    import re
    # Remove or replace unsafe characters
    safe = re.sub(r'[^\w\s.-]', '', filename)
    safe = re.sub(r'[\s]+', '_', safe)
    return safe[:255]  # Limit to max filename length
