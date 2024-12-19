from enum import Enum


class MessageType(Enum):
    BUG_REPORT = 'BUG_REPORT'
    BUG_DUPLICATE = 'BUG_DUPLICATE'

class DuplicateLevel(Enum):
  LOW = 'LOW'
  MEDIUM = 'MEDIUM'
  HIGH = 'HIGH'