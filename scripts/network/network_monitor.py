#!/usr/bin/env python3
"""
Network Monitor - Monitor network bandwidth usage in real-time
Shows upload/download speeds and total data transferred
"""

import psutil
import time
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, format_bytes


logger = get_logger(__name__)


def get_network_stats():
    """Get current network statistics"""
    stats = psutil.net_io_counters()
    return {
        'bytes_sent': stats.bytes_sent,
        'bytes_recv': stats.bytes_recv,
        'packets_sent': stats.packets_sent,
        'packets_recv': stats.packets_recv,
        'errin': stats.errin,
        'errout': stats.errout,
        'dropin': stats.dropin,
        'dropout': stats.dropout
    }


def monitor_network(interval: int = 1, duration: int = None):
    """
    Monitor network bandwidth in real-time

    Args:
        interval: Update interval in seconds
        duration: Total duration to monitor (None for infinite)
    """
    print("Starting network monitor... (Press Ctrl+C to stop)\n")

    prev_stats = get_network_stats()
    start_time = time.time()

    try:
        elapsed = 0
        while True:
            time.sleep(interval)
            current_stats = get_network_stats()
            elapsed += interval

            # Calculate rates
            upload_rate = (current_stats['bytes_sent'] - prev_stats['bytes_sent']) / interval
            download_rate = (current_stats['bytes_recv'] - prev_stats['bytes_recv']) / interval

            # Total transferred
            total_sent = current_stats['bytes_sent']
            total_recv = current_stats['bytes_recv']

            # Clear screen and display stats
            print('\033[2J\033[H')  # Clear screen
            print("=" * 70)
            print(f"{'Network Monitor':^70}")
            print("=" * 70)
            print(f"Monitoring time: {elapsed}s")
            print("-" * 70)
            print(f"{'Upload Speed:':30s} {format_bytes(upload_rate)}/s")
            print(f"{'Download Speed:':30s} {format_bytes(download_rate)}/s")
            print("-" * 70)
            print(f"{'Total Uploaded:':30s} {format_bytes(total_sent)}")
            print(f"{'Total Downloaded:':30s} {format_bytes(total_recv)}")
            print(f"{'Total Data:':30s} {format_bytes(total_sent + total_recv)}")
            print("-" * 70)
            print(f"{'Packets Sent:':30s} {current_stats['packets_sent']:,}")
            print(f"{'Packets Received:':30s} {current_stats['packets_recv']:,}")

            if current_stats['errin'] > 0 or current_stats['errout'] > 0:
                print("-" * 70)
                print(f"{'Errors In:':30s} {current_stats['errin']}")
                print(f"{'Errors Out:':30s} {current_stats['errout']}")

            print("=" * 70)
            print("\nPress Ctrl+C to stop monitoring")

            prev_stats = current_stats

            if duration and elapsed >= duration:
                break

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        total_time = time.time() - start_time
        print(f"\nMonitoring duration: {total_time:.1f}s")


def show_interface_stats():
    """Show statistics for all network interfaces"""
    stats = psutil.net_io_counters(pernic=True)

    print("\n" + "=" * 70)
    print(f"{'Network Interface Statistics':^70}")
    print("=" * 70)

    for interface, stat in stats.items():
        print(f"\nInterface: {interface}")
        print("-" * 70)
        print(f"  {'Sent:':20s} {format_bytes(stat.bytes_sent)}")
        print(f"  {'Received:':20s} {format_bytes(stat.bytes_recv)}")
        print(f"  {'Packets Sent:':20s} {stat.packets_sent:,}")
        print(f"  {'Packets Received:':20s} {stat.packets_recv:,}")

        if stat.errin > 0 or stat.errout > 0:
            print(f"  {'Errors In:':20s} {stat.errin}")
            print(f"  {'Errors Out:':20s} {stat.errout}")

    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor network bandwidth usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Monitor with 1s interval
  %(prog)s -i 2               # Monitor with 2s interval
  %(prog)s -d 60              # Monitor for 60 seconds
  %(prog)s --interfaces       # Show interface statistics
        """
    )

    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=1,
        help="Update interval in seconds (default: 1)"
    )

    parser.add_argument(
        "-d", "--duration",
        type=int,
        help="Monitoring duration in seconds (default: infinite)"
    )

    parser.add_argument(
        "--interfaces",
        action="store_true",
        help="Show statistics for all interfaces and exit"
    )

    args = parser.parse_args()

    if args.interfaces:
        show_interface_stats()
    else:
        monitor_network(args.interval, args.duration)


if __name__ == "__main__":
    main()
