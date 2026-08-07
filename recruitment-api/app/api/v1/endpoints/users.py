from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.core.dependencies import get_user_service

# Heqim prefix="/users" këtu që të mos duplikohet me api_router
router = APIRouter(tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Krijon një përdorues të ri në sistem.
    """
    return user_service.create_user(user_in)


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Përdoruesi nuk u gjet"
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    updated_user = user_service.update_user(user_id, user_in)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Përdoruesi nuk u gjet"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Përdoruesi nuk u gjet"
        )
    return None