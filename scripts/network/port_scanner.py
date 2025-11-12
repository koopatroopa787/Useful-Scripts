#!/usr/bin/env python3
"""
Port Scanner - Scan ports on a target host
Supports both single port and range scanning with multi-threading
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, format_duration
import time


logger = get_logger(__name__)


# Common ports and their services
COMMON_PORTS = {
    20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP Proxy", 8443: "HTTPS Alt"
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """
    Scan a single port

    Args:
        host: Target host
        port: Port number
        timeout: Socket timeout

    Returns:
        Tuple of (port, is_open, service_name)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                return (port, True, service)
    except socket.gaierror:
        logger.error(f"Hostname could not be resolved: {host}")
    except socket.error as e:
        logger.error(f"Could not connect to {host}:{port} - {e}")

    return (port, False, "")


def scan_ports(host: str, ports: List[int], max_workers: int = 100, timeout: float = 1.0):
    """
    Scan multiple ports on a host

    Args:
        host: Target host
        ports: List of ports to scan
        max_workers: Maximum number of threads
        timeout: Socket timeout
    """
    logger.info(f"Scanning {host} for {len(ports)} ports...")
    start_time = time.time()

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, host, port, timeout): port
            for port in ports
        }

        completed = 0
        for future in as_completed(future_to_port):
            completed += 1
            if completed % 100 == 0:
                logger.info(f"Scanned {completed}/{len(ports)} ports...")

            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
                logger.info(f"Port {port} is OPEN - {service}")

    duration = time.time() - start_time

    print("\n" + "=" * 60)
    print(f"Scan Results for {host}")
    print("=" * 60)
    print(f"Total ports scanned: {len(ports)}")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Scan duration: {format_duration(duration)}")

    if open_ports:
        print("\nOpen Ports:")
        print("-" * 60)
        for port, service in sorted(open_ports):
            print(f"  {port:5d}  -  {service}")
    else:
        print("\nNo open ports found.")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Scan ports on a target host",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s example.com -p 80,443,8080
  %(prog)s 192.168.1.1 -r 1-1000
  %(prog)s example.com --common
  %(prog)s example.com -r 1-65535 -t 0.5 -w 200
        """
    )

    parser.add_argument("host", help="Target host (IP or hostname)")
    parser.add_argument("-p", "--ports", help="Comma-separated port list (e.g., 80,443,8080)")
    parser.add_argument("-r", "--range", help="Port range (e.g., 1-1000)")
    parser.add_argument("--common", action="store_true", help="Scan common ports only")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Connection timeout (default: 1.0s)")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Max concurrent threads (default: 100)")

    args = parser.parse_args()

    # Determine which ports to scan
    ports = []

    if args.common:
        ports = list(COMMON_PORTS.keys())
    elif args.ports:
        ports = [int(p.strip()) for p in args.ports.split(',')]
    elif args.range:
        start, end = map(int, args.range.split('-'))
        ports = list(range(start, end + 1))
    else:
        logger.error("Please specify ports with -p, -r, or --common")
        return

    # Validate ports
    ports = [p for p in ports if 1 <= p <= 65535]

    if not ports:
        logger.error("No valid ports to scan")
        return

    scan_ports(args.host, ports, args.workers, args.timeout)


if __name__ == "__main__":
    main()
