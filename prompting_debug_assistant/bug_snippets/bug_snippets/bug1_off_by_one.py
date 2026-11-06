def get_last_n_items(items, n):
    """
    Intended Behavior: Return the last n items of a list.
    Issue: Off-by-one error (slice index excludes boundary item).
    """
    if n <= 0:
        return []
    start_index = len(items) - n + 1
    return items[start_index:]

numbers = [10, 20, 30, 40, 50]
print("Last 3 items:", get_last_n_items(numbers, 3))
