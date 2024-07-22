import json
import os
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

conn = psycopg2.connect(database = POSTGRES_DB,
                        user = POSTGRES_USER,
                        password = POSTGRES_PASSWORD,
                        host = "postgres",
                        port = "5432")

def on_connect(client, userdata, flags, reason_code, properties):
    
    # subscribe to given topic
    client.subscribe(MQTT_TOPIC, qos=2)
    
    # log sucessful connection
    query = """
        INSERT INTO mqtt_logs (mqtt_log, mqtt_local_datetime)
        VALUES (%s, %s)
    """

    # get local datime with timezone (utc)
    naive_dt = datetime.now()
    
    args = [f"Connected with result code: {reason_code}", naive_dt]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()

def on_message(client, userdata, msg):

    # log incoming message
    query = """
        INSERT INTO mqtt_logs (mqtt_log, mqtt_local_datetime, mqtt_topic, mqtt_content)
        VALUES (%s, %s, %s, %s)
    """

    # get local datime with timezone (utc)
    naive_dt = datetime.now()

    # convert message into jsonb format
    msg_payload = msg.payload.decode()
    json_msg = json.dumps(msg_payload)
    
    args = [f"Message with QoS: {msg.qos}", naive_dt, msg.topic, json_msg]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()
    
def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    
    # log sucessful subscription
    query = """
        INSERT INTO mqtt_logs (mqtt_log, mqtt_local_datetime)
        VALUES (%s, %s)
    """

    # get local datime with timezone (utc)
    naive_dt = datetime.now()
    
    args = [f"Subscribed: {mid}, {reason_code_list}", naive_dt]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()
    
def on_log(mqttc, obj, level, string):

    # log logging object
    query = """
        INSERT INTO mqtt_logs (mqtt_log, mqtt_local_datetime)
        VALUES (%s, %s)
    """

    # get local datime with timezone (utc)
    naive_dt = datetime.now()
    
    args = [f"Log: {string}", naive_dt]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()

def on_disconnect(client, userdata, rc):

    # log disconnection
    query = """
        INSERT INTO mqtt_logs (mqtt_log, mqtt_local_datetime)
        VALUES (%s, %s)
    """

    # get local datime with timezone (utc)
    naive_dt = datetime.now()
    
    args = [f"Disconnected: {rc}", naive_dt]
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(query, args)
    cursor.close()

# Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTProtocolVersion.MQTTv5)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
# mqttc.on_disconnect = on_disconnect

# mqttc.tls_set() # requires certificates
# client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
# client.will_set() # last will / testament
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

mqttc.loop_forever()
