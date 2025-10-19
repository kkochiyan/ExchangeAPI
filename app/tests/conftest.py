import pytest
import asyncio

from httpx import AsyncClient

from app.main import app as fastapi_app
from app.db.database import fake_db
from app.core.security import get_hashed_password

@pytest.fixture(scope='session', autouse=True)
def prepare_db():
    fake_db.clear()

    test_users = [
        {
            "username": "test1",
            "hashed_password": get_hashed_password('test1')
        },
        {
            "username": "test2",
            "hashed_password": get_hashed_password('test2')
        },
        {
            "username": "test3",
            "hashed_password": get_hashed_password('test3')
        }
    ]

    for user in test_users:
        fake_db.append(user)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app ,base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app ,base_url='http://test') as ac:
        await ac.post("users/auth/login", json={
            "email": "test1",
            "password": "test1"
        })

        assert ac.cookies["access_token"]
        yield ac