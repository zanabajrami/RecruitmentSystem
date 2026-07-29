import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads/resumes"

class StorageService:
    def __init__(self):
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR, exist_ok=True)

    async def save_resume(self, file: UploadFile) -> str:
        # Only PDF or DOCX files are allowed
        allowed_extensions = [".pdf", ".docx"]
        ext = os.path.splitext(file.filename)[1].lower()
        
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file format. Only PDF and DOCX files are allowed."
            )

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        return file_path

storage_service = StorageService()