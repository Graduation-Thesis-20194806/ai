from fastapi import APIRouter
from app.models.database import get_db_with_ctx_manager
from app.schemas.base import ProcessResponseSchema, ProcessDto
from app.services.bug_report import BugReportService

bugreport_router = APIRouter(tags=["bug-reports"])
@bugreport_router.post("/process", response_model=ProcessResponseSchema)
def process(dto: ProcessDto):
    with get_db_with_ctx_manager() as db:
        return BugReportService(db).process(dto.report_id)
