from parser import parse_log_file

def detect_brute_force(events):
    failed_attempts={}

    for event in events:
        if event["event"] == "LOGIN_FAILED":
            ip_address = event["ip_address"]

            if ip_address not in failed_attempts:
                failed_attempts[ip_address] = 0
            
            failed_attempts[ip_address] += 1

    alerts = []

    for ip_address, count in failed_attempts.items():
        if count >= 5:
            alerts.append({
                "type": "Brute Force",
                "source_ip": ip_address,
                "failed_attempts": count,
                "severity": "HIGH",
                "mitre_id": "T1110",
                "mitre_name": "Brute Force"
            })
    
    return alerts

if __name__ == "__main__":
    events = parse_log_file("logs/sample_auth.log")
    alerts = detect_brute_force(events)

    for alert in alerts:
        print(alert)