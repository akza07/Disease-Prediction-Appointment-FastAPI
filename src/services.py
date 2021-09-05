from typing import Optional
from sqlalchemy.orm import Session, relation
from . import models, schemas
from jose import JWTError, jwt #JSON Web Token
from datetime import datetime, time, timedelta

SECRET_KEY = 'e2c6a3bc1aad22372e102e8f9f657bccd65676aef94587815b9d4d2c4960a650'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_by_email(db: Session, email: str):
    print("Checking existing users")
    return db.query(models.UserBase).filter(models.UserBase.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password+"temp_pwd"
    db_user = models.UserBase(
        # username = user.username,
        name = user.name,
        email = user.email,
        password = fake_hashed_password,
        is_active = True
    )
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt