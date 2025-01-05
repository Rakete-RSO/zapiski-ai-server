# zapiski-ai-server

Frontend

## Run locally

1. `.\.venv\Scripts\Activate`
2. `cp frontend/.example.env frontend/.env` (sets base API URL for development)
3. `cd frontend`
4. `streamlit run app.py`

## Local development

1. Start the docker compose in `zapiski-ai-dev-env`
2. Start the auth server on `zapiski-ai-auth` (instructions there). The port of API server must match AUTH_BASE_URL in the .env file.
3. Start the chat server on `zapiski-ai-openai-api` (instructions there). The port of API server must match OPENAI_BASE_URL in the .env file.
