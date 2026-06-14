# House Price Prediction Study Project

This project implements a regression pipeline to predict house prices based on synthetic features like size (sqft), number of bedrooms/bathrooms, age of the house, and distance to the city center.

## Project Structure
- `dataset.csv`: Generated CSV dataset with features (`sqft_living`, `bedrooms`, `bathrooms`, `age_years`, `distance_to_center_km`) and target (`price`).
- `train.py`: Self-contained Python script to generate synthetic data, perform hyperparameter tuning, and train regression models.
- `predict.py`: Interactive and CLI script to make predictions using the trained model.
- `exploration.ipynb`: Jupyter notebook for interactive data analysis, visualization, and model comparison.
- `requirements.txt`: Python libraries required.
- `plots/`: Directory containing generated visualizations:
  - `correlation_matrix.png`: Heatmap showing correlation between features.
  - `size_vs_price.png`: Scatter plot visualization of size vs price.
  - `model_evaluation.png`: Prediction accuracy visualization (Actual vs Predicted).
  - `residuals_distribution.png`: Error analysis visualization.
  - `feature_importance.png`: Importance score of features for the Random Forest model.
- `house_price_model.pkl`: The serialized Random Forest model.

## Features
- **sqft_living**: Internal living space in square feet.
- **bedrooms**: Number of bedrooms.
- **bathrooms**: Number of bathrooms.
- **age_years**: Age of the house in years.
- **distance_to_center_km**: Distance to the nearest city center in kilometers.
- **price**: Target variable (house price in USD).

## Modeling
Two models are compared:
1. **Linear Regression** (Baseline)
2. **Random Forest Regressor** (Tuned via Grid Search)

## How to Run

1. Navigate to the project directory:
   ```bash
   cd house-price-prediction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the training pipeline:
   ```bash
   python train.py
   ```
4. Run predictions via CLI:
   ```bash
   python predict.py
   ```
   Or pass parameters directly:
   ```bash
   python predict.py --sqft 2000 --bedrooms 3 --bathrooms 2.5 --age 15 --distance 4.5
   ```

