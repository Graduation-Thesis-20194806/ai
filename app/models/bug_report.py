import enum

from sqlalchemy import Column, Integer, String, Enum, Boolean, Text, JSON, ARRAY, DateTime, func, ForeignKey

from app.models.database import Base


class ReportType(enum.Enum):
    BUG = "BUG"
    FEEDBACK = "FEEDBACK"
    WISH = "WISH"


class Severity(enum.Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ReportStatus(enum.Enum):
    INIT = "INIT"
    CONFIRMING = "CONFIRMING"
    IN_PROCESSING = "IN_PROCESSING"
    REJECTED = "REJECTED"
    DONE = "DONE"


class ReportIssueType(enum.Enum):
    UI = "UI"
    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    NETWORK = "NETWORK"
    COMPATIBILITY = "COMPATIBILITY"
    DATA = "DATA"


class BugReport(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ReportType), default=ReportType.BUG, nullable=False)
    severity = Column(Enum(Severity))
    is_public = Column('is_public', Boolean, default=True, nullable=False)
    created_by_id = Column('created_by_id', Integer, nullable=False)
    project_id = Column('project_id', Integer, nullable=False)
    assigned_to = Column('assigned_to', Integer, nullable=True)
    status_id = Column('statusId', Integer, nullable=True)
    steps_to_reproduce = Column('steps_to_reproduce', Text)
    expected_behavior = Column('expected_behavior', Text)
    actual_result = Column('actual_result', Text)
    description = Column(Text, nullable=False)
    issue_type = Column('issue_type', Enum(ReportIssueType))
    url = Column(Text, nullable=False)
    addition_info = Column('additionInfo', JSON)
    status = Column(Enum(ReportStatus), default=ReportStatus.INIT, nullable=False)
    tags = Column(ARRAY(Integer))
    created_at = Column('created_at', DateTime, server_default=func.now(), nullable=False)
    updated_at = Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
