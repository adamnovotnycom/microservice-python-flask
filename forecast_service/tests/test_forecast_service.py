import datetime
import numpy
import pandas as pd
import pytest
import os
import requests
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from fixtures import db_fix
from fixtures import requests_fix

def insert_fake_data():
    from forecast_service.forecast import models
    df = models.build_empty_df()
    df.loc[0] = ["1999-12-31 12:00:00", "IBM", "2000-01-01 12:00:00", 0.1, 0.11]
    df.loc[1] = ["2000-01-01 12:00:00", "IBM", "2000-01-02 12:00:00", 0.2, 0.22]
    df.loc[2] = ["2000-01-02 12:00:00", "IBM", "2000-01-03 12:00:00", 0.3, 0.33]
    df.loc[3] = ["2000-01-03 12:00:00", "IBM", "2000-01-04 12:00:00", 0.4, 0.44]
    df.loc[4] = ["1999-12-31 12:00:00", "TSLA", "2000-01-01 12:00:00", 0.5, 0.55]
    df.loc[5] = ["2000-01-01 12:00:00", "TSLA", "2000-01-02 12:00:00", 0.6, 0.66]
    df.loc[6] = ["2000-01-02 12:00:00", "TSLA", "2000-01-03 12:00:00", 0.7, 0.77]
    df.loc[7] = ["2000-01-03 12:00:00", "TSLA", "2000-01-04 12:00:00", 0.8, 0.8]
    result, msg = models.insert(df)
    return df

def test_home(requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    r = requests.get("{0}/".format(requests_fix["url"]),
        auth=(requests_fix["user"], requests_fix["password"]))
    assert r.status_code == 200

def test_insert_models(db_fix):
    from forecast_service.forecast import models
    df = models.build_empty_df()
    df.loc[0] = ["2000-01-04 12:00:00", "TSLA", "2000-01-05 12:00:00", 0.8, 0.88]
    result, msg = models.insert(df)
    assert True == result

def test_select_models(db_fix):
    from forecast_service.forecast import models
    fake_df = insert_fake_data()
    df = models.select(ticker=fake_df.loc[0]["ticker"], 
        date_from=fake_df.loc[0]["date_from"])
    assert 1 == len(df)

def test_select_models_2(db_fix):
    from forecast_service.forecast import models
    fake_df = insert_fake_data()
    df = models.select(ticker="VIX", 
        date_from="2000-01-05 12:00:00")
    print(df)
    assert 1 == len(df)

def test_select_requests(db_fix, requests_fix):
    from forecast_service.forecast import models
    fake_df = insert_fake_data()
    r = requests.get("{}/forecast".format(requests_fix["url"]),
        auth=(requests_fix["user"], requests_fix["password"]), 
        params={"ticker": fake_df.loc[0]["ticker"], 
            "date_from": fake_df.loc[0]["date_from"]})
    df = pd.read_json(r.json()["data"], orient='split')
    assert r.status_code == 200 and len(df) == 1

def test_get_prices(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    from forecast_service.forecast import update
    df = update.get_prices(ticker="VIX")
    assert len(df) > 2

def test_current_timestamp_price(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    from forecast_service.forecast import update
    df = update.get_prices(ticker="VIX")
    ts, price = update.current_timestamp_price(df)
    assert price > 0

def test_new_next_day_forecast(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    from forecast_service.forecast import update
    ts = datetime.datetime.strptime("2000-01-01  12:00:00", "%Y-%m-%d %H:%M:%S")
    resp = update.new_next_day_forecast("VIX", ts)
    assert resp == True
    
def test_select_requests_2(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    fake_df = insert_fake_data()
    r = requests.get("{}/forecast".format(requests_fix["url"]),
        auth=(requests_fix["user"], requests_fix["password"]), 
        params={"ticker": fake_df.loc[1]["ticker"], 
            "date_from": fake_df.loc[1]["date_from"]})
    df = pd.read_json(r.json()["data"], orient='split')
    assert r.status_code == 200 and len(df) == 1

def test_select_requests_3(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    fake_df = insert_fake_data()
    r = requests.get("{}/forecast".format(requests_fix["url"]),
        auth=(requests_fix["user"], requests_fix["password"]), 
        params={"ticker": "VIX", 
            "date_from": "2000-01-04 12:00:00"})
    df = pd.read_json(r.json()["data"], orient='split')
    assert r.status_code == 200 and len(df) == 1

def test_update(db_fix):
    import forecast_service.app # set credentials
    import forecast_service.forecast.update as forecast_update
    result = forecast_update.main("VIX")
    assert True == result

def test_put_requests(db_fix, requests_fix):
    if not requests_fix["run"]:
        pytest.skip()
    import forecast_service.app # set credentials
    import forecast_service.gcp.subscriber as subscriber
    subscription_name = "optimal_portfolio_new_forecast_" + os.environ["APP_MODE"].lower()
    subscriber.subscribe(subscription_name)
    r = requests.put("{}/forecast".format(requests_fix["url"]),
        auth=(requests_fix["user"], requests_fix["password"]),
        params={"ticker": "VIX"})
    assert r.status_code == 200
    time.sleep(5) # wait for pubsub