import requests
import pandas as pd
import json
import joblib
import os
from sklearn.preprocessing import RobustScaler
from flask import current_app as app
from app.mod_predict.utils.ta_indicators import add_technical_indicators

TIME = "time"
OPEN = "open"
HIGH = "high"
LOW = "low"
CLOSE = "close"
VOLUME = "volume"


def get_input_for_prediction(date, model):
    # Get data from our API
    url = "http://" + app.config["API"] + "/getPrices"
    datetime = {"datetime": date}
    response = requests.get(url, params=datetime)

    # Transform JSON to Pandas Dataframe for preprocessing purposes
    df = pd.read_json(response.content)

    # Pre processing of input (addition of ta indicators and removal of extra info)
    df = pre_process_input(df, model)

    return df


# Pre process input from API
def pre_process_input(df, model):
    # Convert "time" column to DateTime dftype
    df[TIME] = pd.to_datetime(df[TIME], errors="coerce")

    # Dropping any NaNs
    df.dropna(inplace=True)

    # Adding technical indicators
    df = add_technical_indicators(df)

    # Dropping everything but the indicators
    df.drop([TIME, OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)

    # Scaling data for the nn
    scaler = model.get_scaler()
    df = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)

    # Dropping first 50 values because of the lag of the technical indicators (moving averages and so)
    df = df.drop(df.index[:50])

    return df
