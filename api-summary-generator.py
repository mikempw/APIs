import csv
from collections import defaultdict
import json
import re

def parse_csv(file_path):
    api_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))
    endpoint_info = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['http_uri'] and row['http_method'] and row['http_status'] and row['pool']:
                pool_name, ip_address = split_pool_info(row['pool'])
                api_data[row['http_uri']][row['http_method']][pool_name][ip_address][row['http_status']] += 1
                
                # Store virtual server information
                if row['http_uri'] not in endpoint_info:
                    endpoint_info[row['http_uri']] = row.get('virtual_server', 'N/A')
    
    return api_data, endpoint_info

def split_pool_info(pool_string):
    match = re.match(r'(/.*?)\s+(\S+)\s+(\d+)', pool_string)
    if match:
        return match.group(1), f"{match.group(2)}:{match.group(3)}"
    return pool_string, "N/A"

def generate_mermaid(api_data):
    mermaid = ["graph TD"]
    node_id = 0
    for uri, methods in api_data.items():
        uri_node = f"URI{node_id}"
        mermaid.append(f'{uri_node}["{uri}"]')
        node_id += 1
        for method, pools in methods.items():
            method_node = f"M{node_id}"
            mermaid.append(f'{method_node}["{method}"]')
            mermaid.append(f'{uri_node} --> {method_node}')
            node_id += 1
            for pool_name, ips in pools.items():
                pool_node = f"P{node_id}"
                mermaid.append(f'{pool_node}["{pool_name}"]')
                mermaid.append(f'{method_node} --> {pool_node}')
                node_id += 1
                for ip in ips:
                    ip_node = f"IP{node_id}"
                    mermaid.append(f'{ip_node}["{ip}"]')
                    mermaid.append(f'{pool_node} --> {ip_node}')
                    node_id += 1
    return "\n".join(mermaid)

def generate_summary(api_data):
    summary = {
        "endpoints": len(api_data),
        "methods": set(),
        "pools": set(),
        "ip_addresses": set(),
        "status_codes": set()
    }
    for uri, methods in api_data.items():
        summary["methods"].update(methods.keys())
        for method, pools in methods.items():
            summary["pools"].update(pools.keys())
            for pool, ips in pools.items():
                summary["ip_addresses"].update(ips.keys())
                for ip, statuses in ips.items():
                    summary["status_codes"].update(statuses.keys())
    summary["methods"] = list(summary["methods"])
    summary["pools"] = list(summary["pools"])
    summary["ip_addresses"] = list(summary["ip_addresses"])
    summary["status_codes"] = list(summary["status_codes"])
    return summary

def generate_html(mermaid, summary, api_data, endpoint_info):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Summary</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            .mermaid {{ background-color: #f0f0f0; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>API Summary</h1>
        <h2>Overview</h2>
        <ul>
            <li>Total Endpoints: {summary['endpoints']}</li>
            <li>Methods: {', '.join(summary['methods'])}</li>
            <li>Pools: {', '.join(summary['pools'])}</li>
            <li>IP Addresses: {', '.join(summary['ip_addresses'])}</li>
            <li>Status Codes: {', '.join(summary['status_codes'])}</li>
        </ul>
        <h2>API Structure</h2>
        <div class="mermaid">
        {mermaid}
        </div>
        <h2>Endpoint Details</h2>
        <table>
            <tr>
                <th>Endpoint</th>
                <th>Virtual Server</th>
                <th>Methods (Count)</th>
                <th>Status Codes (Count)</th>
                <th>TRACE (Count)</th>
                <th>TRACE Status Codes (Count)</th>
                <th>Pools</th>
                <th>IP Addresses</th>
            </tr>
    """
    
    for uri, methods in api_data.items():
        methods_count = defaultdict(int)
        trace_count = 0
        status_codes_count = defaultdict(int)
        trace_status_codes_count = defaultdict(int)
        pools = set()
        ip_addresses = set()
        for method, pool_data in methods.items():
            for pool, ip_data in pool_data.items():
                pools.add(pool)
                for ip, statuses in ip_data.items():
                    ip_addresses.add(ip)
                    for status, count in statuses.items():
                        if method.upper() == 'TRACE':
                            trace_count += count
                            trace_status_codes_count[status] += count
                        else:
                            methods_count[method] += count
                            status_codes_count[status] += count
        
        methods_str = ", ".join([f"{m} ({c})" for m, c in methods_count.items() if m.upper() != 'TRACE'])
        status_codes_str = ", ".join([f"{s} ({c})" for s, c in status_codes_count.items()])
        trace_status_codes_str = ", ".join([f"{s} ({c})" for s, c in trace_status_codes_count.items()])
        pools_str = ", ".join(pools)
        ip_addresses_str = ", ".join(ip_addresses)
        
        virtual_server = endpoint_info[uri]
        
        html += f"""
            <tr>
                <td>{uri}</td>
                <td>{virtual_server}</td>
                <td>{methods_str}</td>
                <td>{status_codes_str}</td>
                <td>{trace_count}</td>
                <td>{trace_status_codes_str}</td>
                <td>{pools_str}</td>
                <td>{ip_addresses_str}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

def main(csv_file, output_file):
    api_data, endpoint_info = parse_csv(csv_file)
    mermaid = generate_mermaid(api_data)
    summary = generate_summary(api_data)
    html = generate_html(mermaid, summary, api_data, endpoint_info)
    
    with open(output_file, 'w') as f:
        f.write(html)
    print(f"API summary has been written to {output_file}")

if __name__ == "__main__":
    main('f5_api_data.csv', 'api_summary_with_separate_trace_and_status.html')
