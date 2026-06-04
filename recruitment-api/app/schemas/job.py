from pydantic import BaseModel
from typing import Optional, Dict

class JobBase(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    location: str
    salary: Optional[str] = None
    company_id: int

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    converted_salaries: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True