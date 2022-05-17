# pull official base image
FROM python:3.10-slim

ENV TZ=America/Chicago

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# copy project
COPY . .
