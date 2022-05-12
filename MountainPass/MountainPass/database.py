from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .functions import get_env


SQLALCHEMY_DATABASE_URL = f'postgresql://{get_env("FSTR_DB_LOGIN")}:{get_env("FSTR_DB_PASS")}@{get_env("FSTR_DB_HOST")}/{get_env("FSTR_DB_NAME")}'

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
