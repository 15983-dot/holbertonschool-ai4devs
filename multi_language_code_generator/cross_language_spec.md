Cross-Language Specification - Log AnalyzerAlgorithmParse Apache/Nginx Combined Log Format entries from raw log streams or files and compute core traffic and reliability metrics:Total Valid Requests: Total count of successfully parsed HTTP request entries.Unique Visitors: Count of distinct client IPv4/IPv6 addresses across valid entries.Error Rate: Percentage of valid requests resulting in HTTP 4xx or 5xx status codes, rounded to 2 decimal places ((error_count / total_requests) * 100, or 0.0 when total_requests == 0).Top Endpoints: Top 3 most frequently requested URL paths (sorted descending by hit count, then lexicographically by path on ties).Malformed Entries: Count of non-empty lines that fail schema validation and are skipped without halting execution.Processing RulesRead input line-by-line (trimming trailing \r\n or \n).Ignore completely blank or whitespace-only lines (do not count them as valid requests or malformed entries).Extract client_ip, timestamp, method, path (strip query strings ?key=val when aggregating endpoint counts), status_code, and bytes_sent using standard Apache Combined Log regex matching.Any non-blank line failing pattern extraction or containing an invalid HTTP status code (< 100 or > 599) increments malformed_entries and is excluded from traffic metrics.InputsSource: UTF-8 encoded plain-text log file (e.g., access.log) or newline-delimited string stream.Line Schema (Apache Combined Log Format):<client_ip> - - [<timestamp>] "<method> <path> <protocol>" <status_code> <bytes_sent> "<referrer>" "<user_agent>"
Sample Input:192.168.1.10 - - [12/Nov/2026:10:00:01 +0000] "GET /api/v1/users HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.1.11 - - [12/Nov/2026:10:00:02 +0000] "POST /api/v1/login HTTP/1.1" 401 256 "-" "curl/8.4.0"
192.168.1.10 - - [12/Nov/2026:10:00:05 +0000] "GET /api/v1/users?page=2 HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
OutputsA deterministic JSON object summarizing aggregated statistics:{
  "total_requests": 3,
  "unique_visitors": 2,
  "error_count": 1,
  "error_rate": 33.33,
  "malformed_entries": 0,
  "top_endpoints": [
    { "path": "/api/v1/users", "count": 2 },
    { "path": "/api/v1/login", "count": 1 }
  ]
}
Field ConstraintsFieldTypeDescriptiontotal_requestsintegerCount of valid parsed log lines (>= 0).unique_visitorsintegerCount of unique IP addresses among valid lines (>= 0).error_countintegerCount of valid requests with 400 <= status_code <= 599.error_ratefloatError percentage rounded to 2 decimal places (0.00 if total_requests == 0).malformed_entriesintegerCount of non-empty unparseable lines (>= 0).top_endpointsarray<object>Up to 3 objects containing path (string) and count (integer).Edge CasesEmpty File (0 bytes or whitespace-only): Must not raise division-by-zero errors; returns total_requests: 0, unique_visitors: 0, error_rate: 0.0, and top_endpoints: [].All Malformed Entries: When every non-empty line is corrupted, total_requests remains 0, error_rate is 0.0, and malformed_entries equals the exact number of corrupted lines.Query Parameters on Same Endpoint: /api/items?id=1 and /api/items?id=2 must normalize and aggregate under /api/items.IPv6 & Loopback Addresses: Must accurately parse IPv6 addresses (e.g., 2001:db8::1, ::1) alongside standard IPv4 addresses without failing regex validation.100% Error Rate & Zero Error Rate: Properly handles boundary rates (0.0 when all responses are 2xx/3xx, and 100.0 when all responses are 4xx/5xx).Large Byte Size or Hyphen (-) for Bytes Sent: Apache logs often output - instead of 0 when response body size is empty (e.g., 204 or 304 responses); parser must accept both digits and -.Test CasesTest Case 1: Empty Log File (log_empty.txt)Input: Empty string "" (or whitespace/newlines only).Expected Output:{
  "total_requests": 0,
  "unique_visitors": 0,
  "error_count": 0,
  "error_rate": 0.0,
  "malformed_entries": 0,
  "top_endpoints": []
}
Test Case 2: Standard Mixed Traffic (log_small.txt)Input: 5 valid lines from 3 unique IPs (10.0.0.1 x2, 10.0.0.2 x2, 10.0.0.3 x1) with statuses 200, 200, 404, 500, 201 across paths /home (x3), /login (x1), /admin (x1).Expected Output:{
  "total_requests": 5,
  "unique_visitors": 3,
  "error_count": 2,
  "error_rate": 40.0,
  "malformed_entries": 0,
  "top_endpoints": [
    { "path": "/home", "count": 3 },
    { "path": "/admin", "count": 1 },
    { "path": "/login", "count": 1 }
  ]
}
Test Case 3: Malformed & Corrupted Lines (log_corrupted.txt)Input:192.168.0.1 - - [12/Nov/2026:11:00:00 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "Safari"
CORRUPTED_RAW_TEXT_ENTRY
192.168.0.2 - - [12/Nov/2026:11:00:05 +0000] "GET /missing HTTP/1.1" 999 - "-" "Bot"
192.168.0.1 - - [12/Nov/2026:11:00:10 +0000] "GET /index.html HTTP/1.1" 304 - "-" "Safari"
Expected Output:{
  "total_requests": 2,
  "unique_visitors": 1,
  "error_count": 0,
  "error_rate": 0.0,
  "malformed_entries": 2,
  "top_endpoints": [
    { "path": "/index.html", "count": 2 }
  ]
}
Test Case 4: Query String Normalization & IPv6 Support (log_ipv6_queries.txt)Input:2001:db8::1 - - [12/Nov/2026:12:00:01 +0000] "GET /search?q=python HTTP/1.1" 200 1200 "-" "Chrome"
::1 - - [12/Nov/2026:12:00:02 +0000] "GET /search?q=rust&page=2 HTTP/1.1" 200 1350 "-" "Firefox"
2001:db8::1 - - [12/Nov/2026:12:00:03 +0000] "GET /search?q=go HTTP/1.1" 503 300 "-" "Chrome"
Expected Output:{
  "total_requests": 3,
  "unique_visitors": 2,
  "error_count": 1,
  "error_rate": 33.33,
  "malformed_entries": 0,
  "top_endpoints": [
    { "path": "/search", "count": 3 }
  ]
}
Test Case 5: 100% Server Outage Spike (log_outage.txt)Input: 4 valid requests from 4 distinct IPs, all returning 502 Bad Gateway or 504 Gateway Timeout on /api/checkout.Expected Output:{
  "total_requests": 4,
  "unique_visitors": 4,
  "error_count": 4,
  "error_rate": 100.0,a
  "malformed_entries": 0,
  "top_endpoints": [
    { "path": "/api/checkout", "count": 4 }
  ]
}
