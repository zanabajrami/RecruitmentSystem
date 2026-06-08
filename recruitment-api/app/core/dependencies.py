from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.services.ai_service import AIService

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_job_repository(db: Session = Depends(get_db)) -> JobRepository:
    return JobRepository(db)

def get_job_service(repo: JobRepository = Depends(get_job_repository)) -> JobService:
    return JobService(repo)

def get_ai_service() -> AIService:
    return AIService()