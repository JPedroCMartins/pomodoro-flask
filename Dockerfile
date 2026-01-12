FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8004

CMD ["uv", "run", "gunicorn", "--workers", "3", "--bind", "0.0.0.0:8004", "main:app"]