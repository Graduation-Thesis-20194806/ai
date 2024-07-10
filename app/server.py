import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from os import getenv, system

load_dotenv()


from .routes import app_router
from .models.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(servers=[{"url": getenv("SERVER_URL")}])

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(app_router, prefix="/api")


def dev():
    """Launched with `poetry run dev` at root level"""
    migrate_run()
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)


def start():
    """Launched with `poetry run start` at root level"""
    migrate_run()
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000)


def migrate_gen():
    system('alembic revision --autogenerate -m "edit seller"')


def migrate_run():
    system("alembic upgrade head")


def celery_worker():
    # system(
    #     f"celery -A app.utils.queue.celery_app worker --loglevel=info --concurrency=10 --max-tasks-per-child {getenv("MAX_TASKS_PER_CHILD")}"
    # )
    system(
        f"celery -A app.utils.queue.celery_app worker --loglevel=info --pool threads --concurrency=10 --max-tasks-per-child {getenv("MAX_TASKS_PER_CHILD")}"
    )