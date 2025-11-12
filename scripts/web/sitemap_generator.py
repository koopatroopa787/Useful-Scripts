#!/usr/bin/env python3
"""
Sitemap Generator - Generate XML sitemaps for websites
Crawls a website and creates a sitemap following the sitemaps.org protocol
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, validate_url


logger = get_logger(__name__)


class SitemapGenerator:
    """Generate XML sitemaps by crawling a website"""

    def __init__(self, base_url, max_pages=100):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.visited = set()
        self.urls = []

    def is_valid_url(self, url):
        """Check if URL is valid and belongs to the same domain"""
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            parsed.netloc == self.domain and
            url not in self.visited
        )

    def crawl(self, url):
        """
        Crawl a URL and extract links

        Args:
            url: URL to crawl
        """
        if len(self.visited) >= self.max_pages:
            return

        if url in self.visited:
            return

        try:
            logger.info(f"Crawling: {url}")
            self.visited.add(url)

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Only process HTML pages
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type:
                return

            self.urls.append(url)

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']

                # Convert relative URLs to absolute
                full_url = urljoin(url, href)

                # Remove fragments
                full_url = full_url.split('#')[0]

                if self.is_valid_url(full_url):
                    self.crawl(full_url)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error crawling {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def generate_sitemap(self, output_file='sitemap.xml', priority=0.5, changefreq='weekly'):
        """
        Generate XML sitemap

        Args:
            output_file: Output file path
            priority: Default priority for URLs
            changefreq: Change frequency
        """
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for url in sorted(self.urls):
            xml.append('  <url>')
            xml.append(f'    <loc>{url}</loc>')
            xml.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            xml.append(f'    <changefreq>{changefreq}</changefreq>')
            xml.append(f'    <priority>{priority}</priority>')
            xml.append('  </url>')

        xml.append('</urlset>')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml))

        logger.info(f"Sitemap generated: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate XML sitemaps for websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com -o sitemap.xml -m 500
  %(prog)s https://example.com -p 0.8 -c daily
        """
    )

    parser.add_argument(
        'url',
        help='Website base URL'
    )

    parser.add_argument(
        '-o', '--output',
        default='sitemap.xml',
        help='Output file (default: sitemap.xml)'
    )

    parser.add_argument(
        '-m', '--max-pages',
        type=int,
        default=100,
        help='Maximum pages to crawl (default: 100)'
    )

    parser.add_argument(
        '-p', '--priority',
        type=float,
        default=0.5,
        help='Default priority (0.0-1.0, default: 0.5)'
    )

    parser.add_argument(
        '-c', '--changefreq',
        choices=['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'],
        default='weekly',
        help='Change frequency (default: weekly)'
    )

    args = parser.parse_args()

    if not validate_url(args.url):
        logger.error("Invalid URL provided")
        sys.exit(1)

    try:
        generator = SitemapGenerator(args.url, args.max_pages)

        print(f"Starting sitemap generation for: {args.url}")
        print(f"Max pages: {args.max_pages}\n")

        generator.crawl(args.url)

        print(f"\nCrawled {len(generator.urls)} page(s)")

        generator.generate_sitemap(args.output, args.priority, args.changefreq)

        print("\n" + "=" * 70)
        print("Sitemap Generated Successfully")
        print("=" * 70)
        print(f"Output file: {args.output}")
        print(f"Total URLs: {len(generator.urls)}")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\nCrawling interrupted by user")
        if generator.urls:
            print(f"Generating sitemap with {len(generator.urls)} URLs found so far...")
            generator.generate_sitemap(args.output, args.priority, args.changefreq)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
