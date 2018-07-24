import json
import os
import time
from google.cloud import pubsub_v1

import forecast_service.utils.log_me as log_me
from forecast_service.parse_instance import google_project

def publish_data(topic, data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(google_project, topic)
    data = json.dumps(data)
    data = data.encode('utf-8') # Data must be a bytestring
    publisher.publish(topic_path, data=data)
    log_me.log(filename=__name__, function_name="publish_data", msg_details=data, error_flag=False)
    return True