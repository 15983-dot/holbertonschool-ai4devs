def process_user_scores(user_data):
    """
    Intended Behavior: Extract score values from user list and compute average.
    Issue Type: Runtime Exception (KeyError & ZeroDivisionError).
    """
    total_score = 0
    count = 0

    for user in user_data:
        total_score += user['score']
        count += 1

    average = total_score / count
    return average

users = [{"name": "Alice"}, {"name": "Bob", "score": 85}]
print("Average Score:", process_user_scores(users))
