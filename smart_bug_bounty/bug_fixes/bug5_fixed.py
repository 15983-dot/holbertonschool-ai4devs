def remove_expired_tokens(tokens):
    """
    Removes all tokens marked as expired (status == 'expired')
    and returns the active tokens list.
    """
    return [token for token in tokens if token.get("status") != "expired"]


if __name__ == "__main__":
    session_tokens = [
        {"id": "t1", "status": "expired"},
        {"id": "t2", "status": "expired"},
        {"id": "t3", "status": "active"},
        {"id": "t4", "status": "expired"},
    ]
    result = remove_expired_tokens(session_tokens)
    assert result == [{"id": "t3", "status": "active"}]
    print("Active tokens:", result)
