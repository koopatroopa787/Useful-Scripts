# Examples

This directory contains example outputs and use cases for the Useful Scripts collection.

## Quick Examples

### Network Tools

#### Port Scanning
```bash
# Scan common ports on a host
$ python useful_scripts.py port-scan example.com --common

======================================================================
Scan Results for example.com
======================================================================
Total ports scanned: 18
Open ports found: 3
Scan duration: 2.5s

Open Ports:
----------------------------------------------------------------------
    80  -  HTTP
   443  -  HTTPS
  8080  -  HTTP Proxy
======================================================================
```

#### IP Information
```bash
$ python useful_scripts.py ip-info 8.8.8.8

======================================================================
IP Address Information
======================================================================
IP Address          : 8.8.8.8
Version             : IPv4
City                : Mountain View
Region              : California
Country             : United States
Country Code        : US
ISP                 : Google LLC
ASN                 : AS15169
======================================================================
```

### Data Processing

#### CSV to JSON Conversion
```bash
$ python useful_scripts.py csv-json data.csv --to-json

Converted 1000 rows from CSV to JSON
Output: data.json

Conversion completed successfully!
```

#### Log Analysis
```bash
$ python useful_scripts.py log-analyzer access.log

======================================================================
                        Log Analysis Report
======================================================================
File: access.log
Size: 15.3 MB
Total lines: 125,432
======================================================================

Issues:
----------------------------------------------------------------------
Errors: 23
Warnings: 156

----------------------------------------------------------------------
Top IP Addresses:
----------------------------------------------------------------------
  192.168.1.100   - 5,234 requests
  10.0.0.52       - 3,891 requests
  172.16.0.10     - 2,456 requests

----------------------------------------------------------------------
HTTP Status Codes:
----------------------------------------------------------------------
  200 - 112,345 occurrences
  304 - 8,932 occurrences
  404 - 3,421 occurrences
  500 - 734 occurrences
======================================================================
```

### Automation

#### File Watcher
```bash
# Watch Downloads folder for PDFs and move them
$ python useful_scripts.py file-watcher ~/Downloads -p "*.pdf" \
  -c "mv {file} ~/Documents/PDFs/"

======================================================================
File Watcher Started
======================================================================
Watching: /home/user/Downloads
Recursive: True
Patterns: *.pdf
Command: mv {file} ~/Documents/PDFs/
======================================================================

Press Ctrl+C to stop watching

[2024-01-15 14:23:45] CREATED: /home/user/Downloads/document.pdf
  Executing: mv /home/user/Downloads/document.pdf ~/Documents/PDFs/
  Command completed successfully
```

#### Backup Utility
```bash
$ python useful_scripts.py backup ~/Projects ~/Backups/Projects --keep-count 5

Creating backup: /home/user/Backups/Projects/Projects_20240115_142530.tar.gz
Backup created successfully: 245.7 MB in 12.3s

======================================================================
Backup Created Successfully
======================================================================
Source: /home/user/Projects
Backup: /home/user/Backups/Projects/Projects_20240115_142530.tar.gz
Size: 245.7 MB
======================================================================

Deleting 2 old backup(s)
Deleted: Projects_20240110_082315.tar.gz
Deleted: Projects_20240109_082430.tar.gz
```

### Web Utilities

#### Link Checker
```bash
$ python useful_scripts.py link-checker https://example.com https://google.com

Checking 2 URL(s)...

[✓] 200 - https://example.com
[✓] 200 - https://google.com

======================================================================
Link Check Summary
======================================================================
Total URLs checked: 2
Successful (2xx): 2
Redirects (3xx): 0
Client Errors (4xx): 0
Server Errors (5xx): 0
Failed: 0
======================================================================
```

#### Sitemap Generator
```bash
$ python useful_scripts.py sitemap https://example.com -m 100

Starting sitemap generation for: https://example.com
Max pages: 100

Crawled 47 page(s)

======================================================================
Sitemap Generated Successfully
======================================================================
Output file: sitemap.xml
Total URLs: 47
======================================================================
```

## Integration Examples

### Automation Pipeline

Create a complete automation pipeline that watches for new CSV files, converts them to JSON, and backs them up:

```bash
# Terminal 1: Watch for CSV files and convert
python useful_scripts.py file-watcher ~/data/incoming -p "*.csv" \
  -c "python useful_scripts.py csv-json {file} --to-json"

# Terminal 2: Schedule daily backups
python useful_scripts.py scheduler add "Data Backup" \
  "python useful_scripts.py backup ~/data ~/backups --keep-count 7" \
  daily "02:00"

python useful_scripts.py scheduler run
```

### Network Monitoring

Monitor your network and generate reports:

```bash
#!/bin/bash
# network_audit.sh

# Discover active hosts
python useful_scripts.py ping-sweep 192.168.1.0/24 > hosts.txt

# Scan each host for common vulnerabilities
while read host; do
    echo "Scanning $host..."
    python useful_scripts.py port-scan $host --common >> scan_results.txt
done < hosts.txt

# Generate report
echo "Network audit completed. Results in scan_results.txt"
```

### Data Processing Workflow

Process and analyze data:

```bash
# Generate test data
python useful_scripts.py data-generator users 1000 -o test_users.json

# Convert to CSV for analysis
python useful_scripts.py csv-json test_users.json --to-csv

# Analyze logs
python useful_scripts.py log-analyzer system.log --export report.txt
```

## Sample Output Files

The `outputs/` directory contains sample output files from various scripts:

- `sample_sitemap.xml` - Example generated sitemap
- `sample_backup_meta.json` - Backup metadata example
- `sample_log_report.txt` - Log analysis report
- `sample_generated_data.json` - Generated test data

## Tips and Tricks

### Combining Scripts

Use Unix pipes to combine scripts:

```bash
# Get IP info for all IPs in a file
cat ips.txt | while read ip; do
    python useful_scripts.py ip-info $ip
done
```

### Cron Integration

Add scripts to crontab:

```bash
# Daily backup at 2 AM
0 2 * * * python /path/to/useful_scripts.py backup ~/data ~/backups --keep-count 7

# Hourly link check
0 * * * * python /path/to/useful_scripts.py link-checker -f urls.txt -o /var/log/link_check.log
```

### Error Handling

Redirect errors and output:

```bash
# Log all output
python useful_scripts.py port-scan 192.168.1.1 > scan.log 2>&1

# Only log errors
python useful_scripts.py backup ~/data ~/backups 2> errors.log
```

## Need More Help?

Check the individual script documentation:

```bash
python useful_scripts.py <script-name> --help
```

Or visit the main [README](../README.md) for comprehensive documentation.
