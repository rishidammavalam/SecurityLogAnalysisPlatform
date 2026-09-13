def parse_log_line(line):
    parts = line.split()

    timestamp = parts[0] + " " + parts[1]
    ip_address = parts[2]
    username = parts[3]
    event = parts[4]

    return {
        "timestamp": timestamp,
        "ip_address": ip_address,
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