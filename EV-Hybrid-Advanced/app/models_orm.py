from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, nullable=True)
    input_json = Column(String, nullable=True)
    output_label = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
