from typing import List, Optional

from fastapi import APIRouter, Depends, status, Request, File
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .. import database
from ..repository import rekognition as rekognition_repository
from ..schemas import rekognition as rekognition_schemas

from .routers_function import get_summary_location

router = APIRouter(
    prefix='/rekognition',
    tags=['Rekognition']
)

get_db = database.get_db

templates = Jinja2Templates(directory="FaceEmotion/templates/rekognition")


@router.get('/', status_code=status.HTTP_200_OK, summary="get_html_rekognition" + " | " + get_summary_location())
def get_html_rekognition(request: Request, db: Session = Depends(get_db)):
    '''
    ### 설명
    - rekognition html 요청
    ### 관련 모델
    - None
    '''
    return templates.TemplateResponse("rekognition.html", {"request": request})


@router.post('/', status_code=status.HTTP_201_CREATED, summary="request_rekognition" + " | " + get_summary_location())
def request_rekognition(file: bytes = File(...), db: Session = Depends(get_db)):
    '''
    ### 설명
    - Amazon Rekognition 을 요청하고 그 결과를 받는 api
    - 분석에 1초 정도 소요됨
    ### 관련 모델
    - user, rekognition_result
    '''
    return rekognition_repository.request_rekognition(file, db)


@router.get('/result/all', status_code=status.HTTP_200_OK,
            response_model=List[rekognition_schemas.ShowRekognitionResult],
            summary="get_all_rekognition_result_list" + " | " + get_summary_location())
def get_all_rekognition_result_list(user_id: int, db: Session = Depends(get_db)):
    '''
    ### 설명
    - 해당 유저의 rekognition 결과들을 전부 요청하는 API
    ### 관련 모델
    - User, Rekognition
    '''
    return rekognition_repository.get_all_rekognition_result_list(user_id, db)


@router.get('/result/duration', status_code=status.HTTP_200_OK,
            response_model=List[rekognition_schemas.ShowRekognitionResult],
            summary="get_rekognition_by_duration" + " | " + get_summary_location())
def get_rekognition_result_list_by_duration(user_id: int, duration_second: Optional[int] = None,
                                            db: Session = Depends(get_db)):
    '''
    ### 설명
    - 해당 유저의 rekognition 결과 중 일정 시간 전(default 2초, duration_second 에서 지정) 까지의 결과를 반환하는 API
    ### 관련 모델
    - User, Rekognition
    '''
    return rekognition_repository.get_rekognition_result_list_by_duration(user_id, duration_second, db)
