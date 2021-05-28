import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import joblib
from flask import current_app as app
from abc import ABC


class ModelFactory:
    def get_model(self, id):
        if id == "0":
            return Model_100_10()
        elif id == "1":
            return Model_100_1()
        else:
            return Model_600_60()


class AbstractModel(ABC):
    def get_model(self):
        pass

    def get_time_steps(self):
        pass

    def get_number_predictions(self):
        pass

    def get_prediction(self, x):
        pass

    def get_scaler(self):
        filename = os.path.join(
            app.config["BASE_DIR"], "app\mod_predict\data_scalers\scaler.pkl"
        )
        return joblib.load(filename)

    def get_close_price_scaler(self):
        filename = os.path.join(
            app.config["BASE_DIR"], "app\mod_predict\data_scalers\close_scaler.pkl"
        )
        return joblib.load(filename)

    def make_prediction(self, data, model):
        input_data = data.reshape(-1, data.shape[0], data.shape[1])
        prediction = model.predict(input_data)
        return prediction[0, :]


class Model_100_10(AbstractModel):
    def get_model(self):
        return tf.keras.models.load_model(
            os.path.join(
                app.config["BASE_DIR"], "app/mod_predict/lstm_models/" + "100_10"
            )
        )

    def get_time_steps(self):
        return 100

    def get_number_predictions(self):
        return 10

    def get_prediction(self, data):
        return self.accumulate_predictions(data, self.get_model())

    def accumulate_predictions(self, data, model):
        set_of_predictions = []
        for i in range(0, len(data) + 1, self.get_number_predictions()):
            if i == 0:
                prediction = self.make_prediction(data[i], model)
            else:
                prediction = self.make_prediction(data[i - 1], model)
            for j in range(len(prediction)):
                set_of_predictions.append(prediction[j])
        return set_of_predictions


class Model_100_1(AbstractModel):
    def get_model(self):
        return tf.keras.models.load_model(
            os.path.join(
                app.config["BASE_DIR"], "app/mod_predict/lstm_models/" + "100_1"
            )
        )

    def get_time_steps(self):
        return 100

    def get_number_predictions(self):
        return 1

    def get_prediction(self, data):
        return self.make_prediction(data[-1], self.get_model())


class Model_600_60(AbstractModel):
    def get_model(self):
        return tf.keras.models.load_model(
            os.path.join(
                app.config["BASE_DIR"], "app/mod_predict/lstm_models/" + "600_60"
            )
        )

    def get_time_steps(self):
        return 600

    def get_number_predictions(self):
        return 60

    def get_prediction(self, data):
        return self.make_prediction(data[-1], self.get_model())
