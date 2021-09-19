import enum
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    name: str
    is_admin: Optional[bool] = False


class CreateUser(User):
    password: str
    pass


class ShowUser(User):
    user_id: int

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    username: str
    new_password: str
    check_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
