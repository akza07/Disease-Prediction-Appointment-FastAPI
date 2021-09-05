from pydantic import BaseModel
from typing import Optional, List

class Symptoms(BaseModel):
    percieved_symptoms: List[str]

class User(BaseModel):
    # username: str
    is_active: Optional[bool]

class UserData(User):
    name: str
    email: str
    class Config:
        orm_mode = True

class UserCreate(UserData):
    password: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
