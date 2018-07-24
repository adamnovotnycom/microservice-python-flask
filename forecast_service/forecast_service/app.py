import configparser
import logging.config
import os
from flask import Flask

import forecast_service.utils.log_me as log_me
from forecast_service.parse_instance import google_creds


app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds

LOGGING_CONFIG = {
    'version': 1, # required
    'disable_existing_loggers': True, # this config overrides all other loggers
    'formatters': {
        'details': {
            'format': '%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'details',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        '': { # 'root' logger
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}

log_me.log(filename=__name__, function_name="", msg_details="APP STARTED", error_flag=False)