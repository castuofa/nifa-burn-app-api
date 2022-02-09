from app.config.database import DatabaseSettings
from app.config.app import AppSettings


class Config:
    """
    Config to be used throughout the app.

    Properties
        database: DatabaseSettings
        app: AppSettings

    Example
        from app import config
        CONFIG = config.get()
    """

    database: DatabaseSettings

    app: AppSettings

    def __init__(self):
        self.database = DatabaseSettings()
        self.app = AppSettings()
