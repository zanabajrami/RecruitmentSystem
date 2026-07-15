from pydantic import BaseModel, ConfigDict  
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
    
    # Advanced AI data integration fields
    ai_match_score: Optional[str] = None
    recommendation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None 
    notes: Optional[str] = None