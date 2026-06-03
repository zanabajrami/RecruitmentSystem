from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate

class JobRepository:
    @staticmethod
    def get_by_id(db: Session, job_id: int):
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Job).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, job_in: JobCreate):
        db_job = Job(
            title=job_in.title,
            description=job_in.description,
            requirements=job_in.requirements,
            location=job_in.location,
            company_id=job_in.company_id
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job