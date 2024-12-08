# config.py

import os

from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Base URL of the authentication server
API_URL = os.getenv(
    "API_URL", "http://127.0.0.1:8000"
)  # Default to localhost if not setreadme
