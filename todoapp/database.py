from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import env_settings

# For sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Postgresql
POSTGRESQL_DATABASE_URL = env_settings.DB_URL
engine = create_engine(POSTGRESQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
