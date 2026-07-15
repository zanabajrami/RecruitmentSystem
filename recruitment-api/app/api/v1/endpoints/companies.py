from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.auth_service import get_db 
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.repositories.company_repository import CompanyRepository

router = APIRouter()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    existing_company = CompanyRepository.get_by_name(db, name=company_in.name)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this name already exists in the system."
        )
    return CompanyRepository.create(db, company_in=company_in)

@router.get("/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CompanyRepository.get_all(db, skip=skip, limit=limit)

@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_in: CompanyUpdate, db: Session = Depends(get_db)):
    """
    Partially update an existing company's details.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found."
        )
    
    # Extract only the fields that were sent in the request
    update_data = company_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)
        
    db.commit()
    db.refresh(company)
    return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Remove a company and all its associated listings from the system.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found."
        )
    
    db.delete(company)
    db.commit()
    return None