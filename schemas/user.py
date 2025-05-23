from os import name
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    full_name: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str


class User(BaseModel):
    users: list[User]
