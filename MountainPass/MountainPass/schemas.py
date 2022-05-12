from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    fam: str
    name: str
    otc: str
    phone: str


class User(UserBase):
    id: int
    # passes: List[Pass] = []

    class Config:
        orm_mode = True
