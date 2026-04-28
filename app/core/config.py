import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.environ["SECRET_KEY"]
ALGORITHM: str = os.environ["ALGORITHM"]
DATABASE_URL: str = os.environ["DATABASE_URL"]

if not SECRET_KEY or not ALGORITHM or not DATABASE_URL:
    raise RuntimeError("Missing env vars")