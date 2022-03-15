import pathlib
import logging
from .config import Config


CONFIG = Config()


def storage(sub_path: str = None) -> pathlib.PosixPath:
    """
    Construct a valid Path to persisted storage pulled from the
    .env Config object
    """
    base_path = f"{CONFIG.app.STORAGE}"

    base_path += f"/{sub_path}" if sub_path else base_path

    return pathlib.Path(base_path)


storage("logs").mkdir(775, exist_ok=True)


# Create and configure logger
logging.basicConfig(
    filename=str(storage("logs/backend.log")),
    format="%(asctime)s %(message)s",
    filemode="w",
)

# Creating an object
Log = logging.getLogger("backend")

# Setting the threshold of logger to DEBUG
Log.setLevel(logging.DEBUG)
