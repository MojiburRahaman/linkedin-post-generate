# syntax=docker/dockerfile:1.5

FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src /app/src
COPY README.md /app/README.md
COPY entrypoint.sh /app/entrypoint.sh
COPY watch_entrypoint.py /app/watch_entrypoint.py

RUN pip install watchfiles && chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/app/entrypoint.sh"]
