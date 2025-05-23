from fastapi import APIRouter, HTTPException
from database import users
from schemas.book import Response, UserCreate
from services.user import user_service


user_router = APIRouter()


@user_router.get("/{id}")
def get_user_by_id(id: str):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="user not found.")
    return user


@user_router.post("")
def add_user(user_in: UserCreate):
    user = user_service.create_user(user_in)
    return Response(message="User added successfully", data=user)
