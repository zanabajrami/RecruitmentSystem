from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database.session import get_db
from app.models.job import Job
from app.models.company import Company
from app.models.application import Application
from app.models.user import User

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Retrieve aggregated metrics and chart-ready data for the recruiter dashboard.
    """
    # 1. Fetch total counts for the main dashboard numeric cards
    total_jobs = db.query(Job).count()
    total_companies = db.query(Company).count()
    total_applications = db.query(Application).count()
    total_candidates = db.query(User).count()

    # 2. Group and count applications by status for the Pie/Donut chart
    # Normalized to lowercase database lookup while keeping clean frontend keys
    status_mapping = {"Pending": "pending", "Reviewed": "reviewed", "Accepted": "accepted", "Rejected": "rejected"}
    status_counts = {}
    
    for display_name, db_status in status_mapping.items():
        status_counts[display_name] = db.query(Application).filter(Application.status == db_status).count()

    # 3. Group and count jobs by location for the Bar chart
    location_counts = {}
    jobs = db.query(Job.location).all()
    for job in jobs:
        if job.location:
            location_counts[job.location] = location_counts.get(job.location, 0) + 1

    # 4. Construct the structured JSON payload optimized for frontend chart components
    return {
        "cards": {
            "total_jobs": total_jobs,
            "total_companies": total_companies,
            "total_applications": total_applications,
            "total_candidates": total_candidates
        },
        "charts": {
            "application_status_pie_chart": status_counts,
            "jobs_by_location_bar_chart": location_counts
        }
    }