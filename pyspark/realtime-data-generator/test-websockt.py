import asyncio
import websockets
import json


async def connect():
    uri = "ws://localhost:8080/ws"
    uri = "wss://mock-data-generator-822350334323.asia-south1.run.app/ws"
    headers = {"api_key": "Ex2ZUw6brnTro5FZADh1aVWvxbsmLn0i2k1GxrdElTIuZEKEPbqGTD4ogZclR4mw5OeJswMNa35SD1oOD8qHcuvpGn1uEHRjaTrAdVrJ51BZ6CGhU10i3aIfZaDRNCad"}


    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(headers))
        response = await websocket.recv()
        print(response)

asyncio.run(connect())
