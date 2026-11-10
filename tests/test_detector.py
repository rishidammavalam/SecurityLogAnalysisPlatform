from detector import detect_brute_force

def test_below_threshold():
    events = [
        {"ip_address": "192.168.1.25", "event": "LOGIN_FAILED"}
        for _ in range(4)
    ]

    alerts = detect_brute_force(events)

    assert len(alerts) == 0

def test_at_threshold():
    events = [
        {"ip_address": "192.168.1.25", "event": "LOGIN_FAILED"}
        for _ in range(5)
    ]

    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.25"
    assert alerts[0]["failed_attempts"] == 5

def test_over_threshold():
    events = [
        {"ip_address": "192.168.1.25", "event": "LOGIN_FAILED"}
        for _ in range(6)
    ]

    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.25"
    assert alerts[0]["failed_attempts"] == 6

def test_multiple_ips():
    events = (
        [{"ip_address": "192.168.1.25", "event": "LOGIN_FAILED"} for _ in range(5)]
        +
        [{"ip_address": "10.0.0.8", "event": "LOGIN_FAILED"} for _ in range(3)]
    )

    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.25"
    assert alerts[0]["failed_attempts"] == 5

def test_successful_logins():
    events = [
        {"ip_address": "192.168.1.25", "event": "LOGIN_SUCCESS"}
        for _ in range(5)
    ]

    alerts = detect_brute_force(events)

    assert len(alerts) == 0

def test_empty_events():
    alerts = detect_brute_force([])

    assert alerts == []

def test_alert_metadata():
    events = [
        {"ip_address": "192.168.1.25", "event": "LOGIN_FAILED"}
        for _ in range(5)
    ]

    alerts = detect_brute_force(events)

    assert alerts[0]["type"] == "Brute Force"
    assert alerts[0]["severity"] == "HIGH"
    assert alerts[0]["mitre_id"] == "T1110"
    assert alerts[0]["mitre_name"] == "Brute Force"