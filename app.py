from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import joblib
from tqdm import tqdm

app = Flask(__name__, static_folder='static')

# Cargar el modelo entrenado
model = joblib.load('rf_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Obtener los datos de entrada del formulario HTML
    input_data = request.form.to_dict()

    # Convertir los datos en un DataFrame de pandas
    input_df = pd.DataFrame([input_data])

    flight_data = pd.read_csv("Airlines_with_dummies.csv",nrows=1).drop(columns=['Delay'])

    for column in tqdm(flight_data.columns):
        if "_" in column:
            flight_data[column] = 0

    column_dummies = ["Airline","AirportFrom","AirportTo"]
    for column, value in input_data.items():
        if column in column_dummies:
            flight_data[column+"_"+value]=1
    flight_data["DayOfWeek"] = input_data["DayOfWeek"]
    flight_data["Flight"] = input_data["Flight"]

    # Realizar la predicción
    prediction = model.predict(flight_data)[0]

    # Determine the result message and style
    if prediction == 1:  # Adjust condition based on your model's output
        result_message = 'Your flight is delayed'
        result_style = 'delayed-style'
    else:
        result_message = 'Your flight is on time'
        result_style = 'on-time-style'

    # Render the result.html template with the prediction result and style
    return render_template('result.html', result_message=result_message, result_style=result_style)

if __name__ == '__main__':
    app.run(debug=True)