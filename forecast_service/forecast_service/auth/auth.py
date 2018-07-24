import configparser
import os
from functools import wraps
from flask import request, Response
from forecast_service.parse_instance import app_user, app_password


def check_auth(username, password):
    return username == app_user and password == app_password

def not_authenticated():
    return Response("Invalid credentials.", 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return not_authenticated()
        else:
            return f(*args, **kwargs)
    return decorated