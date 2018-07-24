import datetime
import json
import logging
import requests

from forecast_service.parse_instance import slack_url # requires os.environ["APP_MODE"]

def log(msg):
    data = {"text": msg}
    r = requests.post("{}".format(slack_url),
        data = json.dumps(data))
    logging.info("{} - chat info status code {} - {}".format(__name__, 
        r.status_code, datetime.datetime.now()))