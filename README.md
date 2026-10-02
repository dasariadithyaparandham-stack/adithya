# AI-Based Resume and Job Skill Gap Analysis System

This project implements a lightweight MVP of the AI-based resume and job skill gap analysis workflow described in the project specification.

## Stack
- Frontend: Next.js + React + TypeScript + Tailwind CSS
- Backend: Python + FastAPI + SQLAlchemy
- Database: SQLite for local development
- Resume parsing: PyMuPDF and python-docx

## Quick start

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000.

## Features
- Resume upload for PDF and DOCX files
- Text extraction and cleaning
- Skill detection and normalization
- Job-role selection
- Match score calculation
- Missing skill detection and priorities
- Personalized recommendations and roadmap
- Analysis history and dashboard

## Notes
This is an MVP implementation focused on explainability and reliability before adding deeper AI features.
