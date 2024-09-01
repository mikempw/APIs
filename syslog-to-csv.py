import csv
import re
import argparse
from typing import List, Dict
from datetime import datetime

def parse_syslog_message(message: str) -> Dict[str, str]:
    """
    Parse a syslog message into its components based on the provided F5 format.
    """
    # Parse the timestamp and hostname
    timestamp_hostname_pattern = r"(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)"
    match = re.match(timestamp_hostname_pattern, message)
    if not match:
        return {"message": message.strip()}

    timestamp, hostname = match.groups()
    
    # Parse the key-value pairs
    kv_pattern = r'(\w+)="([^"]*)"'
    kv_pairs = re.findall(kv_pattern, message)
    
    parsed = {
        "timestamp": timestamp,
        "hostname": hostname
    }
    parsed.update(dict(kv_pairs))
    
    return parsed

def extract_relevant_data(parsed_message: Dict[str, str]) -> Dict[str, str]:
    """
    Extract relevant fields from the parsed message.
    """
    fields = [
        "uri", "host", "method", "statusCode", "vs", "pool", "referrer",
        "cType", "userAgent", "httpv", "vip"
    ]
    return {
        "timestamp": parsed_message["timestamp"],
        "http_uri": parsed_message.get("uri", ""),
        "http_host": parsed_message.get("host", ""),
        "http_method": parsed_message.get("method", ""),
        "http_status": parsed_message.get("statusCode", ""),
        "virtual_server": parsed_message.get("vs", ""),
        "pool": parsed_message.get("pool", ""),
        "http_referrer": parsed_message.get("referrer", ""),
        "http_content_type": parsed_message.get("cType", ""),
        "http_user_agent": parsed_message.get("userAgent", ""),
        "http_version": parsed_message.get("httpv", ""),
        "vip": parsed_message.get("vip", "")
    }

def read_syslog_files(file_paths: List[str]) -> List[str]:
    """
    Read syslog messages from multiple files.
    """
    messages = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            messages.extend(file.readlines())
    return messages

def write_csv(data: List[Dict[str, str]], output_file: str):
    """
    Write the extracted data to a CSV file.
    """
    if not data:
        print("No data to write.")
        return

    fieldnames = list(data[0].keys())
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Extract F5 syslog data for Grafana visualization")
    parser.add_argument('files', nargs='+', help='Syslog files to process')
    parser.add_argument('-o', '--output', default='f5_api_data.csv', help='Output CSV file')
    args = parser.parse_args()

    # Read syslog messages from files
    syslog_messages = read_syslog_files(args.files)
    
    # Parse and extract relevant data
    extracted_data = []
    for message in syslog_messages:
        parsed = parse_syslog_message(message)
        relevant_data = extract_relevant_data(parsed)
        extracted_data.append(relevant_data)
    
    # Write data to CSV
    write_csv(extracted_data, args.output)
    
    print(f"Data has been written to {args.output}")

if __name__ == "__main__":
    main()
