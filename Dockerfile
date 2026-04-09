# Stage 1: Build Frontend
FROM node:latest AS build-frontend

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./

RUN npm ci

COPY frontend/ ./

RUN npm run build

# Stage 2: Build Backend
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS build-backend

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock* ./

RUN uv sync --no-dev --no-install-project

# Stage 3: Runtime
FROM python:3.13-slim-bookworm AS runtime

WORKDIR /app

COPY --from=build-backend /app/.venv /app/.venv
COPY backend/app/ ./app/
COPY --from=build-frontend /app/frontend/dist ./static/

ENV PATH="/app/.venv/bin:$PATH"
ENV DB_PATH=/data/sqwark.db

EXPOSE 8080
VOLUME ["/data"]

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "app.main"]
