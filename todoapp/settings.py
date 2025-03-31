from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str

    class Config:
        env_file = ".env"


env_settings = Settings()
