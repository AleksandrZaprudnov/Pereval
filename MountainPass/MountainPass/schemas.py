from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CoordsCreate(BaseModel):
    """
    Класс схемы для создания записи координат.
    """
    latitude: float
    longitude: float
    height: int

    class Config:
        schema_extra = {
            'example': {
                'latitude': 56.2368,
                'longitude': 41.683,
                'height': 120,
            }
        }


class Coords(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Класс схемы для создания пользователя.
    """
    email: str
    fam: str
    name: str
    otc: str
    phone: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'test.mail@email.ru',
                'fam': 'Иванов',
                'name': 'Петр',
                'otc': 'Иванович',
                'phone': '79001010102',
            }
        }


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PerevalAddedCreate(BaseModel):
    """
    Класс схемы для создания перевала.
    """
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

    class Config:
        schema_extra = {
            'example': {
                'beauty_title': 'пер.',
                'title': 'Беляши',
                'other_titles': 'Айгасу, Лигайский',
                'connect': ', ',
                'add_time': '2022-05-20T07:18:06.456Z',
                'user': {
                    'email': 'test.mail@email.ru',
                    'fam': 'Иванов',
                    'name': 'Петр',
                    'otc': 'Иванович',
                    'phone': '79001010102',
                },
                'coords': {
                    'latitude': 56.2368,
                    'longitude': 41.683,
                    'height': 120,
                },
                'winter': '1Б',
                'summer': '1А',
                'autumn': '1А',
                'spring': '1А',
            }
        }


class PerevalAddedUpdate(BaseModel):
    """
    Класс схемы для обновления сведений о перевале.
    """
    beauty_title: Optional[str] = None
    title: Optional[str] = None
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    coords: Optional[CoordsCreate] = None
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'beauty_title': 'пер.',
                'title': 'Беляши',
                'other_titles': 'Айгасу, Лигайский',
                'connect': ', ',
                'coords': {
                    'latitude': 56.2368,
                    'longitude': 41.683,
                    'height': 120,
                },
                'winter': '1Б',
                'summer': '1А',
                'autumn': '1А',
                'spring': '1А',
            }
        }


class PerevalAdded(BaseModel):
    # id: int

    class Config:
        orm_mode = True

