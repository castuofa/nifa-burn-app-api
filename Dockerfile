# pull official base image
FROM python:3.10-slim

ENV TZ=America/Chicago

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry install

# copy project
COPY . .

ENTRYPOINT [ "poetry", "run" ]
