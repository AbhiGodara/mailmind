FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Assuming pyproject.toml exists from uv init
COPY pyproject.toml .
# Fallback installation of packages in case pyproject is not perfectly synced
RUN uv pip install --system fastapi uvicorn celery redis sqlalchemy psycopg2-binary twilio crewai langgraph langchain langchain-core langchain-community python-dotenv google-search-results google-api-python-client google-auth-oauthlib google-auth-httplib2 beautifulsoup4 tavily-python

COPY . .

# Set PYTHONPATH to make root modules discoverable
ENV PYTHONPATH=/app
