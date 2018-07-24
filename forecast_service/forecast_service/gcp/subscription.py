import json
import os
import time
from google.cloud import pubsub_v1
from forecast_service.parse_instance import google_project
        
def create_subscription(topic, subscription_name):
    """Create a new pull subscription on the given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(google_project, topic)
    subscription_path = subscriber.subscription_path(
        google_project, subscription_name)
    subscription = subscriber.create_subscription(
        subscription_path, topic_path)
    print("Subscription created: {}".format(subscription))
    return True

def delete_subscription(subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        google_project, subscription_name)
    subscriber.delete_subscription(subscription_path)
    return True