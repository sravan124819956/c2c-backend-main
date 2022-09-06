import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
import datetime
import uuid
import db

from .state_machine import JournalStatusMachine
from layers.medupdates_utilities.python.datatypes.journal_type import JournalType
from layers.medupdates_utilities.python.datatypes.journal_access import JournalAccess
from sqlalchemy import orm


from layers.medupdates_utilities.python.db.base import Base
from sqlalchemy import Integer, Float, String, DateTime, Sequence, Boolean, Date, Time, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, func, case, inspect
from layers.medupdates_utilities.python.datatypes.journal_reaction import JournalReaction

class JournalReactions(Base):
    __tablename__ = "journal_reactions"
    __table_args__ = {"schema": "medupdates"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(UUID(as_uuid=True))
    user_id = Column(UUID(as_uuid=True))
    reaction = Column(Enum(JournalReaction),nullable=True,default=None)
    created_at = Column(DateTime, default=datetime.datetime.now)


    
