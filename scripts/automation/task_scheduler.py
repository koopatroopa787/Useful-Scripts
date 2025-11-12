#!/usr/bin/env python3
"""
Task Scheduler - Schedule and run tasks at specific times or intervals
Simple cron-like task scheduler with support for one-time and recurring tasks
"""

import time
import argparse
import subprocess
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, get_timestamp


logger = get_logger(__name__)


class Task:
    """Represents a scheduled task"""

    def __init__(self, name, command, schedule_type, schedule_value, enabled=True):
        self.name = name
        self.command = command
        self.schedule_type = schedule_type  # 'interval', 'daily', 'time'
        self.schedule_value = schedule_value
        self.enabled = enabled
        self.last_run = None
        self.next_run = None
        self.run_count = 0

        self._calculate_next_run()

    def _calculate_next_run(self):
        """Calculate next run time"""
        now = datetime.now()

        if self.schedule_type == 'interval':
            # Run every N seconds
            if self.last_run:
                self.next_run = self.last_run + timedelta(seconds=self.schedule_value)
            else:
                self.next_run = now

        elif self.schedule_type == 'daily':
            # Run daily at specific time (HH:MM format)
            hour, minute = map(int, self.schedule_value.split(':'))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if next_run <= now:
                next_run += timedelta(days=1)

            self.next_run = next_run

        elif self.schedule_type == 'time':
            # Run once at specific time
            target_time = datetime.strptime(self.schedule_value, '%Y-%m-%d %H:%M:%S')
            self.next_run = target_time

    def should_run(self):
        """Check if task should run now"""
        if not self.enabled:
            return False

        if self.next_run is None:
            return False

        return datetime.now() >= self.next_run

    def execute(self):
        """Execute the task"""
        timestamp = get_timestamp()
        logger.info(f"[{timestamp}] Executing task: {self.name}")

        try:
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            self.last_run = datetime.now()
            self.run_count += 1

            if result.returncode == 0:
                logger.info(f"Task '{self.name}' completed successfully")
                if result.stdout:
                    logger.info(f"Output: {result.stdout.strip()}")
            else:
                logger.error(f"Task '{self.name}' failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"Error: {result.stderr.strip()}")

            # Calculate next run time
            if self.schedule_type != 'time':  # Don't reschedule one-time tasks
                self._calculate_next_run()
            else:
                self.enabled = False  # Disable one-time tasks after execution

        except subprocess.TimeoutExpired:
            logger.error(f"Task '{self.name}' timed out")
        except Exception as e:
            logger.error(f"Error executing task '{self.name}': {e}")

    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'name': self.name,
            'command': self.command,
            'schedule_type': self.schedule_type,
            'schedule_value': self.schedule_value,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count
        }


class TaskScheduler:
    """Manage and execute scheduled tasks"""

    def __init__(self, config_file=None):
        self.config_file = config_file or Path.home() / '.useful_scripts' / 'tasks.json'
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from config file"""
        if not Path(self.config_file).exists():
            return

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                for task_data in data.get('tasks', []):
                    task = Task(
                        task_data['name'],
                        task_data['command'],
                        task_data['schedule_type'],
                        task_data['schedule_value'],
                        task_data.get('enabled', True)
                    )
                    self.tasks.append(task)

            logger.info(f"Loaded {len(self.tasks)} task(s)")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")

    def save_tasks(self):
        """Save tasks to config file"""
        Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)

        data = {
            'tasks': [task.to_dict() for task in self.tasks]
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")

    def add_task(self, name, command, schedule_type, schedule_value):
        """Add a new task"""
        task = Task(name, command, schedule_type, schedule_value)
        self.tasks.append(task)
        self.save_tasks()
        logger.info(f"Task '{name}' added")

    def remove_task(self, name):
        """Remove a task"""
        self.tasks = [t for t in self.tasks if t.name != name]
        self.save_tasks()
        logger.info(f"Task '{name}' removed")

    def list_tasks(self):
        """List all tasks"""
        if not self.tasks:
            print("No tasks scheduled")
            return

        print("\n" + "=" * 80)
        print("Scheduled Tasks")
        print("=" * 80)

        for task in self.tasks:
            status = "Enabled" if task.enabled else "Disabled"
            print(f"\n{task.name} [{status}]")
            print(f"  Command: {task.command}")
            print(f"  Schedule: {task.schedule_type} - {task.schedule_value}")
            print(f"  Run count: {task.run_count}")

            if task.last_run:
                print(f"  Last run: {task.last_run.strftime('%Y-%m-%d %H:%M:%S')}")

            if task.next_run and task.enabled:
                print(f"  Next run: {task.next_run.strftime('%Y-%m-%d %H:%M:%S')}")

        print("=" * 80 + "\n")

    def run(self):
        """Run the scheduler"""
        logger.info("Task scheduler started")
        print("Task scheduler is running. Press Ctrl+C to stop.\n")

        try:
            while True:
                for task in self.tasks:
                    if task.should_run():
                        task.execute()
                        self.save_tasks()

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\nScheduler stopped")


def main():
    parser = argparse.ArgumentParser(
        description="Schedule and run tasks at specific times or intervals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add tasks
  %(prog)s add "Backup" "python backup.py" interval 3600
  %(prog)s add "Daily Report" "python report.py" daily "09:00"
  %(prog)s add "One Time" "echo 'Hello'" time "2024-12-31 23:59:00"

  # List and manage tasks
  %(prog)s list
  %(prog)s remove "Backup"

  # Run scheduler
  %(prog)s run
        """
    )

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Add task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('name', help='Task name')
    add_parser.add_argument('command', help='Command to execute')
    add_parser.add_argument('type', choices=['interval', 'daily', 'time'], help='Schedule type')
    add_parser.add_argument('value', help='Schedule value (seconds for interval, HH:MM for daily, datetime for time)')

    # Remove task
    remove_parser = subparsers.add_parser('remove', help='Remove a task')
    remove_parser.add_argument('name', help='Task name')

    # List tasks
    subparsers.add_parser('list', help='List all tasks')

    # Run scheduler
    subparsers.add_parser('run', help='Run the scheduler')

    parser.add_argument('-c', '--config', help='Config file path')

    args = parser.parse_args()

    scheduler = TaskScheduler(args.config)

    if args.action == 'add':
        # Validate schedule value
        if args.type == 'interval':
            try:
                value = int(args.value)
            except ValueError:
                logger.error("Interval must be a number (seconds)")
                return
        else:
            value = args.value

        scheduler.add_task(args.name, args.command, args.type, value)
        print(f"Task '{args.name}' added successfully")

    elif args.action == 'remove':
        scheduler.remove_task(args.name)
        print(f"Task '{args.name}' removed")

    elif args.action == 'list':
        scheduler.list_tasks()

    elif args.action == 'run':
        scheduler.run()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
