from sqlalchemy.orm import Session
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobUpdate
from app.services.currency import CurrencyService
from fastapi import HTTPException, status
import re

class JobService:
    def __init__(self, db: Session):
        self.job_repo = JobRepository(db)
        self.currency_service = CurrencyService()

    def create_job(self, job_in: JobCreate):
        """
        Creates a new job listing after performing basic validations.
        """
        # Simple safety check if salary comes as a negative number
        if hasattr(job_in, 'salary') and job_in.salary and isinstance(job_in.salary, (int, float)) and job_in.salary < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Salary cannot be negative."
            )
        return self.job_repo.create(obj_in=job_in)

    def get_job_by_id(self, job_id: int):
        """
        Retrieves a specific job by its ID. Returns 404 if it does not exist.
        """
        job = self.job_repo.get(id=job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job listing with ID {job_id} not found."
            )
        return job

    def get_jobs_with_currency_conversion(self, target_currency: str = "EUR"):
        """
        Retrieves all jobs and converts the 'salary' field to the requested currency.
        Correctly handles both numbers and strings like '1500-2500 EUR'.
        """
        jobs = self.job_repo.get_all()
        
        for job in jobs:
            if not job.salary:
                continue
                
            # Source currency (defaults to EUR if not specified in the model)
            source_currency = getattr(job, 'currency', 'EUR')
            if not source_currency:
                source_currency = 'EUR'

            # If the job currency is the same as requested, no conversion is needed
            if source_currency == target_currency:
                continue

            # CASE 1: If salary is stored as text (String) e.g. "1500-2500 EUR"
            if isinstance(job.salary, str):
                try:
                    # Clean the text from letters (EUR, USD, etc.) and extract only numbers and dashes
                    clean_salary = re.sub(r'[a-zA-Z\s]+', '', job.salary).strip()
                    
                    # If it is a range (e.g. "1500-2500")
                    if "-" in clean_salary:
                        parts = clean_salary.split("-")
                        min_sal = float(parts[0].strip())
                        max_sal = float(parts[1].strip())
                        
                        # Correctly convert the minimum and maximum value
                        min_conv = self.currency_service.convert(min_sal, source_currency, target_currency)
                        max_conv = self.currency_service.convert(max_sal, source_currency, target_currency)
                        
                        # Format it back nicely into a converted string format
                        job.salary = f"{round(min_conv)}-{round(max_conv)} {target_currency}"
                    else:
                        # If it is just a single number inside the text (e.g. "1500")
                        single_sal = float(clean_salary)
                        conv = self.currency_service.convert(single_sal, source_currency, target_currency)
                        job.salary = f"{round(conv)} {target_currency}"
                        
                except Exception:
                    # If something fails during text cleaning, keep the original value to prevent blocking the API
                    pass

            # CASE 2: If the database is changed and salary is stored as a pure number (int/float)
            elif isinstance(job.salary, (int, float)):
                try:
                    conv = self.currency_service.convert(job.salary, source_currency, target_currency)
                    job.salary = round(conv)
                    if hasattr(job, 'currency'):
                        job.currency = target_currency
                except Exception:
                    pass

        return jobs

    def update_job_listing(self, job_id: int, job_in: JobUpdate):
        """
        Updates the data of an existing job listing.
        """
        job = self.get_job_by_id(job_id)
        return self.job_repo.update(db_obj=job, obj_in=job_in)

    def delete_job_listing(self, job_id: int):
        """
        Deletes a job listing from the database.
        """
        job = self.get_job_by_id(job_id)
        return self.job_repo.delete(id=job_id)