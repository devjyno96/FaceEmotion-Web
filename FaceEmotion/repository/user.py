from datetime import timedelta

from fastapi import HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from sqlalchemy.orm import Session

from ..models import user as models

from ..schemas import user as user_schemas

from ..hashing import Hash


def create(request: user_schemas.CreateUser, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Username {request.username} is already used')
    new_user = models.User(username=request.username,
                           password=Hash.bcrypt(request.password),
                           name=request.name,
                           is_admin=request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return user


def show_by_name(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def login(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Incorrect password')
    # generate a jwt token and return

    # generate refresh token
    Authorize = AuthJWT()
    access_token = Authorize.create_access_token(algorithm="HS256", subject=user.username, expires_time=timedelta(seconds=60))
    refresh_token = Authorize.create_refresh_token(algorithm="HS256",subject=user.username, expires_time=timedelta(seconds=60))

    # if token already exist in DB == delete and create token
    refresh_token_db = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id)
    if refresh_token_db.first():
        refresh_token_db.delete()
        db.commit()

    # refresh token create and save to DB
    refresh_token_db = models.RefreshToken(
        user_id=user.id,
        token=refresh_token
    )
    db.add(refresh_token_db)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def change_password(request: user_schemas.ChangePassword, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    if request.new_password != request.check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password does not matched')
    user.password = Hash.bcrypt(request.new_password)
    db.commit()
    return "done"


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')

    user.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def refresh_token(Authorize: AuthJWT, db: Session):
    # Refresh Token
    try:
        Authorize.jwt_refresh_token_required()
    except JWTDecodeError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Token is not Refresh Token')

    try:
        Authorize.get_raw_jwt()
    except JWTDecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Refresh Token is not available')

    # user의 refresh token이랑 jti 값이 동일한지 확인
    user = db.query(models.User).filter(models.User.username == Authorize.get_jwt_subject()).first()
    refresh_token_db = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id).first()

    if Authorize.get_jti(refresh_token_db.token) != Authorize.get_raw_jwt()['jti']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Refresh Token does not Matched')

    new_access_token = Authorize.create_access_token(subject=Authorize.get_jwt_subject())

    return {"access_token": new_access_token}
