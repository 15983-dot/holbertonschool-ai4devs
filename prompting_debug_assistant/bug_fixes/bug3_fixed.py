def process_user_metrics(data_records):
    """
    Computes ratio of completed tasks to total assigned tasks per user.
    Handles zero denominators and string input types safely.
    """
    results = {}
    for user_id, metrics in data_records.items():
        try:
            total_tasks = float(metrics.get("total", 0))
            completed_tasks = float(metrics.get("completed", 0))
        except (ValueError, TypeError):
            results[user_id] = 0.0
            continue

        if total_tasks <= 0:
            results[user_id] = 0.0
        else:
            completion_rate = completed_tasks / total_tasks
            results[user_id] = round(completion_rate * 100, 2)
            
    return results


if __name__ == "__main__":
    test_users = {
        "user_101": {"completed": 8, "total": 10},
        "user_102": {"completed": 0, "total": 0},
        "user_103": {"completed": "5", "total": 10},
        "user_104": {"completed": "invalid", "total": 10}
    }
    output = process_user_metrics(test_users)
    assert output["user_101"] == 80.0
    assert output["user_102"] == 0.0
    assert output["user_103"] == 50.0
    assert output["user_104"] == 0.0
    print("All tests passed for bug3_fixed.py!")
