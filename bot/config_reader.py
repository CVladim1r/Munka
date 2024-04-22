from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    DB_CONFIG: dict
    model_config: SettingsConfigDict = SettingsConfigDict (
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
    
config = Settings(
    bot_token="6848117166:AAGxWjBudAQulBcY6lCG1_cdwlArp3r4iKI",
    DB_CONFIG={
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1q1q1q1',
        'database': 'jfdatabase'
    }
)
