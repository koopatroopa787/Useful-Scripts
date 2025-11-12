#!/usr/bin/env python3
"""
Log Analyzer - Analyze log files for patterns, errors, and statistics
Supports multiple log formats and provides detailed insights
"""

import re
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, format_bytes


logger = get_logger(__name__)


class LogAnalyzer:
    """Analyze log files"""

    def __init__(self, log_file):
        self.log_file = Path(log_file)
        self.lines = []
        self.errors = []
        self.warnings = []
        self.timestamps = []
        self.ip_addresses = Counter()
        self.status_codes = Counter()
        self.methods = Counter()
        self.user_agents = Counter()

        if not self.log_file.exists():
            raise FileNotFoundError(f"Log file not found: {log_file}")

        self._parse_log()

    def _parse_log(self):
        """Parse the log file"""
        logger.info(f"Analyzing log file: {self.log_file}")

        # Common patterns
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        timestamp_pattern = r'\[(.*?)\]'
        status_pattern = r'\s(\d{3})\s'
        method_pattern = r'\"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)'

        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                self.lines.append(line.strip())

                # Check for errors and warnings
                line_lower = line.lower()
                if 'error' in line_lower:
                    self.errors.append((line_num, line.strip()))
                if 'warning' in line_lower or 'warn' in line_lower:
                    self.warnings.append((line_num, line.strip()))

                # Extract IP addresses
                ips = re.findall(ip_pattern, line)
                for ip in ips:
                    self.ip_addresses[ip] += 1

                # Extract timestamps
                timestamps = re.findall(timestamp_pattern, line)
                self.timestamps.extend(timestamps)

                # Extract HTTP status codes
                status = re.findall(status_pattern, line)
                for code in status:
                    self.status_codes[code] += 1

                # Extract HTTP methods
                methods = re.findall(method_pattern, line)
                for method in methods:
                    self.methods[method] += 1

    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 70)
        print(f"{'Log Analysis Report':^70}")
        print("=" * 70)
        print(f"File: {self.log_file}")
        print(f"Size: {format_bytes(self.log_file.stat().st_size)}")
        print(f"Total lines: {len(self.lines):,}")
        print("=" * 70)

        # Errors and warnings
        print("\nIssues:")
        print("-" * 70)
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print(f"\nTop 5 Errors:")
            for line_num, error in self.errors[:5]:
                print(f"  Line {line_num}: {error[:80]}...")

        # IP addresses
        if self.ip_addresses:
            print("\n" + "-" * 70)
            print("Top IP Addresses:")
            print("-" * 70)
            for ip, count in self.ip_addresses.most_common(10):
                print(f"  {ip:15s} - {count:,} requests")

        # HTTP status codes
        if self.status_codes:
            print("\n" + "-" * 70)
            print("HTTP Status Codes:")
            print("-" * 70)
            for code, count in sorted(self.status_codes.items()):
                print(f"  {code} - {count:,} occurrences")

        # HTTP methods
        if self.methods:
            print("\n" + "-" * 70)
            print("HTTP Methods:")
            print("-" * 70)
            for method, count in self.methods.most_common():
                print(f"  {method:8s} - {count:,} requests")

        print("\n" + "=" * 70)

    def search_pattern(self, pattern, case_sensitive=False):
        """
        Search for a pattern in the log file

        Args:
            pattern: Regex pattern to search
            case_sensitive: Case sensitive search

        Returns:
            List of matching lines
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)

        matches = []
        for line_num, line in enumerate(self.lines, 1):
            if regex.search(line):
                matches.append((line_num, line))

        return matches

    def filter_by_time(self, start_time=None, end_time=None):
        """
        Filter log entries by time range

        Args:
            start_time: Start time string
            end_time: End time string

        Returns:
            Filtered lines
        """
        # This is a simplified implementation
        # In production, you'd parse actual timestamps
        filtered = []

        for line_num, line in enumerate(self.lines, 1):
            # Add time filtering logic based on your log format
            filtered.append((line_num, line))

        return filtered

    def export_report(self, output_file):
        """Export analysis report to file"""
        with open(output_file, 'w') as f:
            f.write("Log Analysis Report\n")
            f.write("=" * 70 + "\n")
            f.write(f"File: {self.log_file}\n")
            f.write(f"Total lines: {len(self.lines):,}\n")
            f.write(f"Errors: {len(self.errors)}\n")
            f.write(f"Warnings: {len(self.warnings)}\n\n")

            if self.errors:
                f.write("Errors:\n")
                for line_num, error in self.errors:
                    f.write(f"Line {line_num}: {error}\n")

            if self.warnings:
                f.write("\nWarnings:\n")
                for line_num, warning in self.warnings:
                    f.write(f"Line {line_num}: {warning}\n")

        logger.info(f"Report exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for patterns, errors, and statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s access.log
  %(prog)s error.log --search "404"
  %(prog)s app.log --export report.txt
  %(prog)s system.log --search "error" -i
        """
    )

    parser.add_argument(
        'log_file',
        help='Log file to analyze'
    )

    parser.add_argument(
        '-s', '--search',
        help='Search for a pattern (regex supported)'
    )

    parser.add_argument(
        '-i', '--case-insensitive',
        action='store_true',
        help='Case insensitive search'
    )

    parser.add_argument(
        '-e', '--export',
        help='Export report to file'
    )

    parser.add_argument(
        '--errors-only',
        action='store_true',
        help='Show only errors'
    )

    parser.add_argument(
        '--warnings-only',
        action='store_true',
        help='Show only warnings'
    )

    args = parser.parse_args()

    try:
        analyzer = LogAnalyzer(args.log_file)

        if args.search:
            # Search for pattern
            case_sensitive = not args.case_insensitive
            matches = analyzer.search_pattern(args.search, case_sensitive)

            print(f"\nFound {len(matches)} matching line(s):\n")
            print("-" * 70)

            for line_num, line in matches[:50]:  # Show first 50 matches
                print(f"Line {line_num}: {line}")

            if len(matches) > 50:
                print(f"\n... and {len(matches) - 50} more matches")

        elif args.errors_only:
            # Show only errors
            print(f"\nFound {len(analyzer.errors)} error(s):\n")
            print("-" * 70)

            for line_num, error in analyzer.errors:
                print(f"Line {line_num}: {error}")

        elif args.warnings_only:
            # Show only warnings
            print(f"\nFound {len(analyzer.warnings)} warning(s):\n")
            print("-" * 70)

            for line_num, warning in analyzer.warnings:
                print(f"Line {line_num}: {warning}")

        else:
            # Show full summary
            analyzer.print_summary()

        # Export report if requested
        if args.export:
            analyzer.export_report(args.export)
            print(f"\nReport exported to: {args.export}")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
