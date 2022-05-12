from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    fam: str
    name: str
    otc: str
    phone: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    # passes: List[Pass] = []

    class Config:
        orm_mode = True
