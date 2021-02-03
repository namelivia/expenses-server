import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from sqlalchemy_utils import database_exists, create_database, drop_database
from alembic.config import Config
from alembic import command

os.environ["TESTING"] = "True"
url = os.environ["TEST_DATABASE_URL"]

engine = create_engine(url, connect_args={"check_same_thread": False})


def get_test_db():
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        command.downgrade(config, "base")
        test_db.close()


@pytest.fixture()
def database_test_session():
    yield from get_test_db()


def _drop_database_safely(url: str):
    if database_exists(url):
        drop_database(url)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    _drop_database_safely(url)
    create_database(url)
    app.dependency_overrides[get_db] = get_test_db
    yield
    _drop_database_safely(url)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
