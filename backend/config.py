
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGO")
ACCESS_TTL= int(30 if os.getenv("ACCESS_TTL") is None else os.getenv("ACCESS_TTL"))
