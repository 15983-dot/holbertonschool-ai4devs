# Bug Descriptions

Directory: `prompting_debug_assistant/bug_snippets/`

---

## Bug 1 – bug1_off_by_one.py
- **Language**: Python
- **Intended Behavior**: Return the last `n` items of a list.
- **Issue Type**: Off-by-one / Slice Index Logic Error.
- **Notes**: Calculating `len(items) - n + 1` skips the first item of the requested subslice. For example, asking for the last 3 items of a 5-item list returns only 2 items.

---

## Bug 2 – bug2_syntax_error.js
- **Language**: JavaScript
- **Intended Behavior**: Calculate and return the discounted price given an initial price and percentage discount rate.
- **Issue Type**: Syntax Error.
- **Notes**: Missing a closing parenthesis `)` in the `if` condition line (`if (price <= 0 || discountRate < 0 {`), causing the JavaScript parser to throw a `SyntaxError: Unexpected token '{'`.

---

## Bug 3 – bug3_runtime_exception.py
- **Language**: Python
- **Intended Behavior**: Iterate through a list of user profile dictionaries, aggregate their scores, and compute the average score.
- **Issue Type**: Runtime Exception (`KeyError` & `ZeroDivisionError`).
- **Notes**: Accessing `user['score']` directly without `.get()` throws a `KeyError` if any dictionary lacks the `'score'` key. Additionally, passing an empty list results in a `ZeroDivisionError`.

---

## Bug 4 – bug4_logic_error.js
- **Language**: JavaScript
- **Intended Behavior**: Filter out even integers from an array and compute their sum.
- **Issue Type**: Logical Error.
- **Notes**: The conditional uses `numbers[i] % 2 === 1`, which targets odd numbers instead of evens. Inside the loop, it uses assignment (`sum = numbers[i]`) instead of addition assignment (`sum += numbers[i]`), returning only the last odd number.

---

## Bug 5 – bug5_datatype_misuse.cpp
- **Language**: C++
- **Intended Behavior**: Calculate the exact double-precision floating-point average of a collection of integer test scores.
- **Issue Type**: Misuse of Data Types / Type Casting Failure.
- **Notes**: Performing `sum / scores.size()` where both operands are integers causes implicit integer division, truncating fractional decimal parts before assigning the result to the `double` return variable.
