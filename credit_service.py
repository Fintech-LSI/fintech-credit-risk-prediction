from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from flask_cors import CORS # Import flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes # Enable CORS for all routes

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

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        input_data = request.json
        
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

# Sample input format for documentation
@app.route('/sample_input', methods=['GET'])
def sample_input():
    return jsonify({
        'person_age': 30,
        'person_income': 60000,
        'person_home_ownership': 'RENT',
        'person_emp_length': 5.0,
        'loan_intent': 'PERSONAL',
        'loan_amnt': 10000,
        'loan_int_rate': 12.0,
        'loan_percent_income': 0.15,
        'cb_person_default_on_file': 'N',
        'cb_person_cred_hist_length': 5,
        'loan_grade': 'B'
    })

if __name__ == '__main__':
    app.run(debug=True)