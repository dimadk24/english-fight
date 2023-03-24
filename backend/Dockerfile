FROM python:3.11.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    # pip
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1\
    # poetry
    POETRY_VERSION=1.3.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # Because of the https://chanind.github.io/2021/09/27/cloud-run-home-env-change.html need to set config dir
    # Otherwise during run poetry ignores config set during build
    POETRY_CONFIG_DIR="/home/.config/pypoetry" \
    POETRY_HOME="/usr/local/pypoetry"

# For mysqlclient
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential -y

RUN python3 -m pip install --user pipx

RUN pipx install poetry==$POETRY_VERSION

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --only=main --no-root --no-interaction --no-ansi

COPY . /app

ENV PORT="8080"

EXPOSE $PORT

CMD poetry run python manage.py collectstatic --noinput && \
    poetry run python manage.py migrate --noinput && \
    poetry run daphne -b 0.0.0.0 -p $PORT enfight.asgi:application
