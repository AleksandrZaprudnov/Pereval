from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .errors import ErrorConnectionServer, ErrorCreatingRecord, ReJSONResponse

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
    return ReJSONResponse(500, exc.name)


@app.exception_handler(ErrorConnectionServer)
async def unicorn_exception_handler(request: Request, exc: ErrorConnectionServer):
    return ReJSONResponse(500, exc.name)


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise ErrorCreatingRecord('Пльзователь с таким email существует')

    return crud.create_user(db=db, user=user)


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

    return new_pereval

