# Benchmark Tasks — Copilot Productivity Sprint

A set of 4 varied coding tasks scoped for 15–30 minutes each, formatted for the `holbertonschool-ai4devs/copilot_productivity_sprint` benchmark suite.

---

## Task 1 - CRUD Endpoint
**Requirements**: Implement a RESTful `POST /users` endpoint with payload validation and duplicate email checks.  
**Inputs**: JSON `{ "name": "string", "email": "string" }`  
**Outputs**: Stored user object with generated ID (`{ "id": "uuid", "name": "string", "email": "string", "created_at": "ISO-8601" }`)  
**Acceptance Criteria**:  
- Returns `201 Created` with the newly created user JSON on success  
- Returns `400 Bad Request` on missing `name` or invalid `email` format  
- Returns `409 Conflict` if the email address is already registered  

---

## Task 2 - Server Log Stream Parser & Anomaly Detector
**Requirements**: Implement a Python function `analyze_logs(log_lines, window_seconds=60, error_threshold=3)` using only the standard library to bucket HTTP status categories (`2xx`, `4xx`, `5xx`) and detect rolling time-window `5xx` error spikes.  
**Inputs**: List of log strings formatted as `"<ISO-8601 Timestamp> | <METHOD> | <ENDPOINT> | <STATUS_CODE>"`  
**Outputs**: Dictionary `{ "status_counts": dict, "invalid_lines": int, "anomaly_detected": bool, "first_anomaly_timestamp": str | None }`  
**Acceptance Criteria**:  
- Accurately aggregates `2xx`, `4xx`, and `5xx` counts across all valid entries  
- Skips malformed lines safely without throwing exceptions and increments `invalid_lines`  
- Flags `anomaly_detected: True` when `>= error_threshold` `5xx` responses occur within any `window_seconds` span  

---

## Task 3 - Rate-Limited Async Batch Fetcher
**Requirements**: Implement an asynchronous JavaScript/TypeScript function `fetchWithRetry(urls, maxConcurrency, maxRetries)` using native `fetch` that enforces a maximum number of simultaneous requests and retries transient failures (`429`, `5xx`, network errors) with exponential backoff.  
**Inputs**: Array of URL strings (`string[]`), `maxConcurrency` (`number`), and `maxRetries` (`number`)  
**Outputs**: Array of result objects preserving original input index order: `[{ "url": string, "status": "fulfilled" | "rejected", "data"?: any, "error"?: string }]`  
**Acceptance Criteria**:  
- Never exceeds `maxConcurrency` simultaneous in-flight network requests  
- Does not retry non-transient client errors (`400`, `401`, `403`, `404`)  
- Preserves exact input order in the output array regardless of completion order  

---

## Task 4 - Shopping Cart Refactor & Precision Bug Fix
**Requirements**: Refactor a legacy Python `calculate_checkout_total(items, promo_code=None, tax_rate=0.08)` function to eliminate mutable default argument state leakage, enforce input validation, and fix floating-point rounding inaccuracies using `decimal.Decimal`.  
**Inputs**: List of item dictionaries `[{"name": str, "price": float, "qty": int}]`, optional `promo_code` (`"SAVE10"` or `"SAVE20"`), and `tax_rate` (`float`)  
**Outputs**: Final checkout total as a `float` rounded to exactly 2 decimal places (`ROUND_HALF_UP`)  
**Acceptance Criteria**:  
- Subsequent function calls do not retain promo codes from prior invocations  
- Raises `ValueError` if any item has negative `price` or `qty`, or if `tax_rate < 0`  
- Accurately computes currency totals without binary floating-point drift
