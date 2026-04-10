# Sqwark

Super Simple Feedback aggregator with an API for submitting feedback and a dashboard for viewing it.

## Stack

- **Backend**: Robyn + SQLAlchemy (SQLite)
- **Frontend**: Vue + Tailwind CSS + daisyUI

## Quick Start

```bash
docker compose up --build
```

Dashboard available at `http://localhost:8080`. Set your API key in `.env` (see `.env.example`).

## Local Development

```bash
# Backend
cd backend
SQWARK_API_KEY=dev uv run python -m app.main

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

The Vite dev server on `:5173` proxies `/api` and `/web` to the backend on `:8080`.

## Environment Variables

| Variable         | Required | Default      | Description          |
|------------------|----------|--------------|----------------------|
| `SQWARK_API_KEY` | Yes      | —            | API key for POST     |
| `DB_PATH` | No       | `sqwark.db`  | SQLite database path |
| `PORT`    | No       | `8080`       | Server port          |

## API

### POST /api/feedback

Submit feedback. Requires `X-API-Key` header.

**curl:**

```bash
curl -X POST http://localhost:8080/api/feedback \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"text": "The onboarding flow is confusing", "tags": ["ux", "onboarding"]}'
```

**Python (httpx):**

```python
import httpx

response = httpx.post(
    "http://localhost:8080/api/feedback",
    headers={"X-API-Key": "your-api-key"},
    json={
        "text": "The onboarding flow is confusing",
        "tags": ["ux", "onboarding"],
    },
)
print(response.json())
```
