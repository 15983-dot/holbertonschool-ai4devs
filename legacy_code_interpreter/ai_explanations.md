# AI Explanations of Complex Code (`ai_explanations.md`)

Structured plain-English analyses, architectural patterns, vulnerabilities, and refactoring recommendations for five high-complexity modules in the Legacy Inventory & Order Management System (`legacy_code_interpreter`).

---

## Section 1 – `OrderController::process_order()` (`controllers/process_order.php`, Lines 114–389)

### Legacy Code Snippet
```php
function process_order($order_id) {
    global $DB_CONN, $GLOBAL_CONFIG;
    $res = mysql_query("SELECT * FROM orders WHERE id = " . $_POST['order_id'], $DB_CONN);
    if ($res) {
        $row = mysql_fetch_assoc($res);
        if ($row['status'] == 'PENDING') {
            $items = mysql_query("SELECT * FROM order_items WHERE order_id = " . $row['id']);
            while ($item = mysql_fetch_assoc($items)) {
                $stock = mysql_fetch_assoc(mysql_query("SELECT qty FROM inventory WHERE sku = '" . $item['sku'] . "'"));
                if ($stock['qty'] >= $item['qty']) {
                    mysql_query("UPDATE inventory SET qty = qty - " . $item['qty'] . " WHERE sku = '" . $item['sku'] . "'");
                } else {
                    die("Out of stock");
                }
            }
            mysql_query("UPDATE orders SET status = 'CONFIRMED' WHERE id = " . $row['id']);
        }
    }
}
```

* **Plain English**: Fetches an order by ID, verifies that its current status is `PENDING`, loops through every line item to check warehouse stock levels, deducts the purchased quantities from the `inventory` table, and marks the order as `CONFIRMED`.
* **Pattern**: Transaction Script anti-pattern with deeply nested conditionals (`if` inside `if` inside `while`) and N+1 database queries inside a loop.
* **Issues**:
  * **Critical SQL Injection**: Directly concatenates `$_POST['order_id']` and `$item['sku']` into raw SQL strings.
  * **No Database Transactions**: If the third item in an order is out of stock, `die("Out of stock")` halts execution after the first two items have already had their inventory deducted, corrupting stock counts.
  * **Deprecated Driver & Global State**: Relies on removed `mysql_*` functions and implicit `$DB_CONN` globals.
* **Improvements**: Wrap the workflow in a PDO database transaction (`beginTransaction()` / `commit()` / `rollBack()`), use prepared statements with bound parameters, lock inventory rows with `SELECT ... FOR UPDATE`, and throw structured domain exceptions instead of calling `die()`.

---

## Section 2 – `AuthManager::verify_legacy_session()` (`includes/auth_session.php`, Lines 42–118)

### Legacy Code Snippet
```php
function verify_legacy_session($user_input_pass, $stored_hash) {
    $salt = "INV_SYS_2011_STATIC";
    if (md5($salt . $user_input_pass) == $stored_hash) {
        $_SESSION['auth'] = true;
        $_SESSION['role'] = $_COOKIE['user_role'] ? $_COOKIE['user_role'] : 'staff';
        return true;
    }
    return false;
}
```

* **Plain English**: Prepends a hardcoded string salt to the user's plaintext password, hashes it with MD5, compares it against the stored password hash, and initializes an authenticated PHP session using a role read from a browser cookie.
* **Pattern**: Custom procedural authentication helper relying on client-trusted state (`$_COOKIE`).
* **Issues**:
  * **Broken Cryptography**: MD5 with a static global salt is vulnerable to GPU rainbow-table and collision attacks.
  * **Type Juggling Vulnerability**: Uses loose equality (`==`) instead of `hash_equals()`, allowing PHP magic-hash type juggling bypasses (e.g., hashes starting with `0e...`).
  * **Privilege Escalation**: Reads `$_SESSION['role']` directly from an unsigned client-side cookie (`$_COOKIE['user_role']`), letting any user escalate privileges to `admin` by editing their browser cookie.
* **Improvements**: Migrate password storage to `password_hash()` / `password_verify()` (Bcrypt/Argon2id), regenerate session IDs on login (`session_regenerate_id(true)`), and load user roles exclusively from the server-side database record.

---

## Section 3 – `PricingEngine::calculate_tiered_discount()` (`libs/pricing_rules.php`, Lines 210–305)

### Legacy Code Snippet
```php
function calculate_tiered_discount($subtotal, $cust_type, $promo, $is_holiday) {
    $disc = 0;
    if ($cust_type == 'VIP') {
        if ($subtotal > 500) {
            $disc = ($promo == 'SAVE20') ? 0.25 : 0.15;
        } else {
            $disc = ($is_holiday) ? 0.12 : 0.10;
        }
    } else {
        if ($promo == 'SAVE20' && !$is_holiday) {
            $disc = 0.20;
        } elseif ($subtotal > 1000) {
            $disc = 0.05;
        }
    }
    return round($subtotal - ($subtotal * $disc), 2);
}
```

* **Plain English**: Determines a percentage discount based on customer tier (`VIP` vs. regular), order subtotal thresholds, promotional codes, and holiday flags, then returns the discounted subtotal rounded to two decimal places.
* **Pattern**: Deeply nested conditional decision tree with hardcoded magic numbers and overlapping business rules.
* **Issues**:
  * **Floating-Point Precision Drift**: Uses native IEEE 754 binary floats for currency arithmetic, leading to cent-level rounding discrepancies on multi-item invoices.
  * **Hidden Business Rule Conflicts**: `VIP` customers using `SAVE20` on orders under `$500` receive `0%` promo benefit (falling back to `10%`), whereas non-VIP customers receive `20%`—an unintentional logic bug caused by nested branching.
  * **Poor Extensibility**: Adding a new customer tier or seasonal rule requires modifying core conditional branches (violating the Open/Closed Principle).
* **Improvements**: Refactor into a Strategy / Rule-Engine pattern where discrete discount rules are evaluated independently, use integer cents or `BCMath` (`bcmul` / `bcsub`) for exact monetary math, and cover all rule combinations with parameterized unit tests.

---

## Section 4 – `StockSyncDaemon::reconcile_warehouse_feed()` (`cron/sync_stock.php`, Lines 15–142)

### Legacy Code Snippet
```php
function reconcile_warehouse_feed($csv_path) {
    $handle = fopen($csv_path, "r");
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $sku = trim($data[0]);
        $delta = intval($data[1]);
        $current = fetch_scalar("SELECT qty FROM inventory WHERE sku = '$sku'");
        if ($current !== null) {
            exec_sql("UPDATE inventory SET qty = " . ($current + $delta) . " WHERE sku = '$sku'");
        }
    }
    fclose($handle);
}
```

* **Plain English**: Reads a comma-separated warehouse inventory feed line by line, queries the current stock quantity for each SKU, adds the incoming delta adjustment in PHP memory, and writes the new absolute quantity back to the database.
* **Pattern**: Read-Modify-Write batch file processor without concurrency locking or stream validation.
* **Issues**:
  * **Lost Update Race Condition**: Reading `$current` into PHP and writing `$current + $delta` overwrites concurrent customer orders placed between the `SELECT` and `UPDATE` queries.
  * **Missing File & Row Validation**: Fails with warnings/fatals if `$csv_path` does not exist, if a CSV line exceeds 1,000 characters, or if malformed rows lack index `[1]`.
  * **Memory & Execution Bottlenecks**: Executes two synchronous database round-trips per CSV row, causing cron job timeouts on large warehouse feeds (10,000+ SKUs).
* **Improvements**: Perform atomic relative SQL updates (`UPDATE inventory SET qty = qty + :delta WHERE sku = :sku`), validate file handles and column counts before processing, and batch updates inside chunked transactions.

---

## Section 5 – `InvoicePdfBuilder::render_line_items()` (`reports/invoice_pdf.php`, Lines 88–195)

### Legacy Code Snippet
```php
function render_line_items($pdf, $order_id) {
    $rows = query_all("SELECT * FROM order_items WHERE order_id = $order_id");
    $y = 65;
    foreach ($rows as $r) {
        if ($y > 260) {
            $pdf->AddPage();
            $y = 20;
        }
        $pdf->SetXY(10, $y);
        $pdf->Cell(80, 8, iconv('UTF-8', 'windows-1252', $r['description']), 1);
        $pdf->Cell(30, 8, $r['qty'], 1);
        $pdf->Cell(40, 8, number_format($r['unit_price'], 2), 1);
        $y += 8;
    }
}
```

* **Plain English**: Queries all line items for an invoice, manually tracks vertical cursor coordinates (`$y`) on an `FPDF` canvas, inserts a page break whenever `$y` exceeds `260mm`, converts UTF-8 descriptions to `windows-1252`, and draws bordered table cells for each item.
* **Pattern**: Procedural coordinate-driven layout rendering tightly coupled to direct database queries.
* **Issues**:
  * **Text Truncation & Silent Character Loss**: `iconv('UTF-8', 'windows-1252', ...)` fails with a notice or truncates strings if product descriptions contain unsupported Unicode characters (e.g., emojis, CJK, or non-Latin symbols), and long descriptions overflow the fixed `80mm` cell width.
  * **Coupled Data Fetching & Rendering**: Executes SQL queries directly inside the PDF presentation loop, making it impossible to preview or test invoice layouts without a live database.
  * **Magic Layout Constants**: Hardcoded page height thresholds (`260`) and column widths break whenever paper size or header height changes.
* **Improvements**: Decouple data retrieval by passing an immutable `InvoiceDTO` object into the renderer, enable `iconv(..., 'windows-1252//TRANSLIT//IGNORE', ...)` or upgrade to a UTF-8 capable PDF library (e.g., `TCPDF` / `mPDF`), and use `MultiCell` with dynamic row-height calculation.
