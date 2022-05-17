from typing import List

from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .errors import ErrorConnectionServer, ErrorCreatingRecord, get_json_response

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(ErrorCreatingRecord)
async def unicorn_exception_handler(request: Request, exc: ErrorCreatingRecord):
    return get_json_response(500, exc.name, 'null')


@app.exception_handler(ErrorConnectionServer)
async def srv_connect_exception_handler(request: Request, exc: ErrorConnectionServer):
    return get_json_response(500, exc.name, 'null')


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise ErrorCreatingRecord('Пльзователь с таким email существует')

    db_user_id = crud.create_user(db=db, user=user)
    return get_json_response(200, 'Отправлено успешно', db_user_id)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/coords/", response_model=schemas.Coords)
async def create_coords(coords: schemas.CoordsCreate, db: Session = Depends(get_db)):
    return crud.create_coords(db=db, coords=coords)


@app.post("/submitData/", response_model=schemas.PerevalAdded)
async def submitData(pereval: schemas.PerevalAddedCreate, db: Session = Depends(get_db)):

    try:
        db.execute('SELECT * FROM users')
    except Exception as error:
        raise ErrorConnectionServer(f'Ошибка соединения с сервером: {error}')

    new_user = crud.create_user(db=db, user=pereval.user)
    new_coords = crud.create_coords(db=db, coords=pereval.coords)

    pereval.user = new_user
    pereval.coords = new_coords

    new_pereval = crud.create_pereval(db=db, pereval=pereval)

    return get_json_response(200, 'Отправлено успешно', new_pereval.id)

