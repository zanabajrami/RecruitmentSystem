import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine
from app.database.base_model import Base

# Import the new middleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware

# Import models so SQLAlchemy can detect and create the tables during lifespan startup
from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application

# Setup standard logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("recruitment_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Creates database tables automatically when the server starts.
    """
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic can be added here if needed

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# --- MIDDLEWARE STACK ---

# 1. Rate Limiting: Protects the API from brute-force and spam (30 requests per minute)
app.add_middleware(RateLimitMiddleware, requests_limit=30, window_seconds=60)

# 2. Request Logging: Calculates processing time and logs API calls
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Method: {request.method} | Path: {request.url.path} "
        f"| Status: {response.status_code} | Duration: {process_time:.2f}ms"
    )
    return response

# 3. CORS: Configures Cross-Origin Resource Sharing
cors_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS] if settings.BACKEND_CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTER INCLUSION ---

# Include the centralized API router with versioning prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"])
def root():
    """
    Basic health check endpoint to verify that the API is operational.
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }