import asyncio
import websockets
import json
import os

async def connect():
 
    headers = {"api_key": os.getenv("API_KEY", "yzptTfIM2rpF5tXt9plNxHx61CVS7tEraMYYJLsQNB2MnOe7gxNTSdCyMIRt8SqAkuQJWACIYpxxLNFhoQ2nkcoT2jtvaducsQPOi2sglIquqZTTudEHKEgimXhdV6NI")}

    uri = "wss://mock-data-generator-822350334323.asia-south1.run.app/ws"
 
    async with websockets.connect(uri) as websocket:
 
        await websocket.send(json.dumps(headers))
 
        response = await websocket.recv()
 
        print(response)
 

 
asyncio.run(connect())