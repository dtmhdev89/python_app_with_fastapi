from todoapp.main import app
from todoapp.database import Base
from todoapp.test import env_test_settings
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from todoapp.models import Todos, Users
from todoapp.routers.auth import bcrypt_context
import pytest



SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{env_test_settings.TEST_DB_USER}:{env_test_settings.TEST_DB_PASSWORD}@{env_test_settings.TEST_DB_HOST}:{env_test_settings.TEST_DB_PORT}/{env_test_settings.TEST_DB_NAME}?sslmode=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool
)

try:
    with engine.connect() as connection:
        print("Connection Test database successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        "username": "test user",
        "id": 1,
        "user_role": "admin"
    }


client = TestClient(app)


@pytest.fixture
def test_todo(test_user):
    todo = Todos(
        title="Learn to code",
        description="desc",
        priority=5,
        complete=False,
        owner_id=test_user.id,
        id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as conn:
        conn.execute(text("DELETE from todos;"))
        conn.commit()

