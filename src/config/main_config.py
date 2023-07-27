from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_ENGINE: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    APP_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    PUSHER_APP_ID: str
    PUSHER_KEY: str
    PUSHER_SECRET: str
    PUSHER_CLUSTER: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
