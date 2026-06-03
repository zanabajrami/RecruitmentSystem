from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate

class CompanyRepository:
    @staticmethod
    def get_by_id(db: Session, company_id: int):
        return db.query(Company).filter(Company.id == company_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Company).filter(Company.name == name).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Company).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, company_in: CompanyCreate):
        db_company = Company(
            name=company_in.name,
            description=company_in.description,
            website=str(company_in.website) if company_in.website else None
        )
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company