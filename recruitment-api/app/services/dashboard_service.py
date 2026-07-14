# app/services/dashboard_service.py
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.company import Company
from app.models.application import Application

class DashboardService:
    """
    Aggregates database metrics to provide real-time analytical data 
    for the recruitment platform's administrative dashboard.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_system_statistics(self) -> dict:
        """
        Queries active counts from the database and calculates system-wide ratios.
        """
        total_companies = self.db.query(Company).count()
        total_jobs = self.db.query(Job).count()
        total_applications = self.db.query(Application).count()

        # Calculate acceptance rate safely to avoid division by zero
        accepted_apps = self.db.query(Application).filter(Application.status == "accepted").count()
        acceptance_rate = 0.0
        if total_applications > 0:
            acceptance_rate = round((accepted_apps / total_applications) * 100, 2)

        return {
            "total_companies": total_companies,
            "total_active_jobs": total_jobs,
            "total_applications_received": total_applications,
            "overall_candidate_acceptance_rate": f"{acceptance_rate}%",
            "system_status": "Operational"
        }