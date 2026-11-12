from reference.log_analyzer import LogAnalyzer


def test_standard_mixed_traffic():
    logs = [
        '10.0.0.1 - - [12/Nov/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 2048',
        '10.0.0.2 - - [12/Nov/2026:12:00:02 +0000] "GET /index.html HTTP/1.1" 200 2048',
        '10.0.0.1 - - [12/Nov/2026:12:00:03 +0000] "POST /api/orders HTTP/1.1" 500 128',
        '10.0.0.3 - - [12/Nov/2026:12:00:04 +0000] "GET /missing HTTP/1.1" 404 64',
    ]
    assert LogAnalyzer().analyze(logs) == {
        "total_requests": 4,
        "unique_visitors": 3,
        "error_count": 2,
        "error_rate": 50.0,
        "malformed_lines": 0,
        "top_endpoint": "/index.html",
    }
