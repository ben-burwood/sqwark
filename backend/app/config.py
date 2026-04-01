import os

API_KEY = os.environ.get("SQWARK_API_KEY")
DB_PATH = os.environ.get("SQWARK_DB_PATH", "sqwark.db")
PORT = int(os.environ.get("SQWARK_PORT", "8080"))

if not API_KEY:
    raise RuntimeError("SQWARK_API_KEY environment variable is required")
