import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from database.tables import TUser
from database.db_base import sessionmanager
from database.manager import get_db


@pytest.fixture
def user1():
    """
    create user
        user_id = Column(String, primary_key=True)
    role = Column(String)
    score = Column(Float)
    last_login = Column(DateTime)
    """
    task1 = TUser(user_id="11", role="staff", score=10, last_login=datetime.now())
    yield task1


@pytest.fixture
def db_instance(scope="session"):
    """
    Create a DB Instance
    """
    db = get_db()
    yield db


@pytest.fixture
def session(db_instance, scope="session"):
    """
    Create a Session, close after test session, uses `db_instance` fixture
    """
    session = sessionmanager.session
    yield session
    session.close()


@pytest.fixture
def client():
    from main import app

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
