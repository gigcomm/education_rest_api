import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    user: str
    name: str
    password: str
    ip: str
    port: str


@dataclass(frozen=True)
class Settings:
    database_url: str
    database: DatabaseConfig
    cors_origins: list[str]


def load_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("DATABASE_URL"),
        database=DatabaseConfig(
            user=os.environ.get("USER_NAME_DB"),
            name=os.environ.get("NAME_DB"),
            password=os.environ.get("USER_PASSWORD_DB"),
            ip=os.environ.get("USER_HOST_DB"),
            port=os.environ.get("USER_PORT_DB"),
        ),
        cors_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    )