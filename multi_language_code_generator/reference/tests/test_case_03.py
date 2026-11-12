from reference.log_analyzer import LogAnalyzer


def test_whitespace_only_lines():
    logs = ["", "   ", "\n", "\t\r\n"]
    assert LogAnalyzer().analyze(logs) == {
        "total_requests": 0,
        "unique_visitors": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": None,
    }
