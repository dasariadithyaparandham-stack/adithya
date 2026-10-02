from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    experience_level = Column(String(32), nullable=False, default='fresher')
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship('Resume', back_populates='user')


class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    filename = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='resumes')
    resume_skills = relationship('ResumeSkill', back_populates='resume')
    analyses = relationship('Analysis', back_populates='resume')


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    canonical_name = Column(String(255), nullable=False)

    job_skills = relationship('JobSkill', back_populates='skill')
    resume_skills = relationship('ResumeSkill', back_populates='skill')
    analysis_skills = relationship('AnalysisSkill', back_populates='skill')
    aliases = relationship('SkillAlias', back_populates='skill', cascade='all, delete-orphan')


class SkillAlias(Base):
    __tablename__ = 'skill_aliases'
    __table_args__ = (UniqueConstraint('skill_id', 'alias', name='uq_skill_alias'),)

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    alias = Column(String(255), nullable=False)

    skill = relationship('Skill', back_populates='aliases')


class JobRole(Base):
    __tablename__ = 'job_roles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    job_skills = relationship('JobSkill', back_populates='job_role')
    analyses = relationship('Analysis', back_populates='job_role')


class JobSkill(Base):
    __tablename__ = 'job_skills'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('job_roles.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    importance = Column(Integer, nullable=False, default=1)

    job_role = relationship('JobRole', back_populates='job_skills')
    skill = relationship('Skill', back_populates='job_skills')
    __table_args__ = (UniqueConstraint('job_id', 'skill_id', name='uq_job_skill'),)


class ResumeSkill(Base):
    __tablename__ = 'resume_skills'

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    confidence = Column(Float, default=0.0)

    resume = relationship('Resume', back_populates='resume_skills')
    skill = relationship('Skill', back_populates='resume_skills')
    __table_args__ = (UniqueConstraint('resume_id', 'skill_id', name='uq_resume_skill'),)


class Analysis(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job_roles.id'), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship('Resume', back_populates='analyses')
    job_role = relationship('JobRole', back_populates='analyses')
    analysis_skills = relationship('AnalysisSkill', back_populates='analysis')


class AnalysisSkill(Base):
    __tablename__ = 'analysis_skills'

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey('analyses.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)

    analysis = relationship('Analysis', back_populates='analysis_skills')
    skill = relationship('Skill', back_populates='analysis_skills')
    __table_args__ = (UniqueConstraint('analysis_id', 'skill_id', name='uq_analysis_skill'),)
