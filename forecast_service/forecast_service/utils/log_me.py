import datetime
import logging
import os
import sys

import forecast_service.utils.slack as slack

logger = logging.getLogger('') # factory method

def log(filename, function_name, msg_details, error_flag=False):
    msg_type = "log"
    if error_flag:
        msg_type = "ERROR"
    log_msg = "{}: {}.{}(). mode: {}. time: {}. details: {}".format(
                    msg_type, filename, function_name, 
                    os.environ["APP_MODE"].lower(), 
                    datetime.datetime.now(), msg_details)
    logger.debug(log_msg)
    slack.log(log_msg)