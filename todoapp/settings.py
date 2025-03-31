from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str

    class Config:
        env_file = ".env"


env_settings = Settings()
