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



