from datetime import datetime
import json
import os
from dotenv import load_dotenv

from factory import HistoryFactory
from mqtt_publisher.publisher import publish

CONNECTION_STRING = f"dbname={os.getenv('BD_NAME')} user={os.getenv('BD_USER')} password={os.getenv('BD_PASSWORD')} host={os.getenv('BD_HOST')} port={os.getenv('BD_PORT')}"

load_dotenv(override=True)
history = HistoryFactory().get_history(use_db=True, connection_string=CONNECTION_STRING)

REQ_TOPIC = os.getenv("REQ_TOPIC")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} connected to broker sucessfully")
        client.subscribe(f"{REQ_TOPIC}")
        client.subscribe(f"{REQ_TOPIC}/get")
        
    else:
        print(f"Connection failed with code {rc}")
        
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} subscribed to topic with mid {mid} and QOS {granted_qos} on {REQ_TOPIC}")

def on_message(client, userdata, message):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] Received a message on topic {message.topic}")
    
    if message.topic == f"{REQ_TOPIC}":
        data = message.payload.decode()
        data_converted = json.loads(data)
        print(data_converted)
        history.add_history(data_converted["command"], data_converted["response"])
        publish(data_converted["response"])   