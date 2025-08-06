# backend/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    gender = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

    saju_logs = relationship("SajuLog", back_populates="user")


class SajuLog(Base):
    __tablename__ = "saju_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    year = Column(String(10))
    month = Column(String(10))
    day = Column(String(10))
    hour = Column(String(10))
    result = Column(Text)  # JSON 문자열로 저장 가능
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saju_logs")