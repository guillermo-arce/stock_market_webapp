from app.mod_predict.prediction.prediction_data import get_input_for_prediction
from app.mod_predict.lstm_models.Model import *
import numpy as np
import tensorflow as tf
import os
from flask import current_app as app

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def model_predict(date, model_type):

    # Gets model according to prediction type
    model = get_model(model_type)

    # Get processed input and scaler
    df = get_input_for_prediction(date, model)

    # Converts data to time series format
    x = convert_to_time_series(df.values, model)

    # Gets model prediction
    y = model.get_prediction(x)

    # Rescales prediction to real values
    y = model.get_close_price_scaler().inverse_transform(np.asarray(y).reshape(1, -1))

    print("Y: ", y)

    return y[0]


def convert_to_time_series(data, model):
    dim_0 = data.shape[0] - model.get_time_steps()
    dim_1 = data.shape[1]

    if dim_0 == 0:
        dim_0 = 1

    x = np.zeros((dim_0, model.get_time_steps(), dim_1))

    for i in range(dim_0):
        x[i] = data[i : model.get_time_steps() + i]

    return x


def get_model(model_type):
    return ModelFactory().get_model(model_type)
