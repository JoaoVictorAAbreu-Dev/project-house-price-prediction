import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import joblib

def generate_synthetic_data(filepath, n_samples=1000):
    """Generates synthetic housing data and saves it to a CSV file."""
    print("Generating synthetic housing dataset...")
    np.random.seed(42)
    
    # Feature generation
    sqft_living = np.random.normal(1800, 500, n_samples).astype(int)
    # Ensure house size is positive and realistic
    sqft_living = np.clip(sqft_living, 500, 5000)
    
    bedrooms = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.3, 0.4, 0.15, 0.05])
    bathrooms = np.round(bedrooms * 0.75 + np.random.normal(0, 0.3, n_samples) * 0.5)
    bathrooms = np.clip(bathrooms, 1, 4).astype(float)
    
    age_years = np.random.randint(0, 80, n_samples)
    distance_to_center = np.random.exponential(10, n_samples)
    distance_to_center = np.clip(distance_to_center, 0.5, 50)
    
    # Price logic: baseline + size contribution - age contribution - distance contribution + noise
    base_price = 100000
    price = (
        base_price 
        + sqft_living * 120 
        + bedrooms * 15000 
        + bathrooms * 25000 
        - age_years * 800 
        - distance_to_center * 3000
        + np.random.normal(0, 25000, n_samples)
    )
    # Ensure prices are reasonable
    price = np.clip(price, 50000, None).astype(int)
    
    df = pd.DataFrame({
        'sqft_living': sqft_living,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age_years': age_years,
        'distance_to_center_km': distance_to_center,
        'price': price
    })
    
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to {filepath}")
    return df

def run_eda(df, plots_dir):
    """Performs exploratory data analysis and saves visualizations."""
    print("Running exploratory data analysis...")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Set plotting style
    sns.set_theme(style="whitegrid")
    
    # 1. Correlation Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'correlation_matrix.png'))
    plt.close()
    
    # 2. Scatter plot: Size vs Price
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='sqft_living', y='price', hue='bedrooms', palette='viridis', alpha=0.7)
    plt.title('House Price vs. Living Space (Sqft)')
    plt.xlabel('Sqft Living')
    plt.ylabel('Price ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'size_vs_price.png'))
    plt.close()
    
    print("EDA visualizations saved successfully.")

def train_and_evaluate(df, project_dir):
    """Trains regression models and evaluates performance."""
    print("Preparing data for modeling...")
    plots_dir = os.path.join(project_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    # Split features and target
    X = df.drop(columns=['price'])
    y = df['price']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training models...")
    # 1. Linear Regression model (Baseline)
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    # 2. Random Forest Regressor with GridSearchCV
    print("Tuning Random Forest Regressor via GridSearchCV...")
    rf_base = RandomForestRegressor(random_state=42)
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    grid_search = GridSearchCV(estimator=rf_base, param_grid=param_grid, cv=5, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    rf_model = grid_search.best_estimator_
    print(f"Best RF Parameters: {grid_search.best_params_}")
    
    # Evaluation
    models = {
        'Linear Regression': lr_model,
        'Random Forest': rf_model
    }
    
    results = {}
    for name, model in models.items():
        # Cross-validation on train set
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        # Test set predictions
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, preds)
        mape = mean_absolute_percentage_error(y_test, preds) * 100
        r2 = r2_score(y_test, preds)
        
        results[name] = {
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape,
            'R2': r2,
            'CV_R2_Mean': np.mean(cv_scores),
            'preds': preds
        }
        
        print(f"\n--- {name} Results ---")
        print(f"CV R2 Mean (5-fold): {np.mean(cv_scores):.4f}")
        print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
        print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
        print(f"R-squared (R2) Score: {r2:.4f}")
        
    # Plot predictions comparison
    plt.figure(figsize=(12, 5))
    for i, (name, res) in enumerate(results.items(), 1):
        plt.subplot(1, 2, i)
        plt.scatter(y_test, res['preds'], alpha=0.5, color='teal' if i == 1 else 'coral')
        # Perfect fit line
        min_val = min(y_test.min(), res['preds'].min())
        max_val = max(y_test.max(), res['preds'].max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        plt.title(f"{name}: Actual vs Predicted\n(R2: {res['R2']:.4f})")
        plt.xlabel("Actual Price ($)")
        plt.ylabel("Predicted Price ($)")
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'model_evaluation.png'))
    plt.close()
    
    # Plot residuals distribution for the best model (Random Forest)
    best_model_name = 'Random Forest'
    rf_preds = results[best_model_name]['preds']
    residuals = y_test - rf_preds
    
    plt.figure(figsize=(8, 5))
    sns.histplot(residuals, kde=True, color='purple', bins=30)
    plt.axvline(0, color='red', linestyle='--')
    plt.title('Residuals Distribution (Random Forest)')
    plt.xlabel('Residual (Actual - Predicted)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'residuals_distribution.png'))
    plt.close()
    
    # Save the best model
    best_model_path = os.path.join(project_dir, 'house_price_model.pkl')
    joblib.dump(rf_model, best_model_path)
    print(f"\nBest model saved to {best_model_path}")
    
    # Plot feature importances for Random Forest
    importances = rf_model.feature_importances_
    feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=False)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=feat_imp.values, y=feat_imp.index, palette='viridis')
    plt.title('Feature Importances (Random Forest)')
    plt.xlabel('Importance Score')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'feature_importance.png'))
    plt.close()
    
    print("\nFeature Importances (Random Forest):")
    print(feat_imp)

if __name__ == "__main__":
    # Paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(project_dir, 'dataset.csv')
    plots_dir = os.path.join(project_dir, 'plots')
    
    # Generate data
    df = generate_synthetic_data(dataset_path)
    
    # EDA
    run_eda(df, plots_dir)
    
    # Training & Evaluation
    train_and_evaluate(df, project_dir)

