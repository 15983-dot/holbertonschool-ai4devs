def get_last_n_items(items, n):
    """
    Returns the last n elements from the provided list.
    Handles edge cases where n exceeds array length or is non-positive.
    """
    if not items or n <= 0:
        return []
    
    start_index = max(0, len(items) - n)
    return items[start_index:]


if __name__ == "__main__":
    # Internal assertions for quick validation
    assert get_last_n_items([10, 20, 30, 40, 50], 3) == [30, 40, 50]
    assert get_last_n_items([10, 20, 30, 40, 50], 5) == [10, 20, 30, 40, 50]
    assert get_last_n_items([10, 20, 30, 40, 50], 10) == [10, 20, 30, 40, 50]
    assert get_last_n_items([10, 20, 30, 40, 50], 0) == []
    print("All tests passed for bug1_fixed.py!")
