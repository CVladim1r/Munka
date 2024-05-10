import os
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    bot_token: str
    DB_CONFIG: dict

    model_config = SettingsConfigDict(env_file=DOTENV)