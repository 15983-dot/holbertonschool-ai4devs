"""
Unit test suite for the reference LogAnalyzer implementation.
Covers all specification test cases, edge cases, and boundary conditions.
"""

import pytest
from reference.log_analyzer import LogAnalyzer


@pytest.fixture
def analyzer() -> LogAnalyzer:
    return LogAnalyzer()


def test_01_standard_mixed_traffic(analyzer: LogAnalyzer) -> None:
    """Spec Test Case 1: Standard mixed 200, 404, and 500 traffic."""
    logs = [
        '10.0.0.1 - - [12/Nov/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 2048',
        '10.0.0.2 - - [12/Nov/2026:12:00:02 +0000] "GET /index.html HTTP/1.1" 200 2048',
        '10.0.0.1 - - [12/Nov/2026:12:00:03 +0000] "POST /api/orders HTTP/1.1" 500 128',
        '10.0.0.3 - - [12/Nov/2026:12:00:04 +0000] "GET /missing HTTP/1.1" 404 64',
    ]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 4,
        "unique_visitors": 3,
        "error_count": 2,
        "error_rate": 50.0,
        "malformed_lines": 0,
        "top_endpoint": "/index.html",
    }


def test_02_empty_log_list(analyzer: LogAnalyzer) -> None:
    """Spec Test Case 2: Empty input list avoids division by zero."""
    result = analyzer.analyze([])
    assert result == {
        "total_requests": 0,
        "unique_visitors": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": None,
    }


def test_03_whitespace_only_lines(analyzer: LogAnalyzer) -> None:
    """Blank and whitespace-only lines are ignored without counting as malformed."""
    logs = ["", "   ", "\n", "\t\r\n"]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 0,
        "unique_visitors": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": None,
    }


def test_04_malformed_entries_mixed_with_valid(analyzer: LogAnalyzer) -> None:
    """Spec Test Case 3: Corrupted entries increment malformed_lines safely."""
    logs = [
        '172.16.0.5 - - [12/Nov/2026:12:05:00 +0000] "GET /health HTTP/1.1" 200 32',
        "CORRUPTED_RAW_LOG_LINE_WITHOUT_STRUCTURE",
        '172.16.0.5 - - [12/Nov/2026:12:05:02 +0000] "GET /health HTTP/1.1" INVALID_CODE 32',
    ]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 1,
        "unique_visitors": 1,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 2,
        "top_endpoint": "/health",
    }


def test_05_endpoint_tie_breaking_lexicographical(analyzer: LogAnalyzer) -> None:
    """Spec Test Case 4: Equal request counts resolve alphabetically ascending."""
    logs = [
        '192.168.0.10 - - [12/Nov/2026:12:10:01 +0000] "GET /api/zeta HTTP/1.1" 200 512',
        '192.168.0.11 - - [12/Nov/2026:12:10:02 +0000] "GET /api/alpha HTTP/1.1" 200 512',
    ]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 2,
        "unique_visitors": 2,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": "/api/alpha",
    }


def test_06_hundred_percent_error_rate(analyzer: LogAnalyzer) -> None:
    """Spec Test Case 5: All 4xx/5xx responses yield 100.0 error_rate."""
    logs = [
        '203.0.113.1 - - [12/Nov/2026:12:15:01 +0000] "POST /api/pay HTTP/1.1" 502 120',
        '203.0.113.2 - - [12/Nov/2026:12:15:02 +0000] "POST /api/pay HTTP/1.1" 503 120',
        '203.0.113.1 - - [12/Nov/2026:12:15:03 +0000] "GET /api/pay HTTP/1.1" 429 90',
    ]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 3,
        "unique_visitors": 2,
        "error_count": 3,
        "error_rate": 100.0,
        "malformed_lines": 0,
        "top_endpoint": "/api/pay",
    }


def test_07_error_rate_rounding_precision(analyzer: LogAnalyzer) -> None:
    """Error rate rounds cleanly to 2 decimal places (2/3 = 66.67%)."""
    logs = [
        '192.168.1.10 - - [12/Nov/2026:10:00:01 +0000] "GET /api/v1/users HTTP/1.1" 200 1024',
        '192.168.1.11 - - [12/Nov/2026:10:00:02 +0000] "POST /api/v1/login HTTP/1.1" 401 256',
        '192.168.1.10 - - [12/Nov/2026:10:00:05 +0000] "GET /api/v1/users HTTP/1.1" 500 512',
    ]
    result = analyzer.analyze(logs)
    assert result["error_rate"] == 66.67


def test_08_status_code_boundaries(analyzer: LogAnalyzer) -> None:
    """399 is not an error; 400 and 599 are classified as errors."""
    logs = [
        '10.0.0.1 - - [12/Nov/2026:12:20:01 +0000] "GET /redirect HTTP/1.1" 302 0',
        '10.0.0.1 - - [12/Nov/2026:12:20:02 +0000] "GET /edge399 HTTP/1.1" 399 0',
        '10.0.0.1 - - [12/Nov/2026:12:20:03 +0000] "GET /bad400 HTTP/1.1" 400 10',
        '10.0.0.1 - - [12/Nov/2026:12:20:04 +0000] "GET /err599 HTTP/1.1" 599 10',
    ]
    result = analyzer.analyze(logs)
    assert result["total_requests"] == 4
    assert result["error_count"] == 2
    assert result["error_rate"] == 50.0


def test_09_hyphen_byte_size_handling(analyzer: LogAnalyzer) -> None:
    """Valid Apache CLF lines with '-' for zero/missing bytes parse accurately."""
    logs = [
        '10.1.1.1 - - [12/Nov/2026:12:25:01 +0000] "HEAD /ping HTTP/1.1" 204 -',
    ]
    parsed = analyzer.parse_line(logs[0])
    assert parsed is not None
    assert parsed["bytes"] == 0
    assert parsed["status"] == 204

    result = analyzer.analyze(logs)
    assert result["total_requests"] == 1
    assert result["malformed_lines"] == 0


def test_10_only_malformed_lines(analyzer: LogAnalyzer) -> None:
    """Input containing exclusively invalid entries returns zero valid requests."""
    logs = [
        "bad line 1",
        '10.0.0.1 - - [bad-timestamp] "BROKEN" 999 abc',
    ]
    result = analyzer.analyze(logs)
    assert result == {
        "total_requests": 0,
        "unique_visitors": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 2,
        "top_endpoint": None,
    }


def test_11_single_visitor_multiple_requests(analyzer: LogAnalyzer) -> None:
    """Repeated requests from the same IP count once in unique_visitors."""
    logs = [
        '192.168.50.5 - - [12/Nov/2026:12:30:01 +0000] "GET /a HTTP/1.1" 200 100',
        '192.168.50.5 - - [12/Nov/2026:12:30:02 +0000] "GET /b HTTP/1.1" 200 100',
        '192.168.50.5 - - [12/Nov/2026:12:30:03 +0000] "GET /b HTTP/1.1" 200 100',
    ]
    result = analyzer.analyze(logs)
    assert result["total_requests"] == 3
    assert result["unique_visitors"] == 1
    assert result["top_endpoint"] == "/b"


def test_12_ipv6_client_addresses(analyzer: LogAnalyzer) -> None:
    """Supports IPv6 client addresses cleanly alongside IPv4."""
    logs = [
        '2001:db8::1 - - [12/Nov/2026:12:35:01 +0000] "GET /v6 HTTP/1.1" 200 512',
        '::1 - - [12/Nov/2026:12:35:02 +0000] "GET /v6 HTTP/1.1" 403 128',
    ]
    result = analyzer.analyze(logs)
    assert result["total_requests"] == 2
    assert result["unique_visitors"] == 2
    assert result["error_count"] == 1
    assert result["error_rate"] == 50.0
    assert result["top_endpoint"] == "/v6"
