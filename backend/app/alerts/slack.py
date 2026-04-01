from slack_sdk.webhook import WebhookClient

from app.config import SLACK_WEBHOOK_URL
from app.models import Feedback


def notify_new_feedback(feedback: Feedback) -> None:
    """Send a Slack notification for new feedback. No-op if webhook URL is not configured."""
    if not SLACK_WEBHOOK_URL:
        return

    tags = ", ".join(t.name for t in feedback.tags)
    msg = f"*New feedback*\n{feedback.text}"
    if tags:
        msg += f"\n_Tags: {tags}_"

    try:
        client = WebhookClient(SLACK_WEBHOOK_URL)
        client.send(text=msg)
    except Exception:
        pass
