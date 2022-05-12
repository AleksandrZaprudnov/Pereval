from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# /users/{"email":"a@a.ru","fam":"F","name":"N","otc":"O","phone":"+79000000000"}
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict(), email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

