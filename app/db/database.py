fake_db = []

def find_one_or_none(username: str) -> dict | None:
    for user in fake_db:
        if user['username'] == username:
            return user
    return None

def add(username: str, hashed_password: str) -> None:
    fake_db.append(
        {
            'username': username,
            'hashed_password': hashed_password
        }
    )


