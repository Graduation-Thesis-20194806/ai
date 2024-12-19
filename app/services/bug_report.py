from app.utils.queue import process_report, process_duplicate


class BugReportService:
    def __init__(self, db) -> None:
        self.db = db
    @staticmethod
    def process(report_id: int):
        process_report.delay(report_id)
        process_duplicate.delay(report_id)
        return {
            "success": True,
        }
