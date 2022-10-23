import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env = os.environ["APP_CONFIG_FILE"]
        env_file = Path(__file__).parent / f"config/{env}.env"
        case_sensitive = True
