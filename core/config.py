import os
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    name: str
    user: str
    password: str
    ip: str
    port: str


@dataclass(frozen=True)
class Settings:
    database: DatabaseConfig
    cors_origins: list[str]


def load_settings() -> Settings:
    return Settings(
        database=DatabaseConfig(
            name=os.environ.get("USER_NAME_DB"),
            user=os.environ.get("USER_NAME_DB"),
            password=os.environ.get("USER_PASSWORD_DB"),
            ip=os.environ.get("USER_HOST_DB"),
            port=os.environ.get("USER_PORT_DB"),
        ),
        cors_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    )