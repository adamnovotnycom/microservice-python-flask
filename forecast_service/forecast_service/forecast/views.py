import datetime
import os
import pandas as pd
from flask import Blueprint, jsonify, request, make_response
from forecast_service.auth.auth import requires_auth
import forecast_service.forecast.models as forecast_model
import forecast_service.forecast.update as forecast_update

forecast_view = Blueprint('forecast', __name__)

@forecast_view.route('/forecast', methods=["GET"])
@requires_auth
def forecast_get():
    ticker = request.args.get("ticker")
    date_from = request.args.get("date_from")
    df = forecast_model.select(ticker=ticker, date_from=date_from)
    df_json = df.to_json(orient='split')
    resp = make_response(jsonify({"data": df_json}), 200)
    return resp

@forecast_view.route('/forecast', methods=["PUT"])
@requires_auth
def forecast_put():
    ticker = request.args.get("ticker")
    forecast_update.main(ticker)
    msg = jsonify({"msg": "/forecast PUT {} for ticker {} status OK servertime: {}".format(
        os.environ["APP_MODE"], ticker, datetime.datetime.now())})
    resp = make_response(msg, 200)
    return resp