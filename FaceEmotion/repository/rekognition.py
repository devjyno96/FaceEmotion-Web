import datetime

from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

from .. import amazon as amazon
from ..models import rekognition as rekognition_models
from ..schemas import rekognition as rekognition_schemas



def request_rekognition(byte_image: bytes, db: Session):
    response = amazon.run_rekognition_by_byte_image(byte_image)
    return response
