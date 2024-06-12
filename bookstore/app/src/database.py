from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.src.env import (USER, PASSWORD, HOST, PORT, DB_NAME,
                         DB_TYPE, POOL_RECYCLE, DB_POOL_SIZE, DB_MAX_OVERFLOW)

DATABASE_URL = f"{DB_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

ECHO_LOG = False

engine = create_engine(
    DATABASE_URL,
    encoding='utf-8',
    echo=ECHO_LOG,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = SessionLocal.query_property()


def get_db():
    """
    Provide the DB instance
    """
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
