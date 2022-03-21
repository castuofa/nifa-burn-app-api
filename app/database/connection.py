import databases
import sqlalchemy


from app.config.database import DatabaseSettings

# Initialize and validate database configuration
database_config = DatabaseSettings()

# Init the database connection to PostGRES
database = databases.Database(str(database_config.POSTGRES_DSN))

metadata = sqlalchemy.MetaData()


class BaseMeta:
    """Base Metadata class to be defined for ormar based models

    Example
    -------
    ```
    class Meta(BaseMeta):
        pass
    ```
    """

    database = database
    metadata = metadata
