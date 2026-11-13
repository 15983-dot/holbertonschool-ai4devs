# Fix Validation

## bug1.py
- **Original Issue**: Off-by-one slicing error (`len(items) - n + 1`) dropped the first required element, and mutable default argument (`cache=[]`) leaked state across calls.
- **Fix Applied**: Changed slice index to `max(0, len(items) - n)` and replaced mutable default argument with `cache=None` initialized inside the function body.
- **Test Results**: All 3 test cases passed (`n=3` returned `[30, 40, 50]`, `n=2` returned `[40, 50]`, `n=0` returned `[]`).

## bug2.js
- **Original Issue**: Function-scoped `var i` caused `users[i]` to evaluate to `undefined` inside asynchronous `setTimeout` callbacks, throwing a `TypeError`.
- **Fix Applied**: Replaced `var i = 0` with block-scoped `let i = 0` in the `for` loop declaration.
- **Test Results**: Executed with Node.js; all 3 user alerts (`Alice`, `Bob`, `Charlie`) logged cleanly without `TypeError`.

## bug3.java
- **Original Issue**: Reference equality (`==`) failed to match `new String("admin")` against the `"admin"` string literal in the list.
- **Fix Applied**: Replaced `==` with null-safe `Objects.equals(role, targetRole)` and added null guard checks on parameters.
- **Test Results**: Compiled and executed cleanly; `isAdminUser` skipped the `null` element without throwing `NullPointerException` and printed `Access Granted.`.

## bug4.cpp
- **Original Issue**: Uninitialized `sum` variable, out-of-bounds loop condition (`i <= size`), and integer division truncating decimal precision.
- **Fix Applied**: Initialized `sum = 0`, updated loop condition to `i < size`, added a `size <= 0` guard, and used `static_cast<double>(sum) / size`.
- **Test Results**: Compiled with `g++` and executed; returned exact floating-point result `Average Score: 86.25` without memory access errors.

## bug5.py
- **Original Issue**: In-place list mutation (`tokens.remove(token)`) during forward iteration skipped adjacent expired token `t2`.
- **Fix Applied**: Replaced the mutating loop with a list comprehension filtering out items where `token.get("status") == "expired"`.
- **Test Results**: Verified with assertion and console output; returned only `[{'id': 't3', 'status': 'active'}]`.
