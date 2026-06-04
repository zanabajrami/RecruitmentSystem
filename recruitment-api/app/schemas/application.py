from pydantic import BaseModel

class ApplicationBase(BaseModel):
    job_id: int
    user_id: int
    resume_url: str
    status: str = "Pending"

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: int

    class Config:
        from_attributes = True