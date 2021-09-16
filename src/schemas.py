from pydantic import BaseModel
from typing import Optional, List

class Symptoms(BaseModel):
    perceived_symptoms: List[str]

class UserData(BaseModel):
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

class Consultation_data(Symptoms):
    required_doctor: str
