# Burn Recommendations API

- MVC style service built in Python allowing for a RESTful service with scheduling (via celery)
- built in python with FastAPI + `noaa-sdk`
- NOAA REST API information: https://www.weather.gov/documentation/services-web-api#/

## Running the service


### Docker-compose Approach (recommended on windows)

For this, use the docker-compose file for both development and execution.

```bash
# Copy the given example .env
$ cp .env.example .env
# Edit the necessary variables if needed
$ vim .env
# Daemonize the docker services
$ docker-compose up -d
```

Stopping the service

```bash
$ docker-compose down
```


### Poetry

To install poetry:

```bash
$ pip install --user poetry
```

Install the project dependencies

```bash
$ poetry install
```

Create the `.env` file:

```bash
cp .env.example .env
```

Run the service

```bash
$ poetry run uvicorn main:app
```

Should be able to visit - http://localhost:8000/docs


## Development

This project requires `poetry` to use in development. To start the dev server for hot reloading run

```bash
$ poetry run uvicorn main:app --reload
```


## Running the Scheduler

The scheduled tasks are run using APScheduler and the AsyncIOScheduler class. This scheduler is used to extract, transform, and load (ETL) NOAA data.

In order to register a scheduled task, insert a settings dict in `app/tasks/__init__.py` under `SCHEDULED_TASKS`

Executing the scheduler can be down with docker:

```bash
$ docker build -t burn-api
$ docker run --rm -it --name burn-api burn-api python scheduler.py
```

This will also report INFO level logs to the console.


## Running a Command

There is a CLI interface that allows you to manually run a `REGISTERED_TASK` as needed. These are also defined in `app/tasks/__init__.py`.

Depending on the `Task.signature`, the command can run the task using:

```bash
$ docker build -t burn-api
$ docker run --rm -it --name burn-api burn-api python burn task:run -t "<task.name>"
```

Or in poetry:

```bash
poetry run python burn task:run -t "<task.name>"
```

To list all registered tasks you can run:

```bash
$ docker build -t burn-api
$ docker run --rm -it --name burn-api burn-api python burn task:list
```

Or in poetry:

```bash
poetry run python burn task:list
```


## Interactive Mode

This is provided mostly for development convenience. It allows you to drop into an IPython interface with top-level access to asyncio, an active database connection, and the models already imported

In poetry:

```bash
poetry run python burn tinker
```

In docker:

```bash
$ docker run --rm -it --name burn-api burn-api python burn tinker
```

The name `tinker` is borrowed from a similar command in Laravel's artisan CLI



