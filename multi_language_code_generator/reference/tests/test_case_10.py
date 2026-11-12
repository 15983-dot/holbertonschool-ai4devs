from reference.log_analyzer import LogAnalyzer


def test_ipv6_client_addresses():
    logs = [
        '2001:db8::1 - - [12/Nov/2026:12:35:01 +0000] "GET /v6 HTTP/1.1" 200 512',
        '::1 - - [12/Nov/2026:12:35:02 +0000] "GET /v6 HTTP/1.1" 403 128',
    ]
    result = LogAnalyzer().analyze(logs)
    assert result["total_requests"] == 2
    assert result["unique_visitors"] == 2
    assert result["error_count"] == 1
    assert result["error_rate"] == 50.0
    assert result["top_endpoint"] == "/v6"
