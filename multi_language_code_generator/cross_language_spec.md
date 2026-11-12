# Cross-Language Specification - Server Log Analyzer (`cross_language_spec.md`)

## Algorithm Description
The Server Log Analyzer parses raw Common Log Format (CLF) / Apache access log streams line-by-line to compute operational traffic metrics and reliability statistics across multiple programming languages (e.g., Python, JavaScript/TypeScript, Go, C++).

For each input stream, the algorithm must execute the following steps:
1. **Line Parsing:** Extract the client IP address, HTTP method, request path, HTTP status code, and response byte size from each valid log entry.
2. **Request Aggregation:** Increment `total_requests` for every syntactically valid log line.
3. **Unique Visitor Tracking:** Maintain a deduplicated set of valid client IP addresses to compute `unique_visitors`.
4. **Error Classification:** Classify any HTTP status code in the `400–599` range (`4xx` client errors and `5xx` server errors) as an error request.
5. **Rate & Endpoint Calculation:**
   * Compute `error_rate` as `(error_count / total_requests) * 100`, rounded to **2 decimal places** (or `0.0` if `total_requests == 0`).
   * Identify the most frequently requested endpoint (`top_endpoint`); break ties lexicographically (alphabetically ascending).
6. **Fault-Tolerant Filtering:** Skip malformed or blank lines without throwing unhandled exceptions, incrementing `malformed_lines` for each invalid entry.

---

## Input Format
A UTF-8 plain-text log string or newline-delimited file (`\n` or `\r\n`) following the standard Apache Common Log Format:

```text
<ip_address> - - [<timestamp>] "<method> <endpoint> <protocol>" <status_code> <bytes>
```

### Example Input
```text
192.168.1.10 - - [12/Nov/2026:10:00:01 +0000] "GET /api/v1/users HTTP/1.1" 200 1024
192.168.1.11 - - [12/Nov/2026:10:00:02 +0000] "POST /api/v1/login HTTP/1.1" 401 256
192.168.1.10 - - [12/Nov/2026:10:00:05 +0000] "GET /api/v1/users HTTP/1.1" 500 512
```

---

## Output Format
A deterministic JSON object containing aggregated traffic statistics:

```json
{
  "total_requests": 3,
  "unique_visitors": 2,
  "error_count": 2,
  "error_rate": 66.67,
  "malformed_lines": 0,
  "top_endpoint": "/api/v1/users"
}
```

### Field Definitions
* `total_requests` (`integer`): Total number of valid parsed log lines.
* `unique_visitors` (`integer`): Count of distinct client IP addresses among valid lines.
* `error_count` (`integer`): Total valid requests returning status codes `>= 400` and `<= 599`.
* `error_rate` (`float`): Percentage of valid requests resulting in an error, rounded to 2 decimal places.
* `malformed_lines` (`integer`): Count of non-empty lines failing regex/format validation.
* `top_endpoint` (`string | null`): Most frequently requested endpoint path among valid lines, or `null` when `total_requests == 0`.

---

## Edge Cases
1. **Empty Input (`""` or whitespace-only):** Must not divide by zero; returns `0` for all numeric counts, `0.0` for `error_rate`, and `null` for `top_endpoint`.
2. **Malformed Entries:** Corrupted lines (missing quotes, non-numeric status codes, truncated lines) are skipped safely and increment `malformed_lines` without affecting `total_requests`.
3. **100% Error Rate:** When every valid request returns a `4xx` or `5xx` status code, `error_rate` must accurately equal `100.0`.
4. **Endpoint Frequency Tie-Breaking:** If two or more endpoints share the exact same highest request count, return the lexicographically smallest path (e.g., `"/api/a"` before `"/api/b"`).
5. **Duplicate IP Addresses:** Multiple requests from the same IP increment `total_requests` each time, but count only once toward `unique_visitors`.

---

## Test Cases

### Test Case 1: Standard Mixed Traffic (`log_standard.txt`)
* **Input:**
  ```text
  10.0.0.1 - - [12/Nov/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 2048
  10.0.0.2 - - [12/Nov/2026:12:00:02 +0000] "GET /index.html HTTP/1.1" 200 2048
  10.0.0.1 - - [12/Nov/2026:12:00:03 +0000] "POST /api/orders HTTP/1.1" 500 128
  10.0.0.3 - - [12/Nov/2026:12:00:04 +0000] "GET /missing HTTP/1.1" 404 64
  ```
* **Expected Output:**
  ```json
  {
    "total_requests": 4,
    "unique_visitors": 3,
    "error_count": 2,
    "error_rate": 50.0,
    "malformed_lines": 0,
    "top_endpoint": "/index.html"
  }
  ```

---

### Test Case 2: Empty Log File (`log_empty.txt`)
* **Input:**
  ```text
  ```
* **Expected Output:**
  ```json
  {
    "total_requests": 0,
    "unique_visitors": 0,
    "error_count": 0,
    "error_rate": 0.0,
    "malformed_lines": 0,
    "top_endpoint": null
  }
  ```

---

### Test Case 3: Malformed Entries Mixed with Valid Traffic (`log_malformed.txt`)
* **Input:**
  ```text
  172.16.0.5 - - [12/Nov/2026:12:05:00 +0000] "GET /health HTTP/1.1" 200 32
  CORRUPTED_RAW_LOG_LINE_WITHOUT_STRUCTURE
  172.16.0.5 - - [12/Nov/2026:12:05:02 +0000] "GET /health HTTP/1.1" INVALID_CODE 32
  ```
* **Expected Output:**
  ```json
  {
    "total_requests": 1,
    "unique_visitors": 1,
    "error_count": 0,
    "error_rate": 0.0,
    "malformed_lines": 2,
    "top_endpoint": "/health"
  }
  ```

---

### Test Case 4: Endpoint Tie-Breaking (`log_tie_breaker.txt`)
* **Input:**
  ```text
  192.168.0.10 - - [12/Nov/2026:12:10:01 +0000] "GET /api/zeta HTTP/1.1" 200 512
  192.168.0.11 - - [12/Nov/2026:12:10:02 +0000] "GET /api/alpha HTTP/1.1" 200 512
  ```
* **Expected Output:**
  ```json
  {
    "total_requests": 2,
    "unique_visitors": 2,
    "error_count": 0,
    "error_rate": 0.0,
    "malformed_lines": 0,
    "top_endpoint": "/api/alpha"
  }
  ```

---

### Test Case 5: 100% Error Rate Outage (`log_all_errors.txt`)
* **Input:**
  ```text
  203.0.113.1 - - [12/Nov/2026:12:15:01 +0000] "POST /api/pay HTTP/1.1" 502 120
  203.0.113.2 - - [12/Nov/2026:12:15:02 +0000] "POST /api/pay HTTP/1.1" 503 120
  203.0.113.1 - - [12/Nov/2026:12:15:03 +0000] "GET /api/pay HTTP/1.1" 429 90
  ```
* **Expected Output:**
  ```json
  {
    "total_requests": 3,
    "unique_visitors": 2,
    "error_count": 3,
    "error_rate": 100.0,
    "malformed_lines": 0,
    "top_endpoint": "/api/pay"
  }
  ```
