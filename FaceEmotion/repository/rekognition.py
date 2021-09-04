from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

from ..models import rekognition as rekognition_models
from ..schemas import rekognition as rekognition_schemas

import FaceEmotion.amazon as amazon


