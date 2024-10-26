import paho.mqtt.client as paho
from paho import mqtt

MQTT_CLUSTER_URL = "620e8b73916a4c0faabaa8b1e3f4812f.s1.eu.hivemq.cloud"
MQTT_CLUSTER_PORT = 8883
MQTT_CLUSTER_USERNAME = "raychannudam"
MQTT_CLUSTER_PASSWORD = "Ranger@2002"


# MQTT_CLUSTER_URL = "localhost"
# MQTT_CLUSTER_PORT = 1883
# MQTT_CLUSTER_USERNAME = "admin"
# MQTT_CLUSTER_PASSWORD = "admin"


def on_mqtt_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_mqtt_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


mqtt_client = paho.Client(client_id="backend_server", userdata=None, protocol=paho.MQTTv5)
mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
mqtt_client.username_pw_set(MQTT_CLUSTER_USERNAME, MQTT_CLUSTER_PASSWORD)
mqtt_client.connect(MQTT_CLUSTER_URL, MQTT_CLUSTER_PORT)
mqtt_client.on_subscribe = on_mqtt_subscribe
mqtt_client.on_publish = on_mqtt_publish
        








