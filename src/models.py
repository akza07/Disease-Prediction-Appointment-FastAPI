from .database import Base

from sqlalchemy import Column, Integer, String, Boolean

class UserBase(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean)
    
    class Config:
        orm_mode = True

class Doctors(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
