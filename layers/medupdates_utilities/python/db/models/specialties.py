import db
import datetime
import uuid
import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from sqlalchemy import Integer, Float, String, DateTime, Sequence, Boolean, Date, Time, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, func, case, inspect

class Specialty(Base):
    __tablename__ = "specialties"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    