# Bug Descriptions

## bug1.py
- **Intended Behavior**: Return the exact last `n` elements of a list and store query results safely per invocation.
- **Current Issue**: 
  1. Off-by-one slicing error (`len(items) - n + 1` drops the first required element, returning `n - 1` items instead of `n`).
  2. Uses a mutable default argument (`cache=[]`), causing state to persist unexpectedly across separate function calls.

## bug2.js
- **Intended Behavior**: Iterate through the `users` array and log a personalized alert message for each user after a staggered delay.
- **Current Issue**: Uses `var` in the `for` loop declaration. By the time the `setTimeout` callbacks execute, the loop has finished and `i` equals `users.length` (3), throwing a `TypeError: Cannot read properties of undefined (reading 'name')`.

## bug3.java
- **Intended Behavior**: Check whether a list of user roles contains the `"admin"` role without crashing on `null` entries.
- **Current Issue**: Uses `==` instead of `.equals()` to compare `String` objects, which checks reference equality rather than value equality and returns `false` for `new String("admin")`.

## bug4.cpp
- **Intended Behavior**: Compute and return the accurate floating-point average of an integer array of exam scores.
- **Current Issue**: 
  1. `sum` is uninitialized, leading to undefined garbage values.
  2. Off-by-one loop condition (`i <= size`) reads out-of-bounds memory at `scores[4]`.
  3. Integer division (`sum / size`) truncates the decimal remainder before returning a `double`.

## bug5.py
- **Intended Behavior**: Filter out all dictionaries with `"status": "expired"` and return only active session tokens.
- **Current Issue**: Mutates the `tokens` list in place (`tokens.remove(token)`) while iterating over it, causing the iterator to skip adjacent elements (`t2` is skipped after `t1` is removed).
