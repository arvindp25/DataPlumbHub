import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8080/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server!")
        response = await websocket.recv()
        print(response)

asyncio.run(test_ws())
