# config.py

import os

from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Base URL of the authentication server
AUTH_BASE_URL = os.getenv(
    "AUTH_BASE_URL", "http://127.0.0.1:8000"
)  # Default to localhost if not setreadme

CHAT_BASE_URL = os.getenv("CHAT_BASE_URL", "http://127.0.0.1:8001")

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"
