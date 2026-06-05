from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    job_id: int
    user_id: int
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    expected_salary: Optional[str] = None
    experience_years: Optional[int] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: int
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True