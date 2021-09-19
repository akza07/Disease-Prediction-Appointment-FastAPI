from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy.sql.sqltypes import Integer, String

class Symptoms(BaseModel):
    perceived_symptoms: List[str]

class UserData(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

    
class UserCreate(UserData):
    password: str

class ResponseUserData(UserData):
    token: str
    class Config:
        orm_mode = True

class ConsultationData(Symptoms):
    required_doctor: str
    predicted_disease: str 

class ConsultationResponse(BaseModel):
    appointment_id :int
    user_id :int
    patient_name: str
    required_doctor :str
    symptoms: str
    predicted_disease: str
    doctor_id: int
    status: bool

    class Config:
        orm_mode = True

class DoctorData(BaseModel):
    id: int
    email: str
    name: str
    specialization: str

class DoctorWithPassword(DoctorData):
    password: str

class DeleteAppointmentRequest(BaseModel):
    id: int