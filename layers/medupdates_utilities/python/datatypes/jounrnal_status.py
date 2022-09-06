from enum import Enum

class JournalStatus(Enum):
    Draft = 0
    Scheduled = 1
    Published = 2
    Archived = 3