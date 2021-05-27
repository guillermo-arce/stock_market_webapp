# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for,jsonify

from app.mod_predict.utils.input_validator import input_validation,date_validation
from app.mod_predict.prediction.prediction_manager import model_predict

# Define the blueprint: 'predict', set its url prefix: app.url/predict
mod_predict = Blueprint('predict', __name__, url_prefix='/predict')

# Set the route and accepted methods
@mod_predict.route('', methods=['GET','POST'])

def predict():
    
    if(request.method=='GET'):
        return render_template("404.html")

    # Get parameters from POST request
    date = request.form.get('date')
    prediction_type = request.form.get('prediction_type')

    #Validate date
    valid_date = False
    if date is not None: valid_date = valid_date or date_validation(date)

    #Validate prediction_type
    valid_prediction_type = False
    if prediction_type is not None: valid_prediction_type = valid_prediction_type or input_validation(prediction_type)

    # Make model prediction (if parameters are correct) and return result in JSON format
    if (valid_prediction_type and valid_date):
        #Make prediction
        prediction = model_predict(date,prediction_type)
        
        if(prediction_type=='0'):
            return jsonify(prediction.tolist())
        elif(prediction_type=='1'):
            return jsonify(prediction.tolist())
        elif(prediction_type=='2'):
            return jsonify(prediction.tolist())
    
    return "None"

    