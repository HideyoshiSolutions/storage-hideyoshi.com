## ------------------------------- Builder Stage ------------------------------ ##
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry==2.2.1

COPY pyproject.toml poetry.lock poetry.toml ./

RUN poetry sync --no-root --without dev


## ------------------------------- Final Stage ------------------------------ ##
FROM python:3.12-slim-bookworm AS production

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY . .

# Set up environment variables for production
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "storage_service"]
