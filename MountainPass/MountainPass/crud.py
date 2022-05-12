import datetime

from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user.id


def create_coords(db: Session, coords: schemas.CoordsCreate):
    db_coords = models.Coords(**coords.dict())

    db.add(db_coords)
    db.commit()
    db.refresh(db_coords)

    return db_coords.id


def create_pereval(db: Session, pereval: schemas.PerevalAddedCreate):
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

