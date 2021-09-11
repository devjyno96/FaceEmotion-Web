from sqlalchemy import MetaData

from . import rekognition, user
from ..database import engine, get_db


def create_all():
    user.Base.metadata.create_all(bind=engine)
    rekognition.Base.metadata.create_all(bind=engine)


def delete_all():
    user.Base.metadata.drop_all(bind=engine)
    rekognition.Base.metadata.drop_all(bind=engine)