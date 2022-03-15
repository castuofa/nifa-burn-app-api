from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.config import Config
from app.tasks.noaa_scraper import NOAA_Grid


CONFIG = Config()


REGISTERED_TASKS = [
    {
        'task': NOAA_Grid,
        'settings': {
            'trigger': 'interval',
            'hours': 6
        }
    }
]

TASK_STORE = {
    'default': SQLAlchemyJobStore(url=CONFIG.database.POSTGRES_DSN)
}

SCHEDULER = AsyncIOScheduler(
    jobstores=TASK_STORE
)

def start():
    for task in REGISTERED_TASKS:

        name = task['settings']['id'] = task['task'].name

        active = SCHEDULER.get_job(name)
        if not active:
            SCHEDULER.add_job(task.get("task").handle, **task.get('settings'))

    SCHEDULER.start()
    return SCHEDULER
