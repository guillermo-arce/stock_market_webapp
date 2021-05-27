import requests
import pandas as pd
import json
from sklearn.preprocessing import RobustScaler
from flask import current_app as app
import joblib
import os
from app.mod_predict.utils.ta_indicators import add_technical_indicators,add_technical_indicators_complex

TIME = "time"
OPEN = "open"
HIGH = "high"
LOW = "low"
CLOSE = "close"
VOLUME = "volume"

def get_input_for_prediction(date,prediction_type):
    # Get data from our API
    url="http://" + app.config['API'] + "/getPrices"
    datetime = {'datetime': date}
    response = requests.get(url, params=datetime)

    # Transform JSON to Pandas Dataframe for preprocessing purposes
    df = pd.read_json(response.content)

    # Pre processing of input (addition of ta indicators and removal of extra info)
    df,scaler = pre_process_input(df,prediction_type)

    return df,scaler

#Pre process input from API
def pre_process_input(df,prediction_type):
    # Convert "time" column to DateTime dftype
    df[TIME]= pd.to_datetime(df[TIME], errors='coerce') 

    # Dropping any NaNs
    df.dropna(inplace=True)

    # Adding technical indicators
    if(prediction_type=='0'):
        df = add_technical_indicators(df)
    else:
        df = add_technical_indicators_complex(df)

    # Dropping everything but the indicators
    df.drop([TIME, OPEN, HIGH, LOW, CLOSE, VOLUME], axis=1, inplace=True)

    # Scaling data for the nn
    df,scaler = scale_data(df,prediction_type)

    # Dropping first 50 values because of the lag of the technical indicators (moving averages and so)
    df = df.drop(df.index[:50])

    return df,scaler

def scale_data(df,prediction_type):
    dirname = app.config['BASE_DIR']
    if(prediction_type=='0'):
        filename = os.path.join(dirname, 'app/mod_predict/data_scalers/close_scaler.pkl')
        close_scaler = joblib.load(filename) 
        filename = os.path.join(dirname, 'app/mod_predict/data_scalers/scaler.pkl')
        scaler = joblib.load(filename) 
    else:
        filename = os.path.join(dirname, 'app/mod_predict/data_scalers/close_scaler_complex.pkl')
        close_scaler = joblib.load(filename) 
        filename = os.path.join(dirname, 'app/mod_predict/data_scalers/scaler_complex.pkl')
        scaler = joblib.load(filename) 
    
    close_scaler.transform(df[["close_sma"]])
    df = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)

    return df, close_scaler