from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.base import engine, Base
from models import *
from influxdb_client import Point
from utils.jwt import get_hashed_password, create_access_token, create_refresh_token, verify_password
import base64
import uuid
from sqlalchemy.orm import Session
from services.mqtt import *
from services.influxdb import *
from schemas import UserResponse, UserCreate
from services.users import create_user
from deps import get_current_user
import time
from fastapi.middleware.cors import CORSMiddleware
import requests
import threading
import requests
from routers import alert_service, influx, phone_number, telegram_account, user

SMSCHEF_API_KEY = "cda7a6cbe5e82668ae4b3f6c080e7580b6894a2e"

# app initialization
def start_mqtt():
    mqtt_client.loop_start()
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    run_populate()
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.start()
    yield
    mqtt_client.disconnect()
    mqtt_thread.join()
origins = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1",
    "http://localhost:8080",
    "http://localhost",
    "https://floodalert.live",
    "https://dashboard.floodalert.live",
    "https://telegram.floodalert.live",
]
app = FastAPI(
    title="MRC Flash Floods Monitoring API Application",             
    description="This is an API application serves as a backend.",  
    version="1.0.0",                    
    contact={
        "name": "Support Team",
        "tel": "+855-17-701-656",
        "email": "support@floodalert.live",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mqtt setup
def on_mqtt_connect(client, userdata, flags, rc, properties=None):
    print("CONNECT received with code %s." % rc)
    mqtt_client.subscribe('mrc/bassac')
image_string = ""
last_received_time = time.time()
def on_mqtt_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    topic = str(msg.topic)
    payload = str(msg.payload.decode('utf-8'))
    measurement = payload.split("-")[1]
    value = payload.split("-")[2]
    station = topic.split("/")[1]
    if measurement != "image":
        value = float(value)
        data = Point(measurement).tag("station", station).field("data", value)
        if writeInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, data):
            print(f"Write data of measurement : {measurement} from station : {station} with value : {value} to influxdb.")
    else:
        global image_string
        global last_received_time
        if value == "reset":
            byte_string = image_string.encode('utf-8')
            image_data = base64.b64decode(byte_string)
            name = uuid.uuid4()
            with open(f"static/images/{name}.jpg", 'wb') as file:
                file.write(image_data)
                file.close()
            data = Point(measurement).tag("station", station).field("data", str(name))
            if writeInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, data):
                print(f"Write data of measurement : {measurement} from station : {station} with value : {value} to influxdb.")
            image_string = ""
        else:
            image_string = image_string + value
mqtt_client.on_connect = on_mqtt_connect    
mqtt_client.on_message = on_mqtt_message


# define endpoints
app.include_router(user.router, prefix="/api/users", tags=["Users"], dependencies=[Depends(get_current_user)])
app.include_router(telegram_account.router, prefix="/api/telegram_accounts", tags=["Telegram Accounts"], dependencies=[Depends(get_current_user)])
app.include_router(phone_number.router, prefix="/api/phone_numbers", tags=["Phone Numbers"], dependencies=[Depends(get_current_user)])
app.include_router(alert_service.router, prefix="/api/alert_services", tags=["Alert Services"], dependencies=[Depends(get_current_user)])
app.include_router(influx.router, prefix="/api/influxs", tags=["InfluxDB"], dependencies=[Depends(get_current_user)])

@app.post("/api/users", tags=["Users"], response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.post('/api/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.password),
    }

@app.get("/api/pred-water-level")
async def pred_water_level(forward:int, authicated_user = Depends(get_current_user)):
    url = f"https://kay168-water-level-forecast.hf.space/predict?forward={forward}"
    response = requests.get(url)
    if response.status_code == 200:
        return {
            'data':response.json()
        }
    else:
        return {
            "message": response.text
        }
    
@app.post("/api/send-sms")
def send_sms(phone_number: str, message: str, authicated_user = Depends(get_current_user)):
    message = {
        "secret": SMSCHEF_API_KEY,
        "mode": "devices",
        "device": "00000000-0000-0000-e0c6-005ce3802ab9",
        "sim": 1,
        "priority": 1,
        "phone": phone_number,
        "message": message
    }
    response = requests.get(url = "https://www.cloud.smschef.com/api/send/sms", params = message)
    if response.status_code == 200:
        return {
            'data':response.json()
        }
    else:
        return {
            "message": response.text
        }
    
