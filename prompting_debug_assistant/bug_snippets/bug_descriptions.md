# Bug Descriptions & Intended Behavior

This document outlines the intended behavior, issue classification, and reproduction notes for each flawed code snippet inside `bug_snippets/`.

---

## Bug 1 – `bug1.py`
* **Intended Behavior**: Slice and return the last `n` items from a list of elements. If `n` equals or exceeds the list length, it should return the complete list.
* **Issue Type**: Off-by-one / Array slicing logic error.
* **Notes**: The formula `len(items) - n + 1` skips one element too many. When `n == len(items)`, it omits the first item instead of returning the entire list.

---

## Bug 2 – `bug2.js`
* **Intended Behavior**: Calculate and return the average score from an array of numbers, printing a debug log statement of the total sum.
* **Issue Type**: Syntax error.
* **Notes**: Line 11 contains an unclosed parenthesis (`console.log("Calculated total sum:", sum;`). The engine fails during parsing before execution.

---

## Bug 3 – `bug3.py`
* **Intended Behavior**: Calculate the completion percentage (`completed / total * 100`) for a map of user records.
* **Issue Type**: Runtime exception / Unhandled data type & zero-division edge cases.
* **Notes**: Throws `ZeroDivisionError` when a user has zero total tasks (`user_102`). It also throws a `TypeError` if numeric data is passed as a string (`user_103`).

---

## Bug 4 – `bug4.cpp`
* **Intended Behavior**: Compute the product of all integers in a vector.
* **Issue Type**: Integer overflow & Out-of-bounds memory access.
* **Notes**: Using a 16-bit `short` for cumulative multiplication causes rapid integer overflow. Additionally, loop bound condition `i <= numbers.size()` reads past the allocated vector boundary.

---

## Bug 5 – `bug5.js`
* **Intended Behavior**: Asynchronously fetch user object profiles for a list of target IDs and return the accumulated list.
* **Issue Type**: Logical error (Asynchronous timing & closure scope).
* **Notes**: `fetchUserData` returns synchronously before `setTimeout` callbacks run, yielding an empty list. Furthermore, using `var i` instead of `let i` causes `userIds[i]` to evaluate `userIds[3]` (`undefined`) for all callbacks.
