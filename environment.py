import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)


class _Environment:
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    DB_DATABASE_CONNECTION: str

    def __init__(self):
        self.MAIL_SERVER = os.getenv('MAIL_SERVER')
        self.MAIL_PORT = os.getenv('MAIL_PORT')
        self.MAIL_USE_SSL = True
        self.MAIL_USE_TLS = False
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

        self.DB_DATABASE_TYPE = os.getenv("DB_DATABASE_TYPE")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_DATABASE = os.getenv("DB_DATABASE")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_PORT = os.getenv("DB_PORT")

        self.FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


__environment = _Environment()


def get_env():
    return __environment
