from reference.log_analyzer import LogAnalyzer


def test_hyphen_byte_size_handling():
    logs = [
        '10.1.1.1 - - [12/Nov/2026:12:25:01 +0000] "HEAD /ping HTTP/1.1" 204 -',
    ]
    analyzer = LogAnalyzer()
    parsed = analyzer.parse_line(logs[0])
    assert parsed is not None
    assert parsed["bytes"] == 0
    assert analyzer.analyze(logs)["total_requests"] == 1
