from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.security import HTTPBasicCredentials
from google.cloud import pubsub_v1
import secrets
from fastapi import FastAPI, WebSocket
import json
import random
from datetime import datetime, timezone
import os
import uuid
app = FastAPI()
API_KEY = os.getenv("API_KEY")
project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("PUB_SUB_TOPIC")
publisher = pubsub_v1.PublisherClient(
)
topic_path = publisher.topic_path(project_id, topic_id, enable_message_ordering=True)

def generate_complex_iot_data():
    return {
        "device_id": f"machine_{random.randint(100, 999)}",
        "device_type": random.choice(["industrial_robot", "CNC_machine", "conveyor_belt"]),
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "location": {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "factory_section": random.choice(["assembly_line_A", "packaging_B", "quality_control_C"])
        },
        "sensors": {
            "temperature": {
                "value": round(random.uniform(50, 120), 2),
                "unit": "C",
                "status": random.choice(["normal", "warning", "critical"])
            },
            "vibration": {
                "value": round(random.uniform(0, 5), 2),
                "unit": "mm/s",
                "status": random.choice(["normal", "warning", "critical"])
            },
            "energy_consumption": {
                "value": round(random.uniform(2, 10), 2),
                "unit": "kWh",
                "status": "normal"
            },
            "pressure": {
                "value": round(random.uniform(900, 1100), 2),
                "unit": "hPa",
                "status": random.choice(["normal", "warning", "critical"])
            }
        },
        "alerts": [
            {
                "type": "pressure",
                "severity": "critical",
                "message": "Pressure too high! Immediate action required",
                "timestamp":  datetime.now(timezone.utc).isoformat()
            }
        ] if random.random() < 0.3 else [],  # 30% chance of an alert
        "status": random.choice(["operational", "maintenance_required", "faulty"]),
        "battery_level": random.randint(10, 100),
        "network": {
            "signal_strength": random.randint(-90, -40),
            "connection_type": random.choice(["WiFi", "LTE", "5G"])
        },
        "metadata": {
            "firmware_version": f"3.{random.randint(0,9)}.{random.randint(0,9)}",
            "last_maintenance":  datetime.now(timezone.utc).isoformat(),
            "operating_hours": random.randint(1000, 5000),
            "warranty_valid": random.choice([True, False])
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Wait for authentication message
    auth_message = await websocket.receive_json()
    if auth_message.get("api_key") != API_KEY:
        await websocket.close(code=1008)
        return

    try:
        while True:
            order_key = uuid.uuid4()
            data = generate_complex_iot_data()
            message = (data,order_key)
            data = json.dumps(message[0]).encode("utf-8")
            ordering_key = message[1]
            # When you publish a message, the client returns a future.
            future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
            await websocket.send_json(data)
    except WebSocketDisconnect:
        print("Client disconnected")
