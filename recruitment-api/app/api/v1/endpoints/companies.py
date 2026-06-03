from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.auth_service import get_db 

from app.schemas.company import CompanyCreate, CompanyResponse
from app.repositories.company_repository import CompanyRepository

router = APIRouter()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    existing_company = CompanyRepository.get_by_name(db, name=company_in.name)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Një kompani me këtë emër ekziston në sistem."
        )
    return CompanyRepository.create(db, company_in=company_in)

@router.get("/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CompanyRepository.get_all(db, skip=skip, limit=limit)