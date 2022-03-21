from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.config import Config
from app.tasks.noaa_scraper import NOAA_ForecastCollector, NOAA_Grid, NOAA_GridUpdater
from app import Log


CONFIG = Config()


REGISTERED_TASKS = [
    {
        'task': NOAA_Grid
    },
    {
        'task': NOAA_GridUpdater
    }
]


SCHEDULED_TASKS = [
    {
        'task': NOAA_ForecastCollector,
        'settings': {
            'trigger': 'interval',
            'minutes': 1
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

    TASK_STORE['default'].remove_all_jobs()
    SCHEDULER.remove_all_jobs()

    for task in SCHEDULED_TASKS:

        signature = task['settings']['id'] = task['task'].signature

        active = SCHEDULER.get_job(signature)

        if not active:
            try:
                SCHEDULER.add_job(task.get("task").runner, **task.get('settings'))
            except Exception as exc:
                Log.error(exc)

    SCHEDULER.start()
    return SCHEDULER
