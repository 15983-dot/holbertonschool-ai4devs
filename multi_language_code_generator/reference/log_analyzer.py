"""
Reference implementation of the Cross-Language Server Log Analyzer.
Parses Apache Common Log Format (CLF) entries and computes deterministic traffic metrics.
"""

from collections import Counter
import re
from typing import Any, Optional


class LogAnalyzer:
    """Parses Apache CLF access logs and computes traffic and error statistics."""

    # Standard Apache Common Log Format regex:
    # <ip_address> - - [<timestamp>] "<method> <endpoint> <protocol>" <status_code> <bytes>
    LOG_PATTERN = re.compile(
        r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>[A-Z]+)\s+(?P<endpoint>\S+)\s+(?P<protocol>[^"]+)"\s+'
        r'(?P<status>\d{3})\s+(?P<bytes>\d+|-)$'
    )

    def parse_line(self, line: str) -> Optional[dict[str, Any]]:
        """
        Parse a single Apache CLF log line into structured fields.

        Args:
            line: Raw log entry string.

        Returns:
            Dictionary with extracted fields if valid, otherwise None.
        """
        cleaned = line.strip()
        if not cleaned:
            return None

        match = self.LOG_PATTERN.match(cleaned)
        if not match:
            return None

        status_code = int(match.group("status"))
        if not (100 <= status_code <= 599):
            return None

        raw_bytes = match.group("bytes")
        byte_count = 0 if raw_bytes == "-" else int(raw_bytes)

        return {
            "ip": match.group("ip"),
            "timestamp": match.group("timestamp"),
            "method": match.group("method"),
            "endpoint": match.group("endpoint"),
            "protocol": match.group("protocol"),
            "status": status_code,
            "bytes": byte_count,
        }

    def analyze(self, lines: list[str]) -> dict[str, Any]:
        """
        Analyze a sequence of raw log lines and compute aggregate statistics.

        Args:
            lines: List of raw log entry strings.

        Returns:
            Dictionary adhering to the Cross-Language Specification output schema.
        """
        total_requests = 0
        unique_ips: set[str] = set()
        error_count = 0
        malformed_lines = 0
        endpoint_counts: Counter[str] = Counter()

        for line in lines:
            # Blank/whitespace-only lines are ignored without counting as malformed
            if not line or not line.strip():
                continue

            parsed = self.parse_line(line)
            if parsed is None:
                malformed_lines += 1
                continue

            total_requests += 1
            unique_ips.add(parsed["ip"])
            endpoint_counts[parsed["endpoint"]] += 1

            if 400 <= parsed["status"] <= 599:
                error_count += 1

        if total_requests == 0:
            error_rate = 0.0
            top_endpoint = None
        else:
            error_rate = round((error_count / total_requests) * 100, 2)
            # Sort by highest count descending, then lexicographically ascending for ties
            top_endpoint = min(
                endpoint_counts.keys(),
                key=lambda ep: (-endpoint_counts[ep], ep),
            )

        return {
            "total_requests": total_requests,
            "unique_visitors": len(unique_ips),
            "error_count": error_count,
            "error_rate": error_rate,
            "malformed_lines": malformed_lines,
            "top_endpoint": top_endpoint,
        }
