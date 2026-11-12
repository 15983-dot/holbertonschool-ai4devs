from reference.log_analyzer import LogAnalyzer


def test_endpoint_tie_breaking_lexicographical():
    logs = [
        '192.168.0.10 - - [12/Nov/2026:12:10:01 +0000] "GET /api/zeta HTTP/1.1" 200 512',
        '192.168.0.11 - - [12/Nov/2026:12:10:02 +0000] "GET /api/alpha HTTP/1.1" 200 512',
    ]
    assert LogAnalyzer().analyze(logs) == {
        "total_requests": 2,
        "unique_visitors": 2,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": "/api/alpha",
    }
