import asyncio
import websockets
import json


async def connect():
    uri = "ws://localhost:8080/ws"
    headers = {"api_key": "abc123"}


    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(headers))
        response = await websocket.recv()
        print(response)

asyncio.run(connect())
