Markdown
# AI Debugging Log

Directory: `prompting_debug_assistant/bug_snippets/`

---

## Bug 1 – bug1_off_by_one.py

**Prompt**:  
"This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?"

**AI Diagnosis**:  
The slice index `start_index = len(items) - n + 1` shifts the starting index one position too far to the right, causing the function to exclude the first element of the intended slice. For example, given a 5-element list and `n = 3`, `5 - 3 + 1 = 3`, which returns index `[3:]` (2 elements) instead of index `[2:]` (3 elements).

**Suggested Fix**:  
Change the slice index to negative indexing `items[-n:]` or use `start_index = len(items) - n`.

```python
def get_last_n_items(items, n):
    if n <= 0:
        return []
    return items[-n:]
Alternative Fixes Tested:

items[len(items) - n:]: Correctly calculates the zero-based offset and returns the expected slice.

Result:

Works as expected.

Bug 2 – bug2_syntax_error.js
Prompt:

"This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?"

AI Diagnosis:

The if condition statement is missing a closing parenthesis: if (price <= 0 || discountRate < 0 {. This causes the JavaScript parser to encounter an unexpected token { and throw a SyntaxError: Unexpected token '{'.

Suggested Fix:

Add the missing closing parenthesis to close the if conditional expression:

JavaScript
function calculateDiscount(price, discountRate) {
    if (price <= 0 || discountRate < 0) {
        return price;
    }

    let finalPrice = price - (price * (discountRate / 100));
    return finalPrice;
}
Alternative Fixes Tested:

None.

Result:

Works as expected.

Bug 3 – bug3_runtime_exception.py
Prompt:

"This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?"

AI Diagnosis:

KeyError: Accessing user['score'] directly assumes every dictionary contains the 'score' key.

ZeroDivisionError: If user_data is empty, count remains 0, leading to division by zero.

Suggested Fix:

Use .get('score', 0) and add a guard clause for empty lists:

Python
def process_user_scores(user_data):
    if not user_data:
        return 0.0

    total_score = 0
    valid_users = 0

    for user in user_data:
        if 'score' in user:
            total_score += user['score']
            valid_users += 1

    return total_score / valid_users if valid_users > 0 else 0.0
Alternative Fixes Tested:

user.get('score', 0) directly in total count calculation.

Result:

Works as expected.

Bug 4 – bug4_logic_error.js
Prompt:

"This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?"

AI Diagnosis:

Wrong Condition: numbers[i] % 2 === 1 checks for odd numbers rather than even numbers.

Variable Overwrite: sum = numbers[i] repeatedly overwrites sum instead of accumulating values via sum += numbers[i].

Suggested Fix:

Update condition to % 2 === 0 and use +=:

JavaScript
function filterAndSumEvens(numbers) {
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        if (numbers[i] % 2 === 0) {
            sum += numbers[i];
        }
    }
    return sum;
}
Alternative Fixes Tested:

numbers.filter(n => n % 2 === 0).reduce((acc, curr) => acc + curr, 0)

Result:

Works as expected.

Bug 5 – bug5_datatype_misuse.cpp
Prompt:

"This code throws an error / doesn't behave as expected. Can you identify and explain the issue and how to fix it?"

AI Diagnosis:

sum is defined as an int, causing sum / scores.size() to perform integer division before assigning the result to double average, truncating fractional parts.

Suggested Fix:

Use double for std::accumulate initial value:

C++
#include <iostream>
#include <vector>
#include <numeric>

double calculateAverage(const std::vector<int>& scores) {
    if (scores.empty()) return 0.0;
    
    double sum = std::accumulate(scores.begin(), scores.end(), 0.0);
    return sum / scores.size();
}
Alternative Fixes Tested:

static_cast<double>(sum) / scores.size()

Result:

Works as expected.
