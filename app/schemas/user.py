from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    password_hash: str

    class Config:
        from_attributes = True

class UserTokenData(BaseModel):
    email: str
