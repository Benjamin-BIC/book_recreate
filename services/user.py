from uuid import UUID
from database import users
from schemas.user import User, UserCreate


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        user = users.get(str(user_id))
        if not user:
            return None
        return user

    @staticmethod
    def create_book(user_in: UserCreate):
        user = User(id=str(UUID(int=len(users) + 1)),
                    **user_in.model_dump())
        users[user.id] = user
        return user
