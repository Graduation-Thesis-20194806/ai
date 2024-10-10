from http.client import HTTPException
from os import getenv
from contextlib import contextmanager
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_NAME')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    # To make it faster to fail, but also fails with the default options
    # pool_size=1,
    # max_overflow=0,
    # echo_pool="debug",
    # pool_timeout=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db_with_ctx_manager():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()