from __future__ import annotations

import os
import pathlib
import secrets
import warnings
from dataclasses import asdict
from dataclasses import dataclass

from dotenv import load_dotenv
from filelock import FileLock

ENV_PATH = '.env'
ENV_LOCK_PATH = '.env.lock'


@dataclass
class Settings:
    LOGGING_LEVEL: str
    LOGGING_FORMAT: str

    SECRET_KEY: str
    PERMANENT_SESSION_LIFETIME_MINUTES: int

    SQLALCHEMY_DATABASE_URI: str

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}


def init_settings_env():
    env_file_path = pathlib.Path(ENV_PATH)
    if not env_file_path.exists():
        with FileLock(ENV_LOCK_PATH) as lock:
            if not env_file_path.exists():
                with open(ENV_PATH, 'w+') as f:
                    secret_key = secrets.token_hex(16)
                    f.write(f'SECRET_KEY={secret_key}\n')
                    warnings.warn(f'已经生成.env文件')


def load_settings() -> Settings | None:
    if not load_dotenv(ENV_PATH):
        warnings.warn(f'没有找到 {ENV_PATH} ，已使用默认设置。当前工作路径为： {os.getcwd()}')
        init_settings_env()

    return Settings(
        LOGGING_LEVEL=os.environ.get('LOGGING_LEVEL', 'INFO'),
        LOGGING_FORMAT=os.environ.get(
            'LOGGING_FORMAT',
            '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        ),
        SECRET_KEY=os.environ.get('SECRET_KEY', 'mibiao'),
        PERMANENT_SESSION_LIFETIME_MINUTES=int(os.environ.get('PERMANENT_SESSION_LIFETIME_MINUTES', 10)),
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3'),
    )


settings = load_settings()

if __name__ == '__main__':
    print(settings.SQLALCHEMY_DATABASE_URI)
