# Software Requirements Summary

The application accepts PDF/DOCX resumes, extracts controlled skills, lets a user select a seeded role, computes exact and weighted compatibility, identifies categorized gaps, generates gap-based recommendations and a learning roadmap, and persists analysis history.

Security requirements include extension and byte validation, a 10 MB upload limit, private file handling, environment-based secrets, ORM queries, and restrictive production CORS. Known limitations are authentication, OCR for image-only PDFs, production migrations, and external job ingestion.
