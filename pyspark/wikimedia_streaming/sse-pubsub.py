# main.py
import requests
from requests_sse import EventSource
import json
import os
from flask import Flask
from google.cloud import pubsub_v1
import threading

app = Flask(__name__)

project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("PUB_SUB_TOPIC")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def stream_and_publish():
    try:
        with EventSource("https://stream.wikimedia.org/v2/stream/recentchange", timeout=30) as event_source:
            for event in event_source:
                data = json.loads(event.data)
                payload = json.dumps(data).encode("utf-8")
                publisher.publish(topic_path, payload)
                print("Published")
    except Exception as e:
        print(f"Exception: {e}")

@app.route("/")
def home():
    return "Service is up!"

@app.route("/start")
def start_streaming():
    thread = threading.Thread(target=stream_and_publish)
    thread.start()
    return "Started streaming."
