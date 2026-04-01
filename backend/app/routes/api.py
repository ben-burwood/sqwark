import json

from robyn import Request, Response, Robyn

from app.alerts import notify_new_feedback
from app.auth import require_api_key
from app.database import get_session
from app.models import Feedback, Tag


def register_api_routes(app: Robyn):
    @app.post("/api/feedback")
    async def post_feedback(request: Request) -> Response:
        auth_error = require_api_key(request)
        if auth_error:
            return auth_error

        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return Response(
                status_code=400,
                headers={"content-type": "application/json"},
                description='{"error": "Invalid JSON body"}',
            )

        text = body.get("text", "").strip()
        if not text:
            return Response(
                status_code=400,
                headers={"content-type": "application/json"},
                description='{"error": "text is required and must be non-empty"}',
            )

        raw_tags = body.get("tags", [])
        if not isinstance(raw_tags, list):
            return Response(
                status_code=400,
                headers={"content-type": "application/json"},
                description='{"error": "tags must be a list of strings"}',
            )

        tag_names = list({t.strip().lower() for t in raw_tags if isinstance(t, str) and t.strip()})

        with get_session() as session:
            feedback = Feedback(text=text)

            for name in tag_names:
                tag = session.query(Tag).filter(Tag.name == name).first()
                if not tag:
                    tag = Tag(name=name)
                    session.add(tag)
                    session.flush()
                feedback.tags.append(tag)

            session.add(feedback)
            session.commit()
            session.refresh(feedback)

        notify_new_feedback(feedback)

        return Response(
            status_code=201,
            headers={"content-type": "application/json"},
            description=json.dumps(feedback.to_dict()),
        )
