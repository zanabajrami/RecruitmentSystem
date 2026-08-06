from typing import List, Optional
from app.repositories.user import UserRepository
from app.schemas.user import UserUpdate, UserResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Retrieves a list of all users with pagination.
        """
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Retrieves user details by ID.
        """
        return await self.user_repo.get_by_id(user_id)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[UserResponse]:
        """
        Updates specific user details.
        """
        return await self.user_repo.update(user_id, user_in)

    async def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user from the system.
        """
        return await self.user_repo.delete(user_id)