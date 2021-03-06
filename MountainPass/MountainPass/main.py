from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .errors import ErrorConnectionServer, ErrorCreatingRecord, get_json_response

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """
    Получение сессии, подключение к БД
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(ErrorCreatingRecord)
async def unicorn_exception_handler(request: Request, exc: ErrorCreatingRecord) -> str:
    """
    Декорирование ошибки создания записи в БД
    (развернутое описание ошибки вместо Internal Server Error).
    :param request: запрос
    :param exc: переопределен класс Exception
    :return: результат ошибки в формате JSON
    """
    return get_json_response(500, exc.name, 'null')


@app.exception_handler(ErrorConnectionServer)
async def srv_connect_exception_handler(request: Request, exc: ErrorConnectionServer) -> str:
    """
    Декорирование ошибки проверки подключения к БД
    (развернутое описание ошибки вместо Internal Server Error).
    :param request: запрос
    :param exc: переопределен класс Exception
    :return: результат ошибки в формате JSON
    """
    return get_json_response(500, exc.name, 'null')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> object:
    """
    Декорирование ошибки на несоответствия схеме объекта БД
    (развернутое описание ошибки вместо Request Validation Error).
    :param request: запрос
    :param exc: класс исключения RequestValidationError
    :return: результат ошибки в формате JSON с дополнением описанием и схемой
    """
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {'detail': exc.errors(), 'description': 'Несоответствие схеме', 'body': exc.body}
        )
    )


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> str:
    """
    Вызов функции создание пользователя и предварительная проверка наличия в БД по email,
    если пользователь с email существует, вызов исключения.
    Используется декоратор POST.
    :param user: класс схема базовой модели пользователя
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON о результате создания и id объекта
    """
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise ErrorCreatingRecord('Пльзователь с таким email существует')

    db_user_id = crud.create_user(db=db, user=user)
    return get_json_response(200, 'Отправлено успешно', db_user_id)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение id пользователей
    Используется декоратор GET.
    :param skip: пропуск по id
    :param limit: лимит выборки по количеству записей
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON (id объектов)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/coords/", response_model=schemas.Coords)
async def create_coords(coords: schemas.CoordsCreate, db: Session = Depends(get_db)):
    """
    Вызов функции создание пользователя и предварительная проверка наличия в БД по email,
    если пользователь с email существует, вызов исключения.
    Используется декоратор POST.
    :param coords: класс схема базовой модели координат
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON id объекта
    """
    return crud.create_coords(db=db, coords=coords)


@app.post("/submitData/", response_model=schemas.PerevalAdded)
async def submitData(pereval: schemas.PerevalAddedCreate, db: Session = Depends(get_db)):
    """
    Вызов функции создания пользователя, координат и записи о перевале,
    Используется декоратор POST.
    :param pereval: класс схема базовой модели перевала
    :param db: сессия подключения к БД
    :return: в случае успешного создания записи в БД, возвращается JSON с ответом
    об успешной отправке и id объекта (перевала)
    """
    # Предварительная проверка подключения (простое выполнение запроса)
    try:
        db.execute('SELECT * FROM users')
    except Exception as error:
        raise ErrorConnectionServer(f'Ошибка соединения с сервером: {error}')
    # Создание записи пользователя
    new_user = crud.create_user(db=db, user=pereval.user)
    # Создание записи координат
    new_coords = crud.create_coords(db=db, coords=pereval.coords)

    pereval.user = new_user
    pereval.coords = new_coords
    # Создание записи о перевале
    new_pereval = crud.create_pereval(db=db, pereval=pereval)

    return get_json_response(200, 'Отправлено успешно', new_pereval.id)


@app.get("/submitData/{pereval_id}", response_model=schemas.PerevalAdded)
async def get_submitData_id(pereval_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о перевале по id
    Используется декоратор GET.
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON
    """
    db_pereval_info = crud.get_pereval(db, pereval_id)

    if db_pereval_info is None:
        return get_json_response(422, f'Перевал с id {pereval_id} отсутствует')

    return get_json_response(200, 'Объект получен', jsonable_encoder(db_pereval_info))


@app.patch("/submitData/{pereval_id}", response_model=schemas.PerevalAdded, response_model_exclude_none=True)
async def patch_submitData_id(pereval_id: int, pereval: schemas.PerevalAddedUpdate, db: Session = Depends(get_db)):
    """
    Обновление информации по id о перевале
    Используется декоратор PATCH.
    :param pereval: класс схема базовой модели перевала
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON
    """

    # pending — если модератор взял в работу;
    # accepted — модерация прошла успешно;
    # rejected — модерация прошла, информация не принята.
    statuses = [
        'pending',
        'accepted',
        'rejected',
    ]

    db_pereval_info = crud.get_pereval(db, pereval_id)

    if db_pereval_info is None:
        return get_json_response(422, f'Перевал с id {pereval_id} отсутствует')

    if db_pereval_info['status'] in statuses:
        return get_json_response(422, f'Перевал с id {pereval_id} на модерации')

    update_pereval = crud.update_pereval(pereval_id, db, pereval)
    return get_json_response(200, 'Запись обновлена', update_pereval.id)


@app.get("/perevals/{email}", response_model=List[schemas.PerevalAddedCreate])
async def read_perevals(email: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение информации о перевалах, созданных пользователем (фильтр по email)
    Используется декоратор GET.
    :param skip: пропуск по id
    :param limit: лимит выборки по количеству записей
    :param db: сессия подключения к БД
    :return: сообщение в формате JSON
    """
    perevals = crud.get_perevals(db=db, email=email, skip=skip, limit=limit)
    return perevals

