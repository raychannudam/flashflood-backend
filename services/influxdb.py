import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pytz
cambodia_tz = pytz.timezone('Asia/Phnom_Penh')


INFLUXDB_TOKEN="fgB6MHfAZd25DoxbFVOHUJXtvLxXD4hZMm6QCckn8TEJhL7nO0GnRFSBAvxYU_o7lq9nyaksg2spvhV-a5EF-A=="
INFLUXDB_ORG = "ASEAN-MRC-TECHNOLOGY"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_BUCKET = "sensors"
INFLUXDB_WRITE_CLIENT = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)


def writeInfluxData(write_client, bucket, org, data):
    try:
        write_api  = write_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, data)
        return True
    except Exception as e:
        print("Fail to write data to influx in bucket", bucket)
        print(e)
        return False
    
def getInfluxData(write_client, bucket, org, station, range:str="5m", measurement=""):
    try:
        query_api = write_client.query_api() 
        if measurement !="":
            query = f"""from(bucket: "{bucket}") 
                    |> range(start: -{range}) 
                    |> filter(fn: (r) => 
                        r.station == "{station}" and
                        r._measurement == "{measurement}")"""
        else:
            query = f"""
                    from(bucket: "{bucket}") 
                    |> range(start: -{range}) 
                    |> filter(fn: (r) => 
                        r.station == "{station}")
                    """
        tables = query_api.query(query, org=org)
        response = []
        for items in tables:
            for data in items.records:
                utc_time = data.get_time()
                utc_start = data.get_start()
                utc_stop = data.get_stop()
                data.values["_time"] = utc_time.astimezone(cambodia_tz)
                data.values["_start"] = utc_start.astimezone(cambodia_tz)
                data.values["_stop"] = utc_stop.astimezone(cambodia_tz)
                response.append(data.values)
        return {
            "data": response,
            "meta": {
                "counts": len(response)
            }
        }
    except Exception as e:
        print("Fail to get data from influx in bucket", bucket)
        print(e)
        return e
        







