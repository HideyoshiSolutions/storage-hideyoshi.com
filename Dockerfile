FROM python:3.12-slim-bookworm AS base


FROM base AS dependencies


RUN apt-get update && \
    apt-get install -y build-essential curl && \
    rm -rf /var/lib/apt/lists/*


ENV POETRY_NO_INTERACTION=1
ENV POETRY_VERSION=2.2.1


# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"


WORKDIR /app

COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry sync --without=dev --no-root --no-interaction --no-ansi


FROM base AS runtime

WORKDIR /app

COPY --from=dependencies /app/.venv ./

COPY . .

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/.venv

ENTRYPOINT ["python", "-m", "storage_service"]
