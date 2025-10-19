import pytest

from httpx import AsyncClient

@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ('kotopes', 'kotopes_pass', 200),
        ('kotopes', 'kot0pes_pass', 409),
        ('pesokot', 'pesocot_pass', 200),
        (10, 'pass', 422)
    ]
)
async def test_register(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/users/auth/register", json={
        "username": username,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ('test1', 'test1', 200),
        ('test2', 'test2', 200),
        ('test10', 'test10', 401)
    ]
)
async def test_login(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/users/auth/login", json={
        "username": username,
        "password": password
    })

    assert response.status_code == status_code