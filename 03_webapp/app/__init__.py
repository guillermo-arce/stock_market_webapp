from flask import Flask, render_template
import requests
import json
import pandas as pd

app = Flask(__name__)

# Configurations
app.config.from_object("config")

# HTTP error handling for 404
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# Import module / component using its blueprint handler variable (mod_predict)
from app.mod_predict.controller import mod_predict as predict_module

# Register blueprint
app.register_blueprint(predict_module)

# Define view
@app.route("/", methods=["GET"])
def index():
    date = get_random_date()
    current_prices, datetimes_prices = get_prices(date)
    return render_template(
        "index.html",
        date=date,
        current_prices=current_prices,
        datetimes_prices=datetimes_prices,
    )


def get_random_date():
    # Get random date from our API
    url = "http://" + app.config["API"] + "/getRandomDate"
    response = requests.get(url)
    date = json.loads(response.content)
    return date[0][0]


def get_prices(date):
    # Get prices data from our API
    url = "http://" + app.config["API"] + "/getPrices"
    datetime = {"datetime": date}
    response = requests.get(url, params=datetime)

    # Transform JSON to Pandas Dataframe in order to leave just closing price
    df = pd.read_json(response.content)
    # Dropping any NaNs
    df.dropna(inplace=True)
    # Dropping everything but the indicators
    df.drop(["open", "high", "low", "volume"], axis=1, inplace=True)

    return df["close"].tolist(), ",".join(df["time"].tolist())


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
