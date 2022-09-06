import sys
sys.path.append("C:\\Users\\user\\Downloads\\c2c-backend-main")
from layers.medupdates_utilities.python.db.base import Base
from layers.medupdates_utilities.python.db.base import generate_session
from layers.medupdates_utilities.python.db.base import terminate
from layers.medupdates_utilities.python.db.base import local_engine


# from enum import Enum

from sqlalchemy import orm
from sqlalchemy import Column, func, case, inspect
from sqlalchemy import Integer, Float, String, DateTime, Sequence, Boolean, Date, Time, Text, Enum
from sqlalchemy import select, cast
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID

from .models import *

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.sql import *