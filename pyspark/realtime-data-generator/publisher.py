from google.cloud import pubsub_v1
import os
import websockets
import json
import asyncio
import uuid

project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("PUB_SUB_TOPIC")
API_KEY = os.getenv("API_KEY")

publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
# Sending messages to the same region ensures they are received in order
# even when multiple publishers are used.
client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
publisher = pubsub_v1.PublisherClient(
    publisher_options=publisher_options, client_options=client_options
)
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

async def connect():
    uri = "wss://mock-data-generator-822350334323.asia-south1.run.app/ws"
    headers = {"api_key": API_KEY}


    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(headers))
        response = await websocket.recv()
    return response

while True:
    order_id = uuid.uuid4()
    msg =asyncio.run(connect())
    # Data must be a bytestring
    message = (msg,order_id)
    data = message[0].encode("utf-8")
    ordering_key = message[1]
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
    print(future.result())

    print(f"Published messages with ordering keys to {topic_path}.")