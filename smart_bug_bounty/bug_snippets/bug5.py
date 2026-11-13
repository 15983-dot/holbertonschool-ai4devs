def remove_expired_tokens(tokens):
    """
    Removes all tokens marked as expired (status == 'expired')
    and returns the active tokens list.
    """
    for token in tokens:
        if token.get("status") == "expired":
            tokens.remove(token)
    return tokens


if __name__ == "__main__":
    session_tokens = [
        {"id": "t1", "status": "expired"},
        {"id": "t2", "status": "expired"},
        {"id": "t3", "status": "active"},
        {"id": "t4", "status": "expired"},
    ]
    print("Active tokens:", remove_expired_tokens(session_tokens))
