# Risk Assessment - Legacy Inventory & Order Management System

Prioritized technical, security, and operational risks identified across the `legacy_code_interpreter` codebase, ranked by severity and potential business impact.

| Risk | Severity | Notes |
| --- | --- | --- |
| SQL Injection Vulnerabilities | High | Raw user inputs are directly concatenated into SQL queries without sanitization or prepared statements across core controllers (`controllers/process_order.php`). |
| Broken Authentication & Privilege Escalation | High | Passwords use MD5 with a static salt and loose comparison, while user roles are read directly from an unsigned browser cookie (`includes/auth_session.php`). |
| Deprecated MySQL API Usage | High | Relies on procedural `mysql_query()` and `mysql_fetch_assoc()` functions removed in PHP 7.0+, blocking runtime upgrades and leaving the server on unsupported PHP 5.6. |
| Hardcoded Credentials & Secrets | High | Database passwords, SMTP credentials, and third-party API keys are stored in plaintext across 19 source and configuration files (`config.php`, controllers). |
| Non-Transactional Inventory Deductions | High | Multi-item order processing (`controllers/process_order.php`) deducts stock sequentially without database transactions, causing partial stock corruption if an item fails validation. |
| Inventory Lost-Update Race Conditions | Medium | Warehouse stock synchronization (`cron/sync_stock.php`) uses a non-atomic Read-Modify-Write pattern in PHP memory, overwriting concurrent customer order deductions. |
| Zero Automated Test Coverage | Medium | Critical checkout, pricing, and reconciliation modules have no unit or integration tests, making bug fixes and refactoring prone to silent regressions. |
| Tight Coupling & Mixed Paradigms | Medium | SQL queries, business logic, global variables, and HTML/PDF rendering are interleaved inside 2,300+ line procedural scripts, preventing isolated component testing. |
| Floating-Point Currency Rounding Drift | Medium | Tiered discount and tax calculations (`libs/pricing_rules.php`) use native binary float arithmetic rather than integer cents or `BCMath`, causing cent-level invoice discrepancies. |
| Lack of Structured Error Logging | Low | Failures terminate abruptly via `die()` or fail silently without structured application logs, stack traces, or correlation IDs, slowing down production debugging. |
