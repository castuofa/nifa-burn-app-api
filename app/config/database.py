from typing import Optional, Dict, Any
from pydantic import BaseSettings, AnyUrl, validator


class DatabaseSettings(BaseSettings):
    """
    General Database settings pulled from the env file
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DBNAME: str
    # # This MUST be below previous variables
    POSTGRES_DSN: Optional[AnyUrl] = None

    @validator("POSTGRES_DSN")
    def assemble_postgres_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        """
        Validator for the db connection and sets the constructed
        mongodb url for the client. This lints strangely because the
        decorator requires this to be a @classmethod, but the linter
        expects the self parameter.

        Parameters
        ----------
        v : Optional[str]
            Value to validate
        values : Dict[str, Any]
            Currently stored values within the class properties

        Returns
        -------
        AnyUrl
            The constructed DSN for PostgreSQL
        """

        if isinstance(v, str):
            return v

        return AnyUrl.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASS"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DBNAME') or ''}",
        )

    class Config:
        """
        Defines the location of the .env file
        """

        env_file = ".env"
        env_file_encoding = "utf-8"
