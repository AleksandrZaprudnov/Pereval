from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field


class CoordsCreate(BaseModel):
    """
    Класс схемы для создания записи координат.
    """
    latitude: float = Field(title='Широта (гр)', ge=0, le=90)
    longitude: float = Field(title='Долгота (гр)', ge=0, le=90)
    height: int = Field(title='Высота (м)', ge=0)

    class Config:
        schema_extra = {
            'example': {
                'latitude': 56.2368,
                'longitude': 41.683,
                'height': 120,
            }
        }


class Coords(BaseModel):
    id: int = Field(title='Уникальный идентификатор записи (устанавливается автоматически)')

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Класс схемы для создания пользователя.
    """
    email: str = Field(title='Email пользователя', max_length=50)
    fam: str = Field(title='Фамилия пользователя', max_length=30)
    name: str = Field(title='Имя пользователя', max_length=30)
    otc: str = Field(title='Отчество пользователя', max_length=30)
    phone: str = Field(title='Номер телефона пользователя', max_length=11)

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
    id: int = Field(title='Уникальный идентификатор записи (устанавливается автоматически)')

    class Config:
        orm_mode = True


class PerevalAddedCreate(BaseModel):
    """
    Класс схемы для создания перевала.
    """
    beauty_title: str = Field(title='Вид географического объекта', max_length=10)
    title: str = Field(title='Сокращенное название', max_length=100)
    other_titles: str = Field(title='Полное название, дополненное/расширенное', max_length=500)
    connect: str = Field(title='Разделитель', max_length=3)
    add_time: datetime
    user: Optional[UserCreate] = None
    coords: Optional[CoordsCreate] = None
    winter: str = Field(title='Сложность передвижения по местности в зимнее время', max_length=2)
    summer: str = Field(title='Сложность передвижения по местности в летнее время', max_length=2)
    autumn: str = Field(title='Сложность передвижения по местности в весеннее время', max_length=2)
    spring: str = Field(title='Сложность передвижения по местности в осеннее время', max_length=2)

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
    beauty_title: Union[str, None] = Field(default=None, title='Вид географического объекта', max_length=10)
    title: Union[str, None] = Field(default=None, title='Сокращенное название', max_length=100)
    other_titles: Union[str, None] = Field(default=None, title='Полное название, дополненное/расширенное', max_length=500)
    connect: Union[str, None] = Field(default=None, title='Разделитель', max_length=3)
    coords: Union[CoordsCreate, None] = None
    winter: Union[str, None] = Field(default=None, title='Сложность передвижения по местности в зимнее время', max_length=2)
    summer: Union[str, None] = Field(default=None, title='Сложность передвижения по местности в летнее время', max_length=2)
    autumn: Union[str, None] = Field(default=None, title='Сложность передвижения по местности в весеннее время', max_length=2)
    spring: Union[str, None] = Field(default=None, title='Сложность передвижения по местности в осеннее время', max_length=2)

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
    id: int = Field(title='Уникальный идентификатор записи (устанавливается автоматически)')

    class Config:
        orm_mode = True

