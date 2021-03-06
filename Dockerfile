FROM python:3.9-alpine
LABEL org.opencontainers.image.authors="rochette.jonathan@gmail.com"

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.11

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev postgresql-client jpeg-dev musl-dev zlib zlib-dev

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D recipebookapp
RUN chown -R recipebookapp:recipebookapp /vol/
RUN chmod -R 755 /vol/web
USER recipebookapp