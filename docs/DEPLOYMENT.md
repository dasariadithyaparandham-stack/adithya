# Deployment

For local development, start FastAPI from `backend` with `python -m uvicorn app.main:app --reload --port 8000` and Next.js from `frontend` with `npm run dev`.

For containers, run `docker compose up --build`. Set `DATABASE_URL`, `CORS_ORIGINS`, and `SECRET_KEY` through the deployment environment. Set `NEXT_PUBLIC_API_URL` to the public API origin. Replace local SQLite with managed PostgreSQL, add migrations, private object storage, HTTPS, restrictive CORS, and centralized logs before production use.
