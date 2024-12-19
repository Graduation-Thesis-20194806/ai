from sqlalchemy import desc

from app.models import BugReport
from app.repositories.base_repository import BaseRepository


class BugReportRepository(BaseRepository):
    def find_similar_reports(self, report: BugReport) -> list[BugReport]:
        return self.db.query(self.model).filter(self.model.project_id == report.project_id, self.model.url == report.url, self.model.id != report.id).order_by(desc(self.model.created_at)).all()
