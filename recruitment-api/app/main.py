from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine
from app.database.base_model import Base

# Import models so SQLAlchemy can detect and create the tables
from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application

# Define lifespan context manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions to execute on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Actions to execute on shutdown (if needed)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Include the main API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"status": "healthy"}