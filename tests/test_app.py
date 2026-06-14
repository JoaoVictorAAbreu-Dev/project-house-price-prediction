from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as house_app


def test_model_info_endpoint_returns_metadata():
    client = house_app.app.test_client()

    response = client.get('/model_info')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'metrics' in payload
    assert 'feature_importances' in payload


def test_predict_endpoint_rejects_invalid_json():
    client = house_app.app.test_client()

    response = client.post('/predict', data='not-json', content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Request body must be valid JSON.'


def test_predict_endpoint_returns_price_and_breakdown():
    client = house_app.app.test_client()

    response = client.post(
        '/predict',
        json={
            'sqft_living': 2200,
            'bedrooms': 3,
            'bathrooms': 2.5,
            'age_years': 8,
            'distance_to_center_km': 4.2,
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert 'price' in payload
    assert 'breakdown' in payload
    assert payload['price'] > 0
