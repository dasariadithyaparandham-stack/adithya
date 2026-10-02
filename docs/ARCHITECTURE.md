# Architecture

The system is a Next.js client over a FastAPI REST API. FastAPI owns parsing, controlled skill extraction, matching, scoring, recommendations, and SQLite persistence. The frontend stores only the current analysis id and reloads details from the API.

The matching service combines canonical/alias extraction with exact required-skill matching. `backend/app/services/semantic_matcher.py` is an optional constrained extension: it uses Sentence Transformers when installed and falls back to token similarity without inventing skills outside the seeded taxonomy.

The production boundary is frontend hosting -> FastAPI -> PostgreSQL or SQLite for local development. Uploaded files are parsed into stored text and deleted after extraction failure; resume files should use private object storage in production.
