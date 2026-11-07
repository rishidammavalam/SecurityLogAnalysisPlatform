from datetime import datetime
from ipaddress import ip_address

def parse_log_line(line):
    parts = line.split()

    if len(parts) != 5:
        raise ValueError("Log entry must contain exactly 5 fields")
    
    timestamp = parts[0] + " " + parts[1]
    source_ip = parts[2]
    username = parts[3]
    event = parts[4]

    # Validate timestamp
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid timestamp format")

    # Validate IP address
    try:
        ip_address(source_ip)
    except ValueError:
        raise ValueError("Invalid IP address")
    
    # Validate event type
    if event not in ("LOGIN_SUCCESS", "LOGIN_FAILED"):
        raise ValueError("Unsupported event type")
    
    return {
        "timestamp": timestamp,
        "ip_address": source_ip,
        "username": username,
        "event": event
    }

def parse_log_file(file_path):
    events = []

    with open(file_path, "r") as file:
        for line in file:
            event = parse_log_line(line)
            events.append(event)
        
    return events

if __name__ == "__main__":
    events = parse_log_file("logs/sample_auth.log")

    for event in events:
        print(event)