from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load('your_trained_model.joblib')

# Example preprocessing function (customize as per your data preprocessing steps)
def preprocess_input(input_data):
    # Example: convert input data to a format suitable for your model
    processed_data = pd.DataFrame([input_data])
    return processed_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Example: receive input from form data
    input_data = {
        'flight_number': request.form['flight_number'],
        'airline': request.form['airline'],
        'departure_airport': request.form['departure_airport'],
        'arrival_airport': request.form['arrival_airport'],
        # Add more fields as needed
    }
    
    # Preprocess input data
    processed_data = preprocess_input(input_data)
    
    # Make prediction
    prediction = model.predict(processed_data)
    
    # Example: return prediction result
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
