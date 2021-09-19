import enum
from typing import List

from datetime import datetime

from pydantic import BaseModel

from FaceEmotion.schemas.user import ShowUser


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


class RekognitionResult(BaseModel):
    smile: float
    happy: float
    confused: float
    disgusted: float
    surprised: float
    calm: float
    angry: float
    sad: float
    fear: float


class CreateRekognitionResult(RekognitionResult):
    user_id = int


class ShowRekognitionResult(RekognitionResult):
    rekognition_result_id: int
    created_time: datetime

    user: ShowUser

    class Config():
        orm_mode = True
