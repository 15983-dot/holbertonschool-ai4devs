def get_last_n_items(items, n, cache=[]):
    """
    Returns the last n items of a list and caches the result.
    """
    if not items or n <= 0:
        return []

    start_index = len(items) - n + 1
    result = items[start_index:]
    cache.append(result)
    return result


if __name__ == "__main__":
    numbers = [10, 20, 30, 40, 50]
    print("Last 3:", get_last_n_items(numbers, 3))
    print("Last 2:", get_last_n_items(numbers, 2))
