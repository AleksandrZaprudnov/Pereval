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

    return db_user


def create_coords(db: Session, coords: schemas.CoordsCreate):
    db_coords = models.Coords(**coords.dict())
    db.add(db_coords)
    db.commit()
    db.refresh(db_coords)

    return db_coords


# {
#     "status": "new"
#     "beauty_title": "пер."
#     "title": "Перевал №1"
#     "other_titles": "Наипрекраснейший перевал"
#     "connect": ", "
#     "winter": ""
#     "summer": "1А"
#     "autumn": "3А"
#     "spring": "2А"
# }
def create_pereval(db: Session, pereval: schemas.PerevalAddedCreate):
    db_pereval = models.PerevalAdded(**pereval.dict(), status='new')
    db.add(db_pereval)
    db.commit()
    db.refresh(db_pereval)

    return db_pereval

