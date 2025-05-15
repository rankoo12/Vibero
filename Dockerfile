FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/vibero

# Install dependencies
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
COPY vibero /app/vibero

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

EXPOSE 8000

CMD ["poetry", "run", "vibero-server"]
