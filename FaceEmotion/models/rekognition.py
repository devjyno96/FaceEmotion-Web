from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from ..database import Base

from .models_function import get_now_time


class RekognitionResult(Base):
    __tablename__ = 'rekognition_results'

    rekognition_result_id = Column(Integer, primary_key=True, index=True)
    # 각 수치는 확룰을 의미합니다
    smile = Column(Float)

    happy = Column(Float, nullable=True)
    confused = Column(Float, nullable=True)
    disgusted = Column(Float, nullable=True)
    surprised = Column(Float, nullable=True)
    clam = Column(Float, nullable=True)
    angry = Column(Float, nullable=True)
    sad = Column(Float, nullable=True)
    fear = Column(Float, nullable=True)

    created_time = Column(DateTime, default=get_now_time)

    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    user = relationship("User", back_populates="rekognition_result", passive_deletes=True)
