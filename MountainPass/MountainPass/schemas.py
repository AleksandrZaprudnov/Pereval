from datetime import datetime
from typing import Optional
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
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: datetime
    user: Optional[UserCreate] = None
    coords: Optional[CoordsCreate] = None
    winter: str
    summer: str
    autumn: str
    spring: str


class PerevalAddedUpdate(BaseModel):
    beauty_title: Optional[str] = None
    title: Optional[str] = None
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    coords: Optional[CoordsCreate] = None
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class PerevalAdded(BaseModel):
    # id: int

    class Config:
        orm_mode = True

