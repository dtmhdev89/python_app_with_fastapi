from pydantic_settings import BaseSettings
import os


class TestSettings(BaseSettings):
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str

    class Config:
        env_file = os.environ.get('TEST_ENV_FILE_PATH')


env_test_settings = TestSettings()
