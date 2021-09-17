from src.schemas import Symptoms
from typing import List, Optional
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base

from sqlalchemy import Column, Integer, String, Boolean

class UserBase(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hashed = Column(String)
    # is_active = Column(Boolean)
    consultation = relationship("Consultation", back_populates="users")
    
    class Config:
        orm_mode = True

class Doctors(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password_hashed = Column(String)
    name = Column(String)
    specialization = Column(String)
    # is_active = Column(Boolean)

    consultation = relationship("Consultation", back_populates="doctors")

class Consultation(Base):
    __tablename__ = "consultation"
    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_name = Column(String)
    required_doctor = Column(String)
    symptoms = Column(String)
    predicted_disease = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    status = Column(Boolean)

    doctors = relationship("Doctors", back_populates="consultation")
    users = relationship("UserBase", back_populates="consultation")