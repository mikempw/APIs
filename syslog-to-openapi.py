import json
import re
import argparse
from typing import List, Dict
from collections import defaultdict

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

def discover_api_paths(messages: List[str]) -> Dict[str, Dict[str, Dict[str, set]]]:
    """
    Discover API paths from syslog messages, including HTTP methods, response codes, and additional details.
    """
    paths = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    for message in messages:
        parsed = parse_syslog_message(message)
        if 'uri' in parsed and 'method' in parsed and 'statusCode' in parsed:
            path = parsed['uri']
            method = parsed['method']
            status_code = int(parsed['statusCode'])
            paths[path][method]['status_codes'].add(status_code)
            paths[path][method]['content_types'].add(parsed.get('cType', ''))
            paths[path][method]['pools'].add(parsed.get('pool', ''))

    return paths

def generate_response_schema(status_code: int) -> Dict:
    """
    Generate a detailed response schema based on the status code.
    """
    description = "Unknown status"
    if 100 <= status_code < 200:
        description = "Informational response"
    elif 200 <= status_code < 300:
        description = "Successful response"
    elif 300 <= status_code < 400:
        description = "Redirection"
    elif 400 <= status_code < 500:
        description = "Client error"
    elif 500 <= status_code < 600:
        description = "Server error"

    return {
        "description": f"{description} (Status: {status_code})",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "integer"},
                        "message": {"type": "string"}
                    }
                }
            }
        }
    }

def generate_openapi_schema(messages: List[str]) -> Dict:
    """
    Generate an OpenAPI schema from a list of syslog messages, including discovered paths and response codes.
    """
    discovered_paths = discover_api_paths(messages)
    
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Discovered API from F5 Syslog",
            "version": "1.0.0",
            "description": "API discovered from F5 syslog messages"
        },
        "paths": {}
    }
    
    for path, methods in discovered_paths.items():
        schema["paths"][path] = {}
        for method, details in methods.items():
            schema["paths"][path][method.lower()] = {
                "summary": f"{method} request to {path}",
                "responses": {
                    str(status_code): generate_response_schema(status_code)
                    for status_code in details['status_codes']
                },
                "x-content-types": list(details['content_types'] - {''}),
                "x-pools": list(details['pools'] - {''})
            }
    
    return schema

def read_syslog_files(file_paths: List[str]) -> List[str]:
    """
    Read syslog messages from multiple files.
    """
    messages = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            messages.extend(file.readlines())
    return messages

def main():
    parser = argparse.ArgumentParser(description="Generate OpenAPI schema from F5 syslog files")
    parser.add_argument('files', nargs='+', help='Syslog files to process')
    parser.add_argument('-o', '--output', default='openapi_schema.json', help='Output file for the OpenAPI schema')
    args = parser.parse_args()

    # Read syslog messages from files
    syslog_messages = read_syslog_files(args.files)
    
    # Generate OpenAPI schema
    openapi_schema = generate_openapi_schema(syslog_messages)
    
    # Write the schema to a file
    with open(args.output, 'w') as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"OpenAPI schema has been written to {args.output}")

if __name__ == "__main__":
    main()
