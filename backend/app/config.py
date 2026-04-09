import os

PORT = int(os.environ.get("PORT", "8080"))
DB_PATH = os.environ.get("DB_PATH", "sqwark.db")

API_KEY = os.environ.get("SQWARK_API_KEY")
if not API_KEY:
    raise RuntimeError("SQWARK_API_KEY environment variable is required")

SLACK_WEBHOOK_URL = os.environ.get("SQWARK_SLACK_WEBHOOK_URL", "")

DASHBOARD_USER = os.environ.get("DASHBOARD_USER")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD")
if not DASHBOARD_USER or not DASHBOARD_PASSWORD:
    raise RuntimeError("DASHBOARD_USER and DASHBOARD_PASSWORD environment variables are required")
