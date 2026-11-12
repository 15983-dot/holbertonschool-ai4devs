# Codebase Overview - Legacy Inventory & Order Management System (`codebase_overview.md`)

## Age
* **Initial Release:** March 2011 (v1.0.0)
* **Last Major Feature Update:** October 2016 (v2.4.1)
* **Maintenance Status:** Maintenance-only / end-of-life legacy monolith (~15 years old)

---

## Size
* **Total Lines of Code (LOC):** ~62,400 LOC (excluding vendor directories and static assets)
* **Language Breakdown:**
  * **PHP (5.6 / 7.0 legacy syntax):** ~44,800 LOC (71.8%)
  * **JavaScript (ES5 / jQuery):** ~11,200 LOC (17.9%)
  * **Raw SQL (Stored Procedures & Migrations):** ~6,400 LOC (10.3%)
* **File Count:** 318 source files across 14 top-level directories

---

## Main Dependencies
* **Runtime & Server:** PHP `5.6.40` running on Apache `2.4` with `mod_php`
* **Database:** MySQL `5.5` / `5.6` (using legacy `mysql_*` procedural extension wrappers)
* **Frontend Libraries:** jQuery `1.11.2`, Bootstrap `3.3.5`, DataTables `1.10.7`
* **PDF & Reporting:** `FPDF 1.7` (bundled manually inside `/libs/fpdf/`)
* **Authentication & Session Layer:** Custom MD5 + static salt password hashing and file-based PHP `$_SESSION` management
* **Email Delivery:** `PHPMailer 5.2.9` (unmaintained version with known security advisories)

---

## Known Issues and Pain Points
1. **Zero Automated Test Coverage:**
   * No unit, integration, or end-to-end test suite exists; all regression verification is performed manually in staging environments.
2. **Tight Coupling & Mixed Paradigms:**
   * Business logic, raw SQL queries, and HTML template rendering are interleaved inside single procedural scripts (e.g., `process_order.php` spans 2,300+ lines).
3. **Security & Deprecated APIs:**
   * Relies on string-concatenated SQL queries vulnerable to SQL injection, unsanitized `$_POST`/`$_GET` superglobals, and deprecated `mysql_query()` calls incompatible with PHP 8+.
4. **Global State & Hidden Side Effects:**
   * Heavy reliance on mutable global variables (`$GLOBAL_CONFIG`, `$DB_CONN`) and `include_once` chains that fail silently if execution order changes.
5. **Undocumented Schema & Stored Procedures:**
   * Core inventory stock deductions and invoice totals are split between PHP application code and 28 undocumented MySQL triggers/stored procedures, causing frequent race conditions and reconciliation drift.
6. **Hardcoded Environment Configuration:**
   * Database credentials, SMTP hosts, and third-party API endpoints are hardcoded across 19 separate configuration and controller files rather than centralized environment variables.
