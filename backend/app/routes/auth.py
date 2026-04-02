import json

from robyn import Request, Response, Robyn

from app.auth import create_session, delete_session
from app.config import DASHBOARD_PASSWORD, DASHBOARD_USER


def register_auth_routes(app: Robyn):
    @app.post("/web/login")
    async def login(request: Request) -> Response:
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return Response(
                status_code=400,
                headers={"content-type": "application/json"},
                description='{"error": "Invalid JSON body"}',
            )

        username = body.get("username", "")
        password = body.get("password", "")

        if username != DASHBOARD_USER or password != DASHBOARD_PASSWORD:
            return Response(
                status_code=401,
                headers={"content-type": "application/json"},
                description='{"error": "Invalid credentials"}',
            )

        token = create_session()
        return Response(
            status_code=200,
            headers={
                "content-type": "application/json",
                "set-cookie": f"sqwark_session={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400",
            },
            description='{"ok": true}',
        )

    @app.post("/web/logout")
    async def logout(request: Request) -> Response:
        cookie_header = request.headers.get("cookie") or ""
        for part in cookie_header.split(";"):
            part = part.strip()
            if part.startswith("sqwark_session="):
                delete_session(part.split("=", 1)[1])
                break

        return Response(
            status_code=200,
            headers={
                "content-type": "application/json",
                "set-cookie": "sqwark_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0",
            },
            description='{"ok": true}',
        )
