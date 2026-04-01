import csv
import io
import json

from robyn import Request, Response, Robyn
from sqlalchemy import func, select

from app.auth import create_session, delete_session
from app.config import DASHBOARD_PASSWORD, DASHBOARD_USER
from app.database import get_session
from app.models import Feedback, Tag, feedback_tag


def register_web_routes(app: Robyn):
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

    @app.get("/web/feedback", auth_required=True)
    async def list_feedback(request: Request) -> Response:
        params = request.query_params

        search = params.get("search", "").strip()
        sort = params.get("sort", "newest")
        tag_filter = params.get("tag", "")

        try:
            limit = int(params.get("limit", "100"))
            offset = int(params.get("offset", "0"))
        except ValueError:
            limit, offset = 100, 0

        limit = min(max(limit, 1), 500)
        offset = max(offset, 0)

        with get_session() as session:
            query = select(Feedback)

            if search:
                query = query.where(Feedback.text.ilike(f"%{search}%"))

            if tag_filter:
                tag_names = [t.strip().lower() for t in tag_filter.split(",") if t.strip()]
                if tag_names:
                    query = query.where(
                        Feedback.id.in_(
                            select(feedback_tag.c.feedback_id)
                            .join(Tag, Tag.id == feedback_tag.c.tag_id)
                            .where(Tag.name.in_(tag_names))
                            .group_by(feedback_tag.c.feedback_id)
                            .having(func.count() == len(tag_names))
                        )
                    )

            # Count total before pagination
            count_query = select(func.count()).select_from(query.subquery())
            total = session.execute(count_query).scalar() or 0

            if sort == "oldest":
                query = query.order_by(Feedback.created_at.asc())
            else:
                query = query.order_by(Feedback.created_at.desc())

            query = query.limit(limit).offset(offset)
            items = session.execute(query).scalars().all()

            result = {
                "items": [f.to_dict() for f in items],
                "total": total,
            }

        return Response(
            status_code=200,
            headers={"content-type": "application/json"},
            description=json.dumps(result),
        )

    @app.get("/web/feedback/export", auth_required=True)
    async def export_feedback(request: Request) -> Response:
        with get_session() as session:
            items = session.execute(select(Feedback).order_by(Feedback.created_at.desc())).scalars().all()

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["id", "text", "tags", "created_at"])
            for f in items:
                writer.writerow([f.id, f.text, ";".join(t.name for t in f.tags), f.created_at.isoformat()])

        return Response(
            status_code=200,
            headers={
                "content-type": "text/csv",
                "content-disposition": "attachment; filename=sqwark-feedback.csv",
            },
            description=output.getvalue(),
        )

    @app.get("/web/tags", auth_required=True)
    async def list_tags(request: Request) -> Response:
        with get_session() as session:
            rows = session.execute(
                select(Tag.name, func.count(feedback_tag.c.feedback_id).label("count"))
                .join(feedback_tag, Tag.id == feedback_tag.c.tag_id)
                .group_by(Tag.id)
                .order_by(func.count(feedback_tag.c.feedback_id).desc())
            ).all()

            result = {"tags": [{"name": name, "count": count} for name, count in rows]}

        return Response(
            status_code=200,
            headers={"content-type": "application/json"},
            description=json.dumps(result),
        )
