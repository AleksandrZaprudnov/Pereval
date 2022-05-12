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
#   "beauty_title": "пер.",
#   "title": "Перевал №1",
#   "other_titles": "Прекрасный перевал в народе",
#   "connect": ", ",
#   "add_time": "2022-05-12T19:32:38.462Z",
#   "user": {
#     "email": "string@rem.ru",
#     "fam": "String",
#     "name": "S.",
#     "otc": "T.",
#     "phone": "790500000"
#   },
#   "coords": {
#     "latitude": 89.0234,
#     "longitude": 45.02,
#     "height": 100
#   },
#   "winter": "1А",
#   "summer": "1А",
#   "autumn": "1А",
#   "spring": "3А"
# }
def create_pereval(db: Session, pereval: schemas.PerevalAddedCreate):
    # db_pereval = models.PerevalAdded(**pereval.dict())
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

    db.add(db_pereval)
    db.commit()
    db.refresh(db_pereval)

    return db_pereval

