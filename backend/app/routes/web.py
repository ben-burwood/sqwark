import json

from robyn import Request, Response, Robyn
from sqlalchemy import func, select

from app.database import get_session
from app.models import Feedback, Tag, feedback_tag


def register_web_routes(app: Robyn):
    @app.get("/web/feedback")
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

    @app.get("/web/tags")
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
