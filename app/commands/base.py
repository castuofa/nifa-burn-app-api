import app
# from app.database.base import Connection

from argparse import ArgumentParser, Namespace
from pydantic import BaseModel


class Arguments(BaseModel):
    # input_directory: pydantic.DirectoryPath
    pass


class BaseCommand:

    name: str = "Base Command"

    command: str = "snake_case_command"

    validator: BaseModel = Arguments

    # db: Connection = Connection

    name = "Command Name"

    """
    Set required arguments

    Example
    -------
    [
        {
            "argument": "-i",
            "properties": {
                "type": str,
                "required": True,
                "dest": "input_directory"
            }
        }
    ]

    """
    arguments = []
    # Define the arguments to catch their values explicitly

    # input_directory: str = None

    def __init__(self, parser: ArgumentParser, logger=None):
        self.args = self.parse_arguments(
            parser) if parser else None

        self.log = logger or app.Log
        self.log.info(f"Starting command: {self.__class__.name}")

    def handle(self):
        raise NotImplementedError(
            "Start command should not be called directly on BaseCommand"
        )

    def parse_arguments(self, parser: ArgumentParser) -> Arguments:
        for argument in self.arguments:
            parser.add_argument(
                argument.get('argument'),
                **argument.get('properties')
            )

        args = parser.parse_args()

        self.validate_arguments(args)

        for k, v in args.__dict__.items():

            attr = hasattr(self, k)
            if attr:
                setattr(self, k, v)

        return args

    def validate_arguments(self, args: Namespace):
        return self.validator(**args.__dict__)
