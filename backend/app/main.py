from __future__ import annotations

import os
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.config import settings
from app.data.company_catalog import COMPANY_CATALOG
from app.data.skill_catalog import JOB_ROLE_SEED, SKILL_CATALOG
from app.database import Base, engine, get_db
from app.models import Analysis, AnalysisSkill, JobRole, JobSkill, Resume, ResumeSkill, Skill, SkillAlias, User
from app.schemas import AnalysisRequest, AnalysisResponse, AuthResponse, HistoryEntry, JobOut, ResumeUploadResponse, UserLogin, UserOut, UserRegister
from app.services.auth import create_access_token, decode_access_token, hash_password, verify_password
from app.services.resume_parser import extract_text_from_file
from app.services.skill_extractor import extract_resume_skills
from app.services.skill_matcher import analyze_resume_against_job

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title='AI Resume Skill Gap Analysis API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(',') if origin.strip()],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
bearer_scheme = HTTPBearer(auto_error=False)


Base.metadata.create_all(bind=engine)


def seed_database(db: Session):
    skill_names = set(SKILL_CATALOG.keys())
    for skill_name in skill_names:
        if not db.query(Skill).filter(Skill.name == skill_name).first():
            meta = SKILL_CATALOG[skill_name]
            db.add(Skill(name=skill_name, category=meta['category'], canonical_name=skill_name))
    db.commit()

    for skill_name, meta in SKILL_CATALOG.items():
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        for alias in set(meta.get('aliases', []) + [skill_name]):
            if not db.query(SkillAlias).filter(SkillAlias.skill_id == skill.id, SkillAlias.alias == alias).first():
                db.add(SkillAlias(skill_id=skill.id, alias=alias))
    db.commit()

    for title, meta in JOB_ROLE_SEED.items():
        role = db.query(JobRole).filter(JobRole.title == title).first()
        if not role:
            role = JobRole(title=title, description=meta['description'])
            db.add(role)
            db.commit()
            db.refresh(role)

        for skill_name, importance in meta['skills'].items():
            skill = db.query(Skill).filter(Skill.name == skill_name).first()
            if skill is None:
                skill = Skill(name=skill_name, category=SKILL_CATALOG.get(skill_name, {}).get('category', 'General'), canonical_name=skill_name)
                db.add(skill)
                db.commit()
                db.refresh(skill)
            if not db.query(JobSkill).filter(JobSkill.job_id == role.id, JobSkill.skill_id == skill.id).first():
                db.add(JobSkill(job_id=role.id, skill_id=skill.id, importance=int(importance)))
    db.commit()


@app.on_event('startup')
def startup_event():
    if 'experience_level' not in {column['name'] for column in inspect(engine).get_columns('users')}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN experience_level VARCHAR(32) NOT NULL DEFAULT 'fresher'"))
    db = next(get_db())
    seed_database(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    user_id = decode_access_token(credentials.credentials) if credentials else None
    user = db.query(User).filter(User.id == user_id).first() if user_id else None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please sign in to continue.')
    return user


def auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(user.id),
        user=UserOut(id=user.id, name=user.name, email=user.email, experience_level=user.experience_level),
    )


@app.post('/api/auth/register', response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if '@' not in email or '.' not in email.rsplit('@', 1)[-1]:
        raise HTTPException(status_code=422, detail='Enter a valid email address.')
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail='An account with this email already exists.')

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        experience_level=payload.experience_level,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return auth_response(user)


@app.post('/api/auth/login', response_model=AuthResponse)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Email or password is incorrect.')
    return auth_response(user)


@app.get('/api/auth/me', response_model=UserOut)
def get_account(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, name=user.name, email=user.email, experience_level=user.experience_level)


@app.get('/api/health')
def health():
    return {'status': 'ok'}


@app.post('/api/resume/upload', response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file selected.')

    ext = Path(file.filename).suffix.lower()
    allowed = {'.pdf', '.docx'}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail='Unsupported format. Please upload a PDF or DOCX resume.')

    file_id = uuid.uuid4().hex
    safe_name = f'{file_id}{ext}'
    save_path = UPLOAD_DIR / safe_name
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File is too large. Please upload a smaller resume.')
    if ext == '.pdf' and not contents.startswith(b'%PDF'):
        raise HTTPException(status_code=400, detail='The uploaded file is not a valid PDF.')
    if ext == '.docx' and not contents.startswith(b'PK'):
        raise HTTPException(status_code=400, detail='The uploaded file is not a valid DOCX.')
    save_path.write_bytes(contents)

    try:
        extracted_text = extract_text_from_file(str(save_path), ext)
    except Exception:
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail='We could not extract enough information from this resume. Please upload a text-based PDF or DOCX resume.')

    if not extracted_text.strip():
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail='The resume is empty or unreadable. Please upload a valid document.')

    resume = Resume(user_id=user.id, filename=file.filename, extracted_text=extracted_text)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeUploadResponse(resume_id=resume.id, filename=resume.filename, extracted_text=resume.extracted_text)


@app.post('/api/resume/{resume_id}/skills')
def extract_resume_skills_route(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail='Resume not found.')

    skills = extract_resume_skills(resume.extracted_text)
    db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume.id).delete()

    for item in skills:
        skill = db.query(Skill).filter(Skill.name == item['name']).first()
        if skill is None:
            skill = Skill(name=item['name'], category=item['category'], canonical_name=item['canonical_name'])
            db.add(skill)
            db.commit()
            db.refresh(skill)
        existing = db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume.id, ResumeSkill.skill_id == skill.id).first()
        if not existing:
            db.add(ResumeSkill(resume_id=resume.id, skill_id=skill.id, confidence=item['confidence']))
    db.commit()

    return {'resume_id': resume.id, 'skills': [skill['name'] for skill in skills]}


@app.get('/api/resume/{resume_id}/companies')
def recommend_companies(resume_id: int, job_id: int | None = Query(default=None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Return illustrative company profile matches based on detected resume skills."""
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail='Resume not found.')

    target_role = None
    if job_id is not None:
        target_role = db.query(JobRole).filter(JobRole.id == job_id).first()
        if not target_role:
            raise HTTPException(status_code=404, detail='Target job role not found.')

    detected = {skill.name.casefold() for skill in resume.resume_skills}
    if not detected:
        detected = {item['name'].casefold() for item in extract_resume_skills(resume.extracted_text)}
    if not detected:
        return {'resume_id': resume.id, 'companies': [], 'message': 'No recognizable skills found in this resume.'}

    matches = []
    for company in COMPANY_CATALOG:
        if target_role and target_role.title not in company['roles']:
            continue
        matched_skills = [skill for skill in company['skills'] if skill.casefold() in detected]
        score = round(len(matched_skills) / len(company['skills']) * 100, 2)
        matches.append({
            'name': company['name'],
            'industry': company['industry'],
            'roles': company['roles'],
            'match_score': score,
            'matched_skills': matched_skills,
        })

    matches.sort(key=lambda company: (-company['match_score'], company['name']))
    return {
        'resume_id': resume.id,
        'job_id': job_id,
        'target_role': target_role.title if target_role else None,
        'companies': matches,
        'message': 'Profile matches based on detected resume skills and target role.',
    }


@app.get('/api/jobs')
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobRole).all()
    result = []
    for job in jobs:
        required_skills = []
        for js in job.job_skills:
            skill = js.skill
            required_skills.append({
                'skill_id': skill.id,
                'name': skill.name,
                'category': skill.category,
                'canonical_name': skill.canonical_name,
                'importance': js.importance,
            })
        result.append({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'required_skills': required_skills,
        })
    return result


@app.get('/api/jobs/{job_id}/skills')
def get_job_skills(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobRole).filter(JobRole.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail='Job role not found.')
    return {
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'required_skills': [{
            'skill_id': js.skill.id,
            'name': js.skill.name,
            'category': js.skill.category,
            'canonical_name': js.skill.canonical_name,
            'importance': js.importance,
        } for js in job.job_skills],
    }


@app.post('/api/analysis', response_model=AnalysisResponse)
def run_analysis(payload: AnalysisRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail='Resume not found.')
    job = db.query(JobRole).filter(JobRole.id == payload.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail='Job role not found.')

    resume_skills = [rs.skill.name for rs in resume.resume_skills]
    if resume_skills:
        skill_names = resume_skills
    else:
        extracted_items = extract_resume_skills(resume.extracted_text)
        skill_names = [item['name'] for item in extracted_items]
        for item in extracted_items:
            skill = db.query(Skill).filter(Skill.name == item['name']).first()
            if skill is not None:
                db.add(ResumeSkill(resume_id=resume.id, skill_id=skill.id, confidence=item['confidence']))
        db.commit()
    if not skill_names:
        raise HTTPException(status_code=400, detail='No detectable skills found in the resume.')

    required_skill_map = {js.skill.name: js.importance for js in job.job_skills}
    categories = {js.skill.name: js.skill.category for js in job.job_skills}
    result = analyze_resume_against_job(skill_names, payload.job_id, {'skills': required_skill_map, 'categories': categories}, user.experience_level, job_title=job.title)

    analysis = Analysis(resume_id=resume.id, job_id=job.id, score=result['score'])
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    for skill_name in result['matched_skills']:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if skill is None:
            continue
        db.add(AnalysisSkill(analysis_id=analysis.id, skill_id=skill.id, status='matched', priority='Normal'))

    for skill_name in result['missing_skills']:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if skill is None:
            continue
        priority = 'High' if skill_name in result['priority_summary'].get('High', []) else 'Medium' if skill_name in result['priority_summary'].get('Medium', []) else 'Low'
        db.add(AnalysisSkill(analysis_id=analysis.id, skill_id=skill.id, status='missing', priority=priority))

    db.commit()

    response = {
        'analysis_id': analysis.id,
        'resume_id': resume.id,
        'job_id': job.id,
        'score': result['score'],
        'matched_skills': result['matched_skills'],
        'missing_skills': result['missing_skills'],
        'priority_summary': result['priority_summary'],
        'recommendations': result['recommendations'],
        'roadmap': result['roadmap'],
        'detected_skills': result['detected_skills'],
        'weighted_score': result['weighted_score'],
        'semantic_score': result['semantic_score'],
        'matched_count': result['matched_count'],
        'required_count': result['required_count'],
        'missing_count': result['missing_count'],
        'category_summary': result['category_summary'],
        'experience_level': user.experience_level,
    }
    return response


@app.get('/api/analysis/{analysis_id}', response_model=AnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    analysis = db.query(Analysis).join(Resume).filter(Analysis.id == analysis_id, Resume.user_id == user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail='Analysis not found.')

    resume_skills = [item.skill.name for item in analysis.resume.resume_skills]
    required_skill_map = {item.skill.name: item.importance for item in analysis.job_role.job_skills}
    categories = {item.skill.name: item.skill.category for item in analysis.job_role.job_skills}
    result = analyze_resume_against_job(resume_skills, analysis.job_id, {'skills': required_skill_map, 'categories': categories}, user.experience_level, job_title=analysis.job_role.title)
    return {
        'analysis_id': analysis.id,
        'resume_id': analysis.resume_id,
        'job_id': analysis.job_id,
        'score': analysis.score,
        'matched_skills': result['matched_skills'],
        'missing_skills': result['missing_skills'],
        'priority_summary': result['priority_summary'],
        'recommendations': result['recommendations'],
        'roadmap': result['roadmap'],
        'detected_skills': result['detected_skills'],
        'weighted_score': result['weighted_score'],
        'semantic_score': result['semantic_score'],
        'matched_count': result['matched_count'],
        'required_count': result['required_count'],
        'missing_count': result['missing_count'],
        'category_summary': result['category_summary'],
        'experience_level': user.experience_level,
    }


@app.get('/api/history', response_model=list[HistoryEntry])
def get_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    analyses = db.query(Analysis).join(Resume).filter(Resume.user_id == user.id).order_by(Analysis.created_at.desc()).all()
    result = []
    for analysis in analyses:
        result.append({
            'analysis_id': analysis.id,
            'job_title': analysis.job_role.title,
            'score': analysis.score,
            'created_at': analysis.created_at.isoformat(),
        })
    return result


@app.delete('/api/history/{analysis_id}')
def delete_history_item(analysis_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    analysis = db.query(Analysis).join(Resume).filter(Analysis.id == analysis_id, Resume.user_id == user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail='Analysis not found.')

    db.query(AnalysisSkill).filter(AnalysisSkill.analysis_id == analysis_id).delete()
    db.delete(analysis)
    db.commit()
    return {'message': 'Analysis deleted successfully.'}


@app.get('/')
def root():
    return {'message': 'AI Resume Skill Gap Analysis API is running.'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
