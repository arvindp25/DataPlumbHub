import requests
from requests_sse import EventSource, InvalidStatusCodeError, InvalidContentTypeError
import json
import os
from google.cloud import pubsub_v1
project_id = os.getenv("GCP_PROJECT_ID")
topic_id = os.getenv("PUB_SUB_TOPIC")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


with EventSource("https://stream.wikimedia.org/v2/stream/recentchange", timeout=30) as event_source:
    try:
        for event in event_source:
            data = json.loads(event.data)

            payload = json.dumps(data).encode("utf-8")
            publisher.publish(topic_path, payload)
            print(f"Published")
    except Exception as e:
        print(e)
    except InvalidContentTypeError:
        pass
    except requests.RequestException:
        pass