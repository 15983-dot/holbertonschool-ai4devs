from reference.log_analyzer import LogAnalyzer


def test_hundred_percent_error_rate():
    logs = [
        '203.0.113.1 - - [12/Nov/2026:12:15:01 +0000] "POST /api/pay HTTP/1.1" 502 120',
        '203.0.113.2 - - [12/Nov/2026:12:15:02 +0000] "POST /api/pay HTTP/1.1" 503 120',
        '203.0.113.1 - - [12/Nov/2026:12:15:03 +0000] "GET /api/pay HTTP/1.1" 429 90',
    ]
    assert LogAnalyzer().analyze(logs) == {
        "total_requests": 3,
        "unique_visitors": 2,
        "error_count": 3,
        "error_rate": 100.0,
        "malformed_lines": 0,
        "top_endpoint": "/api/pay",
    }
