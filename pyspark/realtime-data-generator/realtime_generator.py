from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.security import HTTPBasicCredentials
import secrets
from fastapi import FastAPI, WebSocket
import json
import random
from datetime import datetime, timezone
import os
app = FastAPI()
API_KEY = os.getenv("APIKEY")

# Function to authenticate API key
def authenticate_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

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
async def websocket_endpoint(websocket: WebSocket, api_key: str = None):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API key missing")

    # Authenticate the API key
    authenticate_api_key(api_key)
    await websocket.accept()
    while True:
        data = generate_complex_iot_data()
        await websocket.send_json(data)
