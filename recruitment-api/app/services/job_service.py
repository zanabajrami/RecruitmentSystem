from app.schemas.job import JobCreate
from app.repositories.job_repository import JobRepository
from app.services.currency import CurrencyService

class JobService:
    def __init__(self, job_repo: JobRepository):
        """
        Initialize JobService with dependency injection of the repository.
        """
        self.job_repo = job_repo

    async def create_new_job(self, job_in: JobCreate):
        # Notice how cleanly we call self.job_repo.create without passing 'db' manually
        db_job = self.job_repo.create(job_in)
        rates = await CurrencyService.get_exchange_rates()
        db_job.converted_salaries = CurrencyService.clean_and_convert_salary(db_job.salary, rates)
        return db_job

    async def get_all_jobs(self, skip: int = 0, limit: int = 100):
        # Using the updated get_all method from repository
        jobs = self.job_repo.get_all(skip=skip, limit=limit)
        rates = await CurrencyService.get_exchange_rates()
        for job in jobs:
            job.converted_salaries = CurrencyService.clean_and_convert_salary(job.salary, rates)
        return jobs