from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InterviewBase(BaseModel):
    scheduled_at: datetime
    meeting_link: Optional[str] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    application_id: int


class InterviewUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class InterviewResponse(InterviewBase):
    id: int
    application_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True