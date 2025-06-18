FROM python:3.13-alpine3.22

RUN apk update && apk add --no-cache \
    unixodbc-dev curl gnupg jq \
    && rm -rf /var/cache/apk/*

ENV POETRY_VERSION=2.1.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1\
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY . .

RUN poetry install

EXPOSE 80

CMD ["python", "main.py"]