from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from services.influxdb import *
from schemas import InfluxDataCreate
from deps import get_current_user
import os
from influxdb_client import Point

router = APIRouter()

@router.get("/")
async def get_influx_data(station, range, measurement):
    result = getInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, station, range, measurement)
    return result

# @router.post("/")
# async def store_influx_data(data: InfluxDataCreate,  authicated_user = Depends(get_current_user)):
#     data_point = (
#         Point(data.measurement).tag("station", data.station).field("value", data.value)
#     )
#     if writeInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, data_point):
#         return {
#             "response": "success"
#         }, 200
#     return {
#         "response": "fail"
#     }, 500

@router.get("/image")
async def get_image_data(station, range):
    result = getInfluxData(INFLUXDB_WRITE_CLIENT, INFLUXDB_BUCKET, INFLUXDB_ORG, station, range, "image")
    if len(result['data']) > 0:
        image_name = result['data'][0]['_value'] + ".jpg"
        file_path = os.path.join("static/images", image_name)
        if os.path.isfile(file_path):
            return FileResponse(file_path, media_type="image/jpeg")
        return {
            "message": "Image not found"
        }
    else:
        return {
            "message": "Image not found"
        }