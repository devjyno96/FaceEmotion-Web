import enum
from typing import List

from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    task_id: int
    key_name: str

    class Config():
        orm_mode = True


class ShowTask(Task):
    pass


class Job(BaseModel):
    job_id: int
    created_time: datetime
    decrypt_key: str
    company_name: str
    assigned_task: List[Task]

    class Config():
        orm_mode = True


class ShowJob(Job):
    pass