import joblib as jb
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.sqltypes import Integer

from .schemas import Symptoms, TokenData
from sqlalchemy.orm import Session
from . import services, schemas, models
from .database import SessionLocal, engine

from datetime import timedelta, time
from jose import JWTError,jwt


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

model = jb.load('trained_model')

@app.post('/token', response_model=schemas.Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = services.get_user_by_email(db, form_data.username)
    if not user_dict:
        user_dict = services.get_doctor_by_email(db, form_data.username)
    if not user_dict:
        user_dict = services.get_admin_by_mail(db,form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #hashed_pwd = services.create_hashed_password(form_data.password)
    if not services.verify_hashed_password(form_data.password, user_dict.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user_dict.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
# input sample for tb
#perceived_symptoms = {["chest_pain","cough","fatigue","high_fever","loss_of_appetite","malaise","sweating","weight_loss","swelled_lymph_nodes"]}

@app.post("/check_disease/")
async def check_disease( symptoms: Symptoms):
    #print (f"{perceived_symptoms=}")

    #disease_list = [
        #'Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
        #'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
        #'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
        #'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
        #'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis', 'Arthritis',
        #'(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo'
        #]
    symptoms_list = [
        'itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
        'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
        'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
        'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
        'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
        'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
        'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
        'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
        'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
        'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
        'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
        'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
        'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
        'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
        'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
        'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
        'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
        'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
        'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
        'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
        'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
        'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
        'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
        'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
        'yellow_crust_ooze'
        ]
    Rheumatologist = ['Osteoarthristis','Arthritis']
       
    Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
    
    ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

    Orthopedist = []

    Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

    Allergist_Immunologist = ['Allergy','Pneumonia','AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

    Urologist = [ 'Urinary tract infection','Dimorphic hemmorhoids(piles)']

    Dermatologist = ['Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

    Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
    'Alcoholic hepatitis','Jaundice','hepatitis A','Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']

    

    # init all array values to 0
    test_symptoms = [0]*len(symptoms_list)
    for i in range(len(symptoms_list)):
        for p_symptom in symptoms.perceived_symptoms:
            if  p_symptom == symptoms_list[i]:
                test_symptoms[i] = 1
    input_test = [ test_symptoms ]
    disease =  model.predict(input_test)[0]

    if disease in Rheumatologist :
           specialist = "Rheumatologist"
           
    if disease in Cardiologist :
        specialist = "Cardiologist"
        

    elif disease in ENT_specialist :
        specialist = "ENT specialist"
    
    elif disease in Orthopedist :
        specialist = "Orthopedist"
    
    elif disease in Neurologist :
        specialist = "Neurologist"
    
    elif disease in Allergist_Immunologist :
        specialist = "Allergist/Immunologist"
    
    elif disease in Urologist :
        specialist = "Urologist"
    
    elif disease in Dermatologist :
        specialist = "Dermatologist"
    
    elif disease in Gastroenterologist :
        specialist = "Gastroenterologist"
    
    else :
        specialist = "Other"

    result = schemas.ConsultationData(
        perceived_symptoms = symptoms.perceived_symptoms,
        predicted_disease = disease,
        required_doctor = specialist
    )
    return result


@app.post('/signup')
async def create_user(user_data: schemas.UserCreate,  db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user_data.email)
    if db_user:
         HTTPException(status_code=400, detail="E-mail already Registered")
    access_token_expires = timedelta(minutes=services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )
    data = services.create_user(db, user_data)
    data.token = access_token
    return data



@app.post('/me')
async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not Validate the credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, services.SECRET_KEY, algorithms=[services.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username = email)
    except JWTError:
        raise credentials_exception

    if services.is_doctor(db, token_data.username):
        user = services.get_doctor_by_email(db, token_data.username)
        delattr(user, "password_hashed")
        return {
            "my_info" : user,
            "role" : "doctor"
        }
    
    if services.get_admin(db, token_data.username):
        return {
            "my_info": token_data.username,
            "role" : "admin"
        }


    user = services.get_user_by_email(db, token_data.username)
    appointment = services.has_appointment(db, user.id)
    delattr(user, "password_hashed")
    if appointment is not None:
        appointment.doctor_name = services.get_doctor_by_id(db, appointment.doctor_id).name
    return {
        "my_info": services.get_user_by_email(db, token_data.username),
        "appointment" : appointment,
        "role":"user"
    }

@app.put('/appointment/add')
async def make_appointment(data:schemas.ConsultationData, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
    status_code=401,
    detail="Could not Validate the credentials",
    headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, services.SECRET_KEY, algorithms=[services.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username = email)
    except JWTError:
        raise credentials_exception
    user = services.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    if services.has_appointment(db, user.id):
        raise HTTPException(status_code=400, detail="User already has an Appointment")
    if services.get_doctor_by_specialization(db, data.required_doctor) is None:
        raise HTTPException(status_code=500, detail="NO_DOCTOR_AVAILABLE")
    appointment = services.make_appointment(db, user.id, data)
    return {
        "appointment" : appointment,
        "doctor" : services.get_doctor_by_id(db, appointment.doctor_id).name
    }

@app.post('/doctor/show_patients', response_model = List[schemas.ConsultationResponse])
async def show_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=401,
    detail="Could not Validate the credentials",
    headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, services.SECRET_KEY, algorithms=[services.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(username = email)
    except JWTError:
        raise credentials_exception
    doctor = services.get_doctor_by_email(db, email=token_data.username)
    if doctor is None:
        raise credentials_exception
    return services.get_patients_for_doctor(db, doctor.id)


@app.put('/admin/add_doctor')
async def add_doctor(doctor_data: schemas.DoctorWithPassword, token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    response = services.add_doctor(db, doctor_data)
    delattr(response, "password_hashed")
    return{
        "status": "Doctor added successfully!",
        "info" : response
    }

@app.delete('/appointment/delete')
async def delete_appointment(data : dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    services.delete_appointment(db, data.id)




    

    
    

    



        


