from sqlalchemy import Column, Integer

from app.models.database import Base
class DuplicateGroup(Base):
    __tablename__ = 'DuplicateGroup'
    id = Column(Integer, primary_key=True, autoincrement=True)
