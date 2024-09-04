from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BOT_DIR = Path(__file__).resolve().parent.parent.parent

TEMP_DIR = BOT_DIR / "data" / "temporary"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

env_path = BOT_DIR / ".env"


class Settings(BaseSettings):
    NESCAFEBOT_TOKEN: SecretStr
    MONGODB_USERNAME: SecretStr
    MONGODB_PASSWORD: SecretStr
    MONGODB_ABSOLUTE_PATH: SecretStr
    EMAIL_PASSWORD: SecretStr

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )


config = Settings()
