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


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def load_settings() -> Settings:
    return Settings(
        database_url=get_required_env("DATABASE_URL"),
        database=DatabaseConfig(
            user=get_required_env("USER_NAME_DB"),
            name=get_required_env("NAME_DB"),
            password=get_required_env("USER_PASSWORD_DB"),
            ip=get_required_env("USER_HOST_DB"),
            port=get_required_env("USER_PORT_DB"),
        ),
        cors_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    )
