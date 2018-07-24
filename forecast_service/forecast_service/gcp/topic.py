import json
import os
import time
from google.cloud import pubsub_v1
from forecast_service.parse_instance import google_project

def create_topic(topic_name):
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(google_project)
    exists = topic_exists(topic_name)
    if not exists:
        topic_path = publisher.topic_path(google_project, topic_name)
        result = publisher.create_topic(topic_path)
    return True

def delete_topic(topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(google_project, topic_name)
    publisher.delete_topic(topic_path)

def topic_exists(topic_name):
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(google_project)
    exists = False
    for tpc in publisher.list_topics(project_path):
        target_name = ("projects/{}/topics/".format(google_project)
            + topic_name)
        if tpc.name == target_name:
            exists = True
    return exists