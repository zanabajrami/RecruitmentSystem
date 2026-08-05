from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService
from app.services.ai_service import AIService
from app.models.user import User
from app.core.security import verify_token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token i pavlefshëm ose i skaduar.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Përdoruesi nuk u gjet.")
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nuk keni leje për të kryer këtë veprim."
            )
        return current_user


def get_job_repository(db: Session = Depends(get_db)) -> JobRepository:
    return JobRepository(db)


def get_job_service(repo: JobRepository = Depends(get_job_repository)) -> JobService:
    return JobService(repo)


def get_ai_service(db: Session = Depends(get_db)) -> AIService:
    return AIService(db)