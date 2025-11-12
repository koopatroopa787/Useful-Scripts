#!/usr/bin/env python3
"""
Ping Sweep - Scan a network to find active hosts
Uses ICMP ping to discover devices on a network
"""

import subprocess
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger


logger = get_logger(__name__)


def ping_host(ip: str, timeout: int = 1) -> tuple:
    """
    Ping a single host

    Args:
        ip: IP address to ping
        timeout: Ping timeout in seconds

    Returns:
        Tuple of (ip, is_alive)
    """
    # Determine ping command based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    wait_param = '-w' if platform.system().lower() == 'windows' else '-W'

    command = ['ping', param, '1', wait_param, str(timeout), str(ip)]

    try:
        output = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout + 1
        )
        return (ip, output.returncode == 0)
    except subprocess.TimeoutExpired:
        return (ip, False)
    except Exception as e:
        logger.error(f"Error pinging {ip}: {e}")
        return (ip, False)


def ping_sweep(network: str, max_workers: int = 50, timeout: int = 1):
    """
    Perform ping sweep on a network

    Args:
        network: Network in CIDR notation (e.g., 192.168.1.0/24)
        max_workers: Maximum number of concurrent threads
        timeout: Ping timeout in seconds
    """
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        logger.error(f"Invalid network: {e}")
        return

    hosts = list(net.hosts())
    total = len(hosts)

    print(f"Scanning {network} ({total} hosts)...\n")

    active_hosts = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {
            executor.submit(ping_host, str(ip), timeout): str(ip)
            for ip in hosts
        }

        completed = 0
        for future in as_completed(future_to_ip):
            completed += 1
            ip, is_alive = future.result()

            if is_alive:
                active_hosts.append(ip)
                print(f"[+] {ip} is UP")

            # Progress indicator
            if completed % 10 == 0:
                progress = (completed / total) * 100
                print(f"Progress: {progress:.1f}% ({completed}/{total})", end='\r')

    print("\n\n" + "=" * 60)
    print(f"Ping Sweep Results for {network}")
    print("=" * 60)
    print(f"Total hosts scanned: {total}")
    print(f"Active hosts found: {len(active_hosts)}")
    print("=" * 60)

    if active_hosts:
        print("\nActive Hosts:")
        print("-" * 60)
        for ip in sorted(active_hosts, key=lambda x: ipaddress.ip_address(x)):
            print(f"  {ip}")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Perform ping sweep to find active hosts on a network",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 192.168.1.0/24
  %(prog)s 10.0.0.0/24 -w 100 -t 2
  %(prog)s 172.16.0.0/16
        """
    )

    parser.add_argument(
        "network",
        help="Network in CIDR notation (e.g., 192.168.1.0/24)"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=50,
        help="Maximum concurrent threads (default: 50)"
    )

    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (default: 1)"
    )

    args = parser.parse_args()

    ping_sweep(args.network, args.workers, args.timeout)


if __name__ == "__main__":
    main()
