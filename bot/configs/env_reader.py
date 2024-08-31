from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


bot_path = Path(__file__).resolve().parent.parent.parent

env_path = bot_path / ".env"


class Settings(BaseSettings):
    REDIS_PASSWORD: SecretStr
    NESCAFEBOT_TOKEN: SecretStr
    REDIS_ABSOLUTE_PATH: SecretStr
    MONGODB_USERNAME: SecretStr
    MONGODB_PASSWORD: SecretStr

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )
    


config = Settings()
