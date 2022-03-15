from pathlib import Path
from pydantic import BaseSettings


class AppSettings(BaseSettings):

    """
    General app and log related settings.
    Imports values directly from the .env file. If no value is
    set by default, the value MUST exist in the env file.
    """

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str = ""

    VERSION: str = "0.1"

    PRODUCTION: bool = False
    # LOG_INFO_CHANNEL: str
    # LOG_INFO_HOOK: str

    JWT_TOKEN_PREFIX = "Token"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

    # Global paths
    LOGS: str = str(Path("./app/logs"))
    STORAGE: str = str(Path("./app/storage"))

    class Config:
        """
        Sets the expected location of the .env file
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
