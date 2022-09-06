import datetime
import uuid
import db
from layers.medupdates_utilities.python.db.base import Base
from sqlalchemy import Integer, Float, String, DateTime, Sequence, Boolean, Date, Time, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, func, case, inspect

class JournalDocuments(Base):
    __tablename__ = "journal_documents"
    __table_args__ = {"schema": "medupdates"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(UUID(as_uuid=True))
    title = Column(String)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    