import os
import sys
import argparse
import joblib
import pandas as pd

def load_model(model_path):
    """Loads the serialized machine learning model."""
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please run train.py first to train and save the model.")
        sys.exit(1)
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

def get_interactive_inputs():
    """Prompts the user interactively for house features."""
    print("\n" + "="*45)
    print("   House Price Prediction - Interactive CLI")
    print("="*45)
    print("Please enter the details of the house:\n")
    
    while True:
        try:
            sqft = int(input("1. Living Space (sqft, e.g. 1500): "))
            if sqft <= 0:
                print("Size must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            bedrooms = int(input("2. Number of Bedrooms (1-5, e.g. 3): "))
            if bedrooms < 1 or bedrooms > 10:
                print("Please enter a realistic number of bedrooms (1-10).")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            bathrooms = float(input("3. Number of Bathrooms (1-4, e.g. 2.5): "))
            if bathrooms < 0.5 or bathrooms > 6.0:
                print("Please enter a realistic number of bathrooms (0.5-6.0).")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            age = int(input("4. Age of the House (years, e.g. 10): "))
            if age < 0:
                print("Age cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            distance = float(input("5. Distance to City Center (km, e.g. 5.2): "))
            if distance < 0:
                print("Distance cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
            
    return sqft, bedrooms, bathrooms, age, distance

def main():
    parser = argparse.ArgumentParser(description="Predict house prices using the trained Random Forest model.")
    parser.add_argument("--sqft", type=int, help="Living area in square feet")
    parser.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    parser.add_argument("--bathrooms", type=float, help="Number of bathrooms")
    parser.add_argument("--age", type=int, help="Age of the house in years")
    parser.add_argument("--distance", type=float, help="Distance to city center in kilometers")
    
    args = parser.parse_args()
    
    # Locate model
    project_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_dir, 'house_price_model.pkl')
    
    # Load model
    model = load_model(model_path)
    
    # Determine if CLI args were provided or we should run interactively
    cli_args_provided = all(v is not None for v in [args.sqft, args.bedrooms, args.bathrooms, args.age, args.distance])
    
    if cli_args_provided:
        sqft, bedrooms, bathrooms, age, distance = args.sqft, args.bedrooms, args.bathrooms, args.age, args.distance
    else:
        sqft, bedrooms, bathrooms, age, distance = get_interactive_inputs()
        
    # Prepare feature DataFrame matching training columns:
    # ['sqft_living', 'bedrooms', 'bathrooms', 'age_years', 'distance_to_center_km']
    features = pd.DataFrame({
        'sqft_living': [sqft],
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'age_years': [age],
        'distance_to_center_km': [distance]
    })
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    # Output the result
    print("\n" + "-"*45)
    print("                  RESULT")
    print("-"*45)
    print(f"Features: Size={sqft} sqft | Bed={bedrooms} | Bath={bathrooms} | Age={age} yrs | Dist={distance} km")
    print(f"Estimated Price: ${prediction:,.2f}")
    print("="*45 + "\n")

if __name__ == "__main__":
    main()
