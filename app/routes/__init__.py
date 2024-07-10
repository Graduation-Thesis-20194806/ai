from fastapi import APIRouter

from app.routes.bug_report import bugreport_router

app_router = APIRouter()


app_router.include_router(bugreport_router, prefix="/bug-reports")
