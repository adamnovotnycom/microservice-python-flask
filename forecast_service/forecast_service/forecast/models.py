import datetime
import numpy as np
import os
import pandas as pd
import pickle

def build_empty_df():
    columns = ["date_from", "ticker", "date_to", "return", "confidence"]
    df = pd.DataFrame(columns=columns)
    return df

def get_fake_data():
    fake_data = build_empty_df()
    fake_data.loc[0] = ["1999-12-31 12:00:00", "IBM", "2000-01-01 12:00:00", 0.1, 0.11]
    fake_data.loc[1] = ["2000-01-01 12:00:00", "IBM", "2000-01-02 12:00:00", 0.2, 0.22]
    fake_data.loc[2] = ["2000-01-02 12:00:00", "IBM", "2000-01-03 12:00:00", 0.3, 0.33]
    fake_data.loc[3] = ["2000-01-03 12:00:00", "IBM", "2000-01-04 12:00:00", 0.4, 0.44]
    fake_data.loc[4] = ["1999-12-31 12:00:00", "TSLA", "2000-01-01 12:00:00", 0.5, 0.55]
    fake_data.loc[5] = ["2000-01-01 12:00:00", "TSLA", "2000-01-02 12:00:00", 0.6, 0.66]
    fake_data.loc[6] = ["2000-01-02 12:00:00", "TSLA", "2000-01-03 12:00:00", 0.7, 0.77]
    fake_data.loc[7] = ["2000-01-03 12:00:00", "TSLA", "2000-01-04 12:00:00", 0.8, 0.8]
    return fake_data

def insert(df):
    # TODO
    return True, "Insert OK"

def select(ticker, date_from):
    fake_data = get_fake_data()
    df_filter = fake_data.loc[fake_data["ticker"] == ticker]
    df_filter = df_filter.loc[df_filter["date_from"] == date_from]
    if len(df_filter) > 0:
        return df_filter
    else:
        date_from = datetime.datetime.strptime("2000-01-01  12:00:00", "%Y-%m-%d %H:%M:%S")
        delta_seconds = 60*60*24
        next_timestamp = date_from + datetime.timedelta(0, delta_seconds)
        df = build_empty_df()
        df.loc[0] = [date_from, ticker, str(next_timestamp), 0.0, 1.0]
        return df