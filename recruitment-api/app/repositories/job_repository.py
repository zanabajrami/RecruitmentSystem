from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate

class JobRepository:
    def __init__(self, db: Session):
        """
        Initialize JobRepository with an active SQLAlchemy database session.
        This enables proper dependency injection throughout the service layer.
        """
        self.db = db

    def get_by_id(self, job_id: int):
        """
        Retrieve a single job posting by its primary key ID.
        """
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        """
        Query the database to get a list of jobs with specific offset and limit pagination parameters.
        """
        return self.db.query(Job).offset(skip).limit(limit).all()

    def create(self, job_in: JobCreate) -> Job:
        """
        Directly communicate with the database to insert and commit a new Job record.
        Uses model_dump() for clean dictionary unpacking of schema fields.
        """
        db_job = Job(**job_in.model_dump())
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job