from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


env_path = Path(".env")

class Settings(BaseSettings):
    NESCAFEBOT_TOKEN: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )

config = Settings()