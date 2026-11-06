def get_last_n_items(items, n):
    """
    Returns the last n elements from the provided list.
    """
    if not items or n <= 0:
        return []
    
    start_index = len(items) - n + 1  # Bug: off-by-one slicing offset
    return items[start_index:]


if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50]
    print("Last 3 items:", get_last_n_items(numbers, 3))
    print("All items:", get_last_n_items(numbers, 5))
