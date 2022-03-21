import asyncio
from app import tasks
from app.commands.base import BaseCommand


class RunTask(BaseCommand):

    """
    A simple command to force run all of the scheduled tasks. This is
    useful for when the task scheduler stalls or fails for some reason
    """

    name: str = "Run a scheduled task immediately"

    command: str = "task:run"

    """
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
    arguments = [
        {
            "argument": "-t",
            "properties": {
                "type": str,
                "required": True,
                "dest": "task_name"
            }
        }
    ]

    available_tasks = tasks.REGISTERED_TASKS + tasks.SCHEDULED_TASKS

    def handle(self):

        if self.args.task_name == "all":

            for task in self.available_tasks:
                task_instance = task[-1]["task"]()
                asyncio.run(task_instance.handle())

        else:
            task = list(
                filter(
                    lambda task: task["task"].signature == self.args.task_name,
                    self.available_tasks
                )
            )

            if task:
                task_instance = task[-1]["task"]()
                asyncio.run(task_instance.handle())
            else:
                print(
                    f"Task signature {self.args.task_name} does not exist or is not enabled")


class ListTask(BaseCommand):

    """
    A simple command to list all available tasks
    """

    name: str = "List all tasks"

    command: str = "task:list"

    available_tasks = tasks.REGISTERED_TASKS

    def handle(self):
        for task in self.available_tasks:
            print(f"{task['task'].name} | {task['task'].description}")

