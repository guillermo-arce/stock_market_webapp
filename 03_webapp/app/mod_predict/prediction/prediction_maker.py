import numpy as np


def make_prediction(model, data, number_of_predictions):
    all_predictions = []
    input_data = data.reshape(-1, data.shape[0], data.shape[1])
    prediction=model.predict(input_data)
    return prediction[0,:]
	
def single_prediction(model,data, number_of_predictions,time_steps):
    prediction = make_prediction(model,data,number_of_predictions)
    return prediction

# Process for joining the predictions in a single array
def accumulated_prediction(model,data,number_of_predictions,time_steps):    
    accumulated_prediction=[]
    for i in range(0, len(data)+1, number_of_predictions):
        if(i==0): 
            prediction = make_prediction(model,data[i],number_of_predictions)
        else: 
            prediction = make_prediction(model,data[i-1],number_of_predictions)
        for j in range(len(prediction)):
            accumulated_prediction.append(prediction[j])
    return accumulated_prediction
