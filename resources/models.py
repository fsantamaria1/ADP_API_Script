from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from resources.database import Database
import os

db = Database()


class UnnormalizedEmployee(db.Base):
    __tablename__ = 'UnnormalizedEmployees'
    __table_args__ = {'schema': os.environ.get('schema')}

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
    ce_department_id = Column(String(15))


class UnnormalizedTimecards(db.Base):
    __tablename__ = 'UnnormalizedTimecards'
    __table_args__ = {'schema': os.environ.get('schema')}

    timecard_id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    associate_id = Column(String(20))
    timecard_date = Column(Date, nullable=False)
    pay_period_start = Column(Date)
    pay_period_end = Column(Date)
    clock_in = Column(DateTime(timezone=True))
    clock_out = Column(DateTime(timezone=True))
    pay_code_name = Column(String(20))
    processing_status_code = Column(String(20))
    has_exception = Column(Boolean)
