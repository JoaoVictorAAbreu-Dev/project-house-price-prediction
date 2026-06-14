import os
import sys
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Load the model on startup
project_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_dir, 'house_price_model.pkl')

if not os.path.exists(model_path):
    print(f"WARNING: Model file not found at {model_path}.")
    print("Please ensure train.py runs successfully to train the model.")
    model = None
else:
    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.route('/')
def index():
    """Serves the main frontend page."""
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles price prediction requests."""
    global model
    if model is None:
        # Try to reload the model in case it was created after server startup
        if os.path.exists(model_path):
            try:
                model = joblib.load(model_path)
            except Exception as e:
                return jsonify({'error': f'Model failed to load: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Model file not found. Please train the model first.'}), 500

    try:
        data = request.get_json()
        
        # Extract and validate features
        sqft_living = float(data.get('sqft_living', 1800))
        bedrooms = int(data.get('bedrooms', 3))
        bathrooms = float(data.get('bathrooms', 2))
        age_years = float(data.get('age_years', 10))
        distance_to_center_km = float(data.get('distance_to_center_km', 5))
        
        # Verify inputs are within sensible boundaries
        if sqft_living <= 0 or bedrooms < 0 or bathrooms < 0 or age_years < 0 or distance_to_center_km < 0:
            return jsonify({'error': 'All features must be positive numbers.'}), 400

        # Create DataFrame matching training feature names
        features = pd.DataFrame({
            'sqft_living': [sqft_living],
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'age_years': [age_years],
            'distance_to_center_km': [distance_to_center_km]
        })
        
        # Predict
        prediction = model.predict(features)[0]
        
        # Simple analysis breakdown to show in the frontend
        # (How the input values compare to the average dataset values)
        # Average values from synthetic data generation baseline:
        # sqft_living ~ 1800, price baseline ~ 100k, sqft_coeff = 120, bedroom_coeff = 15000, bathroom_coeff = 25000
        # age_coeff = -800, distance_coeff = -3000
        breakdown = {
            'base_value': 100000,
            'size_contribution': sqft_living * 120,
            'rooms_contribution': (bedrooms * 15000) + (bathrooms * 25000),
            'age_depreciation': -age_years * 800,
            'location_effect': -distance_to_center_km * 3000
        }
        
        return jsonify({
            'price': float(prediction),
            'breakdown': breakdown
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/model_info', methods=['GET'])
def model_info():
    """Returns model metrics and feature importances from metadata JSON."""
    metadata_path = os.path.join(project_dir, 'model_metadata.json')
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                import json
                metadata = json.load(f)
                return jsonify(metadata)
        except Exception as e:
            return jsonify({'error': f'Failed to read metadata: {str(e)}'}), 500
    else:
        return jsonify({
            'error': 'Metadata file not found. Please train the model first.'
        }), 404

if __name__ == '__main__':
    # Run server on port 5000
    print("Starting Flask server at http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
