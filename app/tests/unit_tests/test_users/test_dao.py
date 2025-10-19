import pytest

from app.db.database import find_one_or_none, add, fake_db
from app.core.security import get_hashed_password

@pytest.mark.parametrize(
    'username, exists',
    [
        ('test1', True),
        ('test2', True),
        ('test4', False)
    ]
)
def test_find_one_or_none(username, exists):
    user = find_one_or_none(username)

    if exists:
        assert user
        assert user['username'] == username
    else:
        assert not user


@pytest.mark.parametrize(
    'username, hashed_password, length',
    [
        ('test4', get_hashed_password('test4'), 4),
        ('test5', get_hashed_password('test5'), 5)
    ]
)
def test_add(username, hashed_password, length):
    add(username, hashed_password)

    assert len(fake_db) == length