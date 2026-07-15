from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session

# Importet e sakta sipas strukturës tënde të folderave
from app.database.session import get_db
from app.models.job import Job

from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import JobService
from app.core.dependencies import get_job_service

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate, 
    job_service: JobService = Depends(get_job_service)
):
    """
    Endpoint to create a new job posting.
    Delegates database entry and currency conversions to the JobService layer.
    """
    return await job_service.create_new_job(job_in)

@router.get("/", response_model=List[JobResponse])
async def read_jobs(
    skip: int = 0, 
    limit: int = 100, 
    job_service: JobService = Depends(get_job_service)
):
    """
    Endpoint to retrieve a paginated list of job postings.
    Fetches real-time exchange rates and maps currency conversions dynamically.
    """
    return await job_service.get_all_jobs(skip=skip, limit=limit)

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(get_db)
):
    """
    Update job listing requirements, descriptions, or salaries.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job listing with ID {job_id} not found."
        )
    
    update_data = job_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
        
    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Permanently delete a job listing from the system.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job listing with ID {job_id} not found."
        )
        
    try:
        db.delete(job)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete job. It might have linked applications. Error: {str(e)}"
        )
        
    return None