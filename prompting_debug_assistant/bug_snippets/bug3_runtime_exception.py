def process_user_metrics(data_records):
    """
    Computes ratio of completed tasks to total assigned tasks per user.
    """
    results = {}
    for user_id, metrics in data_records.items():
        total_tasks = metrics.get("total", 0)
        completed_tasks = metrics.get("completed", 0)
        
        # Bug: Raises ZeroDivisionError if total is 0, and fails to handle string inputs
        completion_rate = completed_tasks / total_tasks
        results[user_id] = round(completion_rate * 100, 2)
        
    return results


if __name__ == "__main__":
    users = {
        "user_101": {"completed": 8, "total": 10},
        "user_102": {"completed": 0, "total": 0},
        "user_103": {"completed": "5", "total": 10}
    }
    print("User Metrics:", process_user_metrics(users))
