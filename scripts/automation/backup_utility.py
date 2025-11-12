#!/usr/bin/env python3
"""
Backup Utility - Create compressed backups of files and directories
Supports incremental backups, compression, and automatic cleanup of old backups
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import tarfile
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, format_bytes, get_timestamp


logger = get_logger(__name__)


class BackupUtility:
    """Backup utility class"""

    def __init__(self, source, destination, name=None):
        self.source = Path(source).resolve()
        self.destination = Path(destination).resolve()
        self.name = name or self.source.name

        if not self.source.exists():
            raise ValueError(f"Source does not exist: {self.source}")

        self.destination.mkdir(parents=True, exist_ok=True)

    def create_backup(self, compression='gz', incremental=False):
        """
        Create a backup

        Args:
            compression: Compression type (gz, bz2, xz, or none)
            incremental: Create incremental backup

        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{self.name}_{timestamp}"

        # Determine file extension
        if compression == 'none':
            backup_file = self.destination / f"{backup_name}.tar"
            mode = 'w'
        elif compression == 'gz':
            backup_file = self.destination / f"{backup_name}.tar.gz"
            mode = 'w:gz'
        elif compression == 'bz2':
            backup_file = self.destination / f"{backup_name}.tar.bz2"
            mode = 'w:bz2'
        elif compression == 'xz':
            backup_file = self.destination / f"{backup_name}.tar.xz"
            mode = 'w:xz'
        else:
            raise ValueError(f"Unsupported compression: {compression}")

        logger.info(f"Creating backup: {backup_file}")
        start_time = datetime.now()

        try:
            # Create tar archive
            with tarfile.open(backup_file, mode) as tar:
                if self.source.is_file():
                    tar.add(self.source, arcname=self.source.name)
                else:
                    tar.add(self.source, arcname=self.name)

            # Calculate size and duration
            size = backup_file.stat().st_size
            duration = (datetime.now() - start_time).total_seconds()

            # Save backup metadata
            self._save_metadata(backup_file, size, duration)

            logger.info(f"Backup created successfully: {format_bytes(size)} in {duration:.1f}s")
            return backup_file

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            if backup_file.exists():
                backup_file.unlink()
            raise

    def _save_metadata(self, backup_file, size, duration):
        """Save backup metadata"""
        metadata_file = backup_file.with_suffix(backup_file.suffix + '.meta')

        metadata = {
            'backup_file': backup_file.name,
            'source': str(self.source),
            'timestamp': get_timestamp(),
            'size': size,
            'size_human': format_bytes(size),
            'duration': duration,
            'compression': backup_file.suffix.lstrip('.')
        }

        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def list_backups(self):
        """List all backups"""
        backups = []

        for file in self.destination.glob(f"{self.name}_*.tar*"):
            if file.suffix in ['.tar', '.gz', '.bz2', '.xz']:
                meta_file = file.with_suffix(file.suffix + '.meta')

                if meta_file.exists():
                    try:
                        with open(meta_file, 'r') as f:
                            metadata = json.load(f)
                            backups.append(metadata)
                    except:
                        pass
                else:
                    # Create basic info if no metadata
                    backups.append({
                        'backup_file': file.name,
                        'timestamp': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                        'size': file.stat().st_size,
                        'size_human': format_bytes(file.stat().st_size)
                    })

        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

    def cleanup_old_backups(self, keep_count=None, keep_days=None):
        """
        Remove old backups

        Args:
            keep_count: Number of recent backups to keep
            keep_days: Keep backups newer than this many days
        """
        backups = self.list_backups()

        if not backups:
            logger.info("No backups to clean up")
            return

        to_delete = []

        if keep_count:
            to_delete.extend(backups[keep_count:])
        elif keep_days:
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            to_delete = [
                b for b in backups
                if datetime.strptime(b['timestamp'], '%Y-%m-%d %H:%M:%S') < cutoff_date
            ]

        if not to_delete:
            logger.info("No old backups to delete")
            return

        logger.info(f"Deleting {len(to_delete)} old backup(s)")

        for backup in to_delete:
            backup_file = self.destination / backup['backup_file']
            meta_file = backup_file.with_suffix(backup_file.suffix + '.meta')

            if backup_file.exists():
                backup_file.unlink()
                logger.info(f"Deleted: {backup_file.name}")

            if meta_file.exists():
                meta_file.unlink()


def main():
    parser = argparse.ArgumentParser(
        description="Create compressed backups of files and directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/source /path/to/backups
  %(prog)s ~/Documents ~/Backups -c bz2
  %(prog)s /etc /backups/etc --keep-count 5
  %(prog)s ~/project ~/backups/project --keep-days 30
  %(prog)s ~/data ~/backups --list
        """
    )

    parser.add_argument(
        "source",
        help="Source file or directory to backup"
    )

    parser.add_argument(
        "destination",
        help="Backup destination directory"
    )

    parser.add_argument(
        "-n", "--name",
        help="Backup name (default: source name)"
    )

    parser.add_argument(
        "-c", "--compression",
        choices=['none', 'gz', 'bz2', 'xz'],
        default='gz',
        help="Compression type (default: gz)"
    )

    parser.add_argument(
        "--keep-count",
        type=int,
        help="Number of recent backups to keep"
    )

    parser.add_argument(
        "--keep-days",
        type=int,
        help="Keep backups newer than N days"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List existing backups"
    )

    args = parser.parse_args()

    try:
        backup = BackupUtility(args.source, args.destination, args.name)

        if args.list:
            # List backups
            backups = backup.list_backups()

            print("\n" + "=" * 70)
            print(f"Backups for: {args.source}")
            print("=" * 70)

            if not backups:
                print("No backups found")
            else:
                for b in backups:
                    print(f"\n{b['backup_file']}")
                    print(f"  Timestamp: {b['timestamp']}")
                    print(f"  Size: {b['size_human']}")
                    if 'duration' in b:
                        print(f"  Duration: {b['duration']:.1f}s")

            print("=" * 70 + "\n")

        else:
            # Create backup
            backup_file = backup.create_backup(args.compression)

            print("\n" + "=" * 70)
            print("Backup Created Successfully")
            print("=" * 70)
            print(f"Source: {args.source}")
            print(f"Backup: {backup_file}")
            print(f"Size: {format_bytes(backup_file.stat().st_size)}")
            print("=" * 70 + "\n")

            # Cleanup old backups if requested
            if args.keep_count or args.keep_days:
                backup.cleanup_old_backups(args.keep_count, args.keep_days)

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
