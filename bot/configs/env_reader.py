from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


bot_path = Path(__file__).resolve().parent.parent

env_path = bot_path.parent / ".env"


class Settings(BaseSettings):
    NESCAFEBOT_TOKEN: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )


config = Settings()
