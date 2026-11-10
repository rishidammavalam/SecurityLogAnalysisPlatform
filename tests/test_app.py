from app import app
from io import BytesIO

def test_homepage():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Security Log Analysis Platform" in response.data

def test_valid_upload():
    client = app.test_client()

    log_data = b"""2026-09-12 20:10:01 192.168.1.10 alice LOGIN_SUCCESS
2026-09-12 20:11:14 192.168.1.25 bob LOGIN_FAILED
2026-09-12 20:11:40 192.168.1.25 bob LOGIN_FAILED
2026-09-12 20:12:02 192.168.1.25 bob LOGIN_FAILED
2026-09-12 20:12:25 192.168.1.25 bob LOGIN_FAILED
2026-09-12 20:12:49 192.168.1.25 bob LOGIN_FAILED"""

    response = client.post(
        "/upload",
        data={"log_file": (BytesIO(log_data), "test.log")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Total Events: 6" in response.data
    assert b"Total Alerts: 1" in response.data
    assert b"192.168.1.25" in response.data
    assert b"T1110" in response.data

def test_invalid_upload():
    client = app.test_client()

    log_data = b"2026-09-12 20:11:14 invalid_ip bob LOGIN_FAILED"

    response = client.post(
        "/upload",
        data={"log_file": (BytesIO(log_data), "invalid.log")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert b"Invalid IP address" in response.data

def test_empty_upload():
    client = app.test_client()

    response = client.post(
        "/upload",
        data={"log_file": (BytesIO(b""), "empty.log")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert b"The uploaded log file contains no events" in response.data

def test_invalid_file_type():
    client = app.test_client()

    response = client.post(
        "/upload",
        data={"log_file": (BytesIO(b"test data"), "test.pdf")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert b"Invalid file type" in response.data

def test_missing_file():
    client = app.test_client()

    response = client.post(
        "/upload",
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

def test_oversized_upload():
    client = app.test_client()

    large_data = b"A" * (6 * 1024 * 1024)

    response = client.post(
        "/upload",
        data={"log_file": (BytesIO(large_data), "large.log")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 413