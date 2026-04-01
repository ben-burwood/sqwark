from robyn import Request, Response

from app.config import API_KEY


def require_api_key(request: Request) -> Response | None:
    """Check X-API-Key Header. Returns an error Response if invalid, None if OK."""
    key = request.headers.get("x-api-key", "")
    if key != API_KEY:
        return Response(
            status_code=401,
            headers={"content-type": "application/json"},
            description='{"error": "Invalid or missing API key"}',
        )
    return None
