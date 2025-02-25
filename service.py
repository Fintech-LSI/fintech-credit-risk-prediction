from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import requests  # Import the requests library for making HTTP calls
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load pre-trained model and scaler
model_path = 'model/random_forest_model.pkl'
scaler_path = 'model/scaler.pkl'
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Define features
NUMERIC_FEATURES = [
    'person_age', 'person_income', 'person_emp_length', 'loan_amnt',
    'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length'
]

CATEGORICAL_FEATURES = [
    'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'
]

# Spring Boot API URL for updating loan status
PORT = "8222"
SPRING_BOOT_API_URL = 'http://a6d67a21ec9f6481c90554529051afdc-1750605808.us-east-1.elb.amazonaws.com:' + PORT + '/api/loans'  # Replace with your Spring Boot API URL


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        input_data = request.json

        # Extract loan_id
        loan_id = input_data.get('loan_id')
        
        # Convert input to DataFrame
        df = pd.DataFrame([input_data])
        
        # Handle missing values
        df['person_emp_length'].fillna(df['person_emp_length'].median(), inplace=True)
        df['loan_int_rate'].fillna(df['loan_int_rate'].median(), inplace=True)
        
        # Create dummy variables for categorical features
        df_encoded = pd.get_dummies(df, columns=CATEGORICAL_FEATURES, drop_first=True)
        
        # Ensure all columns from training are present
        missing_cols = set(model.feature_names_in_) - set(df_encoded.columns)
        for col in missing_cols:
            df_encoded[col] = 0
            
        # Ensure columns are in the same order as during training
        df_encoded = df_encoded[model.feature_names_in_]
        
        # Scale numeric features
        df_encoded[NUMERIC_FEATURES] = scaler.transform(df_encoded[NUMERIC_FEATURES])
        
        # Make prediction
        prediction = model.predict(df_encoded)[0]
        prediction_prob = model.predict_proba(df_encoded)[0]

        # Send the loan status update to Spring Boot API
        update_spring_boot_loan_status(loan_id, prediction, prediction_prob[1], prediction_prob[0])

        return jsonify({
            'loan_status': f"{prediction}",
            'probability_of_approval': f"{prediction_prob[1]:.2%}",
            'probability_of_denial': f"{prediction_prob[0]:.2%}"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Invalid input data format'
        }), 400
    
def update_spring_boot_loan_status(loan_id, status, probaApproval, probaDenial):
    try:
        # Define Spring Boot API endpoint for updating loan status
        url = f'{SPRING_BOOT_API_URL}/{loan_id}/status'
        
        # Prepare the request body for the update
        params = {
             'status': int(status),
             'probaApproval': float(probaApproval),
             'probaDenial': float(probaDenial)
         }
        
        # Make the PATCH request to the Spring Boot API
        response = requests.patch(url, params=params)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Log successful request
        print(f"Loan {loan_id} status updated successfully in Spring Boot application.")

    except requests.exceptions.RequestException as e:
        # Handle exceptions during the HTTP request
        print(f"Error updating loan {loan_id} status in Spring Boot application: {e}")


# Sample input format for documentation
@app.route('/sample_input', methods=['GET'])
def sample_input():
    return jsonify({
        "loan_id": 2,
        "person_age": 30,
        "person_income": 75000.0,
        "person_home_ownership": "RENT",
        "person_emp_length": 60,
        "loan_intent": "PERSONAL",
        "loan_grade": "A",
        "loan_amnt": 10000.0,
        "loan_int_rate": 5.5,
        "loan_status": None,
        "loan_percent_income": 0.25,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 10
    })

if __name__ == '__main__':
    app.run(debug=True)