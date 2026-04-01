# Stage 1: Build frontend
FROM node:latest AS build-frontend

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./

RUN npm ci

COPY frontend/ ./

RUN npm run build

# Stage 2: Runtime
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS runtime

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock* ./

RUN uv sync --no-dev --no-install-project

COPY backend/app/ ./app/
COPY --from=build-frontend /app/frontend/dist ./static/

ENV SQWARK_DB_PATH=/data/sqwark.db

EXPOSE 8080
VOLUME ["/data"]

CMD ["/app/.venv/bin/python", "-m", "app.main"]
