from datetime import datetime
from typing import Optional, List

from app.schemas import BaseSchema


class ReportType:
    pass


class Severity:
    pass


class ReportIssueType:
    pass

class AdditionInfoSchema(BaseSchema):
    pass


class ReportStatus:
    pass


class BugReportBase(BaseSchema):
    id: int
    name: str
    type: ReportType
    severity: Severity
    is_public: bool
    created_by_id: int
    project_id: int
    assigned_to: Optional[int]
    status_id: Optional[int]
    steps_to_reproduce: Optional[str]
    expected_behavior: Optional[str]
    actual_result: Optional[str]
    description: str
    issue_type: ReportIssueType
    url: str
    status: ReportStatus
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]