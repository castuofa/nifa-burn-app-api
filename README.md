# Burn Recommendations API

- MVC style service built in Python allowing for a RESTful service with scheduling (via celery)
- built in python with FastAPI + `noaa-sdk`

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

### Poetry

To install poetry:

```bash
$ pip install --user poetry
```


## Development

This project requires `poetry` to use in development. To start the dev server for hot reloading run

```bash
$ poetry run uvicorn main:app --reload
```



