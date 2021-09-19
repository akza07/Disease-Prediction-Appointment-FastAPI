from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer
from . import models, schemas
from jose import JWTError, jwt #JSON Web Token
from datetime import datetime, time, timedelta
import random
from passlib.hash import bcrypt


SECRET_KEY = 'e2c6a3bc1aad22372e102e8f9f657bccd65676aef94587815b9d4d2c4960a650'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_hashed_password(password: str):
    return bcrypt.hash(password)

def verify_hashed_password(password: str, password_hashed: str):
    return bcrypt.verify(password, password_hashed)

def get_user_by_email(db: Session, email: str):
    print("Checking existing users")
    return db.query(models.UserBase).filter(models.UserBase.email == email).first()



def get_user_by_id(db: Session, id: int):
    print("Checking existing users")
    return db.query(models.UserBase).filter(models.UserBase.id == id).first()



def is_doctor(db: Session, email: str):
    if get_doctor_by_email(db, email) is None:
        return False
    return True



def has_appointment(db: Session, id: int):
    return db.query(models.Consultation).filter(models.Consultation.user_id == id).first()




def get_doctor_by_specialization(db: Session, required_doctor: str):
    print(required_doctor)
    if required_doctor == "Other":
        required_doctor = "Physician"
    doc = db.query(models.Doctors).filter(models.Doctors.specialization == required_doctor).all()
    if doc is not None:
        rand = random.randint(1, len(doc))  # selecting random
        return doc[rand]
    return doc



def get_doctor_by_email(db: Session, email: str):
    return db.query(models.Doctors).filter(models.Doctors.email == email).first()



def get_doctor_by_id(db: Session, id: int):
    return db.query(models.Doctors).filter(models.Doctors.id == id).first()



def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = create_hashed_password(user.password)
    db_user = models.UserBase(
        # username = user.username,
        name = user.name,
        email = user.email,
        password_hashed = hashed_password,
        # is_active = True
    )
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    delattr(db_user, "password_hashed")
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

def make_appointment(db:Session, current_user_id:int, data: schemas.ConsultationData):

    appointment = models.Consultation(
        user_id = current_user_id,
        patient_name = get_user_by_id(db, current_user_id).name,
        doctor_id = get_doctor_by_specialization(db, data.required_doctor).id,
        required_doctor = data.required_doctor,
        symptoms = str(data.perceived_symptoms),
        predicted_disease = data.predicted_disease,
        status = False
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    # print(db.query(models.Consultation).filter(models.Consultation.user_id == current_user_id).first())
    return db.query(models.Consultation).filter(models.Consultation.user_id == current_user_id).first()

def get_patients_for_doctor(db: Session, id: int, skip: int = 0, limit: int = 100):
    # doc_info = db.query(models.Doctors).filter(models.Doctors.id == id)
    print(f"{id=}")
    patients = db.query(models.Consultation).filter(models.Consultation.doctor_id == id).offset(skip).limit(limit).all()
    return patients


def get_admin_by_mail(db:Session, email :str):
    return db.query(models.Admins).filter(models.Admins.email == email).first()

def add_doctor(db: Session, data: schemas.DoctorWithPassword):
    hashed_password = create_hashed_password(data.password)
    doctor_data = models.Doctors(
        name = data.name,
        email = data.email,
        password_hashed = hashed_password,
        specialization = data.specialization
    )
    db.add(doctor_data)
    db.commit()
    db.refresh(doctor_data)
    return db.query(models.Doctors).filter(models.Doctors.email == data.email).first()
