from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.base_model import Base
from app.database.session import engine

# Krijon automatikisht tabelat në MySQL kur ndizet serveri
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"status": "healthy", "message": f"Welcome to {settings.PROJECT_NAME}"}