import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import time
import psycopg2
import json

load_dotenv()

MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')

conn = psycopg2.connect(database = "postgres",
                        user = "admin",
                        password = "admin",
                        host = "postgres",
                        port = "5432")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code: {reason_code}")
    client.subscribe("azi/dat/lens_bot/#")
    print(f"Subscribed to: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    print(str(msg.qos) + " " + msg.topic+" "+str(msg.payload))

    query = """
        INSERT INTO mqtt_logs (mqtt_topic, mqtt_content)
        VALUES (%s, %s)
    """

    msg_payload = msg.payload.decode()
    json_msg = json.dumps(msg_payload)
    
    args = [msg.topic, json_msg]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()
    
def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))
    
def on_log(mqttc, obj, level, string):
    print(string)

# on_disconnect
# on_pre_connect

# Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log

# client.tls_set()
# client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
# client.will_set()
mqttc.connect("test.mosquitto.org", 1883, 60)

mqttc.loop_forever()
