import os

from robyn import Response, Robyn

from app.auth import CookieGetter, SessionAuthHandler
from app.config import PORT
from app.database import init_db
from app.routes.api import register_api_routes
from app.routes.auth import register_auth_routes
from app.routes.web import register_web_routes

app = Robyn(__file__)
app.configure_authentication(SessionAuthHandler(token_getter=CookieGetter()))

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
INDEX_HTML = os.path.join(STATIC_DIR, "index.html")

if os.path.isdir(STATIC_DIR):
    app.serve_directory(
        route="/",
        directory_path=STATIC_DIR,
    )

    if os.path.isfile(INDEX_HTML):
        with open(INDEX_HTML, encoding="utf-8") as fh:
            _index_body = fh.read()

        @app.get("/")
        async def index() -> Response:
            return Response(status_code=200, headers={"content-type": "text/html"}, description=_index_body)


@app.startup_handler
async def startup():
    init_db()


register_api_routes(app)
register_auth_routes(app)
register_web_routes(app)


@app.get("/health", const=True)
async def health():
    return Response(status_code=200, headers={"content-type": "text/plain"}, description="ok")


if __name__ == "__main__":
    app.start(port=PORT, host="0.0.0.0")
