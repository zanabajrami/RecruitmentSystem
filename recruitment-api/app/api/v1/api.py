from fastapi import APIRouter
from app.api.v1.endpoints import auth, companies, jobs, applications
from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import dashboard  # Shto këtë import

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
