from todoapp.database import Base
from sqlalchemy import Column, Integer, String, \
    Boolean, ForeignKey, UUID, Numeric


class Todos(Base):
    """
    Todos model for todos table
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class Users(Base):
    """
    User model for users table
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Budgets(Base):
    """
    Budget model for bugets table
    """

    __tablename__ = "budgets"

    id = Column(UUID, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("todos.id"), index=True)
    amount = Column(Numeric(precision=10, scale=2), default=0)
