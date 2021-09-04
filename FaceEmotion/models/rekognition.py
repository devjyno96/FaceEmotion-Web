import datetime
from pytz import timezone
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from ..database import Base

from .models_function import get_now_time


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String)

    # Job : Task = 1 : N
    job_id = Column(Integer, ForeignKey('jobs.job_id', ondelete='CASCADE'))
    assigned_task = relationship("Job", back_populates="assigned_task", passive_deletes=True)


class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True, index=True)
    decrypt_key = Column(String)
    company_name = Column(String)
    created_time = Column(DateTime, default=get_now_time)

    # Job : Task = 1 : N
    assigned_task = relationship("Task", back_populates="assigned_task", passive_deletes=True)

    # Job : Assigned_Job = 1:1
    assigned_job = relationship("Assigned_Job", back_populates="assigned_job", passive_deletes=True)


class Assigned_Job(Base):
    __tablename__ = 'assigned_jobs'

    assigned_job_id = Column(Integer, primary_key=True, index=True)
    created_time = Column(DateTime, default=get_now_time)

    # Job : Assigned_Job = 1:1
    job_id = Column(Integer, ForeignKey('jobs.job_id', ondelete='CASCADE'))
    assigned_job = relationship("Job", back_populates="assigned_job", passive_deletes=True)
