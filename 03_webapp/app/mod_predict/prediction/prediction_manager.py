from app.mod_predict.prediction.prediction_data import get_input_for_prediction
from app.mod_predict.prediction.prediction_maker import single_prediction,accumulated_prediction
import numpy as np
import tensorflow as tf
import os
from flask import current_app as app
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def model_predict(date, prediction_type):

    # Get processed input and scaler
    df,scaler = get_input_for_prediction(date,prediction_type)

    #Converts data to time series format
    x, time_steps, number_predictions = convert_to_time_series(df,prediction_type)

    #Gets model according to prediction type
    model = get_model(prediction_type)

    #Gets model prediction 
    y = make_prediction(model,x,number_predictions,time_steps,prediction_type)

    #Unscales prediction to real values
    y = scaler.inverse_transform(np.asarray(y).reshape(1, -1))

    print("Y: ",y)

    return y[0]

def convert_to_time_series(df,prediction_type):
    time_steps, number_predictions = select_parameters_for_model(prediction_type)

    x = build_timeseries(df.values, time_steps, number_predictions)
    
    return x, time_steps, number_predictions

def select_parameters_for_model(prediction_type):
    if(prediction_type=='0'):     
        time_steps = 100
        number_predictions = 10
    if(prediction_type=='1'):    
        time_steps = 100
        number_predictions = 1
    if(prediction_type=='2'):
        time_steps = 600
        number_predictions = 60
    return time_steps,number_predictions

def build_timeseries(data, time_steps, number_predictions):
    dim_0 = data.shape[0] - time_steps
    dim_1 = data.shape[1]

    if(dim_0==0):dim_0=1

    x = np.zeros((dim_0, time_steps, dim_1))

    for i in range(dim_0):
        x[i] = data[i:time_steps+i]

    return x

def get_model(model_type):
    dirname = app.config['BASE_DIR']
    if(model_type=='0'): return tf.keras.models.load_model(os.path.join(dirname, 'app/mod_predict/lstm_models/'+'100_10'))
    if(model_type=='1'): return tf.keras.models.load_model(os.path.join(dirname, 'app/mod_predict/lstm_models/'+'100_1'))
    if(model_type=='2'): return tf.keras.models.load_model(os.path.join(dirname, 'app/mod_predict/lstm_models/'+'600_60'))
    return None


def make_prediction(model,x,number_predictions,time_steps,prediction_type):
    if(prediction_type=='0'):
        y = accumulated_prediction(model,x,number_predictions,time_steps)
    else:
        y = single_prediction(model,x[-1],number_predictions,time_steps)
    return y