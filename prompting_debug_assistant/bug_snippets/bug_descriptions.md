# AI Debugging Log & Resolution Report

This log records the diagnostic process, AI responses, tested fixes, and final verification results for each buggy snippet in `bug_snippets/`.

---

## Bug 1 – `bug1.py`

* **Prompt Sent**:  
  > "This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?  
  > ```python
  > def get_last_n_items(items, n):
  >     if not items or n <= 0:
  >         return []
  >     start_index = len(items) - n + 1
  >     return items[start_index:]
  > ```"

* **AI Diagnosis**:  
  The formula `len(items) - n + 1` introduces an off-by-one error by adding `1` unnecessarily. In Python 0-indexed slicing, the offset starting `n` elements from the end of a list is simply `len(items) - n` or negative slicing `items[-n:]`.

* **Suggested Fix**:  
  Change `start_index = len(items) - n + 1` to `start_index = len(items) - n` (or return `items[-n:]`).

* **Alternative Fixes Tested**:
  1. **Alternative A (Negative Slicing)**: `return items[-n:]`
  2. **Alternative B (Clamped Bounds)**: `return items[max(0, len(items) - n):]`

* **Result**:  
  * **Fix 1 (Direct Index Math)**: Works as expected for standard bounds, but returns extra items if `n > len(items)`.
  * **Fix 2 (Negative Slicing)**: Clean and readable, but `items[-n:]` fails when `n > len(items)` by returning the whole list without clamping.
  * **Fix 3 (Clamped Bounds)**: `items[max(0, len(items) - n):]` is the most robust fix. It handles edge cases where `n` exceeds list size seamlessly.

---

## Bug 2 – `bug2.js`

* **Prompt Sent**:  
  > "This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?  
  > `SyntaxError: Unexpected token ';'`  
  > ```javascript
  > console.log("Calculated total sum:", sum;
  > ```"

* **AI Diagnosis**:  
  Syntax error on line 11 due to a missing closing parenthesis `)` before the terminating semicolon in the `console.log` statement.

* **Suggested Fix**:  
  Add the missing parenthesis: `console.log("Calculated total sum:", sum);`.

* **Alternative Fixes Tested**: None required.

* **Result**:  
  Fix works as expected. Script executes without syntax parsing errors and accurately computes array averages.

---

## Bug 3 – `bug3.py`

* **Prompt Sent**:  
  > "This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?  
  > `ZeroDivisionError: division by zero`  
  > `TypeError: unsupported operand type(s) for /: 'str' and 'int'`"

* **AI Diagnosis**:  
  The function suffers from two distinct runtime bugs:
  1. Unhandled division by zero when `total_tasks == 0`.
  2. Missing type coercion when metric inputs are passed as numeric strings instead of integers or floats.

* **Suggested Fix**:  
  Cast metrics to `float` or `int`, and add a guard condition for zero total tasks:
  ```python
  total_tasks = float(metrics.get("total", 0))
  completed_tasks = float(metrics.get("completed", 0))

  if total_tasks == 0:
      results[user_id] = 0.0
  else:
      completion_rate = completed_tasks / total_tasks
      results[user_id] = round(completion_rate * 100, 2)
