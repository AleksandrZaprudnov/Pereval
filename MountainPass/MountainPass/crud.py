import datetime

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import models, schemas
from .errors import ErrorCreatingRecord


def get_user(db: Session, user_id: int) -> object:
    """
    Получение пользователя по id.
    :param db: сессия подключения к БД
    :param user_id: уникальный идентификатор записи БД
    :return: запись БД - объект
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> object:
    """
    Получение пользователя по email (электронная почта, уникальное значение).
    Функция для проверки наличия пользователя в БД
    :param db: сессия подключения к БД
    :param email: электронная почта
    :return: очередь выбранных записей из БД
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение очереди пользователей, с возможностью лимитирования количества объектов выборке.
    :param db: сессия подключения к БД
    :param skip: индекс для пропуска
    :param limit: количество записей выборки из БД
    :return: очередь выбранных записей из БД
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> int:
    """
    Создание пользователя согласно схеме UserCreate.
    :param db: сессия подключения к БД
    :param user: схема
    :return: уникальный идентификатор пользователя
    """
    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise ErrorCreatingRecord('Пльзователь с таким email существует')

    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user.id


def create_coords(db: Session, coords: schemas.CoordsCreate) -> int:
    """
    Создание записи географических координат согласно схеме CoordsCreate.
    :param db: сессия подключения к БД
    :param coords: схема
    :return: уникальный идентификатор записи координат перевала
    """
    db_coords = models.Coords(**coords.dict())

    db.add(db_coords)
    db.commit()
    db.refresh(db_coords)

    return db_coords.id


def create_pereval(db: Session, pereval: schemas.PerevalAddedCreate) -> object:
    """
    Запись сведений о перевале согласно схеме PerevalAddedCreate.
    :param db: сессия подключения к БД
    :param pereval: схема
    :return: запись БД - объект
    """
    db_pereval = models.PerevalAdded(
        beauty_title=pereval.beauty_title,
        title=pereval.title,
        other_titles=pereval.other_titles,
        connect=pereval.connect,
        add_time=pereval.add_time,
        user_id=pereval.user,
        coords_id=pereval.coords,
        winter=pereval.winter,
        summer=pereval.summer,
        autumn=pereval.autumn,
        spring=pereval.spring
    )

    db_pereval.status = 'new'
    db_pereval.date_added = datetime.datetime.now()

    db.add(db_pereval)
    db.commit()
    db.refresh(db_pereval)

    return db_pereval


def update_pereval(pereval_id: int, db: Session, pereval: schemas.PerevalAddedUpdate) -> object:
    """
    Обновление сведений о перевале согласно схеме PerevalAddedUpdate.
    :param pereval_id: уникальный идентификатор перевала
    :param db: сессия подключения к БД
    :param pereval: схема
    :return: запись БД - объект
    """
    db_pereval = db.query(models.PerevalAdded).filter(models.PerevalAdded.id == pereval_id).first()

    db_pereval.beauty_title = pereval.beauty_title
    db_pereval.title = pereval.title
    db_pereval.other_titles = pereval.other_titles
    db_pereval.connect = pereval.connect
    db_pereval.winter = pereval.winter
    db_pereval.summer = pereval.summer
    db_pereval.autumn = pereval.autumn
    db_pereval.spring = pereval.spring

    if not db_pereval.coords_id is None:
        db_coords = db.query(models.Coords).filter(models.Coords.id == db_pereval.coords_id).first()

        db_coords.latitude = pereval.coords.latitude
        db_coords.longitude = pereval.coords.longitude
        db_coords.height = pereval.coords.height

        db.add(db_coords)
        db.commit()
        db.refresh(db_coords)
    else:
        db_coords = create_coords(db, pereval.coords)
        db_pereval.coords_id = db_coords.id

    db.add(db_pereval)
    db.commit()
    db.refresh(db_pereval)

    return db_pereval


def get_pereval(db: Session, pereval_id: int) -> dict:
    """
    Получение сведений о перевале по id.
    :param db: сессия подключения к БД
    :param pereval_id: уникальный идентификатор перевала
    :return: запись БД типа dict (словарь)
    """
    pereval = db.query(models.PerevalAdded).filter(models.PerevalAdded.id == pereval_id).first()
    user = db.query(models.User).filter(models.User.id == pereval.user_id).first()
    coords = db.query(models.Coords).filter(models.Coords.id == pereval.coords_id).first()

    json_user = jsonable_encoder(user)
    json_coords = jsonable_encoder(coords)
    dict_pereval = jsonable_encoder(pereval)

    dict_pereval['user_id'] = json_user
    dict_pereval['coords_id'] = json_coords

    return dict_pereval


def get_perevals(db: Session, email: str, skip: int = 0, limit: int = 100) -> list:
    """
    Получение сведений о перевалах, созданных пользователем,
    отбор по email пользователя, с возможностью лимитирования количества объектов в выборке.
    :param db: сессия подключения к БД
    :param email: электронная почта пользователя
    :param skip: индекс для пропуска
    :param limit: количество записей выборки из БД
    :return: список объектов, сериализованных в JSON-формат
    """
    db_user = db.query(models.User).filter(models.User.email == email).first()
    q_perevals = db.query(models.PerevalAdded).filter(models.PerevalAdded.user_id == db_user.id).offset(skip).limit(limit).all()

    list_json_perevals = jsonable_encoder(q_perevals)
    json_user = jsonable_encoder(db_user)

    index = -1
    for pereval in q_perevals:
        index += 1
        json_coords = jsonable_encoder(db.query(models.Coords).filter(models.Coords.id == pereval.coords_id).first())

        list_json_perevals[index]['user'] = json_user
        list_json_perevals[index]['coords'] = json_coords

    return list_json_perevals

