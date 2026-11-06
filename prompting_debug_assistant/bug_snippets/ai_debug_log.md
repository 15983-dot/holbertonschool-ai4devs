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
