import datetime
import os
import pandas as pd
import requests

import forecast_service.gcp.publisher as publisher
import forecast_service.utils.log_me as log_me
from forecast_service.parse_instance import (MODE, dataservice_url, dataservice_user,
    dataservice_password, optimal_portfolio_update_url, optimal_portfolio_update_key)
from forecast_service.forecast import models

prices_cols = ("ticker", "timestamp", "open", "high", "low", "close", "volume")

def main(ticker):
    prices_df = get_prices(ticker)
    ts, price = current_timestamp_price(prices_df)
    log_me.log(filename=__name__, function_name="main", msg_details="{}: {}".format(ticker, ts), error_flag=False)
    new_next_day_forecast(ticker, ts)
    notify_optimal_portfolio(ticker, ts)
    return True

def get_prices(ticker):
    r = requests.get("{}/price-select".format(dataservice_url),
        auth=(dataservice_user, dataservice_password), 
        params={"ticker": ticker})
    df = pd.read_json(r.json()["data"], orient='split')
    assert r.status_code == 200
    return df

def current_timestamp_price(prices_df):
    most_recent_timestamp = datetime.datetime.strptime("2000-01-01  12:00:00", "%Y-%m-%d %H:%M:%S")
    most_recent_price = 0
    for i, r in prices_df.iterrows():
        if r[prices_cols[1]] > most_recent_timestamp:
            most_recent_timestamp = r[prices_cols[1]]
            most_recent_price = r[prices_cols[5]]
    return most_recent_timestamp, most_recent_price
    
def new_next_day_forecast(ticker, timestamp):
    df = models.build_empty_df()
    delta_seconds = 60*60*24
    next_timestamp = timestamp + datetime.timedelta(0, delta_seconds)
    df.loc[0] = [str(timestamp), ticker, str(next_timestamp), 0.0, 1.0]
    models.insert(df)
    return True

def notify_optimal_portfolio(ticker, timestamp):
    topic = "new_forecast_" + os.environ["APP_MODE"].lower()
    data = {"msg_type": "new_forecast_available", "timestamp": str(datetime.datetime.now()),
            "ticker": ticker, "timestamp_forecast": str(timestamp)}
    publisher.publish_data(topic, data)