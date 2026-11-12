from reference.log_analyzer import LogAnalyzer


def test_empty_log_list():
    assert LogAnalyzer().analyze([]) == {
        "total_requests": 0,
        "unique_visitors": 0,
        "error_count": 0,
        "error_rate": 0.0,
        "malformed_lines": 0,
        "top_endpoint": None,
    }
