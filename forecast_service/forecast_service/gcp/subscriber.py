import json
import os
import time

from google.cloud import pubsub_v1
from forecast_service.parse_instance import google_project

def subscribe(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(google_project, 
        subscription_name)
    
    def callback(message):
        """
        Args:
            message = {"return_portfolio": True, "timestamp": str}
        """
        message.ack()
        print("{} received message raw:".format(__name__))
        print(message)
        data = message.data.decode("utf-8")
        data = json.loads(data)
        print("{} Data decoded:".format(__name__))
        print(data)

    subscriber.subscribe(subscription_path, callback=callback)
    
    print("Listening {} for messages on {}".format(__name__, subscription_path))
