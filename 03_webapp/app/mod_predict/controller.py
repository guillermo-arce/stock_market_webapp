# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    jsonify
)

from app.mod_predict.utils.input_validator import (
    validate_date,
    validate_prediction_type,
)
from app.mod_predict.prediction.prediction_manager import model_predict

# Define the blueprint: 'predict', set its url prefix: app.url/predict
mod_predict = Blueprint("predict", __name__, url_prefix="/predict")

# Set the route and accepted methods
@mod_predict.route("", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        return render_template("404.html")

    # Get parameters from POST request
    date = request.form.get("date")
    prediction_type = request.form.get("prediction_type")

    # Validate date
    valid_date = False
    if date is not None:
        valid_date = valid_date or validate_date(date)

    # Validate prediction_type
    valid_prediction_type = False
    if prediction_type is not None:
        valid_prediction_type = valid_prediction_type or validate_prediction_type(
            prediction_type
        )

    # Make model prediction (if parameters are correct) and return result in JSON format
    if valid_prediction_type and valid_date:
        prediction = model_predict(date, prediction_type)
        return jsonify(prediction.tolist())

    return "None"
