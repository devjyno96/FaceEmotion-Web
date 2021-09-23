import datetime
import os
import json
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import amazon as amazon
from ..models import rekognition as rekognition_models
from ..models import user as user_models

TEST = True

TEST_REQUEST_RESULT_PATH = str(Path(os.path.realpath(__file__)).parent.parent.parent.absolute()) + '/TestCode/resource'


def request_rekognition(byte_image: bytes, db: Session):
    if not TEST:
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
    else:
        with open(TEST_REQUEST_RESULT_PATH + '/request_result.json') as json_file:
            json_data = json.load(json_file)
        return json_data


def get_all_rekognition_result_list(user_id: int, db: Session):
    if not TEST:
        user = db.query(user_models.User).filter(user_models.User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'author with id {user_id} not found')
        rekognition_result_list = db.query(rekognition_models.RekognitionResult).filter(
            rekognition_models.RekognitionResult.user == user
        ).all()
        return rekognition_result_list
    else:
        with open(TEST_REQUEST_RESULT_PATH + '/request_result_all.json') as json_file:
            json_data = json.load(json_file)
        return json_data


def get_rekognition_result_list_by_duration(user_id: int, duration_second: int, db: Session):
    BackgroundColor = {
        'happy': 'rgba(255, 99, 132, 0.2)',
        'confused': 'rgba(255, 159, 64, 0.2)',
        'disgusted': 'rgba(255, 205, 86, 0.2)',
        'surprised': 'rgba(75, 192, 192, 0.2)',
        'calm': 'rgba(54, 162, 235, 0.2)',
        'angry': 'rgba(153, 102, 255, 0.2)',
        'sad': 'rgba(201, 203, 207, 0.2)',
        'fear': 'rgba(59, 59, 59, 0.2)',
    }
    BorderColor = {
        'happy': 'rgb(255, 99, 132)',
        'confused': 'rgb(255, 159, 64)',
        'disgusted': 'rgb(255, 205, 86)',
        'surprised': 'rgb(75, 192, 192)',
        'calm': 'rgb(54, 162, 235)',
        'angry': 'rgb(153, 102, 255)',
        'sad': 'rgb(201, 203, 207)',
        'fear': 'rgb(59, 59, 59)',

    }
    if not TEST:
        if duration_second is None:
            duration_second = 2
        user = db.query(user_models.User).filter(user_models.User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'author with id {user_id} not found')
        rekognition_result_list = db.query(rekognition_models.RekognitionResult).filter(
            rekognition_models.RekognitionResult.user == user,
            rekognition_models.RekognitionResult.created_time > (
                    datetime.datetime.now() - datetime.timedelta(seconds=duration_second)),
        ).all()
        return rekognition_result_list
    else:
        result = {}
        with open(TEST_REQUEST_RESULT_PATH + '/request_result_all_duration.json') as json_file:
            json_data = json.load(json_file)
        result_dict = {
            'happy': 0,
            'confused': 0,
            'disgusted': 0,
            'surprised': 0,
            'calm': 0,
            'angry': 0,
            'sad': 0,
            'fear': 0,
        }
        select_key_list = ['happy', 'confused', 'disgusted', 'surprised', 'calm', 'angry', 'sad', 'fear', ]
        for item in json_data:
            for selected_key in select_key_list:
                result_dict[selected_key] += item[selected_key]
        sorted_result_dict = sorted(result_dict.items(), key=(lambda x: x[1]), reverse=True)[:3]
        # print(type(sorted_result_dict))
        result['labels'] = [x[0] for x in sorted_result_dict]
        result['data'] = [x[1]/len(json_data) for x in sorted_result_dict]
        result['backgroundColor'] = [BackgroundColor[x[0]] for x in sorted_result_dict]
        result['borderColor'] = [BorderColor[x[0]] for x in sorted_result_dict]

        return result
