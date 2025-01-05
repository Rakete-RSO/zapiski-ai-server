# config.py

import os

from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Base URL of the authentication server
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "")
if not AUTH_BASE_URL:
    raise ValueError("AUTH_BASE_URL is not set")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
if not OPENAI_BASE_URL:
    raise ValueError("OPENAI_BASE_URL is not set")

CHAT_BASE_URL = os.getenv("CHAT_BASE_URL", "")
if not CHAT_BASE_URL:
    raise ValueError("CHAT_BASE_URL is not set")

DOCUMENT_BASE_URL = os.getenv("DOCUMENT_BASE_URL", "")
if not DOCUMENT_BASE_URL:
    raise ValueError("DOCUMENT_BASE_URL is not set")

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"
