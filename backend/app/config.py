import os

PORT = int(os.environ.get("SQWARK_PORT", "8080"))
DB_PATH = os.environ.get("SQWARK_DB_PATH", "sqwark.db")

API_KEY = os.environ.get("SQWARK_API_KEY")
if not API_KEY:
    raise RuntimeError("SQWARK_API_KEY environment variable is required")

DASHBOARD_USER = os.environ.get("SQWARK_DASHBOARD_USER")
DASHBOARD_PASSWORD = os.environ.get("SQWARK_DASHBOARD_PASSWORD")
if not DASHBOARD_USER or not DASHBOARD_PASSWORD:
    raise RuntimeError("SQWARK_DASHBOARD_USER and SQWARK_DASHBOARD_PASSWORD environment variables are required")
