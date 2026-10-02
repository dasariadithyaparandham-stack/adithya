# API

- `GET /api/health` checks service availability.
- `POST /api/resume/upload` accepts a PDF or DOCX under 10 MB.
- `POST /api/resume/{resume_id}/skills` extracts and persists normalized skills.
- `GET /api/jobs` lists the seeded job roles and weighted requirements.
- `POST /api/analysis` accepts `{resume_id, job_id}` and returns score, counts, matched/missing skills, priorities, recommendations, roadmap, and category summary.
- `GET /api/analysis/{analysis_id}` returns the same complete analysis contract as POST.
- `GET /api/history` returns persisted analyses ordered newest first.

Interactive OpenAPI documentation is available at `/docs` when the backend is running.
