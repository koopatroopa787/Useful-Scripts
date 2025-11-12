#!/usr/bin/env python3
"""
Useful Scripts - Unified CLI Tool
Main command-line interface for running all utility scripts
"""

import sys
import subprocess
import argparse
from pathlib import Path
from utils import get_logger, load_config

logger = get_logger(__name__)


class UsefulScriptsCLI:
    """Main CLI for Useful Scripts"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.scripts_dir = self.base_dir / 'scripts'
        self.config = load_config()

        self.categories = {
            'system': {
                'description': 'System monitoring and management',
                'scripts': {
                    'cpu': 'Monitor CPU and memory usage',
                    'shutdown': 'Auto shutdown when downloads complete'
                }
            },
            'file_management': {
                'description': 'File operations and organization',
                'scripts': {
                    'duplicate-remover': 'Find and remove duplicate files',
                    'sorter': 'Organize files into categories',
                    'resizer': 'Batch resize images'
                }
            },
            'media': {
                'description': 'Media processing and conversion',
                'scripts': {
                    'pdf2text': 'Extract text from PDFs',
                    'url2qr': 'Generate QR codes from URLs',
                    'web2ebook': 'Convert web articles to ePub',
                    'text2speech': 'Convert text to speech'
                }
            },
            'web': {
                'description': 'Web scraping and monitoring',
                'scripts': {
                    'webmaster': 'Check website availability',
                    'reddit': 'Fetch Reddit posts',
                    'weather': 'Get weather information',
                    'link-checker': 'Check URL availability',
                    'sitemap': 'Generate website sitemaps'
                }
            },
            'security': {
                'description': 'Security and password tools',
                'scripts': {
                    'password': 'Password generator and manager'
                }
            },
            'network': {
                'description': 'Network utilities and diagnostics',
                'scripts': {
                    'port-scan': 'Scan ports on target hosts',
                    'ip-info': 'Get IP address information',
                    'network-monitor': 'Monitor network bandwidth',
                    'ping-sweep': 'Discover active hosts on network'
                }
            },
            'automation': {
                'description': 'Task automation and scheduling',
                'scripts': {
                    'file-watcher': 'Monitor directories for changes',
                    'backup': 'Create compressed backups',
                    'scheduler': 'Schedule and run tasks'
                }
            },
            'data_processing': {
                'description': 'Data analysis and conversion',
                'scripts': {
                    'csv-json': 'Convert between CSV and JSON',
                    'log-analyzer': 'Analyze log files',
                    'data-generator': 'Generate test data'
                }
            }
        }

        # Map script names to actual file paths
        self.script_map = {
            'cpu': 'system/cpu.py',
            'shutdown': 'system/shutONdown.py',
            'duplicate-remover': 'file_management/duplicate_remover.py',
            'sorter': 'file_management/sorter.py',
            'resizer': 'file_management/image_resizer.py',
            'pdf2text': 'media/pdf2text.py',
            'url2qr': 'media/url2qr.py',
            'web2ebook': 'media/web2ebook.py',
            'text2speech': 'media/text2speech.py',
            'webmaster': 'web/webmaster.py',
            'reddit': 'web/reddit.py',
            'weather': 'web/weather.py',
            'link-checker': 'web/link_checker.py',
            'sitemap': 'web/sitemap_generator.py',
            'password': 'security/password.py',
            'port-scan': 'network/port_scanner.py',
            'ip-info': 'network/ip_info.py',
            'network-monitor': 'network/network_monitor.py',
            'ping-sweep': 'network/ping_sweep.py',
            'file-watcher': 'automation/file_watcher.py',
            'backup': 'automation/backup_utility.py',
            'scheduler': 'automation/task_scheduler.py',
            'csv-json': 'data_processing/csv_json_converter.py',
            'log-analyzer': 'data_processing/log_analyzer.py',
            'data-generator': 'data_processing/data_generator.py'
        }

    def list_scripts(self, category=None):
        """List all available scripts"""
        print("\n" + "=" * 80)
        print(f"{'Useful Scripts - Available Tools':^80}")
        print("=" * 80 + "\n")

        if category:
            if category not in self.categories:
                logger.error(f"Unknown category: {category}")
                return

            categories = {category: self.categories[category]}
        else:
            categories = self.categories

        for cat_name, cat_info in categories.items():
            print(f"\n{cat_name.upper().replace('_', ' ')}")
            print(f"{cat_info['description']}")
            print("-" * 80)

            for script_name, description in cat_info['scripts'].items():
                print(f"  {script_name:25s} - {description}")

        print("\n" + "=" * 80)
        print("\nUsage: useful_scripts.py <script-name> [arguments]")
        print("       useful_scripts.py run <script-name> [arguments]")
        print("       useful_scripts.py list [category]")
        print("=" * 80 + "\n")

    def run_script(self, script_name, args):
        """
        Run a script with given arguments

        Args:
            script_name: Name of the script
            args: Arguments to pass to the script
        """
        if script_name not in self.script_map:
            logger.error(f"Unknown script: {script_name}")
            logger.info("Run 'useful_scripts.py list' to see all available scripts")
            return False

        script_path = self.scripts_dir / self.script_map[script_name]

        if not script_path.exists():
            logger.error(f"Script file not found: {script_path}")
            return False

        # Build command
        cmd = [sys.executable, str(script_path)] + args

        try:
            logger.info(f"Running: {script_name}")
            result = subprocess.run(cmd)
            return result.returncode == 0

        except KeyboardInterrupt:
            print("\n\nScript interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Error running script: {e}")
            return False

    def show_config(self):
        """Show current configuration"""
        print("\n" + "=" * 80)
        print("Current Configuration")
        print("=" * 80)

        import json
        print(json.dumps(self.config, indent=2))

        print("=" * 80 + "\n")


def main():
    cli = UsefulScriptsCLI()

    parser = argparse.ArgumentParser(
        description="Useful Scripts - Unified CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                          # List all scripts
  %(prog)s list network                  # List network scripts
  %(prog)s port-scan 192.168.1.1         # Run port scanner
  %(prog)s run backup /data /backups     # Run backup utility
  %(prog)s config                        # Show configuration

Categories:
  system, file_management, media, web, security,
  network, automation, data_processing
        """,
        add_help=True
    )

    parser.add_argument(
        'command',
        nargs='?',
        help='Command or script name'
    )

    parser.add_argument(
        'args',
        nargs=argparse.REMAINDER,
        help='Arguments to pass to the script'
    )

    if len(sys.argv) == 1:
        cli.list_scripts()
        return

    args = parser.parse_args()

    # Handle special commands
    if args.command == 'list':
        category = args.args[0] if args.args else None
        cli.list_scripts(category)

    elif args.command == 'config':
        cli.show_config()

    elif args.command == 'run':
        if not args.args:
            logger.error("No script name provided")
            return

        script_name = args.args[0]
        script_args = args.args[1:]
        cli.run_script(script_name, script_args)

    else:
        # Treat first argument as script name
        cli.run_script(args.command, args.args)


if __name__ == "__main__":
    main()
