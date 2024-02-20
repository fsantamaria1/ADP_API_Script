from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.types import DECIMAL
from resources.database import Database
import os

db = Database()


class UnnormalizedEmployees(db.Base):
    __tablename__ = 'UnnormalizedEmployees'
    __table_args__ = {'schema': os.environ.get('default_schema')}

    associate_id = Column(String(20), primary_key=True, nullable=False, unique=True, index=True)
    worker_id = Column(String(20), unique=True, nullable=False)
    payroll_name = Column(String(90))
    first_name = Column(String(30))
    last_name = Column(String(30))
    middle_name = Column(String(30))
    location_code = Column(String(10))
    location_description = Column(String(50))
    department_code = Column(String(10))
    department_description = Column(String(50))
    worker_status = Column(String(11))
    is_active = Column(Boolean)
    ce_code = Column(String(10), index=True)
    ce_department = Column(String(15))
    hourly_rate = Column(DECIMAL(10,2))


class UnnormalizedTimecards(db.Base):
    __tablename__ = 'UnnormalizedTimecards'
    __table_args__ = {'schema': os.environ.get('default_schema')}

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)

    # Timecard data
    timecard_id = Column(String(25), index=True)
    associate_id = Column(String(20))
    timecard_status_code = Column(String(20))
    pay_period_start = Column(Date)
    pay_period_end = Column(Date)
    has_exceptions = Column(Boolean)

    # Entry data
    entry_id = Column(String(50))
    entry_date = Column(Date, nullable=False)
    clock_in = Column(DateTime(timezone=True))
    clock_out = Column(DateTime(timezone=True))
    entry_status_code = Column(String(25))
    pay_code = Column(String(20))
    time_duration = Column(Integer)
