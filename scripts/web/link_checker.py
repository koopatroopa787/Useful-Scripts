#!/usr/bin/env python3
"""
Link Checker - Check URLs for availability and response codes
Supports both single URLs and batch checking from files
"""

import requests
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, validate_url


logger = get_logger(__name__)


def check_url(url, timeout=10):
    """
    Check if a URL is accessible

    Args:
        url: URL to check
        timeout: Request timeout

    Returns:
        Tuple of (url, status_code, message)
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return (url, response.status_code, "OK")
    except requests.exceptions.Timeout:
        return (url, 0, "Timeout")
    except requests.exceptions.ConnectionError:
        return (url, 0, "Connection Error")
    except requests.exceptions.TooManyRedirects:
        return (url, 0, "Too Many Redirects")
    except requests.exceptions.RequestException as e:
        return (url, 0, str(e))


def check_urls(urls, max_workers=10, timeout=10):
    """
    Check multiple URLs concurrently

    Args:
        urls: List of URLs to check
        max_workers: Maximum concurrent requests
        timeout: Request timeout
    """
    results = {
        'success': [],
        'redirects': [],
        'client_errors': [],
        'server_errors': [],
        'failed': []
    }

    print(f"Checking {len(urls)} URL(s)...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(check_url, url, timeout): url
            for url in urls
        }

        completed = 0
        for future in as_completed(future_to_url):
            completed += 1
            url, status_code, message = future.result()

            # Categorize results
            if 200 <= status_code < 300:
                results['success'].append((url, status_code, message))
                print(f"[✓] {status_code} - {url}")
            elif 300 <= status_code < 400:
                results['redirects'].append((url, status_code, message))
                print(f"[→] {status_code} - {url}")
            elif 400 <= status_code < 500:
                results['client_errors'].append((url, status_code, message))
                print(f"[✗] {status_code} - {url}")
            elif 500 <= status_code < 600:
                results['server_errors'].append((url, status_code, message))
                print(f"[✗] {status_code} - {url}")
            else:
                results['failed'].append((url, status_code, message))
                print(f"[!] {message} - {url}")

            # Progress
            if completed % 10 == 0:
                print(f"Progress: {completed}/{len(urls)}")

    # Print summary
    print("\n" + "=" * 70)
    print("Link Check Summary")
    print("=" * 70)
    print(f"Total URLs checked: {len(urls)}")
    print(f"Successful (2xx): {len(results['success'])}")
    print(f"Redirects (3xx): {len(results['redirects'])}")
    print(f"Client Errors (4xx): {len(results['client_errors'])}")
    print(f"Server Errors (5xx): {len(results['server_errors'])}")
    print(f"Failed: {len(results['failed'])}")
    print("=" * 70)

    return results


def extract_urls_from_file(file_path):
    """Extract URLs from a text file"""
    urls = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if validate_url(line):
                    urls.append(line)

    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Check URLs for availability and response codes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com
  %(prog)s -f urls.txt
  %(prog)s https://example.com https://google.com -w 20
  %(prog)s -f urls.txt -t 5 --output report.txt
        """
    )

    parser.add_argument(
        'urls',
        nargs='*',
        help='URLs to check'
    )

    parser.add_argument(
        '-f', '--file',
        help='File containing URLs (one per line)'
    )

    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=10,
        help='Maximum concurrent requests (default: 10)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Save results to file'
    )

    args = parser.parse_args()

    # Collect URLs
    urls = list(args.urls) if args.urls else []

    if args.file:
        file_urls = extract_urls_from_file(args.file)
        urls.extend(file_urls)

    if not urls:
        parser.error("No URLs provided. Use positional arguments or -f/--file")

    # Remove duplicates
    urls = list(set(urls))

    # Check URLs
    results = check_urls(urls, args.workers, args.timeout)

    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write("Link Check Results\n")
            f.write("=" * 70 + "\n\n")

            for category, items in results.items():
                if items:
                    f.write(f"\n{category.upper().replace('_', ' ')}:\n")
                    f.write("-" * 70 + "\n")
                    for url, code, msg in items:
                        f.write(f"{code} - {url} - {msg}\n")

        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
