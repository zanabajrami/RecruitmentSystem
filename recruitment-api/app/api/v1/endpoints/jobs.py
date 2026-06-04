from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.services.currency import CurrencyService

router = APIRouter()

@router.post("/", response_model=JobResponse)
async def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job posting and append live currency conversions.
    """
    db_job = Job(**job_in.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Fetch third-party live exchange rates
    rates = await CurrencyService.get_exchange_rates()
    # Process conversion asynchronously before returning the response
    db_job.converted_salaries = CurrencyService.clean_and_convert_salary(db_job.salary, rates)
    
    return db_job

@router.get("/", response_model=List[JobResponse])
async def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of job postings with live salary currency conversions.
    """
    jobs = db.query(Job).offset(skip).limit(limit).all()
    
    # Fetch exchange rates once to avoid hitting the external endpoint inside the loop
    rates = await CurrencyService.get_exchange_rates()
    
    # Map converted salary currencies into each job instance object
    for job in jobs:
        job.converted_salaries = CurrencyService.clean_and_convert_salary(job.salary, rates)
        
    return jobs