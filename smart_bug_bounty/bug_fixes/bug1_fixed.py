def get_last_n_items(items, n, cache=None):
    """
    Returns the last n items of a list and caches the result safely.
    """
    if cache is None:
        cache = []

    if not items or n <= 0:
        return []

    start_index = max(0, len(items) - n)
    result = items[start_index:]
    cache.append(result)
    return result


if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50]
    assert get_last_n_items(numbers, 3) == [30, 40, 50]
    assert get_last_n_items(numbers, 2) == [40, 50]
    assert get_last_n_items(numbers, 0) == []
    print("Last 3:", get_last_n_items(numbers, 3))
    print("Last 2:", get_last_n_items(numbers, 2))
