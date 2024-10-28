from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreate, UserResponse, InfluxDataCreate, ImageCreate
from databases import User, get_db
from influxdb_client import Point
from utils.jwt import get_hashed_password, create_access_token, create_refresh_token, verify_password
import base64
import os
import uuid
from sqlalchemy.orm import Session
from services import *
from deps import get_current_user
import time
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt_client.loop_start()
    yield
    mqtt_client.loop_stop()

origins = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1",
    "http://localhost:8080",
    "http://localhost",
    "http://floodalert.live",
    "https://floodalert.live",
    "http://dashboard.floodalert.live",
    "https://dashboard.floodalert.live",

]


# app
app = FastAPI(
    title="MRC Flash Floods Monitoring API Application",             
    description="This is an API application serves as a backend.",  
    version="1.0.0",                    
    contact={
        "name": "Support Team",
        "tel": "+855-17-701-656",
        "email": "channudam.2002@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# mqtt
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




# endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = get_hashed_password(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, is_authenticated = Depends(get_current_user),  db: Session = Depends(get_db)):
    if (is_authenticated):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

@app.post('/login', summary="Create access and refresh tokens for user")
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


@app.get("/influx")
async def get_influx_data(station, range, measurement,  is_authenticated = Depends(get_current_user)):
    result = getInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, station, range, measurement)
    return result

@app.get("/influx/image")
async def get_image_data(station, range, is_authenticated = Depends(get_current_user)):
    result = getInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, station, range, "image")
    image_name = result['data'][0]['_value'] + ".jpg"
    file_path = os.path.join("static/images", image_name)
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="image/jpeg")
    return {
        "message": "Image not found"
    }

@app.post("/influx")
async def store_influx_data(data: InfluxDataCreate,  is_authenticated = Depends(get_current_user)):
    data_point = (
        Point(data.measurement).tag("station", data.station).field("value", data.value)
    )
    if writeInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, data_point):
        return {
            "response": "success"
        }, 200
    return {
        "response": "fail"
    }, 500

@app.get("/pred-water-level")
async def pred_water_level(forward:int, is_authenticated = Depends(get_current_user)):
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
    
