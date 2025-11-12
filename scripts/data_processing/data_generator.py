#!/usr/bin/env python3
"""
Data Generator - Generate fake/test data for development and testing
Supports various data types and export formats
"""

import random
import string
import json
import csv
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger


logger = get_logger(__name__)


class DataGenerator:
    """Generate fake test data"""

    def __init__(self, seed=None):
        if seed:
            random.seed(seed)

        self.first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah',
                           'James', 'Emma', 'Robert', 'Olivia', 'William', 'Ava']

        self.last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
                          'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']

        self.domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
                       'example.com', 'test.com']

        self.companies = ['TechCorp', 'DataSystems', 'CloudNet', 'WebSolutions',
                         'CodeFactory', 'DigitalWorks']

        self.cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                      'Philadelphia', 'San Antonio', 'San Diego', 'Dallas']

    def generate_name(self):
        """Generate a random name"""
        return f"{random.choice(self.first_names)} {random.choice(self.last_names)}"

    def generate_email(self, name=None):
        """Generate a random email"""
        if name:
            username = name.lower().replace(' ', '.')
        else:
            username = ''.join(random.choices(string.ascii_lowercase, k=8))

        return f"{username}@{random.choice(self.domains)}"

    def generate_phone(self):
        """Generate a random phone number"""
        return f"+1-{''.join(random.choices(string.digits, k=3))}-{''.join(random.choices(string.digits, k=3))}-{''.join(random.choices(string.digits, k=4))}"

    def generate_date(self, start_year=2020, end_year=2024):
        """Generate a random date"""
        start = datetime(start_year, 1, 1)
        end = datetime(end_year, 12, 31)
        delta = end - start
        random_days = random.randint(0, delta.days)
        return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

    def generate_address(self):
        """Generate a random address"""
        return {
            'street': f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} {''.join(random.choices(['St', 'Ave', 'Rd', 'Blvd'], k=1))[0]}",
            'city': random.choice(self.cities),
            'state': ''.join(random.choices(string.ascii_uppercase, k=2)),
            'zip': ''.join(random.choices(string.digits, k=5))
        }

    def generate_user(self):
        """Generate a complete user record"""
        name = self.generate_name()
        return {
            'id': random.randint(1000, 9999),
            'name': name,
            'email': self.generate_email(name),
            'phone': self.generate_phone(),
            'company': random.choice(self.companies),
            'address': self.generate_address(),
            'join_date': self.generate_date(),
            'active': random.choice([True, False]),
            'score': round(random.uniform(0, 100), 2)
        }

    def generate_transaction(self):
        """Generate a transaction record"""
        return {
            'transaction_id': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            'date': self.generate_date(),
            'amount': round(random.uniform(10, 1000), 2),
            'currency': random.choice(['USD', 'EUR', 'GBP']),
            'status': random.choice(['completed', 'pending', 'failed']),
            'category': random.choice(['groceries', 'electronics', 'clothing', 'entertainment'])
        }

    def generate_log_entry(self):
        """Generate a log entry"""
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        messages = [
            'Application started successfully',
            'Database connection established',
            'User authentication failed',
            'Invalid input received',
            'Processing completed',
            'Resource not found',
            'Timeout error occurred'
        ]

        timestamp = datetime.now() - timedelta(seconds=random.randint(0, 86400))
        return {
            'timestamp': timestamp.isoformat(),
            'level': random.choice(levels),
            'message': random.choice(messages),
            'module': f"module_{random.randint(1, 10)}"
        }

    def generate_dataset(self, data_type, count):
        """
        Generate a dataset

        Args:
            data_type: Type of data to generate
            count: Number of records

        Returns:
            List of records
        """
        generators = {
            'users': self.generate_user,
            'transactions': self.generate_transaction,
            'logs': self.generate_log_entry
        }

        if data_type not in generators:
            raise ValueError(f"Unknown data type: {data_type}")

        logger.info(f"Generating {count} {data_type} records...")

        return [generators[data_type]() for _ in range(count)]


def export_to_json(data, output_file, indent=2):
    """Export data to JSON"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=indent)
    logger.info(f"Exported to JSON: {output_file}")


def export_to_csv(data, output_file):
    """Export data to CSV"""
    if not data:
        return

    # Flatten nested dictionaries
    flattened = []
    for record in data:
        flat_record = {}
        for key, value in record.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flat_record[f"{key}_{sub_key}"] = sub_value
            else:
                flat_record[key] = value
        flattened.append(flat_record)

    keys = flattened[0].keys()

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flattened)

    logger.info(f"Exported to CSV: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate fake/test data for development and testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s users 100 -o users.json
  %(prog)s transactions 50 -o transactions.csv -f csv
  %(prog)s logs 200 -o logs.json --seed 42
        """
    )

    parser.add_argument(
        'type',
        choices=['users', 'transactions', 'logs'],
        help='Type of data to generate'
    )

    parser.add_argument(
        'count',
        type=int,
        help='Number of records to generate'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file path'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducible data'
    )

    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='JSON indentation (default: 2)'
    )

    args = parser.parse_args()

    try:
        generator = DataGenerator(args.seed)
        data = generator.generate_dataset(args.type, args.count)

        if args.format == 'json':
            export_to_json(data, args.output, args.indent)
        else:
            export_to_csv(data, args.output)

        print(f"\nGenerated {args.count} {args.type} records")
        print(f"Output: {args.output}")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
