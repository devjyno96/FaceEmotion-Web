from sqlalchemy import MetaData

from . import control
from ..database import engine, get_db


def create_all():
    file.Base.metadata.create_all(bind=engine)


def delete_all():
    file.Base.metadata.drop_all(bind=engine)