import sys
from typing import List

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

@router.get('/', status_code=status.HTTP_201_CREATED, summary="get_html_rekognition" + " | " + get_summary_location())
def get_html_rekognition(request: Request,db: Session = Depends(get_db)):
    '''
    ### 설명
    - rekognition html 요청
    ### 관련 모델
    - None
    '''
    return templates.TemplateResponse("rekognition.html", {"request": request})


@router.post('/', status_code=status.HTTP_201_CREATED, summary="request_rekognition" + " | " + get_summary_location())
def request_rekognition(byte_image: bytes = File(...), db: Session = Depends(get_db)):
    '''
    ### 설명
    - Amazon Rekognition 을 요청하고 그 결과를 받는 api
    - 분석에 1초 정도 소요됨
    ### 관련 모델
    - user, rekognition_result
    '''
    print('test')
    return rekognition_repository.request_rekognition(byte_image, db)


@router.get('/result', status_code=status.HTTP_201_CREATED, summary="get_rekognition" + " | " + get_summary_location())
def get_rekognition(db: Session = Depends(get_db)):
    '''
    ### 설명
    - s3에서 pcap file list를 받아와 job과 task를 생성하는 API
    ### 관련 모델
    - Job, Task
    '''
    pass


@router.get('/result/all', status_code=status.HTTP_201_CREATED,
            summary="get_all_rekognitions" + " | " + get_summary_location())
def get_all_rekognitions(db: Session = Depends(get_db)):
    '''
    ### 설명
    - s3에서 pcap file list를 받아와 job과 task를 생성하는 API
    ### 관련 모델
    - Job, Task
    '''
    pass


@router.get('/result/duration', status_code=status.HTTP_201_CREATED,
            summary="get_rekognition_by_duration" + " | " + get_summary_location())
def get_rekognition_by_duration(db: Session = Depends(get_db)):
    '''
    ### 설명
    - s3에서 pcap file list를 받아와 job과 task를 생성하는 API
    ### 관련 모델
    - Job, Task
    '''
    pass


@router.delete('/result', status_code=status.HTTP_201_CREATED,
               summary="delete_rekognition" + " | " + get_summary_location())
def delete_rekognition(db: Session = Depends(get_db)):
    '''
    ### 설명
    - s3에서 pcap file list를 받아와 job과 task를 생성하는 API
    ### 관련 모델
    - Job, Task
    '''
    pass
