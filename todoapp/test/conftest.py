from todoapp.test.utils import text, bcrypt_context, \
    TestingSessionLocal, engine
from todoapp.models import Users
import pytest


@pytest.fixture
def test_user():
    user = Users(
        username="testuser",
        first_name="first user",
        last_name="last user",
        hashed_password=bcrypt_context.hash("abc123"),
        email="test@local.email",
        phone_number="1111111",
        role="admin",
        id=1
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user

    with engine.connect() as conn:
        conn.execute(text("DELETE from users;"))
        conn.commit()
