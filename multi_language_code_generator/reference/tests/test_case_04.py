from reference.log_analyzer import LogAnalyzer


def test_malformed_entries_mixed_with_valid():
    logs = [
        '172.16.0.5 - - [12/Nov/2026:12:05:00 +0000] "GET /health HTTP/1.1" 200 32',
        "CORRUPTED_RAW_LOG_LINE_WITHOUT_STRUCTURE",
        '172.16.0.5 - - [12/Nov/2026:12:05:02 +0000] "GET /health HTTP/1.1" INVALID_CODE 32',
    ]
    assert LogAnalyzer().analyze(logs) == {
        "total_requests": 1,
        "unique_visitors": 1,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 2,
        "top_endpoint": "/health",
    }
