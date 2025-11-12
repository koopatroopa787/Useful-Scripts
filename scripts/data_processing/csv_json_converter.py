#!/usr/bin/env python3
"""
CSV/JSON Converter - Convert between CSV and JSON formats
Supports both single files and batch conversion
"""

import csv
import json
import argparse
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils import get_logger, format_bytes


logger = get_logger(__name__)


def csv_to_json(csv_file, json_file=None, indent=2):
    """
    Convert CSV to JSON

    Args:
        csv_file: Input CSV file path
        json_file: Output JSON file path (optional)
        indent: JSON indentation

    Returns:
        List of dictionaries
    """
    csv_path = Path(csv_file)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    if json_file is None:
        json_file = csv_path.with_suffix('.json')

    data = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

    logger.info(f"Converted {len(data)} rows from CSV to JSON")
    logger.info(f"Output: {json_file}")

    return data


def json_to_csv(json_file, csv_file=None):
    """
    Convert JSON to CSV

    Args:
        json_file: Input JSON file path
        csv_file: Output CSV file path (optional)

    Returns:
        Number of rows written
    """
    json_path = Path(json_file)

    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    if csv_file is None:
        csv_file = json_path.with_suffix('.csv')

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON must contain an array of objects")

    if not data:
        raise ValueError("JSON array is empty")

    # Get all unique keys from all objects
    keys = set()
    for item in data:
        if isinstance(item, dict):
            keys.update(item.keys())

    keys = sorted(keys)

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"Converted {len(data)} rows from JSON to CSV")
    logger.info(f"Output: {csv_file}")

    return len(data)


def batch_convert(input_dir, output_dir, from_format, to_format):
    """
    Batch convert files

    Args:
        input_dir: Input directory
        output_dir: Output directory
        from_format: Source format (csv or json)
        to_format: Target format (csv or json)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    output_path.mkdir(parents=True, exist_ok=True)

    # Find files
    pattern = f"*.{from_format}"
    files = list(input_path.glob(pattern))

    if not files:
        logger.warning(f"No {from_format} files found in {input_dir}")
        return

    logger.info(f"Found {len(files)} file(s) to convert")

    success = 0
    failed = 0

    for file in files:
        output_file = output_path / file.with_suffix(f'.{to_format}').name

        try:
            if from_format == 'csv' and to_format == 'json':
                csv_to_json(file, output_file)
            elif from_format == 'json' and to_format == 'csv':
                json_to_csv(file, output_file)

            success += 1

        except Exception as e:
            logger.error(f"Failed to convert {file.name}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Batch Conversion Complete")
    print("=" * 60)
    print(f"Total files: {len(files)}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert between CSV and JSON formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single files
  %(prog)s data.csv --to-json
  %(prog)s data.json --to-csv
  %(prog)s input.csv -o output.json

  # Batch convert
  %(prog)s --batch input_dir/ output_dir/ --from csv --to json
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Input file or directory (for batch mode)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path'
    )

    parser.add_argument(
        '--to-json',
        action='store_true',
        help='Convert CSV to JSON'
    )

    parser.add_argument(
        '--to-csv',
        action='store_true',
        help='Convert JSON to CSV'
    )

    parser.add_argument(
        '--batch',
        nargs=2,
        metavar=('INPUT_DIR', 'OUTPUT_DIR'),
        help='Batch convert files from input directory to output directory'
    )

    parser.add_argument(
        '--from',
        dest='from_format',
        choices=['csv', 'json'],
        help='Source format for batch conversion'
    )

    parser.add_argument(
        '--to',
        dest='to_format',
        choices=['csv', 'json'],
        help='Target format for batch conversion'
    )

    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='JSON indentation (default: 2)'
    )

    args = parser.parse_args()

    try:
        if args.batch:
            if not args.from_format or not args.to_format:
                parser.error("--from and --to are required for batch conversion")

            batch_convert(args.batch[0], args.batch[1], args.from_format, args.to_format)

        elif args.input:
            if args.to_json:
                csv_to_json(args.input, args.output, args.indent)
            elif args.to_csv:
                json_to_csv(args.input, args.output)
            else:
                # Auto-detect based on extension
                input_path = Path(args.input)
                if input_path.suffix.lower() == '.csv':
                    csv_to_json(args.input, args.output, args.indent)
                elif input_path.suffix.lower() == '.json':
                    json_to_csv(args.input, args.output)
                else:
                    parser.error("Cannot determine conversion direction. Use --to-json or --to-csv")

            print("\nConversion completed successfully!")

        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
