import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
import db
import datetime
import uuid
from .state_machine import JournalStatusMachine
from layers.medupdates_utilities.python.datatypes.journal_type import JournalType
from layers.medupdates_utilities.python.datatypes.journal_access import JournalAccess
from sqlalchemy import orm


from layers.medupdates_utilities.python.db.base import Base
from sqlalchemy import Integer, Float, String, DateTime, Sequence, Boolean, Date, Time, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, func, case, inspect

class Journal(Base, JournalStatusMachine):
    __tablename__ = "journals"
    __table_args__ = {"schema": "medupdates"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    specialty_id = Column(UUID(as_uuid=True))
    title = Column(String)
    description = Column(String)
    _status = Column('status',Integer)
    featured_for_day = Column(Boolean)
    featured_for_user = Column(Boolean)
    ext_weblink = Column(String)
    ext_name = Column(String)
    ext_type = Column(Enum(JournalType),nullable=True,default=None)
    ext_access = Column(Enum(JournalAccess),nullable=True,default=None)
    scheduled_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime,nullable=True)

    def initialize_state_machine(self):
        JournalStatusMachine.initialize_state_machine(self)
       
    @orm.reconstructor
    def init_on_load(self):
        self.initialize_state_machine()

    