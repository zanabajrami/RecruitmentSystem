# app/api/v1/endpoints/jobs.py
from fastapi import APIRouter, Depends, status
from typing import List

from app.schemas.job import JobCreate, JobResponse
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