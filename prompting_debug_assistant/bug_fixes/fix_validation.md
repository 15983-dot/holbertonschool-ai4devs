# Code Fix Verification & Test Validation Log

This document records the test cases, expected outputs, actual outputs, and execution results for all corrected snippets in `bug_fixes/`.

---

## Bug 1 – `bug1_fixed.py`

* **Changes Applied**: Updated start index calculation from `len(items) - n + 1` to `max(0, len(items) - n)`.
* **Manual Tweaks Beyond AI Suggestion**: Wrapped index offset with `max(0, ...)` to prevent negative slicing when `n > len(items)`.

### Test Cases
* **Test 1.1**: Standard slice
  * **Input**: `items = [10, 20, 30, 40, 50], n = 3`
  * **Expected Output**: `[30, 40, 50]`
  * **Actual Output**: `[30, 40, 50]` ✅
* **Test 1.2**: `n` equal to array length
  * **Input**: `items = [10, 20, 30, 40, 50], n = 5`
  * **Expected Output**: `[10, 20, 30, 40, 50]`
  * **Actual Output**: `[10, 20, 30, 40, 50]` ✅
* **Test 1.3**: `n` larger than array length
  * **Input**: `items = [10, 20, 30, 40, 50], n = 10`
  * **Expected Output**: `[10, 20, 30, 40, 50]`
  * **Actual Output**: `[10, 20, 30, 40, 50]` ✅

---

## Bug 2 – `bug2_fixed.js`

* **Changes Applied**: Added missing closing parenthesis to `console.log("Calculated total sum:", sum);`.
* **Manual Tweaks Beyond AI Suggestion**: None.

### Test Cases
* **Test 2.1**: Syntax validation & standard array average calculation
  * **Input**: `scores = [88, 92, 79, 95]`
  * **Expected Output**:  
    `Calculated total sum: 354`  
    `Average Score: 88.5`
  * **Actual Output**:  
    `Calculated total sum: 354`  
    `Average Score: 88.5` ✅

---

## Bug 3 – `bug3_fixed.py`

* **Changes Applied**: Added safe float parsing within a `try/except` block and explicit `total_tasks <= 0` guard check.
* **Manual Tweaks Beyond AI Suggestion**: Added explicit error handling for unparseable non-numeric strings (e.g., `"invalid"`).

### Test Cases
* **Test 3.1**: Mixed input payload containing zeros and numeric strings
  * **Input**:  
    ```python
    {
        "user_101": {"completed": 8, "total": 10},
        "user_102": {"completed": 0, "total": 0},
        "user_103": {"completed": "5", "total": 10},
        "user_104": {"completed": "invalid", "total": 10}
    }
    ```
  * **Expected Output**: `{'user_101': 80.0, 'user_102': 0.0, 'user_103': 50.0, 'user_104': 0.0}`
  * **Actual Output**: `{'user_101': 80.0, 'user_102': 0.0, 'user_103': 50.0, 'user_104': 0.0}` ✅

---

## Bug 4 – `bug4_fixed.cpp`

* **Changes Applied**: Changed loop from index-bound (`i <= size()`) to range-based `for (int num : numbers)` and variable type of `product` from `short` to `long long`.
* **Manual Tweaks Beyond AI Suggestion**: Added empty array guard returning `0`.

### Test Cases
* **Test 4.1**: Standard product evaluation
  * **Input**: `vector<int>{2, 3, 4, 5, 6}`
  * **Expected Output**: `720`
  * **Actual Output**: `720` ✅

---

## Bug 5 – `bug5_fixed.js`

* **Changes Applied**: Converted function to `async/await` pattern returning `Promise.all(fetchPromises)`.
* **Manual Tweaks Beyond AI Suggestion**: Added self-executing async test block with element verification.

### Test Cases
* **Test 5.1**: Asynchronous resolution with array ID matching
  * **Input**: `[101, 102, 103]`
  * **Expected Output**:  
    `Fetched users: [ { id: 101, status: 'active' }, { id: 102, status: 'active' }, { id: 103, status: 'active' } ]`
  * **Actual Output**:  
    `Fetched users: [ { id: 101, status: 'active' }, { id: 102, status: 'active' }, { id: 103, status: 'active' } ]` ✅
