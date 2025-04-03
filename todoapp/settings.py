from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str

    class Config:
        env_file = os.environ.get('ENV_FILE_PATH')


env_settings = Settings()
