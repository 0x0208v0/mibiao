import os
import warnings
from dataclasses import asdict
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    LOGGING_LEVEL: str
    LOGGING_FORMAT: str

    SECRET_KEY: str
    PERMANENT_SESSION_LIFETIME_MINUTES: int

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ECHO: bool

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}


def load_config(env: str = '.env') -> Config | None:
    if not load_dotenv(env):
        warnings.warn(
            f'{env} not found, using default config, current working directory: {os.getcwd()}'
        )

    return Config(
        LOGGING_LEVEL=os.environ.get('LOGGING_LEVEL', 'INFO'),
        LOGGING_FORMAT=os.environ.get(
            'LOGGING_FORMAT',
            '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        ),
        SECRET_KEY=os.environ.get('SECRET_KEY', 'mibiao'),
        PERMANENT_SESSION_LIFETIME_MINUTES=int(
            os.environ.get('PERMANENT_SESSION_LIFETIME_MINUTES', 10)
        ),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3'
        ),
        SQLALCHEMY_ECHO=os.environ.get('SQLALCHEMY_ECHO', False),
    )


config = load_config()

if __name__ == '__main__':
    print(config.SQLALCHEMY_DATABASE_URI)
