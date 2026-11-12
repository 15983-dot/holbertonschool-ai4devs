from reference.log_analyzer import LogAnalyzer


def test_status_code_boundaries():
    logs = [
        '10.0.0.1 - - [12/Nov/2026:12:20:01 +0000] "GET /redirect HTTP/1.1" 302 0',
        '10.0.0.1 - - [12/Nov/2026:12:20:02 +0000] "GET /edge399 HTTP/1.1" 399 0',
        '10.0.0.1 - - [12/Nov/2026:12:20:03 +0000] "GET /bad400 HTTP/1.1" 400 10',
        '10.0.0.1 - - [12/Nov/2026:12:20:04 +0000] "GET /err599 HTTP/1.1" 599 10',
    ]
    result = LogAnalyzer().analyze(logs)
    assert result["total_requests"] == 4
    assert result["error_count"] == 2
    assert result["error_rate"] == 50.0
