from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import env_settings

# For sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Postgresql
POSTGRESQL_DATABASE_URL = f"postgresql+psycopg2://{env_settings.DB_USER}:{env_settings.DB_PASSWORD}@{env_settings.DB_HOST}:{env_settings.DB_PORT}/{env_settings.DB_NAME}?sslmode=require"
engine = create_engine(POSTGRESQL_DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
