import pytest
from parser import parse_log_line, parse_log_file

def test_valid_log_line():
    line = "2026-09-12 20:11:14 192.168.1.25 bob LOGIN_FAILED"

    result = parse_log_line(line)

    assert result["timestamp"] == "2026-09-12 20:11:14"
    assert result["ip_address"] == "192.168.1.25"
    assert result["username"] == "bob"
    assert result ["event"] == "LOGIN_FAILED"

def test_missing_fields():
    line = "2026-09-12 20:11:14 192.168.1.25"

    with pytest.raises(ValueError, match="exactly 5 fields"):
        parse_log_line(line)

def test_invalid_ip():
    line = "2026-09-12 20:11:14 999.999.999.999 bob LOGIN_FAILED"

    with pytest.raises(ValueError, match="Invalid IP address"):
        parse_log_line(line)

def test_invalid_timestamp():
    line = "2026-15-45 20:11:14 192.168.1.25 bob LOGIN_FAILED"

    with pytest.raises(ValueError, match="Invalid timestamp format"):
        parse_log_line(line)

def test_unsupported_event():
    line = "2026-09-12 20:11:14 192.168.1.25 bob PASSWORD_RESET"

    with pytest.raises(ValueError, match="Unsupported event type"):
        parse_log_line(line)
def test_extra_fields():
    line = "2026-09-12 20:11:14 192.168.1.25 bob LOGIN_FAILED extra"

    with pytest.raises(ValueError, match="exactly 5 fields"):
        parse_log_line(line)

def test_successful_login():
    line = "2026-09-12 20:10:01 192.168.1.10 alice LOGIN_SUCCESS"

    result = parse_log_line(line)

    assert result["username"] == "alice"
    assert result["event"] == "LOGIN_SUCCESS"
    assert result["ip_address"] == "192.168.1.10"

def test_parse_log_file():
    events = parse_log_file("logs/sample_auth.log")

    assert len(events) == 8
    assert events[0]["event"] == "LOGIN_SUCCESS"
    assert events[1]["event"] == "LOGIN_FAILED"