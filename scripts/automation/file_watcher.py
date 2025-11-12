#!/usr/bin/env python3
"""
File Watcher - Monitor directories for file system changes
Triggers actions when files are created, modified, deleted, or moved
"""

import time
import argparse
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, get_timestamp


logger = get_logger(__name__)


class FileWatcherHandler(FileSystemEventHandler):
    """Handle file system events"""

    def __init__(self, command=None, patterns=None, ignore_patterns=None):
        super().__init__()
        self.command = command
        self.patterns = patterns or []
        self.ignore_patterns = ignore_patterns or []

    def should_process(self, path):
        """Check if file should be processed based on patterns"""
        if not self.patterns:
            return True

        path_str = str(path)

        # Check ignore patterns first
        for pattern in self.ignore_patterns:
            if pattern in path_str:
                return False

        # Check include patterns
        for pattern in self.patterns:
            if pattern in path_str or path_str.endswith(pattern):
                return True

        return False

    def execute_command(self, event_type, src_path, dest_path=None):
        """Execute the configured command"""
        if not self.command:
            return

        timestamp = get_timestamp()
        print(f"\n[{timestamp}] {event_type}: {src_path}")

        if dest_path:
            print(f"  -> {dest_path}")

        try:
            # Replace placeholders in command
            cmd = self.command.replace('{file}', str(src_path))
            cmd = cmd.replace('{event}', event_type)

            if dest_path:
                cmd = cmd.replace('{dest}', str(dest_path))

            print(f"  Executing: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            print(f"  Command completed successfully")

        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e}")

    def on_created(self, event):
        if not event.is_directory and self.should_process(event.src_path):
            self.execute_command('CREATED', event.src_path)

    def on_modified(self, event):
        if not event.is_directory and self.should_process(event.src_path):
            self.execute_command('MODIFIED', event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and self.should_process(event.src_path):
            self.execute_command('DELETED', event.src_path)

    def on_moved(self, event):
        if not event.is_directory and self.should_process(event.src_path):
            self.execute_command('MOVED', event.src_path, event.dest_path)


def watch_directory(path, recursive=True, command=None, patterns=None, ignore_patterns=None):
    """
    Watch a directory for changes

    Args:
        path: Directory to watch
        recursive: Watch subdirectories
        command: Command to execute on changes
        patterns: File patterns to watch
        ignore_patterns: File patterns to ignore
    """
    path = Path(path).resolve()

    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return

    if not path.is_dir():
        logger.error(f"Path is not a directory: {path}")
        return

    event_handler = FileWatcherHandler(command, patterns, ignore_patterns)
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=recursive)

    print("=" * 70)
    print("File Watcher Started")
    print("=" * 70)
    print(f"Watching: {path}")
    print(f"Recursive: {recursive}")

    if patterns:
        print(f"Patterns: {', '.join(patterns)}")

    if ignore_patterns:
        print(f"Ignoring: {', '.join(ignore_patterns)}")

    if command:
        print(f"Command: {command}")

    print("=" * 70)
    print("\nPress Ctrl+C to stop watching\n")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\nFile watcher stopped.")

    observer.join()


def main():
    parser = argparse.ArgumentParser(
        description="Monitor directories for file system changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/watch
  %(prog)s /path/to/watch -p "*.py" "*.txt"
  %(prog)s /path/to/watch -c "echo 'File changed: {file}'"
  %(prog)s /path/to/watch -p "*.log" -c "cat {file} >> combined.log"
  %(prog)s ~/Downloads -p "*.pdf" -c "mv {file} ~/Documents/PDFs/"

Placeholders in command:
  {file}  - Path to the file that triggered the event
  {event} - Type of event (CREATED, MODIFIED, DELETED, MOVED)
  {dest}  - Destination path (only for MOVED events)
        """
    )

    parser.add_argument(
        "path",
        help="Directory to watch"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        default=True,
        help="Watch subdirectories recursively (default: True)"
    )

    parser.add_argument(
        "-p", "--patterns",
        nargs="+",
        help="File patterns to watch (e.g., *.py *.txt)"
    )

    parser.add_argument(
        "-i", "--ignore",
        nargs="+",
        help="Patterns to ignore"
    )

    parser.add_argument(
        "-c", "--command",
        help="Command to execute on file changes"
    )

    args = parser.parse_args()

    watch_directory(
        args.path,
        args.recursive,
        args.command,
        args.patterns,
        args.ignore
    )


if __name__ == "__main__":
    main()
