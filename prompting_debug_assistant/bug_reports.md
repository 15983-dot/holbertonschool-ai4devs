# Structured Bug Reports

This document summarizes the findings, root causes, resolutions, and lessons learned for all resolved bug snippets.

---

## Bug 1 Report

* **File Name**: `bug1.py`
* **Bug Summary**: Off-by-one index math error causing array slicing to drop the first element when requesting $n$ items.
* **Root Cause**: The calculation `start_index = len(items) - n + 1` added an unnecessary `+1` offset, shifting the slice start index forward by one element.
* **Resolution**: 
  * **AI Suggestion**: Use `len(items) - n` or negative index slicing `items[-n:]`.
  * **Manual Edits**: Applied `max(0, len(items) - n)` to prevent negative start indices when $n > \text{len}(items)$.
  * **Before / After**:
    ```python
    # Before
    start_index = len(items) - n + 1
    return items[start_index:]

    # After
    start_index = max(0, len(items) - n)
    return items[start_index:]
    ```
* **Lessons Learned**: Relying on manually offset index arithmetic for sequence slicing is prone to off-by-one boundary bugs. Always test edge cases where requested length equals or exceeds array bounds.

---

## Bug 2 Report

* **File Name**: `bug2.js`
* **Bug Summary**: Syntax parsing failure due to a missing closing parenthesis in a logging statement.
* **Root Cause**: `console.log("Calculated total sum:", sum;` missing the closing bracket `)` before the semicolon, halting interpreter parsing.
* **Resolution**: 
  * **AI Suggestion**: Add the missing closing parenthesis to balance the function call signature.
  * **Manual Edits**: None needed.
  * **Before / After**:
    ```javascript
    // Before
    console.log("Calculated total sum:", sum;

    // After
    console.log("Calculated total sum:", sum);
    ```
* **Lessons Learned**: Configure IDE syntax linters (e.g., ESLint) and automated pre-commit hooks to catch trivial syntax mistakes before runtime execution.

---

## Bug 3 Report

* **File Name**: `bug3.py`
* **Bug Summary**: Runtime crash (`ZeroDivisionError` & `TypeError`) when processing user completion metrics.
* **Root Cause**: Executing `completed_tasks / total_tasks` without verifying `total_tasks > 0`, and failing to convert metric values passed as string types.
* **Resolution**: 
  * **AI Suggestion**: Convert metric fields to float/int explicitly and add a zero check before dividing.
  * **Manual Edits**: Wrapped type conversions inside a `try/except (ValueError, TypeError)` block to safely assign default scores for invalid input.
  * **Before / After**:
    ```python
    # Before
    completion_rate = completed_tasks / total_tasks

    # After
    try:
        total_tasks = float(metrics.get("total", 0))
        completed_tasks = float(metrics.get("completed", 0))
    except (ValueError, TypeError):
        results[user_id] = 0.0
        continue

    if total_tasks <= 0:
        results[user_id] = 0.0
    else:
        completion_rate = completed_tasks / total_tasks
        results[user_id] = round(completion_rate * 100, 2)
    ```
* **Lessons Learned**: Never assume incoming data payloads match expected types or non-zero numeric constraints. Implement defensive checks and type validation at the boundary of data processing functions.

---

## Bug 4 Report

* **File Name**: `bug4.cpp`
* **Bug Summary**: Integer overflow during cumulative multiplication and memory access segmentation fault.
* **Root Cause**: 
  1. Accumulated value stored in a 16-bit signed integer (`short`), causing overflow once values exceed 32,767.
  2. Loop condition `i <= numbers.size()` accessed memory out of array bounds at `numbers[numbers.size()]`.
* **Resolution**: 
  * **AI Suggestion**: Upgrade accumulator type to `long long` and change index boundary to `i < numbers.size()`.
  * **Manual Edits**: Replaced indexed loop with a C++ range-based loop `for (int num : numbers)` and added an empty vector check.
  * **Before / After**:
    ```cpp
    // Before
    short product = 1;
    for (size_t i = 0; i <= numbers.size(); ++i) {
        product *= numbers[i];
    }

    // After
    long long product = 1;
    for (int num : numbers) {
        product *= num;
    }
    ```
* **Lessons Learned**: Range-based loops in typed languages prevent buffer overflows by removing manual index access. Always select integer types wide enough (`long long`, `int64_t`) for compounding calculations.

---

## Bug 5 Report

* **File Name**: `bug5.js`
* **Bug Summary**: Function synchronously returns an empty array, and asynchronous closures evaluate undefined user IDs.
* **Root Cause**: 
  1. `fetchUserData` returns `users` synchronously before `setTimeout` callbacks fire.
  2. Function-scoped `var i` evaluates to `userIds.length` by the time asynchronous timers execute, resolving `userIds[i]` to `undefined`.
* **Resolution**: 
  * **AI Suggestion**: Refactor using `Promise.all` with `async/await` and map each ID inside an explicit Promise instance.
  * **Manual Edits**: Added early return guard for empty or missing input arrays `!userIds || userIds.length === 0`.
  * **Before / After**:
    ```javascript
    // Before
    function fetchUserData(userIds) {
        let users = [];
        for (var i = 0; i < userIds.length; i++) {
            setTimeout(function() {
                users.push({ id: userIds[i], status: "active" });
            }, 100);
        }
        return users;
    }

    // After
    async function fetchUserData(userIds) {
        if (!userIds || userIds.length === 0) return [];
        const fetchPromises = userIds.map(id => {
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve({ id: id, status: "active" });
                }, 100);
            });
        });
        return await Promise.all(fetchPromises);
    }
    ```
* **Lessons Learned**: Avoid mixing legacy function-scoped loop counters (`var`) with asynchronous execution. Use `Promise.all` when waiting for multiple concurrent asynchronous tasks to complete.
