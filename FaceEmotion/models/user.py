from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

    name = Column(String)
    is_admin = Column(Boolean, default=False)

    # One To One
    refresh_token = relationship("RefreshToken", uselist=False, back_populates="user")

    # 1 : N
    rekognition_result = relationship("RekognitionResult", back_populates="user", passive_deletes=True)



class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user = relationship("User", back_populates="refresh_token")

    token = Column(String)
