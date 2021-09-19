import datetime

from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

from .. import amazon as amazon
from ..models import rekognition as rekognition_models
from ..schemas import rekognition as rekognition_schemas


def request_rekognition(byte_image: bytes, db: Session):
    response = amazon.run_rekognition_by_byte_image(byte_image)
    if response['FaceDetails'][0]['Smile']['Value']:
        smile_confidence = response['FaceDetails'][0]['Smile']['Confidence']
    else:
        smile_confidence = 0.0

    emotion_confidence = {}

    for emotion in response['FaceDetails'][0]['Emotions']:
        emotion_confidence[emotion['Type']] = emotion['Confidence']

    happy_confidence = emotion_confidence['HAPPY']
    confused_confidence = emotion_confidence['CONFUSED']
    disgusted_confidence = emotion_confidence['DISGUSTED']
    surprised_confidence = emotion_confidence['SURPRISED']
    calm_confidence = emotion_confidence['CALM']
    angry_confidence = emotion_confidence['ANGRY']
    sad_confidence = emotion_confidence['SAD']
    fear_confidence = emotion_confidence['FEAR']

    new_rekognition_result = rekognition_models.RekognitionResult(
        smile=smile_confidence,

        happy=happy_confidence,
        confused=confused_confidence,
        disgusted=disgusted_confidence,
        surprised=surprised_confidence,
        calm=calm_confidence,
        angry=angry_confidence,
        sad=sad_confidence,
        fear=fear_confidence,

        user_id=1,  # 임시로 id 1 사용
    )
    db.add(new_rekognition_result)
    db.commit()

    db.refresh(new_rekognition_result)
    return new_rekognition_result
