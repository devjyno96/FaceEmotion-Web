import os

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

from .. import database

from ..repository import user

from ..schemas import user as schemas

from ..routers.routers_function import get_summary_location

router = APIRouter(
    prefix='/user',
    tags=['User']
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, responses={
    409: {
        "description": "Error: Conflict",
    },
},
             summary='create' + " | " + get_summary_location())
def create(request: schemas.CreateUser, db: Session = Depends(get_db)):
    """
    ### 설명
    - User 생성
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - name : User 의 name
    - is_admin : User 의 admin 여부(true, false 둘 중 하나)
    ### 관련 모델
    - User
    """
    return user.create(request, db)


@router.get('/identifier', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary='check_id' + " | " + get_summary_location())
def check_id(username: str, db: Session = Depends(get_db)):
    """
    ### 설명
    - username 있는지 확인
    - username 는 email(아이디)을 의미함
    ### 파라미터
    - username : User 의 아이디
    ### 관련 모델
    - User
    """

    return user.show_by_name(username, db)


@router.post('/login', status_code=status.HTTP_200_OK, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary='login' + " | " + get_summary_location())
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    ### 설명
    - login 확인 후 token 반환
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - 기타 로그인 관련 파라미터들
    ### 관련 모델
    - User
    """
    return user.login(request, db)


@router.put('/password', status_code=status.HTTP_200_OK, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary='change_pw' + " | " + get_summary_location())
def change_pw(request: schemas.ChangePassword, db: Session = Depends(database.get_db)):
    """
    ### 설명
    - password 변경
    ### Request Body
    - username : User 의 아이디
    - new_password : 새로운 패스워드
    - check_password: 새로운 패스워드 확인
    ### 관련 모델
    - User
    """

    return user.change_password(request, db)


@router.put('/password/init', status_code=status.HTTP_200_OK, summary='init_pw' + " | " + get_summary_location())
def init_pw():
    """
    ### 설명
    - password 초기화
    - 아직 구현 안됨
    ### 관련 모델
    - User
    """
    pass


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary='delete' + " | " + get_summary_location())
def delete(user_id: int, db: Session = Depends(database.get_db)):
    """
    ### 설명
    - User 삭제
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    ### 관련 모델
    - User
    """
    return user.delete(user_id, db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/refresh', summary='refresh' + " | " + get_summary_location())
def refresh(Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    """
    ### 설명
    - refresh token 전송 시, 검증 후 access token 생성해줌
    ### 관련 모델
    - User
    - Refresh Token
    """
    return user.refresh_token(Authorize, db)
