#!/usr/bin/env python3
"""
IP Info - Get detailed information about an IP address
Uses ipapi.co API for geolocation and network information
"""

import requests
import argparse
import socket
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, validate_ip


logger = get_logger(__name__)


def get_my_ip() -> str:
    """Get the public IP address of this machine"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except Exception as e:
        logger.error(f"Failed to get public IP: {e}")
        return None


def get_ip_info(ip: str = None) -> dict:
    """
    Get information about an IP address

    Args:
        ip: IP address (uses public IP if None)

    Returns:
        Dictionary with IP information
    """
    if ip is None:
        ip = get_my_ip()
        if not ip:
            return None

    try:
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get IP info: {e}")
        return None


def resolve_hostname(hostname: str) -> str:
    """
    Resolve hostname to IP address

    Args:
        hostname: Hostname to resolve

    Returns:
        IP address or None
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        logger.error(f"Could not resolve hostname: {hostname}")
        return None


def display_ip_info(info: dict):
    """Display IP information in a formatted way"""
    if not info:
        print("No information available")
        return

    if info.get('error'):
        print(f"Error: {info.get('reason', 'Unknown error')}")
        return

    print("\n" + "=" * 60)
    print("IP Address Information")
    print("=" * 60)

    fields = [
        ("IP Address", "ip"),
        ("Version", "version"),
        ("City", "city"),
        ("Region", "region"),
        ("Country", "country_name"),
        ("Country Code", "country_code"),
        ("Postal Code", "postal"),
        ("Latitude", "latitude"),
        ("Longitude", "longitude"),
        ("Timezone", "timezone"),
        ("UTC Offset", "utc_offset"),
        ("ISP", "org"),
        ("ASN", "asn"),
        ("Network", "network"),
        ("Continent", "continent_code"),
        ("Currency", "currency"),
        ("Languages", "languages"),
    ]

    for label, key in fields:
        value = info.get(key)
        if value:
            print(f"{label:20s}: {value}")

    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Get detailed information about an IP address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Get info about your public IP
  %(prog)s 8.8.8.8            # Get info about a specific IP
  %(prog)s google.com         # Get info about a hostname
        """
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="IP address or hostname (uses your public IP if not specified)"
    )

    args = parser.parse_args()

    target_ip = None

    if args.target:
        # Check if it's an IP or hostname
        if validate_ip(args.target):
            target_ip = args.target
        else:
            # Try to resolve as hostname
            logger.info(f"Resolving hostname: {args.target}")
            target_ip = resolve_hostname(args.target)
            if target_ip:
                logger.info(f"Resolved to: {target_ip}")

    if target_ip is None and args.target:
        logger.error("Invalid IP address or hostname")
        return

    info = get_ip_info(target_ip)
    display_ip_info(info)


if __name__ == "__main__":
    main()
