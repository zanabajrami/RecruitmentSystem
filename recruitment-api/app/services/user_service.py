from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_in: UserCreate) -> UserResponse:
        """
        Creates a new user in the database.
        Checks if the email is already registered.
        """
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Përdoruesi me këtë email ekziston tashmë."
            )
        return self.user_repo.create(user_in)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        return self.user_repo.get_all(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        return self.user_repo.get_by_id(user_id)

    def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[UserResponse]:
        return self.user_repo.update(user_id, user_in)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete(user_id)