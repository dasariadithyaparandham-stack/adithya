from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class SkillOut(BaseModel):
    id: int
    name: str
    category: str
    canonical_name: str


class JobSkillOut(BaseModel):
    skill_id: int
    name: str
    category: str
    canonical_name: str
    importance: int


class JobOut(BaseModel):
    id: int
    title: str
    description: str
    required_skills: List[JobSkillOut] = []


class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    extracted_text: str


class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    experience_level: Literal['fresher', 'intermediate', 'experienced']


class UserLogin(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    experience_level: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserOut


class AnalysisRequest(BaseModel):
    resume_id: int
    job_id: int


class MissingSkillOut(BaseModel):
    skill: str
    priority: str
    reason: str
    topics: List[str]
    practice: str
    learning_order: int
    time_to_learn: str
    experience_guidance: str
    learning_path: dict
    study_schedule: List[dict]
    learning_resources: List[dict]
    job_role_recommendations: List[dict]


class AnalysisResponse(BaseModel):
    analysis_id: int
    resume_id: int
    job_id: int
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    priority_summary: dict
    recommendations: List[MissingSkillOut]
    roadmap: List[str]
    detected_skills: List[str]
    weighted_score: float = 0.0
    semantic_score: float = 0.0
    matched_count: int = 0
    required_count: int = 0
    missing_count: int = 0
    category_summary: dict = {}
    experience_level: str = 'fresher'


class HistoryEntry(BaseModel):
    analysis_id: int
    job_title: str
    score: float
    created_at: str


class ResumeSkillPayload(BaseModel):
    resume_id: int
    skills: List[str]
