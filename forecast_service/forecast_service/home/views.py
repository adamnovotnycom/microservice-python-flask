import datetime
import os
from flask import Blueprint, jsonify, request, make_response
from forecast_service.auth.auth import requires_auth

home_view = Blueprint('home', __name__)

@home_view.route('/', methods=["GET"])
@requires_auth
def home_get():
    data = jsonify({"/ forecast service {} status OK servertime:".format(os.environ["APP_MODE"]): datetime.datetime.now()})
    resp = make_response(data, 200)
    return resp