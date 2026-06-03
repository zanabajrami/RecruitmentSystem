from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine
from app.database.base_model import Base

from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "healthy"}