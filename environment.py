import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(verbose=True)


class _Environment:
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    DB_DATABASE_URI: str

    def __init__(self):
        self.MAIL_SERVER = os.getenv('MAIL_SERVER')
        self.MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
        self.MAIL_USE_SSL = False
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
        self.MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

        # SQLite: DB_DATABASE_TYPE=sqlite, DB_DATABASE=file name (relative to the project root)
        db_type = os.getenv("DB_DATABASE_TYPE", "sqlite")
        db_name = os.getenv("DB_DATABASE", "flaskblog.db")
        if db_type == "sqlite":
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
            self.DB_DATABASE_URI = f"sqlite:///{db_path}"
        else:
            self.DB_DATABASE_URI = (
                f"{db_type}://{os.getenv('DB_USER')}"
                f":{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}"
                f":{os.getenv('DB_PORT')}/{db_name}"
            )

        self.FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


__environment = _Environment()


def get_env():
    return __environment
