from reference.log_analyzer import LogAnalyzer


def test_error_rate_rounding_precision():
    logs = [
        '192.168.1.10 - - [12/Nov/2026:10:00:01 +0000] "GET /api/v1/users HTTP/1.1" 200 1024',
        '192.168.1.11 - - [12/Nov/2026:10:00:02 +0000] "POST /api/v1/login HTTP/1.1" 401 256',
        '192.168.1.10 - - [12/Nov/2026:10:00:05 +0000] "GET /api/v1/users HTTP/1.1" 500 512',
    ]
    assert LogAnalyzer().analyze(logs)["error_rate"] == 66.67
