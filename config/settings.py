from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv
from pathlib import Path
from typing import Union

BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)

load_dotenv(dotenv_path=Path(BASE_DIR, ".env"), override=True)

class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    port_redis: int = 6379


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class RedisConfig(BaseModel):
    host: str
    port: int 
    password: str
    ssl: bool = True

class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class BotConfig(BaseModel):
    token: str
    path: str
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="_",
        env_prefix="SET_",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    bot: BotConfig
    redis: RedisConfig


settings = Settings()
