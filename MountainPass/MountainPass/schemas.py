from typing import List, Optional
from pydantic import BaseModel


class CoordsCreate(BaseModel):
    latitude: float
    longitude: float
    height: int


class Coords(BaseModel):
    id: int

    class Config:
        orm_mode = True


# class UserBase(BaseModel):
#     email: str


class UserCreate(BaseModel):
    email: str
    fam: str
    name: str
    otc: str
    phone: str


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PerevalAddedCreate(BaseModel):
    beautyTitle: str
    title: str
    other_titles: str
    connect: str
    add_time: str
    user: Optional[UserCreate] = None
    coords: Optional[CoordsCreate] = None
    winter: str
    summer: str
    autumn: str
    spring: str


class PerevalAdded(BaseModel):
    # id: int

    class Config:
        orm_mode = True

